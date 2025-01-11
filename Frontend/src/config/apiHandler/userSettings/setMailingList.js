import { apiCredentials } from "../../axios.js";
import { setReduxMailingList } from "../../../redux/utilsRedux/setReduxPreferenceState.js";
import apiEndpoints from "../../apiEndpoints.js";
import { sanitizedUserAgent } from "../../../utils/validation.js";

/**
 * Async function that makes api call to set the user's mailing list preferences.
 * 
 * @param {object} data 
 * @param {bool} data.mailingList # indicates whether user wants to receive news letters (true) or not (false)
 * @param {string} [data.userAgent]
 * @returns {Promise<object>} # with boolean "response",  and string "message"
 * 
 * @example
 * //Input example:
 * const data = {
 *     mailingList: false,
 *     userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
 * }
 * 
 * // Response from disableMfa:
 * setMailingList(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // a successfull response will yield:
 * {
        response: true,
        message: "Mailing list sucessfully set!"
    }
 *  // an error response might yield:
    {
        response: false,
        message: "An error occurred, please try again."
    }
 */
export function setMailingList(data) {
    // checking user agent
    const userAgent = data.userAgent ? data.userAgent : "";
    const agent = userAgent !== "" ? sanitizedUserAgent(userAgent) : userAgent;

    // standard error response
    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    //checking required data
    if (typeof data.mailingList !== "boolean") { return Promise.resolve(errorResponse) };

    let requestData = {
        "mailing_list": data.mailingList,
        "user_agent": agent,
    }

    // preparing the returned response
    let res = {
        response: false,
        message: ""
    }

    // making the request
    const editMailingList = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.setMailingList, requestData);

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    //Logging preferences info in Redux store
                    setReduxMailingList(
                        response.data.in_mailing_list
                    )
                    res.message = "Mailing list sucessfully set!"
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
    return editMailingList();
}