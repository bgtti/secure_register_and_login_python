import { apiHandle404 } from "../../axios";
import apiEndpoints from "../../apiEndPoints";
import { emailValidation } from "../../../utils/validation"
import { INPUT_LENGTH, FLAG_TYPES } from "../../../utils/constants"

/**
 * Function makes api call to set a message status to 'no answer needed' or back to 'answer needed.
 * 
 * The message's id and markNoAnswer are required parameters. markNoAnswer is true to mark message as no reply needed, or false to mark as reply needed.
 * 
 * @param {number} id (the message's id)
 * @param {bool} markNoAnswer (true to mark as no reply needed, false to mark as reply needed)
 * @returns {object}
 * 
 * @example
 * //Usage:
 * markMessageNoAnswerNeeded(55)
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
export function markMessageNoAnswerNeeded(id, markNoAnswer) {
    let theId = (id && Number.isInteger(id)) ? id : "";
    let theMark = (markNoAnswer && (typeof markNoAnswer === "boolean")) ? markNoAnswer : "";

    if (theId === "" || theMark === "") {
        console.warn("No message id provided to markMessageNoAnswerNeeded.")
        return { success: false }
    }

    let requestData = {
        "message_id": theId,
        "mark_no_answer_needed": theMark
    }
    const getData = async () => {
        try {
            const response = await apiHandle404.post(apiEndpoints.adminMessageMarkNoAnswer, requestData)
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

export function markMessageAnswered(id, messageAnsweredBy, messageAnsweredText) {
    let theId = (id && Number.isInteger(id)) ? id : false;
    let theEmail = (messageAnsweredBy && emailValidation(messageAnsweredBy)) ? messageAnsweredBy : false;
    let theText = (messageAnsweredText && (typeof messageAnsweredText === "string") && messageAnsweredText.length <= INPUT_LENGTH.contactMessage.maxValue) ? messageAnsweredText : false;

    if (!theId || !theEmail || !theText) {
        console.warn("Wrong parameter provided to markMessageAnswered.")
        return { success: false }
    }

    let requestData = {
        "message_id": theId,
        "answeredBy": theEmail,
        "answer": theText
    }
    const getData = async () => {
        try {
            const response = await apiHandle404.post(apiEndpoints.adminMessageMarkAnswer, requestData)
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
        "flag_colour": theFlag,
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