import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { emailValidation, passwordValidationSimplified, otpValidation } from "../../../utils/validation.js";

/**
 * Async function that makes api call to save a recovery email address.
 * 
 * @param {object} data 
 * @param {string} data.email # the recovery email as provided by user
 * @param {string} data.password # the password provided by user
 * @param {string} data.otp # the otp provided by user
 * @param {string} data.honeypot # bot trap field, empty field indicates human behaviour
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
        message: ""
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

    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    if (!email || !password || !otp) {
        return errorResponse
    };
    // double-checking the data
    const passwordIsValid = passwordValidationSimplified(password); otpValidation(otp)
    const emailIsValid = emailValidation(email);
    const otpIsValid = otpValidation(otp);
    const dataIsValid = emailIsValid.response && passwordIsValid.response && otpIsValid.response;

    if (!dataIsValid) {
        return errorResponse
    }

    let requestData = {
        "email": email,
        "password": password,
        "otp": otp,
    }

    // preparing the returned response
    let res = {
        response: false,
        message: ""
    }

    // making the request
    const saveRecoveryEmail = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.userLogIn, requestData);

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    res.response = true;
                    break;
                case 400:
                case 401:
                case 403:
                    res.message = "Error: Failed to save recovery email."
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