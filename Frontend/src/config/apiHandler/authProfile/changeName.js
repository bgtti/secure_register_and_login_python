import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { nameValidation, sanitizedUserAgent } from "../../../utils/validation.js"
import { setReduxUserName } from "../../../redux/utilsRedux/setReduxUserState.js";


/**
 * Function makes api call to change a user's name, and if successfull logs the updated user information in the appropriate redux store. Returns a boolean indicating the response status and a message to be displayed to the user in case of failure.
 * 
 * @param {string} name // the new desired name
 * @param {string} userAgent // browser being used
 * @returns {object}
 * 
 * @example
 * //Input example:
 * acctNameChange("Josy", navigator.userAgent)
            .then(response => handleResponse(response))
            .catch(error => handleError(error))
            .finally(handleFinally);
 * 
 * // Response from acctNameChange:
 * // a successfull response will yield:
 * { success: true }
 * // an error response might yield:
 * { success: false }
 */
export function acctNameChange(newName, userAgent = "") {
    // checking if argument was received correctly
    const name = newName ? newName : false;
    const agent = userAgent !== "" ? sanitizedUserAgent(userAgent) : userAgent;

    if (!newName) {
        console.error("Error: no input to change.")
        return { success: false }
    }

    // double-checking the input
    const nameIsValid = nameValidation(name);

    if (!nameIsValid.response) {
        console.error("Error: input invalid.")
        return { success: false }
    }

    let requestData = {
        "new_name": name,
        "user_agent": agent
    }

    // making the request
    const changeName = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.acctChangeName, requestData)

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    setReduxUserName(
                        response.data.user.name,
                    )
                    return { success: true }
                case 400:
                case 401:
                case 409:
                default:
                    console.warn("Something went wrong: Please refresh the page and try again.")
                    return { success: false }
            }
        }
        catch (error) {
            console.error(`Api handler to change name encountered an error: ${error}`)
            return { success: false }
        }
    }

    return changeName();
};