
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
        res = "Sat down"
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
        res = "text-bg-accent"
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

export function patientStatusToDatailsTitle (s: PatientStatus) {
    let res

    switch (s) {
    case PatientStatus.NORMAL :
        res = "No warning"
        break
    case PatientStatus.WARNING :
        res = "Warning"
        break
    case PatientStatus.ALERT :
        res = "Alert"
        break
    default:
        throw `[patientStatusToDatailsTitle] Invalid parameter "${s}"`
    }

    return res
}

export function patientStatusToDatailsBody (s: PatientStatus) {
    let res

    switch (s) {
    case PatientStatus.NORMAL :
        res = "The patient is in good condition, CLEA Platform will alert you in time if any anomalies."
        break
    case PatientStatus.WARNING :
        res = "Attention, the CLEA AI monitoring system detected a patient sitting. You should go and help him."
        break
    case PatientStatus.ALERT :
        res = "Attention, the CLEA AI monitoring system detected a patient raised. You should go and help him."
        break
    default:
        throw `[patientStatusToDatailsBody] Invalid parameter "${s}"`
    }

    return res
}

export function normalizeConfidence (c: number) {
    return Number(c.toFixed(3))
}
