import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { sanitizedUserAgent, passwordValidation, tokenFormatIsValid } from "../../../utils/validation.js";

/**
 * Asynchronously makes an API call to change a user's password.
 * 
 * - **Success Response**:
 *   - `response: true`
 *   - `message`: An empty string or contains additional instructions (e.g., for MFA).
 * - **Failure Response**:
 *   - `response: false`
 *   - `message`: A string describing the error.
 * 
 * @param {object} data - An object containing the necessary input data.
 * @param {string} data.newPassword - The new password for the user.
 * @param {string} data.pwChangeReason - The reason for the password change. Either "change" or "reset".
 * @param {boolean} data.isFirstFactor - Indicates whether this is a first-factor password change.
 * @param {string} data.honeypot - Bot trap field. Should be an empty string for legitimate users.
 * @param {string} [data.userAgent] - Optional user agent string for logging purposes.
 * @param {string} [data.oldPassword] - The current password, required if `pwChangeReason` is "change".
 * @param {string} [data.otp] - One-time password, optionally required for password change.
 * @param {string} [data.signedToken] - A signed token, required if `pwChangeReason` is "reset".
 * @returns {Promise<object>} - A promise that resolves to an object with the following structure:
 *   - `response`: {boolean} - Indicates whether the password change was successful.
 *   - `status`: {number} - HTTP status code returned by the server.
 *   - `message`: {string} - A message describing the result of the operation.
 * 
 * @example
 * // Input example:
 * const data = {
 *     newPassword: "newSecurePassword123!",
 *     pwChangeReason: "change",
 *     isFirstFactor: true,
 *     honeypot: "",
 *     userAgent: "Mozilla/5.0",
 *     oldPassword: "currentPassword123!",
 * };
 * 
 * changePassword(data)
 *     .then(response => {
 *         console.log(response);
 *     });
 * 
 * // Successful response:
 * {
 *     response: true,
 *     status: 200,
 *     message: ""
 * }
 * 
 * // Error response:
 * {
 *     response: false,
 *     status: 400,
 *     message: "Invalid input or password could not be reset."
 * }
 */
export function changePassword(data) {
    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    console.log(data)

    // checking required data
    const newPassword = data.newPassword ? data.newPassword : false;
    const pwChangeReason = data.pwChangeReason ? data.pwChangeReason : false;
    const isFirstFactor = (typeof data.isFirstFactor === "boolean") ? data.isFirstFactor : false;
    const honeypot = data.honeypot ? data.honeypot : "";

    if (!newPassword || !pwChangeReason) { return Promise.resolve(errorResponse) };
    let pwIsValid = passwordValidation(newPassword)
    if (!pwIsValid.response) { return Promise.resolve(errorResponse) };


    const userAgent = data.userAgent ? data.userAgent : "";
    const agent = userAgent !== "" ? sanitizedUserAgent(userAgent) : userAgent;

    let requestData = {
        "new_password": newPassword,
        "pw_change_reason": pwChangeReason,
        "is_first_factor": isFirstFactor,
        "honeypot": honeypot,
        "user_agent": agent,
    }
    if (data.otp && data.otp !== "") { requestData.otp = data.otp }

    const REASON = ["change", "reset"]
    // if "change", oldPassword is required
    if (pwChangeReason == REASON[0]) {
        if (!data.oldPassword) { return Promise.resolve(errorResponse) };
        let oldPwIsValid = passwordValidation(data.oldPassword);
        if (!oldPwIsValid.response) { return Promise.resolve(errorResponse) };
        requestData.old_password = data.otp
        // if "reset", signed token will be required
    } else if (pwChangeReason == REASON[1]) {
        if (!data.signedToken || !tokenFormatIsValid(data.signedToken)) { return Promise.resolve(errorResponse) };
        requestData.signed_token = data.signedToken;
    } else {
        return Promise.resolve(errorResponse);
    }

    // preparing the returned response
    let res = {
        response: false,
        status: 0,
        message: ""
    }

    // making the request
    const changeRequest = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.changePassword, requestData);

            let responseStatus = response.request.status;

            //message and status being passed directly
            res.status = responseStatus;
            res.message = response.data.response;

            switch (responseStatus) {
                case 200:
                case 202:
                    res.response = true;
                    break;
                default:
                    res.message = "An error occurred and password could not be reset."
                    break;
            }
        } catch {
            res.message = "Error: Please refresh the page and try again."
        }
        return res;
    }
    return changeRequest()
}