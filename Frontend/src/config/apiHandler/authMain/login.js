import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { emailValidation, passwordValidationSimplified } from "../../../utils/validation.js";
import { setReduxLogInUser } from "../../../redux/utilsRedux/setReduxUserState.js";
import { setReduxPreferences } from "../../../redux/utilsRedux/setReduxPreferenceState.js";

/**
 * Async function that makes api call to request log in authorization.
 * If MFA is enabled and this function is called on the first auth method,another auth method will be required.
 * If successfull, logs the user information in the appropriate redux store, response will be "true", status of request will be 200 or 202 (indicating mfa need second auth step), message will be empty, and it returns. 
 * If unsuccessfull, response will be false and a message to be displayed to the user in case of failure.
 * 
 * @param {object} data 
 * @param {string} data.email # email as provided by user
 * @param {string} data.password # the password or the otp provided by user
 * @param {string} data.method # one of: ["password", "otp"]
 * @param {string} data.honeypot # bot trap field, empty field indicates human behaviour
 * @returns {object} # with boolean "response", int "status", and string "message"
 * 
 * @example
 * //Input example:
 * const data = {
 *     email: "josy@example.com",
 *     password: "108854cd4b588sszb64010",
 *     method: "password"
 *     honeypot: ""
 * }
 * 
 * // Response from loginUser:
 * loginUser(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // a successfull response will yield:
 * {
        response: true,
        status: 200,
        message: ""
    }
    // a successfull response will yield:
 * {
        response: true,
        status: 202,
        message: "Please confirm the OTP sent to your email address."
    }
    // an error response might yield:
    {
        response: false,
        status: 400,
        message: "Error: Failed to log in."
    }
 */
export function loginUser(data) {
    // checking if data was received correctly
    const email = data.email ? data.email : false;
    const password = data.password ? data.password : false;
    const method = data.method ? data.method : false;
    const honeypot = data.honeypot ? data.honeypot : "";

    const errorResponse = {
        response: false,
        status: 400,
        message: "Error: Invalid input."
    };

    if (!email || !password || !method) {
        return errorResponse
    };
    // double-checking the data
    const passwordIsValid = passwordValidationSimplified(password);
    const emailIsValid = emailValidation(email);
    const methodIsValid = ["password", "otp"].includes(method);
    const dataIsValid = emailIsValid.response && passwordIsValid.response && methodIsValid;

    if (!dataIsValid) {
        return errorResponse
    }

    let requestData = {
        "email": email,
        "password": password,
        "method": method,
        "honeypot": honeypot
    }

    // preparing the returned response
    let res = {
        response: false,
        status: 400,
        message: ""
    }

    // making the request
    const logInRequest = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.userLogIn, requestData);

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    let userIsLoggedIn = setReduxLogInUser(
                        response.data.user.name,
                        response.data.user.email,
                        response.data.user.access,
                        response.data.user.email_is_verified
                    )
                    res.response = userIsLoggedIn;
                    res.message = userIsLoggedIn ? "" : "Error: Registration failed."
                    setReduxPreferences(
                        response.data.preferences.mfa_enabled,
                        response.data.preferences.in_mailing_list,
                        response.data.preferences.night_mode_enabled
                    )
                    break;
                case 202:
                    res.response = true;
                    res.status = 202;
                    res.message = response.data.message;
                    break;
                case 400:
                case 401:
                case 403:
                    res.message = "Error: Failed to log in."
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
    return logInRequest()
}