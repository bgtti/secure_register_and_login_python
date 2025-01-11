import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { passwordValidationSimplified, sanitizedUserAgent } from "../../../utils/validation.js";

/**
 * Async function that makes api call to save a recovery email address.
 * 
 * @param {object} data 
 * @param {string} data.password # the password provided by user
 * @param {string} [data.userAgent]
 * @returns {Promise<object>} # with boolean "response",  and string "message"
 * 
 * @example
 * //Input example:
 * const data = {
 *     password: "108854cd4b588sszb64010",
 * }
 * 
 * // Response from setRecoveryEmail:
 * fetchRecoveryEmail(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // a successfull response will yield:
 * {
        response: true,
        message: "john@email.com"
    }
 *  // an error response might yield:
    {
        response: false,
        message: "Error: Failed to get recovery email."
    }
 */
export function getRecoveryEmail(data) {
    // checking if data was received correctly
    const password = data.password ? data.password : false;
    const userAgent = data.userAgent ? data.userAgent : "";
    const agent = userAgent !== "" ? sanitizedUserAgent(userAgent) : userAgent;

    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    if (!password) { return Promise.resolve(errorResponse) };

    // double-checking the data
    const passwordIsValid = passwordValidationSimplified(password)

    if (!passwordIsValid.response) { return Promise.resolve(errorResponse) }

    let requestData = {
        "password": password,
        "user_agent": agent,
    }

    // preparing the returned response
    let res = {
        response: false,
        message: ""
    }

    // making the request
    const fetchRecoveryEmail = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.getRecoveryEmail, requestData);

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    res.response = true;
                    res.message = response.data.recovery_email
                    break;
                case 400:
                case 401:
                case 403:
                    res.message = response.data.response
                    break;
                default:
                    res.message = "Error: An error occurred, please try again."
                    break;
            }
        } catch {
            res.message = "Error: Please refresh the page and try again."
        }
        return res;
    }
    return fetchRecoveryEmail()
}