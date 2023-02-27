
import cv2 as cv, numpy as np, pandas, logging, math

from utils import commons
from openvino.inference_engine import IECore

from PySide6.QtCore import Signal, QThread, QPoint
from PySide6.QtWidgets import QWidget


# TODO Move inference operations to InferenceEngine class


class Network :
    network     = None
    executor    = None
    # Layers
    input_info  = None
    outputs     = None
    # Sizes
    width       = None
    height      = None

    def __init__(self, ie, executor_device, models_prefix) -> None:
        self.network    = ie.read_network(model=f"{models_prefix}.xml", weights=f"{models_prefix}.bin")
        self.executor   = ie.load_network(self.network, executor_device)
        self.input_info = next(iter(self.executor.input_info))
        self.outputs    = next(iter(self.executor.outputs))
        _, _, h, w      = self.network.input_info[self.input_info].tensor_desc.dims
        self.width      = w
        self.height     = h


class Detection :
    min     = None
    max     = None
    conf    = None

    def __init__(self, x_min, y_min, x_max, y_max, conf) -> None:
        self.min    = QPoint(x_min, y_min)
        self.max    = QPoint(x_max, y_max)
        self.conf   = conf


class VideoThread (QThread) :

    ## Signals
                            # frame, detections, remaining time for detection (possibly None)
    NewImage        = Signal (object, Detection, int)   # Signal sent every time a new frame is processed
    NewPerson       = Signal ()                         # Signal sent when a person (possible customer) is detected
    EscapedPerson   = Signal ()                         # Signal sent when a person go out from camera frame
                            # frame, detection, customer_info
    NewCustomer     = Signal (object, object, object)   # Signal sent when a new customer is detected -> image frizzed
    ## Members
    __logger                    = None
    __video_source              = None
    __customer_found            = None
    __networks                  = None
    __min_conf                  = None
    __current_session           = None
    __new_person_threshold      = None
    __new_customer_threshold    = None

    __freezed_frame             = None
    __target_detection          = None
    __customer_info             = None


    def __init__(self, main_window, config) -> None:
        super().__init__()

        self.__min_conf                 = float(config["ai"]["face_deection_minimum_confidence"])
        self.__new_person_threshold     = int (config["ai"]["new_person_threshold_ms"])
        self.__new_customer_threshold   = int (config["ai"]["new_customer_threshold_ms"])

        self.__logger                   = commons.create_logger(__name__)
        
        self.__logger.debug(f"Loading networks..")
        self.__logger.debug(f'All networks loaded in {self.__load_ai_networks(config["ai"])} seconds')
        # Setting up video source
        self.__video_source = cv.VideoCapture(config["app"]["video_source"])
        self.__video_source.set(cv.CAP_PROP_FRAME_WIDTH, int(config["app"]["video_resolution_width"]))
        self.__video_source.set(cv.CAP_PROP_FRAME_HEIGHT, int(config["app"]["video_resolution_height"]))
        self.__logger.info (f'Camera resolution {self.__video_source.get(cv.CAP_PROP_FRAME_WIDTH)}x{self.__video_source.get(cv.CAP_PROP_FRAME_HEIGHT)}')

        main_window.SessionUpdate.connect(self.__on_session_change)


    def __load_ai_networks(self, ai_config) -> int:
        start_t         = commons.ms_timestamp()
        ie              = IECore()
        self.__networks = {
            "face"          : Network(ie, ai_config['face_detection_net_executor'], ai_config['face_detection_model_prefix']),
            "age-gender"    : Network(ie, ai_config['age_gender_net_executor'], ai_config['age_gender_model_prefix']),
            "emotions"      : Network(ie, ai_config['emotions_net_executor'], ai_config['emotions_model_prefix'])
        }
        
        return commons.ms_timestamp() - start_t


    def __on_session_change(self, current_session):
        self.__current_session  = current_session
        curr_status             = current_session.current_status
        if curr_status == commons.Status.STANDBY or curr_status == commons.Status.RECOGNITION:
            self.start()
        else:
            self.stop()


    def __perform_face_detection(self, curr_frame):
        net             = self.__networks["face"]
        w               = net.width
        h               = net.height
        input_info      = net.input_info
        executor        = net.executor

        resized_frame   = cv.resize(curr_frame, (w,h))
        input_frame     = np.expand_dims(resized_frame.transpose(2, 0, 1), 0)

        tmp_results     = executor.infer(inputs={input_info: input_frame})

        resolution_x    = curr_frame.shape[1]
        resolution_y    = curr_frame.shape[0]
        
        # Fetching image shapes to calculate ratio
        (real_y, real_x), (resized_y, resized_x) = curr_frame.shape[:2], resized_frame.shape[:2]
        ratio_x, ratio_y = real_x / resized_x, real_y / resized_y
        
        final_results   = []

        for i in range(tmp_results["detection_out"].shape[2]):
            curr_conf   = tmp_results["detection_out"][0,0,i,2]
            if curr_conf >= self.__min_conf :
                # Convert float to int and multiply corner position of each box by x and y ratio
                # In case that bounding box is found at the top of the image,
                # we position upper box bar little bit lower to make it visible on image(
                (x_min, y_min, x_max, y_max) = [
                    int(max(corner_position * ratio_y *resized_y, 10)) if idx % 2
                    else int(max(corner_position * ratio_x *resized_x, 10))
                    for idx, corner_position in enumerate(tmp_results["detection_out"][0,0,i,3:])
                ]
                final_results.append (Detection(x_min, y_min, x_max, y_max, curr_conf))
        
        return final_results


    def __infer_age_emotions (self, face_frame) :

        customer_info   = {
            "emotion"   : None,
            "age"       : None,
            "gender"    : None
        }

        ag_net  = self.__networks["age-gender"]
        em_net  = self.__networks["emotions"]

        resized_custome_face_ag = cv.resize(face_frame, (ag_net.width, ag_net.height))
        resized_custome_face_em = cv.resize(face_frame, (em_net.width, em_net.height))
        input_custome_face_ag   = np.expand_dims(resized_custome_face_ag.transpose(2, 0, 1), 0)
        input_custome_face_em   = np.expand_dims(resized_custome_face_em.transpose(2, 0, 1), 0)
        age_gender_prediction   = ag_net.executor.infer(inputs={ag_net.input_info: input_custome_face_ag})
        emotions_prediction     = em_net.executor.infer(inputs={em_net.input_info: input_custome_face_em})['prob_emotion'][0, :, 0, 0]

        if np.argmax(age_gender_prediction["prob"]) == 0:
            customer_info["gender"] = "F"
        elif np.argmax(age_gender_prediction["prob"]) == 1:
            customer_info["gender"] = "M"
        customer_info["emotions"]   = commons.emotions[np.argmax(emotions_prediction)]
        customer_info["age"]        = int(age_gender_prediction["age_conv3"][0,0,0,0]*100)

        return customer_info


    def __get_target_face_idx(self, frame, detections):
        # Chosing the target face by considering the distance from the center of frame
        new_frame       = frame.copy()
        res_x           = frame.shape[1]
        res_y           = frame.shape[0]
        frame_center    = np.array([int(res_x/2), int(res_y/2)])
        min_dist        = None
        target_det_idx  = None
        
        cv.circle(new_frame, (frame_center[0], frame_center[1]), 5, (255, 0, 0), 2)

        for i in range(len(detections)):
            d           = detections[i]
            tl          = np.array([d.min.x(), d.min.y()])
            br          = np.array([d.max.x(), d.max.y()])
            curr_center = commons.midpoint(tl, br)

            if i==0 :
                min_dist        = math.dist(frame_center, curr_center)
                target_det_idx  = i
            else :
                curr_dist    = math.dist(frame_center, curr_center)
                if curr_dist < min_dist :
                    min_dist        = curr_dist
                    target_det_idx  = i


        return target_det_idx



    def run(self):
        start_time_detection    = None  
        self.__customer_found   = False
        self.__freezed_frame    = None
        self.__target_detection = None
        self.__customer_info    = None

        while not self.__customer_found:
            try :
                status,frame    = self.__video_source.read()
                final_frame     = cv.flip(cv.cvtColor(frame, cv.COLOR_BGR2RGB),1)
                detections      = self.__perform_face_detection(final_frame)
                curr_time       = commons.ms_timestamp()

                if self.__current_session.current_status == commons.Status.STANDBY:
                    self.NewImage.emit(final_frame.copy(), detections, 0)

                    if len(detections)>0:
                        if start_time_detection == None:
                            start_time_detection    = commons.ms_timestamp()
                        elif curr_time-start_time_detection >= self.__new_person_threshold :
                            self.NewPerson.emit()
                            pass
                    else:
                        start_time_detection    = None

                elif self.__current_session.current_status == commons.Status.RECOGNITION:
                    # Still retrieving camera frames and providing them to subscribers
                    self.NewImage.emit(final_frame.copy(), detections, 0)

                    # Needed when customer move from SELECTION status to RECOGNITION one
                    if start_time_detection == None:
                        start_time_detection    = commons.ms_timestamp()

                    if len(detections) == 0:
                        # TODO Add a timeout to prevent oscillations
                        self.EscapedPerson.emit()

                    elif curr_time-start_time_detection >= self.__new_customer_threshold :
                        # Freezing image and face
                        self.__customer_found   = True
                        self.__freezed_frame    = final_frame.copy()
                        # Retrieving the target detection from all the detections
                        freezed_face_idx        = self.__get_target_face_idx(self.__freezed_frame, detections)
                        self.__target_detection = detections[freezed_face_idx]
                        # Inferring emotion and age values on freezed face
                        d                       = self.__target_detection
                        freezed_face            = self.__freezed_frame[d.min.y():d.max.y(), d.min.x():d.max.x(), :]
                        self.__customer_info    = self.__infer_age_emotions (freezed_face)
                        # Go to SUGGESTION status
                        self.NewImage.emit(self.__freezed_frame, [self.__target_detection], None)
                        self.NewCustomer.emit(self.__freezed_frame, self.__target_detection, self.__customer_info)
                    else:
                        # Do nothing
                        pass
                else:
                    self.__logger.error("Wrong status: VideoThread should be stopped!")

            except RuntimeError as re:
                self.__logger.error (f"Catched this runtime error: {re}")
            except TypeError as te:
                self.__logger.error (f"Catched this type error: {te}")
            except Exception as e:
                self.__logger.error (f"Catched this generic exception: {e}")


    def start(self):
        # Starting the thread task
        if not self.isRunning():
            super().start()
        else:
            self.__logger.warning("Thread already running!")


    def activate(self):
        # TODO Activate the camera loading
        pass


    def deactivate(self):
        # TODO Deactivate the camera loading
        pass


    def stop(self):
        # Stopping the thread task
        self.__customer_found   = True


    def get_current_frame(self):
        # TODO Retrieving current (maybe freezed) image
        pass


    def get_last_inference_info(self):
        return (self.__freezed_frame, self.__target_detection, self.__customer_info)
    

    def has_freezed_frame(self):
        return (self.__freezed_frame != None)