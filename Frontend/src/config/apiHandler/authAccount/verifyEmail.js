import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { nameValidation, emailValidation, passwordValidation, sanitizedUserAgent, tokenFormatIsValid } from "../../../utils/validation.js"
import { setReduxLogInUser } from "../../../redux/utilsRedux/setReduxUserState.js";



/**
 * Function makes api call to request a token for the user to verify the email address.
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
export function acctRequestVerifyEmail(userAgent) {
    // checking if argument was received correctly
    const agent = userAgent ? sanitizedUserAgent(userAgent) : "";

    let requestData = {
        "user_agent": agent,
    }

    // making the request
    const requestVerificationLink = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.acctRequestVerifyEmail, requestData)

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

    return requestVerificationLink();
};

/**
 * Function makes api call to verify a token used for email address verification.
 * 
 * @todo fix this docstring
 * 
 * 
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
export function confirmEmailVerification(tokenUsed) {
    // checking if argument was received correctly
    const token = (tokenUsed && tokenFormatIsValid(tokenUsed)) ? tokenUsed.trim() : false;

    if (!token) {
        console.error("Error: invalid input.")
        return { success: false }
    }

    let requestData = {
        "signed_token": token,
    }

    // making the request
    const verifyEmail = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.acctVerifyEmail, requestData)

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    let res = {
                        success: true,
                    }
                    //userSlice: update user.acctVerified !!! TODO
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

    return verifyEmail();
};