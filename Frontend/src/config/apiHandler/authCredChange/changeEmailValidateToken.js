import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { sanitizedUserAgent, tokenFormatIsValid } from "../../../utils/validation.js"

/**
 * Function makes api call to validate a token to change a user's email.
 * 
 * 
 * @param {object} data - An object containing the necessary input data.
 * @param {string} data.pathUsed - one of ["confirmEmailChange", "confirmNewEmail"]
 * @param {string} data.tokenUsed - The token provided.
 * @param {string} [data.userAgent] - Optional user agent string for logging purposes.
 * @returns {Promise<object>} - A promise that resolves to an object with the following structure:
 *   - `response`: {boolean} - Indicates whether the email change was successful.
 *   - `status`: {number} - HTTP status code returned by the server.
 *   - `message`: {string} - A message describing the result of the operation.
 * 
 * @example
 * //Input example:
 * const data = {
 *     pathUsed: "confirmEmailChange",
 *     tokenUsed: "Il94YzZPcElIUFdjRi0wZ3MyelU2NW91Unl0b3lJMlN3RWpkTGctblBvT3Mi.Z03aPA.CtQImrnVkLtUH0VpAyRrdzIcuGU",
 *     user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
 * }
 * changeEmailValidateToken(data)
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
 *     status: 500,
 *     message: "Error: Invalid input."
 * }
 */
export function changeEmailValidateToken(data) {
    // Preparing response
    const res = {
        response: false,
        message: "Error: Invalid input.",
        status: 500
    };

    // checking if argument was received correctly
    const validPaths = ["confirmEmailChange", "confirmNewEmail"]
    const urlPath = (data.pathUsed && validPaths.includes(data.pathUsed)) ? data.pathUsed : false;
    const token = (data.tokenUsed && tokenFormatIsValid(data.tokenUsed)) ? data.tokenUsed.trim() : false;
    const agent = data.userAgent ? sanitizedUserAgent(data.userAgent) : "";

    // if (!urlPath || !token) { return Promise.resolve(res) };
    if (!urlPath || !token) {
        if (!token) { res.message = `Invalid token: ${data.tokenUsed}` }
        else { res.message = `Invalid urlPath: ${data.pathUsed}` }
        return Promise.resolve(res)
    };

    //define purpose
    const type = urlPath === "confirmEmailChange" ? "email_change_old_email" : "email_change_new_email"

    let requestData = {
        "purpose": type,
        "signed_token": token,
        "user_agent": agent,
    }

    // making the request
    const reqChangeEmail = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.changeEmailTokenVerification, requestData)

            let responseStatus = response.request.status;
            res.status = responseStatus

            switch (responseStatus) {
                case 200:
                case 202:
                    res.response = true
                    res.message = response.data.response;
                    break;
                case 400:
                case 401:
                case 409:
                    res.message = response.response.data.response;
                    break;
                default:
                    res.message = "An error occurred and token could not be validated."
                    break;
            }
        } catch (error) {
            console.error(`Api handler to validate token for email change encountered an error: ${error}`)
            res.message = "Error: Please refresh the page and try again."
        }
        return res;
    }

    return reqChangeEmail();
};