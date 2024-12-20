import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { setReduxUserAcctVerification } from "../../../redux/utilsRedux/setReduxUserState.js";
import { sanitizedUserAgent, tokenFormatIsValid } from "../../../utils/validation.js"
import { stringToBool } from "../../../utils/helpers.js"



/**
 * Function makes api call to request a token for the user to verify the email address.
 * 
 * @param {string} newEmail
 * @param {string} userAgent
 * @returns {object}
 * The return will always contain a boolean "success".
 * 
 * @example
 * //Input example:
 * const user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
 * }
 * acctRequestVerifyEmail(user_agent)
 * 
 * //Original API response:
 * {
 *  "response": "success",
 *  "mail_sent": true,
 * }
 * 
 * // Response from acctRequestVerifyEmail:
 * acctRequestVerifyEmail(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // the redux user state may be changed: user.acctVerifyEmail will be se to "pending" if resonse is successfull 
 * // a successfull response will yield:
 * { success: true }
 * // an error response might yield:
 * { success: false }
 */
export function acctRequestVerifyEmail(userAgent) {
    // checking if argument was received correctly
    const userAgentIsValid = sanitizedUserAgent(userAgent)
    const agent = userAgentIsValid ? userAgent : "";

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
                    let emailWasSent = stringToBool(response.data.mail_sent)
                    if (emailWasSent) {
                        setReduxUserAcctVerification("pending")
                        return { success: true }
                    }
                    else {
                        setReduxUserAcctVerification(false)
                        return { success: false, info: "An error occurred and the email could not be sent." }
                    }
                case 400:
                case 401:
                case 409:
                default:
                    return { success: false, info: "An error occurred. Please close modal and try again." }
            }
        }
        catch (error) {
            console.error(`Api handler to request email verification link encountered an error: ${error}`)
            return { success: false, info: "An error occurred. Please close modal and try again." }
        }
    }

    return requestVerificationLink();
};

/**
 * Function makes api call to verify a token used for email address verification.
 * 
 * @param {string} tokenUsed
 * @returns {object}
 * The return will always contain a boolean "success".
 * 
 * @example
 * //Input example:
 * const tokenUsed = "Il94YzZPcElIUFdjRi0wZ3MyelU2NW91Unl0b3lJMlN3RWpkTGctblBvT3Mi.Z03aPA.CtQImrnVkLtUH0VpAyRrdzIcuGU"
 * }
 * confirmEmailVerification(tokenUsed)
 * 
 * //Original API response:
 * {
 *  "response": "success",
 *  "mail_sent": true,
 *  "acct_verified": true,
 * }
 * 
 * // Response from confirmEmailChange:
 * confirmEmailVerification(tokenUsed)
 *      .then(response => {
 *          console.log (response)
 * })
 * // the redux user state may be changed: user.acctVerifyEmail will be se to true if resonse is successfull 
 * // a successfull response where the credentials have not been changed (only one token was verified):
 * { success: true }
 * // a failed response:
 * { success: false, info: "An error occurred." }
 */
export function confirmEmailVerification(tokenUsed) {
    // checking if argument was received correctly
    const token = (tokenUsed && tokenFormatIsValid(tokenUsed)) ? tokenUsed.trim() : false

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
                    // set redux
                    setReduxUserAcctVerification(true)
                    // return to component
                    let res = {
                        success: true,
                    }
                    return res
                case 400:
                case 401:
                case 409:
                default:
                    setReduxUserAcctVerification(false) // set redux
                    return { success: false, info: "An error occurred." } // return to component
            }
        }
        catch (error) {
            console.error(`Api handler to verify email token encountered an error: ${error}`)
            return { success: false, info: "An error occurred." }
        }
    }

    return verifyEmail();
};