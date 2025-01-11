import { apiCredentials } from "../../axios.js";
import { setReduxNightMode } from "../../../redux/utilsRedux/setReduxPreferenceState.js";
import apiEndpoints from "../../apiEndpoints.js";
import { sanitizedUserAgent } from "../../../utils/validation.js";

/**
 * Async function that makes api call to set the user's night mode preferences.
 * 
 * @param {object} data 
 * @param {bool} data.nightMode # indicates whether user wants the night mode styles (true) or not (false)
 * @param {string} [data.userAgent]
 * @returns {Promise<object>} # with boolean "response",  and string "message"
 * 
 * @example
 * //Input example:
 * const data = {
 *     nightMode: false,
 *     userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
 * }
 * 
 * // Response from disableMfa:
 * setNightMode(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // a successfull response will yield:
 * {
        response: true,
        message: "Night mode sucessfully set!"
    }
 *  // an error response might yield:
    {
        response: false,
        message: "An error occurred, please try again."
    }
 */
export function setNightMode(data) {
    // checking user agent
    const userAgent = data.userAgent ? data.userAgent : "";
    const agent = userAgent !== "" ? sanitizedUserAgent(userAgent) : userAgent;

    // standard error response
    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    //checking required data
    if (typeof data.nightMode !== "boolean") { return Promise.resolve(errorResponse) };

    let requestData = {
        "night_mode": data.nightMode,
        "user_agent": agent,
    }

    // preparing the returned response
    let res = {
        response: false,
        message: ""
    }

    // making the request
    const editNightMode = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.setNightMode, requestData);

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    //Logging preferences info in Redux store
                    setReduxNightMode(
                        response.data.night_mode_enabled
                    )
                    res.message = "Night mode sucessfully set!"
                    break;
                default:
                    res.message = "An error occurred, please try again."
                    break;
            }
        } catch {
            res.message = "Error: Please refresh the page and try again."
            // console.error("Error:", error); // Logs the error
        }
        return Promise.resolve(res);
    }
    return editNightMode();
}