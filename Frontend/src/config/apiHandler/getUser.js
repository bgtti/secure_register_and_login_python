import { api } from "../axios.js";
import apiEndpoints from "../apiEndpoints.js";
import { setReduxLogInUser } from "../../redux/utilsRedux/setReduxUserState.js";

/**
 * Function makes api call to make sure the user is authorized to access the resource. 
 * It will log the user information to the Redux store if successful.
 * 
 * This function requires no parameters.
 * 
 * Will return an object with a response key whose value is a boolean.
 * 
 * @returns {object}
 * 
 * @example
 * //Original API response:
 * {
 *  "response": "success"
 *  "user": {
 *      "access": "user",
 *      "name": "Josy",
 *      "email": "josy@example.com",
 *   }
 * }
 * 
 * // Response from loginUser:
 * loginUser(requestData)
 *      .then(res => {
 *          console.log (res)
 * })
 * // a successfull response will yield:
 * {
        response: true
    }
    // an error response might yield:
    {
        response: false
    }
 */
export function getUserData() {

    const res = {
        response: false
    };

    // making the request
    const getUser = async () => {
        try {
            const response = await api.get(apiEndpoints.userGetOwnAcctInfo);

            let responseStatus = response.request.status;

            if (responseStatus === 200) {
                //Logging user info in Redux store
                res.response = setReduxLogInUser(
                    response.data.user.name,
                    response.data.user.email,
                    response.data.user.access
                )
            }
            return res;
        } catch {
            console.error("Could not get user.")
            return res;
        }
    }
    return getUser()
}