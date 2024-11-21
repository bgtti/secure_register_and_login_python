import { apiCredentials } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { nameValidation, emailValidation, passwordValidation } from "../../../utils/validation.js"
import { setReduxLogInUser } from "../../../redux/utilsRedux/setReduxUserState.js";


/**
 * Function makes api call to change a user's name, and if successfull logs the updated user information in the appropriate redux store. Returns a boolean indicating the response status and a message to be displayed to the user in case of failure.
 * 
 * Requires argument: a data object with the new name as string value.
 * 
 * 
 * @param {object} data 
 * @param {string} data.name 
 * @returns {object}
 * 
 * @example
 * //Input example:
 * const data = {
 *     name: "Josy",
 * }
 * 
 * //Original API response:
 * {
 *  "response": "success"
 *  "user": {
 *        access: "user",
 *        name: "Josy",
 *        email: "josy@example.com",
 *  }
 * }
 * 
 * // Response from acctNameChange:
 * acctNameChange(requestData)
 *      .then(response => {
 *          console.log (response)
 * })
 * // a successfull response will yield:
 * { success: true }
 * // an error response might yield:
 * { success: false }
 */
export function acctNameChange(newName) {
    // checking if argument was received correctly
    const name = newName ? newName : false;

    if (!newName) {
        console.error("Error: no input to change.")
        return { success: false }
    }

    // double-checking the data
    const nameIsValid = nameValidation(name);

    if (!nameIsValid.response) {
        console.error("Error: input invalid.")
        return { success: false }
    }

    let requestData = {
        "new_name": name,
    }

    // making the request
    const changeName = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.acctChangeName, requestData)

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    setReduxLogInUser(
                        response.data.user.name,
                        response.data.user.email,
                        response.data.user.access
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