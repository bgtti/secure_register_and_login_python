import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { emailValidation, passwordValidationSimplified, sanitizedUserAgent } from "../../../utils/validation.js";
import { setReduxLogInUser } from "../../../redux/utilsRedux/setReduxUserState.js";
import { setReduxPreferences } from "../../../redux/utilsRedux/setReduxPreferenceState.js";

/**
 * Asynchronously makes an API call to request login authorization.
 * Handles multi-factor authentication (MFA) by distinguishing between the first and second factors.
 * 
 * - On success:
 *    - Logs user information into the appropriate Redux store.
 *    - Returns `response: true`, `status: 200` for standard login or `status: 202` if MFA requires a second factor.
 *    - The `message` field will be empty (or contain instructions for MFA).
 * - On failure:
 *   - Returns `response: false` with an appropriate error `status` and a `message` describing the failure.
 * 
 * @param {object} data # object containing the login data
 * @param {string} data.email # the user's email address.
 * @param {string} data.password # the user's password or OTP.
 * @param {string} data.method # auth method, one of: ["password", "otp"]
 * @param {bool} data.isFirstFactor # indicates if this is the first factor in MFA.
 * @param {string} data.honeypot # bot trap field, empty field indicates human behaviour.
 * @param {string} [data.userAgent] # optional user agent string.
 * @returns {Promise<object>} # with boolean "response", int "status", and string "message"
 * 
 * @example
 * //Input example:
 * const data = {
 *     email: "josy@example.com",
 *     password: "108854cd4b588sszb64010",
 *     isFirstFactor: true,
 *     method: "password"
 *     honeypot: "",
 *     userAgent: "Mozilla/5.0"
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
    const userAgent = data.userAgent ? data.userAgent : "";
    const agent = userAgent !== "" ? sanitizedUserAgent(userAgent) : userAgent;

    const errorResponse = {
        response: false,
        status: 400,
        message: "Error: Invalid input."
    };

    if (!email || !password || !method || (typeof data.isFirstFactor !== "boolean")) {
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
        "honeypot": honeypot,
        "is_first_factor": data.isFirstFactor,
        "user_agent": agent,
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
                        response.data.user.email_is_verified,
                        response.data.user.mfa_enabled,
                    )
                    res.response = userIsLoggedIn;
                    res.message = userIsLoggedIn ? "" : "Error: Registration failed."
                    setReduxPreferences(
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