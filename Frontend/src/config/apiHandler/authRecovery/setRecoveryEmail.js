import { apiCredentials } from "../../axios.js";
import { setReduxAccountRecovery } from "../../../redux/utilsRedux/setAccountRecovery.js";
import apiEndpoints from "../../apiEndpoints.js";
import { emailValidation, passwordValidationSimplified, otpValidation, sanitizedUserAgent } from "../../../utils/validation.js";

/**
 * Async function that makes api call to set a recovery email address.
 * 
 * @param {object} data 
 * @param {string} data.email # the recovery email as provided by user
 * @param {string} data.password # the password provided by user
 * @param {string} data.otp # the otp provided by user
 * @param {string} [data.userAgent]
 * @returns {object} # with boolean "response",  and string "message"
 * 
 * @example
 * //Input example:
 * const data = {
 *     email: "josy@example.com",
 *     password: "108854cd4b588sszb64010",
 *     otp: "12345678"
 * }
 * 
 * // Response from setRecoveryEmail:
 * setRecoveryEmail(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // a successfull response will yield:
 * {
        response: true,
        message: "Recovery email added successfully!"
    }
 *  // an error response might yield:
    {
        response: false,
        message: "Error: Failed to save recovery email."
    }
 */
export function setRecoveryEmail(data) {
    // checking if data was received correctly
    const email = data.email ? data.email : false;
    const password = data.password ? data.password : false;
    const otp = data.otp ? data.otp : false;
    const userAgent = data.userAgen ? data.userAgen : "";
    const agent = userAgent !== "" ? sanitizedUserAgent(userAgent) : userAgent;

    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    if (!email || !password || !otp) {
        return errorResponse
    };
    // double-checking the data
    const passwordIsValid = passwordValidationSimplified(password);
    const emailIsValid = emailValidation(email);
    const otpIsValid = otpValidation(otp);
    const dataIsValid = emailIsValid.response && passwordIsValid.response && otpIsValid.response;

    if (!dataIsValid) {
        return errorResponse
    }

    let requestData = {
        "recovery_email": email,
        "password": password,
        "otp": otp,
        "user_agent": agent,
    }

    // preparing the returned response
    let res = {
        response: false,
        message: ""
    }

    // making the request
    const saveRecoveryEmail = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.setRecoveryEmail, requestData);

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    res.response = true;
                    res.message = response.data.response
                    //Logging info in Redux store
                    res.response = setReduxAccountRecovery(
                        response.data.recovery_email_added,
                        response.data.recovery_email_preview,
                    )
                    break;
                case 400:
                case 401:
                case 403:
                    res.message = response.data.response
                    break;
                default:
                    res.message = "Error: Please refresh the page and try again."
                    break;
            }
        } catch {
            res.message = "Error: Please refresh the page and try again."
        }
        return res;
    }
    return saveRecoveryEmail()
}