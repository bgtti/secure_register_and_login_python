import { apiCredentials } from "../axios";
import apiEndpoints from "../apiEndPoints";
import { setReduxLogOutUser } from "../../redux/utilsRedux/setReduxUserState.js";

/**
 * Function makes api call to logout the user, and also logs out user from the redux store.
 * 
 * Takes no parameters and returns an object with a response key and boolean value.
 * 
 * @returns {object}
 * 
 * @example
 * // Response from logoutUser:
 * {
        response: true,
    }
    // an error response might yield:
    {
        response: false
    }
 */
export function logoutUser() {
    // preparing the returned response
    let res = {
        response: false,
    }

    // making the request
    const logout = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.userLogOut)

            let responseStatus = response.request.status;

            if (responseStatus === 200) {
                res.response = true;
            }

            setReduxLogOutUser();

        }
        catch (error) {
            console.warn(`Api handler logout encountered an error: ${error}`)
        }
        return res;
    }

    return logout();

}