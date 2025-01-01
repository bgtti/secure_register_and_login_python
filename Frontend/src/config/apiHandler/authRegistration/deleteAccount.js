import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { passwordValidation, otpValidation, sanitizedUserAgent } from "../../../utils/validation.js"

/**
 * Function makes api call to delete the user's account.
 * 
 * @param {object} data 
 * @param {string} data.password
 * @param {string} [data.otp]
 * @param {string} [data.userAgent]
 * @returns {Promise<object>} 
 * 
 * @example
 * //Input example:
 * const data = {
 *     name: "Josy",
 *     otp: "12345678",
 *     password: "3f61108854cd4b58",
 *     userAgent: "Mozilla/5.0"
 * }
 * 
 * // Response from deleteOwnAccount:
 * deleteOwnAccount(requestData)
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
        message: "Error: Deletion failed."
    }
 */
export function deleteOwnAccount(data = {}) {

    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    // Check password
    if (!data.password) { return errorResponse }
    const passwordIsValid = passwordValidation(data.password);
    if (!passwordIsValid.response) { return errorResponse }

    // If user agent in data, sanitize it
    const userAgent = data.userAgent ? data.userAgent : "";
    const agent = userAgent !== "" ? sanitizedUserAgent(userAgent) : userAgent;

    //Prepare payload
    let requestData = {
        "password": data.password,
        "user_agent": agent
    }

    //If OTP provided (in case user has MFA it will be required), add to payload
    if (data.otp && data.otp !== "") {
        const otpIsValid = otpValidation(data.otp);
        if (!otpIsValid.response) { return errorResponse }
        requestData.otp = data.otp;
    }

    // preparing the returned response
    let res = {
        response: false,
        message: ""
    }

    // making the request
    const deleteUser = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.acctDeleteOwnAccount, requestData)

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    //User not logged out here: deletion page logs user out
                    res.response = true;
                    break;
                case 400:
                case 401:
                case 409:
                    res.message = "Error: Deletion failed."
                    break;
                default:
                    res.message = "Error: Please refresh the page and try again."
                    break;
            }
        }
        catch (error) {
            res.message = "Error: Please refresh the page and try again."
            // console.warn(`Api handler to delete account encountered an error: ${error}`)
        }
        return res;
    }

    return deleteUser();
};