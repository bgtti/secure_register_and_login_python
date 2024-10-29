import { apiHandle404 } from "../../axios";
import apiEndpoints from "../../apiEndpoints";
import { emailValidation } from "../../../utils/validation"
import { INPUT_LENGTH, FLAG_TYPES } from "../../../utils/constants"
import { getUTCString, validateDate, dateToYYYYMMDD } from "../../../utils/helpers"

/**
 * Function makes api call to set the status of a message (whether an answer is needed or if it is spam) and whether the sender should be marked as a spammer.
 * 
 * The message's id and answerNeeded are required parameters. answerNeeded is true to mark message as 'reply needed', or false to mark as 'no reply needed'. The optional argument isSpam can be set to true to send the message to the spam folder, and the other optional argument, senderIsSpammer, will mark all future messages from the sander as spam when set to 'true'. 
 * 
 * @param {number} messageId (the message's id)
 * @param {bool} answerNeeded (true to mark as reply needed)
 * @param {bool} [isSpam] (optional: true to mark message as spam) //= false
 * @param {bool} [senderIsSpammer] (optional:true to mark sender as a spammer) //= false
 * @returns {object}
 * 
 * @example
 * //Usage:
 * markMessageAs(55, false)
 * 
 * //Success response:
 * {
 *  success: true
 * }
 * 
 * //Error response:
 * {
 *  success: false
 * }
 */
export function markMessageAs(messageId, answerNeeded, isSpam = false, senderIsSpammer = false) {
    let theId = (messageId && Number.isInteger(messageId)) ? messageId : "";
    let theAnsNeed = (answerNeeded || (typeof answerNeeded === "boolean")) ? answerNeeded : "";
    let theIsSpam = (isSpam || (typeof isSpam === "boolean")) ? isSpam : "";
    let theIsSpammer = (senderIsSpammer || (typeof senderIsSpammer === "boolean")) ? senderIsSpammer : "";

    if (theId === "" || theAnsNeed === "" || theIsSpam === "" || theIsSpammer === "") {
        console.warn("Improper arguments provided to markMessageAs function.")
        return { success: false }
    }

    let requestData = {
        "message_id": theId,
        "answer_needed": theAnsNeed,
        "is_spam": theIsSpam,
        "sender_is_spammer": theIsSpammer
    }
    const getData = async () => {
        try {
            const response = await apiHandle404.post(apiEndpoints.adminMessageMarkAs, requestData)
            if (response.status === 200) {
                return { success: true }
            } else {
                return { success: false }
            }
        }
        catch (error) {
            console.error("Error marking message as no answer needed:", error);
            return { success: false }
        }
    }

    return getData();

}








// /**
//  * Function makes api call to set a message status to 'no answer needed' or back to 'answer needed.
//  * 
//  * The message's id and markNoAnswer are required parameters. markNoAnswer is true to mark message as no reply needed, or false to mark as reply needed.
//  * 
//  * @param {number} id (the message's id)
//  * @param {bool} markNoAnswer (true to mark as no reply needed, false to mark as reply needed)
//  * @returns {object}
//  * 
//  * @example
//  * //Usage:
//  * markMessageNoAnswerNeeded(55)
//  * 
//  * //Success response:
//  * {
//  *  success: true
//  * }
//  * 
//  * //Error response:
//  * {
//  *  success: false
//  * }
//  */
// export function markMessageNoAnswerNeeded(id, markNoAnswer) {
//     let theId = (id && Number.isInteger(id)) ? id : "";
//     let theMark = (markNoAnswer && (typeof markNoAnswer === "boolean")) ? markNoAnswer : "";

//     if (theId === "" || theMark === "") {
//         console.warn("No message id provided to markMessageNoAnswerNeeded.")
//         return { success: false }
//     }

//     let requestData = {
//         "message_id": theId,
//         "mark_no_answer_needed": theMark
//     }
//     const getData = async () => {
//         try {
//             const response = await apiHandle404.post(apiEndpoints.adminMessageMarkNoAnswer, requestData)
//             if (response.status === 200) {
//                 return { success: true }
//             } else {
//                 return { success: false }
//             }
//         }
//         catch (error) {
//             console.error("Error marking message as no answer needed:", error);
//             return { success: false }
//         }
//     }

//     return getData();

// }

export function markMessageAnswered(id, messageAnsweredBy, messageAnsweredText, messageAnswerDate = false) {
    let theId = (id && Number.isInteger(id)) ? id : false;
    let theEmail = (messageAnsweredBy && emailValidation(messageAnsweredBy)) ? messageAnsweredBy : false;
    let theText = (messageAnsweredText && (typeof messageAnsweredText === "string") && messageAnsweredText.length <= INPUT_LENGTH.contactMessage.maxValue) ? messageAnsweredText : false;

    if (!theId || !theEmail || !theText) {
        console.warn("Wrong parameter provided to markMessageAnswered.")
        return { success: false }
    }

    let requestData = {
        "message_id": theId,
        "answered_by": theEmail,
        "answer": theText
    }

    let today = dateToYYYYMMDD(new Date())
    let theDate = messageAnswerDate && validateDate(messageAnswerDate, "yyyy/mm/dd") && messageAnswerDate !== today

    if (theDate) { requestData["answer_date"] = messageAnswerDate }

    const getData = async () => {
        try {
            const response = await apiHandle404.post(apiEndpoints.adminMessageAnswer, requestData)
            if (response.status === 200) {
                return { success: true }
            } else {
                return { success: false }
            }
        }
        catch (error) {
            console.error("Error marking message as answered:", error);
            return { success: false }
        }
    }

    return getData();

}

export function changeMessageFlag(id, flagColour) {
    let theId = (id && Number.isInteger(id)) ? id : "";
    let theFlag = (flagColour && FLAG_TYPES.includes(flagColour)) ? flagColour : "";

    if (theId === "" || theFlag === "") {
        console.warn("Wrong parameters provided to changeMessageFlag.")
        return { success: false }
    }

    let requestData = {
        "message_id": theId,
        "message_flag": theFlag,
    }
    const getData = async () => {
        try {
            const response = await apiHandle404.post(apiEndpoints.adminMessageFlagChange, requestData)
            if (response.status === 200) {
                return { success: true }
            } else {
                return { success: false }
            }
        }
        catch (error) {
            console.error("Error changing message flag:", error);
            return { success: false }
        }
    }

    return getData();

}

export function deleteMessage(id) {
    let theId = (id && Number.isInteger(id)) ? id : "";

    if (theId === "") {
        console.warn("Wrong parameters provided to v.")
        return { success: false }
    }

    let requestData = {
        "message_id": theId
    }
    const getData = async () => {
        try {
            const response = await apiHandle404.post(apiEndpoints.adminMessageDelete, requestData)
            if (response.status === 200) {
                return { success: true }
            } else {
                return { success: false }
            }
        }
        catch (error) {
            console.error("Error deleting message:", error);
            return { success: false }
        }
    }

    return getData();

}