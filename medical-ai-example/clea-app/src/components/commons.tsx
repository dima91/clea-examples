

export enum PatientStatus {
    NORMAL  = 0,
    WARNING = 1,
    ALERT   = 2
}


export type Event = {
    roomId              : number,
    timestamp           : number,
    eventType           : string,
    confidence          : number,
    initFrameContent    : Uint8Array | undefined,
    initFrameURL        : string | undefined

}


export type RoomDescriptor = {
    roomId                      : number,
    patientId                   : number,
    currentEvent                : Event,
    diagnosis                   : string,
    patientHospitalizationDate  : number,
    patientReleaseDate          : number
}


// ======================================
//    Patient status utility functions
// ======================================
export function stringToPatientStatus (s : string) {
    let res

    switch (s) {
    case "NORMAL":
        res = PatientStatus.NORMAL
        break
    case "WARNING":
        res = PatientStatus.WARNING
        break
    case "ALERT":
        res = PatientStatus.ALERT
        break
    default:
        throw `[stringToPatientStatus] Invalid parameter "${s}"`
    }

    return res
}

export function patientStatusToString (s : PatientStatus) {
    let res

    switch (s) {
    case PatientStatus.NORMAL :
        res = "NORMAL"
        break
    case PatientStatus.WARNING :
        res = "WARNING"
        break
    case PatientStatus.ALERT :
        res = "ALERT"
        break
    default:
        throw `[patientStatusToString] Invalid parameter "${s}"`
    }

    return res
}

export function patientStatusToDescriptionString (s : PatientStatus) {
    let res

    switch (s) {
    case PatientStatus.NORMAL :
        res = "Lying down"
        break
    case PatientStatus.WARNING :
        res = "Sitting"
        break
    case PatientStatus.ALERT :
        res = "Raised"
        break
    default:
        throw `[patientStatusToString] Invalid parameter "${s}"`
    }

    return res
}

export function patientStatusToStringColor (s : PatientStatus) {
    let res

    switch (s) {
    case undefined :
        res = ""
        break
    case PatientStatus.NORMAL :
        res = "bg-success"
        break
    case PatientStatus.WARNING :
        res = "bg-warning"
        break
    case PatientStatus.ALERT :
        res = "bg-danger"
        break
    default:
        throw `[patientStatusToStringColor] Invalid parameter "${s}"`
    }

    return res
}

export function patientStatusToGradientClass (s : PatientStatus) {
    let res

    switch (s) {
    case undefined :
        res = ""
        break
    case PatientStatus.NORMAL :
        res = "bg-info"
        break
    case PatientStatus.WARNING :
        res = "warning-gradient-bg"
        break
    case PatientStatus.ALERT :
        res = "alert-gradient-bg"
        break
    default:
        throw `[patientStatusToStringColor] Invalid parameter "${s}"`
    }

    return res
}