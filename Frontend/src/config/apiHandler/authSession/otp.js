import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { emailValidation } from "../../../utils/validation.js";

/**
 * Function makes api call to request otp to be sent by email.
 * 
 * Requires parameters: an object with the keys as the user's email and honeypot value.
 * 
 * Returns an object with a key named response that indicates if the response was an error (=false) or successfull (=true). 
 * 
 * Note the function accepts a string for honeypot value. Empty stings will be understood as humans, while non-empty strings will yield an error.
 * 
 * 
 * @param {string} data.email
 * @param {string} data.honeypot
 * @returns {Promise<object>}
 * 
 * @example
 * //Input example:
 * const data = {
 *     email: "josy@example.com",
 *     honeypot: ""
 * }
 * 
 * // Response from getOTP:
 * getOTP(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // a successfull response will yield:
 * {
        response: true,
        message: "OTP was sent to the given email address."
    }
    // an error response might yield:
    {
        response: false,
        message: "Error: Failed to get OTP."
    }
 */
export function getOTP(data) {
    // checking if data was received correctly
    const email = data.email ? data.email : false;
    const honeypot = data.honeypot ? data.honeypot : "";

    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    if (!email) {
        return Promise.resolve(errorResponse)
    };
    // double-checking the data
    const emailIsValid = emailValidation(email);

    if (!emailIsValid) {
        return Promise.resolve(errorResponse)
    }

    let requestData = {
        "email": email,
        "honeypot": honeypot
    }

    // preparing the returned response
    let res = {
        response: false,
        message: ""
    }

    // making the request
    const requestOTP = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.getOTP, requestData);

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    res.response = true;
                    res.message = "OTP was sent to the given email address."
                    break;
                default:
                    res.message = "Error: Failed to get OTP."
                    break;
            }
        } catch {
            res.message = "Error: Please refresh the page and try again."
        }
        return res;
    }
    return requestOTP()
}