import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { emailValidation, passwordValidationForLogin } from "../../../utils/validation.js";
import { setReduxLogInUser } from "../../../redux/utilsRedux/setReduxUserState.js";
import { setReduxPreferences } from "../../../redux/utilsRedux/setReduxPreferenceState.js";

/**
 * Function makes api call to request log in authorization, and if successfull logs the user information in the appropriate redux store. Returns a boolean indicating the response status and a message to be displayed to the user in case of failure.
 * 
 * Requires parameters: a data object with an email and password keys with string values.
 * 
 * Returns an object with a key named response that indicates if the response was an error (=false) or successfull (=true). If response is successfull, the user's information will be sent. In the case of failure, an error message will be sent that can be used to inform the user what happened, which should be displayed on the page.
 * 
 * Note the function accepts a string for honeypot value. Empty stings will be understood as humans, while non-empty strings will yield an error.
 * 
 * 
 * @param {object} data 
 * @param {string} data.email
 * @param {string} data.password
 * @param {string} data.honeypot
 * @returns {object}
 * 
 * @example
 * //Input example:
 * const data = {
 *     email: "josy@example.com",
 *     password: "108854cd4b588sszb64010",
 *     honeypot: ""
 * }
 * 
 * //Original API response:
 * {
 *  "response": "success"
 *  "user": {
 *      "access": "user",
 *      "name": "Josy",
 *      "email": "josy@example.com",
 *   }
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
        message: ""
    }
    // an error response might yield:
    {
        response: false,
        message: "Error: Failed to log in."
    }
 */
export function loginUser(data) {
    // checking if data was received correctly
    const password = data.password ? data.password : false;
    const email = data.email ? data.email : false;
    const honeypot = data.honeypot ? data.honeypot : "";

    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    if (!password || !email) {
        return errorResponse
    };
    // double-checking the data
    const passwordIsValid = passwordValidationForLogin(password);
    const emailIsValid = emailValidation(email);
    const dataIsValid = emailIsValid.response && passwordIsValid.response;

    if (!dataIsValid) {
        return errorResponse
    }

    let requestData = {
        "email": email,
        "password": password,
        "honeypot": honeypot
    }

    // preparing the returned response
    let res = {
        response: false,
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