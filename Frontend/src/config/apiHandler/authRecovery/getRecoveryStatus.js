import { api } from "../../axios.js";
import apiEndpoints from "../../apiEndpoints.js";
import { setReduxAccountRecovery } from "../../../redux/utilsRedux/setAccountRecovery.js";

/**
 * Function makes api call to get information about the account recovery from user. 
 * It will log the user information to the Redux store if successful.
 * 
 * This function requires no parameters.
 * 
 * Will return an object with a response key whose value is a boolean.
 * 
 * @returns {object}
 * 
 * @example
 * // Response from loginUser:
 * getRecoveryEmailStatus()
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
export function getRecoveryStatus() {

    const res = {
        response: false
    };

    // making the request
    const getRecoveryEmailStatus = async () => {
        try {
            const response = await api.get(apiEndpoints.getRecoveryEmailStatus);

            let responseStatus = response.request.status;

            if (responseStatus === 200) {
                //Logging info in Redux store
                res.response = setReduxAccountRecovery(
                    response.data.recovery_email_added,
                    response.data.recovery_email_preview,
                )
            }
            res.response = true
            return res;
        } catch {
            console.error("Could not get user.")
            return res;
        }
    }
    return getRecoveryEmailStatus()
}