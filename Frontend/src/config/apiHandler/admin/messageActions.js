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
 * @returns {Promise<object>}
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
        return Promise.resolve({ success: false })
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
                return Promise.resolve({ success: true })
            } else {
                return Promise.resolve({ success: false })
            }
        }
        catch (error) {
            console.error("Error marking message as no answer needed:", error);
            return Promise.resolve({ success: false })
        }
    }

    return getData();
}



/**
 * Function makes api call to record an answer as a reply to a user message in the DB. Optionally, the reply may be sent by the system's email.
 *
 * @param {object} answerData
 * @param {number} answerData.id (the message's id) 
 * @param {string} answerData.answer (answer text)
 * @param {string} answerData.subject (OPTIONAL: subject of the answer email)
 * @param {string} answerData.answeredBy (OPTIONAL: email of admin answering the message)
 * @param {string} answerData.answerDate (OPTIONAL: date the message was answered)
 * @param {bool} sendAnsByEmail (true will send the answer to the sender's stored email address)
 * @returns {object}
 *
 * @example
 * //Usage:
 * const ansData = {
 *  id: 5,
 *  answer:"Thank you for your recommendation, John.",
 *  subject:"Re: recommendation",
 *  answeredBy:"milton@fakemail.com",
 *  answerDate:"2024-11-01"
 * }
 * answerMessage(ansData, true)
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
export function answerMessage(answerData, sendAnsByEmail = false) {
    //Error message
    const error_mes = "Function answerMessage encountered an issue. Check the arguments."

    //Checking required values
    if (arguments.length < 2 || sendAnsByEmail === undefined || (typeof sendAnsByEmail !== 'boolean')) {
        console.warn(error_mes);
        return Promise.resolve({ success: false })
    }
    const id = (answerData.hasOwnProperty("id") && Number.isInteger(answerData.id)) ? answerData.id : false;
    const answer = (answerData.hasOwnProperty("id") && (typeof answerData.answer === "string") && answerData.answer.length <= INPUT_LENGTH.contactMessage.maxValue) ? answerData.answer : false;

    if (!id && !answer) { console.warn(error_mes); return Promise.resolve({ success: false }); }

    //Checking optional values
    const subject = (answerData.hasOwnProperty("subject") && (typeof answerData.subject === "string") && answerData.subject.length <= INPUT_LENGTH.contactMessageAnswerSubject.maxValue) ? answerData.subject : false;
    const answeredBy = (answerData.hasOwnProperty("answeredBy") && emailValidation(answerData.answeredBy)) ? answerData.answeredBy : false;
    const today = dateToYYYYMMDD(new Date())
    const answerDate = (answerData.hasOwnProperty("answerDate") && validateDate(answerData.answerDate, "yyyy-mm-dd")) && answerData.answerDate !== today ? answerData.answerDate : false;

    //Preparing payload
    let requestData = {
        "message_id": id,
        "email_answer": sendAnsByEmail,
        "answer": answer,
    }

    if (subject) { requestData["subject"] = subject }
    if (answeredBy) { requestData["answered_by"] = answeredBy }
    if (answerDate) { requestData["answer_date"] = answerDate }

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