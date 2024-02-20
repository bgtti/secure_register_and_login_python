import { api } from "../axios";
import apiEndpoints from "../apiEndPoints";
import { nameValidation, emailValidation, passwordValidation } from "../../utils/validation"
import { setReduxLogOutUser } from "../../redux/utilsRedux/setReduxUserState.js";
import { INPUT_LENGTH } from "../../utils/constants.js"

/**
 * Function makes api call to send a contact form message.
 * Needs an object as parameter with the name, email, message, honeypot, and a boolean indicating whether a logged in user is the one sending the form
 * 
 * Returns an object with a response key and boolean value.
 * 
 * @param {object} data 
 * @param {string} data.name 
 * @param {string} data.email 
 * @param {string} data.message
 * @param {boolean} data.is_user
 * @param {string} data.honeypot
 * @returns {object}
 * 
 * @example
 * //Input example:
 * const data = {
 *     name: "Josy",
 *     email: "josy@example.comm",
 *     message: "Hello",
 *     is_user: false,
 *     honeypot: ""
 * }
 * // Response from sendContactMessage:
 * {
        response: true,
    }
    // an error response might yield:
    {
        response: false
    }
 */
export function sendContactMessage(data = {}) {
    // checking if data was received correctly
    const name = data.name ? data.name : false;
    const email = data.email ? data.email : false;
    const message = data.message ? data.message : false;
    const is_user = data.is_user ? data.is_user : false;
    const honeypot = data.honeypot ? data.honeypot : "";

    // preparing the returned response
    let res = {
        response: false,
        message: "Error: Invalid input."
    }

    if (!data.name || !data.email || !data.message) {
        return res
    }

    // double-checking the data
    const nameIsValid = nameValidation(name);
    const emailIsValid = emailValidation(email);
    const messageIsValid = message.length >= INPUT_LENGTH.contactMessage.minValue && message.length <= INPUT_LENGTH.contactMessage.maxValue;
    const dataIsValid = emailIsValid.response && nameIsValid.response && messageIsValid;

    if (!dataIsValid) {
        return res
    }

    let requestData = {
        "name": name,
        "email": email,
        "message": message,
        "is_user": is_user,
        "honeypot": honeypot
    }

    // making the request
    const sendMessage = async () => {
        try {
            const response = await api.post(apiEndpoints.contactUs, requestData)

            let responseStatus = response.request.status;

            if (responseStatus === 200) {
                res.response = true;
                res.message = "Message sent. Thank you!";
            }

        }
        catch (error) {
            console.warn(`Api handler sendContactMessage encountered an error: ${error}`)
        }
        return res;
    }

    return sendMessage();

}