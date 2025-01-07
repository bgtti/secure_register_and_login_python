import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { emailValidation, passwordValidation, sanitizedUserAgent } from "../../../utils/validation.js"
import { setReduxUserEmail } from "../../../redux/utilsRedux/setReduxUserState.js";


/**
 * Function makes api call to change a user's email.
 * 
 * @param {object} data - An object containing the necessary input data.
 * @param {string} data.newEmail - The new email.
 * @param {string} data.password - The user's password.
 * @param {string} [data.userAgent] - Optional user agent string for logging purposes.
 * @returns {Promise<object>} - A promise that resolves to an object with the following structure:
 *   - `response`: {boolean} - Indicates whether the email change was successful.
 *   - `status`: {number} - HTTP status code returned by the server.
 *   - `message`: {string} - A message describing the result of the operation.
 * 
 * @example
 * //Input example:
 * const data = {
 *     password: "securePassword123!",
 *     new_email: "josy@example.com",
 *     user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
 * }
 * changeEmail(data)
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
export function changeEmail(data) {
    // Preparing response
    const res = {
        response: false,
        message: "Error: Invalid input.",
        status: 500
    };

    // checking if argument was received correctly
    const newEmail = data.newEmail ? data.newEmail : false;
    const password = data.password ? data.password : false;
    const agent = data.userAgent ? sanitizedUserAgent(data.userAgent) : "";

    if (!newEmail || !password) { return Promise.resolve(res) };

    // double-checking the data
    const emailIsValid = emailValidation(newEmail);
    const pwIsValid = passwordValidation(password);

    if (!emailIsValid.response || !pwIsValid.response) {
        return Promise.resolve(res)
    }

    let requestData = {
        "new_email": newEmail,
        "password": password,
        "user_agent": agent,
    }

    // making the request
    const reqChangeEmail = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.changeEmail, requestData)

            let responseStatus = response.request.status;
            res.status = responseStatus

            switch (responseStatus) {
                case 200:
                    setReduxUserEmail(newEmail)
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
                    res.message = "An error occurred and email change could not be requested."
                    break;
            }
        } catch (error) {
            console.error(`Api handler to change email encountered an error: ${error}`)
            res.message = "Error: Please refresh the page and try again."
        }
        return res;
    }

    return reqChangeEmail();
};
