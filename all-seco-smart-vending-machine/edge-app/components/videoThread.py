
import cv2 as cv, numpy as np, pandas, logging, time

from utils import commons
from openvino.inference_engine import IECore

from PySide6.QtCore import Signal, QThread
from PySide6.QtWidgets import QWidget


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
    x_min   = None
    y_min   = None
    x_max   = None
    y_max   = None
    conf    = None

    def __init__(self, x_min, y_min, x_max, y_max, conf) -> None:
        self.x_min  = x_min
        self.y_min  = y_min
        self.x_max  = x_max
        self.y_max  = y_max
        self.conf   = conf


class VideoThread (QThread) :

    ## Signals
    NewImage    = Signal (object, Detection) # TODO Define signal type
    ## Members
    __logger        = None
    __video_source  = None
    __freezed_image = None
    __networks      = None
    __min_conf      = None


    def __init__(self, main_window, config) -> None:
        super().__init__()

        self.__min_conf     = float(config["ai"]["face_deection_minimum_confidence"])

        self.__logger       = commons.create_logger(logging, __name__)
        
        self.__logger.debug(f"Loading networks..")
        self.__logger.debug(f'All networks loaded in {self.__load_ai_networks(config["ai"])} seconds')
        # Setting up video source
        self.__video_source = cv.VideoCapture(config["app"]["video_source"])
        self.__video_source.set(cv.CAP_PROP_FRAME_WIDTH, int(config["app"]["video_resolution_width"]))
        self.__video_source.set(cv.CAP_PROP_FRAME_HEIGHT, int(config["app"]["video_resolution_height"]))
        self.__logger.info (f'Camera resolution {self.__video_source.get(cv.CAP_PROP_FRAME_WIDTH)}x{self.__video_source.get(cv.CAP_PROP_FRAME_HEIGHT)}')


    def __load_ai_networks(self, ai_config) -> int:
        start_t         = time.time()
        ie              = IECore()
        self.__networks = {
            "face"          : Network(ie, ai_config['face_detection_net_executor'], ai_config['face_detection_model_prefix']),
            "age-gender"    : Network(ie, ai_config['age_gender_net_executor'], ai_config['age_gender_model_prefix']),
            "emotions"      : Network(ie, ai_config['emotions_net_executor'], ai_config['emotions_model_prefix'])
        }
        
        return time.time() - start_t


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


    def run(self):
        time_point  = 0
        while True:
            try :
                time_point      = time.time()
                status,frame    = self.__video_source.read()
                final_frame     = cv.flip(cv.cvtColor(frame, cv.COLOR_BGR2RGB),1)
                detections      = self.__perform_face_detection(final_frame)
                
                self.NewImage.emit(final_frame.copy(), detections)
                

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
            self.__logger.error("Thread already running!")


    def activate(self):
        # TODO Activate the camera loading
        pass


    def deactivate(self):
        # TODO Deactivate the camera loading
        pass


    def stop(self):
        # TODO Stopping the thread task
        pass


    def get_current_frame(self):
        # TODO Retrieving current (maybe freezed) image
        pass