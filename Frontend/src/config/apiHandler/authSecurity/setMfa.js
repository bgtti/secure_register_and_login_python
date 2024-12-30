import { apiCredentials } from "../../axios.js";
import { setReduxUserMfa } from "../../../redux/utilsRedux/setReduxUserState.js";
import apiEndpoints from "../../apiEndpoints.js";
import { stringToBool } from "../../../utils/helpers.js"
import { passwordValidationSimplified, otpValidation, sanitizedUserAgent } from "../../../utils/validation.js";

/**
 * Async function that makes api call to set a recovery email address.
 * 
 * @param {object} data 
 * @param {bool} data.enableMfa # indicates whether mfa shoud be enabled (true) or disabled (false)
 * @param {string} data.password # the password provided by user
 * @param {string} [data.otp] # otp only required if MFA should be disabled
 * @param {string} [data.userAgent]
 * @returns {object} # with boolean "response",  and string "message"
 * 
 * @example
 * //Input example:
 * const data = {
 *     enableMfa: false,
 *     password: "108854cd4b588sszb64010",
 *     otp: "12345678",
 *     userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
 * }
 * 
 * // Response from disableMfa:
 * setMfa(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // a successfull response will yield:
 * {
        response: true,
        message: "MFA was disabled successfully!"
    }
 *  // an error response might yield:
    {
        response: false,
        message: "An error occurred, please try again."
    }
 */
export function setMfa(data) {
    // checking user agent
    const userAgent = data.userAgent ? data.userAgent : "";
    const agent = userAgent !== "" ? sanitizedUserAgent(userAgent) : userAgent;

    // standard error response
    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    //checking required data
    if (!data.password) { return errorResponse };
    if (typeof data.enableMfa !== "boolean") { return errorResponse };

    // double-checking password
    const passwordIsValid = passwordValidationSimplified(data.password);
    if (!passwordIsValid.response) { return errorResponse }

    let requestData = {
        "password": data.password,
        "user_agent": agent,
        "enable_mfa": data.enableMfa
    }

    //OTP is required when disabling MFA
    if (!data.enableMfa) {
        if (!data.otp) { return errorResponse };
        const otpIsValid = otpValidation(data.otp)
        if (!otpIsValid.response) { return errorResponse };
        requestData.otp = data.otp
    }

    // preparing the returned response
    let res = {
        response: false,
        message: ""
    }

    // making the request
    const editMfa = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.setMfa, requestData);

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    //Logging user info in Redux store
                    res.response = setReduxUserMfa(
                        response.data.mfa_enabled,
                    )
                    let enabled = stringToBool(response.data.mfa_enabled)
                    res.message = `MFA was ${enabled ? "enabled" : "disabled"} successfully!`
                    break;
                case 400:
                case 401:
                case 403:
                    res.message = response.data.response ? response.data.response : "An error occurred: MFA could not be set";
                    break;
                default:
                    res.message = "An error occurred, please try again."
                    break;
            }
        } catch {
            res.message = "Error: Please refresh the page and try again."
            // console.error("Error:", error); // Logs the error
        }
        return res;
    }
    return editMfa();
}