import { apiCredentials } from "../../axios.js";
import { setReduxAccountRecovery } from "../../../redux/utilsRedux/setAccountRecovery.js";
import apiEndpoints from "../../apiEndpoints.js";
import { passwordValidationSimplified, sanitizedUserAgent } from "../../../utils/validation.js";

/**
 * Async function that makes api call to delete a recovery email address, the result will update the Redux store accordingly.
 * 
 * @param {object} data 
 * @param {string} data.password # the password provided by user
 * @param {string} [data.userAgent]
 * @returns {object} # with boolean "response",  and string "message"
 * 
 * @example
 * //Input example:
 * const data = {
 *     password: "108854cd4b588sszb64010",
 * }
 * 
 * // Response from setRecoveryEmail:
 * deleteRecoveryEmail(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // a successfull response will yield:
 * {
        response: true,
        message: "Recovery email deleted sucessfully!"
    }
 *  // an error response might yield:
    {
        response: false,
        message: "Error: Failed to delete recovery email."
    }
 */
export function deleteRecoveryEmail(data) {
    // checking if data was received correctly
    const password = data.password ? data.password : false;
    const userAgent = data.userAgent ? data.userAgent : "";
    const agent = userAgent !== "" ? sanitizedUserAgent(userAgent) : userAgent;

    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    if (!password) { return errorResponse };

    // double-checking the data
    const passwordIsValid = passwordValidationSimplified(password)

    if (!passwordIsValid.response) { return errorResponse }

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
    const excludeRecoveryEmail = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.deleteRecoveryEmail, requestData);

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
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
                    res.message = "Error: An error occurred, please try again."
                    break;
            }
        } catch {
            res.message = "Error: Please refresh the page and try again."
        }
        return res;
    }
    return excludeRecoveryEmail()
}