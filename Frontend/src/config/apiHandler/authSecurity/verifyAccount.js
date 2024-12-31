import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { setReduxUserAcctVerification } from "../../../redux/utilsRedux/setReduxUserState.js";
import { sanitizedUserAgent, passwordValidationSimplified } from "../../../utils/validation.js"


/**
 * Function makes api call to request a token for the user to verify the email address.
 * 
 * @param {string} otp
 * @param {string} userAgent
 * @returns {object}
 * The return will always contain a boolean "success".
 * 
 * @example
 * //Input example:
 * const user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
 * const otp = "12345678"
 * acctRequestVerifyEmail(otp, user_agent)
 * 
 * // Response from acctRequestVerifyEmail:
 * acctRequestVerifyEmail(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // the redux user state may be changed: user.acctVerifyEmail will be se to true if resonse is successfull 
 * // a successfull response will yield:
 * { success: true,  info: "Account successfully verified!"}
 * // an error response might yield:
 * { success: false, info: "Error: Invalid otp format."}
 */
export function verifyAccount(otp, userAgent = "") {
    // checking if argument was received correctly
    const oneTimePassword = otp ? passwordValidationSimplified(otp) : false;
    const agent = sanitizedUserAgent(userAgent);

    const errorResponse = {
        response: false,
        status: 400,
        message: "Error: Invalid otp format."
    };

    if (!oneTimePassword || !oneTimePassword.response) {
        return errorResponse
    }

    let requestData = {
        "otp": otp,
        "user_agent": agent,
    }

    // making the request
    const requestVerifyAcct = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.verifyAccount, requestData)

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    setReduxUserAcctVerification(true)
                    return { success: true, info: "Account successfully verified!" }
                case 400:
                case 401:
                case 409:
                default:
                    let message = response.response.data.response;
                    return { success: false, info: message }
            }
        }
        catch (error) {
            console.error(`Api handler to verify user account encountered an error: ${error}`)
            return { success: false, info: "An error occurred. Please close modal and try again." }
        }
    }

    return requestVerifyAcct();
};

