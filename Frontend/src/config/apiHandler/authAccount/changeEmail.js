import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { nameValidation, emailValidation, passwordValidation, sanitizedUserAgent, tokenFormatIsValid } from "../../../utils/validation.js"
import { setReduxLogInUser } from "../../../redux/utilsRedux/setReduxUserState.js";



/**
 * Function makes api call to change a user's email.
 * 
 * @todo fix this docstring
 * 
 * 
 * @param {string} newEmail
 * @param {string} userAgent
 * @returns {object}
 * The return will always contain a boolean "success".
 * The return may contain "info" in the response when relevant.
 * 
 * @example
 * //Input example:
 * const data = {
 *     new_email: "josy@example.com",
 *     user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
 * }
 * acctEmailChange(data.new_email, data.user_agent)
 * 
 * //Original API response:
 * {
 *  "response": "success",
 *  "mail_sent": true,
 * }
 * 
 * // Response from acctEmailChange:
 * acctEmailChange(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // a successfull response will yield:
 * { success: true }
 * // an error response might yield:
 * { success: false }
 * // a successfull response, but mail_sent is false (meaning there was a problem sending the verification email):
 * { success: false, info: "A problem occurred" }
 */
export function acctEmailChange(newEmail, userAgent) {
    // checking if argument was received correctly
    const email = newEmail ? newEmail : false;
    const agent = userAgent ? sanitizedUserAgent(userAgent) : "";

    if (!newEmail) {
        console.error("Error: no input to change.")
        return { success: false }
    }

    // double-checking the data
    const emailIsValid = emailValidation(email);

    if (!emailIsValid.response) {
        console.error("Error: input invalid.")
        return { success: false }
    }

    let requestData = {
        "type": "email",
        "new_email": email,
        "user_agent": agent,
    }

    // making the request
    const changeEmail = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.acctChangeEmail, requestData)

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    let emailWasSent = response.data.mail_sent
                    if (emailWasSent) { return { success: true } }
                    else { return { success: false, info: "One or more emails invalid" } }
                case 400:
                case 401:
                case 409:
                default:
                    return { success: false, info: "An error occurred. Please close modal and try again." }
            }
        }
        catch (error) {
            console.error(`Api handler to change name encountered an error: ${error}`)
            return { success: false, info: "An error occurred. Please close modal and try again." }
        }
    }

    return changeEmail();
};

/**
 * Function makes api call to change a user's email.
 * 
 * @todo fix this docstring
 * 
 * 
 * @param {string} pathUsed # one of ["confirmEmailChange", "confirmNewEmail"]
 * @param {string} tokenUsed
 * @returns {object}
 * The return will always contain a boolean "success".
 * The return may contain emailWasSent and credChanged when there is a successfull response. Their values are boolean and indicate whether an email has been sent to the user and the email credentials were changed in relation to this request
 * 
 * @example
 * //Input example:
 * const data = {
 *     pathUsed: "confirmEmailChange",
 *     tokenUsed: "Il94YzZPcElIUFdjRi0wZ3MyelU2NW91Unl0b3lJMlN3RWpkTGctblBvT3Mi.Z03aPA.CtQImrnVkLtUH0VpAyRrdzIcuGU",
 * }
 * confirmEmailChange(data.pathUsed, data.tokenUsed)
 * 
 * //Original API response:
 * {
 *  "response": "success",
 *  "mail_sent": true,
 *  "cred_changed": true,
 * }
 * 
 * // Response from confirmEmailChange:
 * confirmEmailChange(data.pathUsed, data.tokenUsed)
 *      .then(response => {
 *          console.log (response)
 * })
 * // a successfull response where the credentials have not been changed (only one token was verified):
 * { success: true, emailWasSent: false, credChanged: false }
 * // a successfull response where the credentials were changed and a success email was sent to user:
 * { success: true, emailWasSent: true, credChanged: true }
 * // a failed response:
 * { success: false, info: "An error occurred." }
 */
export function confirmEmailChange(pathUsed, tokenUsed) {
    // checking if argument was received correctly
    const validPaths = ["confirmEmailChange", "confirmNewEmail"]
    const urlPath = (pathUsed && validPaths.includes(pathUsed)) ? pathUsed : false;
    const token = (tokenUsed && tokenFormatIsValid(tokenUsed)) ? tokenUsed.trim() : false;

    if (!urlPath || !token) {
        console.error("Error: invalid input.")
        return { success: false }
    }

    const type = urlPath === "confirmEmailChange" ? "email_change_old_email" : "email_change_new_email"

    let requestData = {
        "purpose": type,
        "signed_token": token,
    }

    // making the request
    const changeEmail = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.acctChangeTokenVerify, requestData)

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    let res = {
                        success: true,
                        emailWasSent: response.data.email_sent, //this variable is not being used by the component at the moment
                        credChanged: response.data.cred_changed,
                    }
                    return res
                case 400:
                case 401:
                case 409:
                default:
                    return { success: false, info: "An error occurred." }
            }
        }
        catch (error) {
            console.error(`Api handler to change email encountered an error: ${error}`)
            return { success: false, info: "An error occurred." }
        }
    }

    return changeEmail();
};