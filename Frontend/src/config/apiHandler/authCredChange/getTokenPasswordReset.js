import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { emailValidation, sanitizedUserAgent } from "../../../utils/validation.js";

/**
 * Asynchronously makes an API call to request a token for password reset.
 * 
 * - On success:
 *    - Returns `response: true`.
 *    - The `message` field will be empty (or contain instructions for MFA).
 * - On failure:
 *   - Returns `response: false` and a `message` describing the failure.
 * 
 * @param {object} data # object containing the login data
 * @param {string} data.email # the user's email address.
 * @param {string} data.honeypot # bot trap field, empty field indicates human behaviour.
 * @param {string} [data.userAgent] # optional user agent string.
 * @returns {Promise<object>} # with boolean "response", int "status", and string "message"
 * 
 * @example
 * //Input example:
 * const data = {
 *     email: "josy@example.com",
 *     honeypot: "",
 *     userAgent: "Mozilla/5.0"
 * }
 * 
 * // Response from getTokenPasswordReset:
 * getTokenPasswordReset(requestData)
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
        message: "An error occurred and password could not be reset."
    }
 */
export function getTokenPasswordReset(data) {
    // checking if data was received correctly
    const email = data.email ? data.email : false;
    const honeypot = data.honeypot ? data.honeypot : "";
    const userAgent = data.userAgent ? data.userAgent : "";
    const agent = userAgent !== "" ? sanitizedUserAgent(userAgent) : userAgent;

    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    if (!email) { return Promise.resolve(errorResponse) };
    // double-checking the data
    const emailIsValid = emailValidation(email);

    if (!emailIsValid) { return Promise.resolve(errorResponse) }

    let requestData = {
        "email": email,
        "honeypot": honeypot,
        "user_agent": agent,
    }

    // preparing the returned response
    let res = {
        response: false,
        message: ""
    }

    // making the request
    const tokenRequest = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.resetPasswordToken, requestData);

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
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
    return tokenRequest()
}