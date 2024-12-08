import { apiCredentials } from "../axios";
import apiEndpoints from "../apiEndpoints.js";
import { nameValidation, emailValidation, passwordValidation } from "../../utils/validation"
import { setReduxLogInUser } from "../../redux/utilsRedux/setReduxUserState.js";

/**
 * Function makes api call to register a user, and if successfull logs the user information in the appropriate redux store. Returns a boolean indicating the response status and a message to be displayed to the user in case of failure.
 * 
 * Requires parameters: a data object with a name, email, and password keys with string values.
 * 
 * Note the function accepts a string for honeypot value. Empty stings will be understood as humans, while non-empty strings will yield an error.
 * 
 * @param {object} data 
 * @param {string} data.name 
 * @param {string} data.email 
 * @param {string} data.password
 * @param {string} data.honeypot
 * @returns {object}
 * 
 * @example
 * //Input example:
 * const data = {
 *     name: "Josy",
 *     email: "josy@example.comm",
 *     password: "3f61108854cd4b58",
 *     honeypot: ""
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
 * // Response from signupUser:
 * signupUser(requestData)
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
        message: "Error: Registration failed."
    }
 */
export function signupUser(data = {}) {
    // checking if data was received correctly
    const name = data.name ? data.name : false;
    const password = data.password ? data.password : false;
    const email = data.email ? data.email : false;
    const honeypot = data.honeypot ? data.honeypot : "";

    const errorResponse = {
        response: false,
        message: "Error: Invalid input."
    };

    if (!data.name || !data.email || !data.password) {
        return errorResponse
    }

    // double-checking the data
    const nameIsValid = nameValidation(name);
    const passwordIsValid = passwordValidation(password);
    const emailIsValid = emailValidation(email);
    const dataIsValid = emailIsValid.response && passwordIsValid.response && nameIsValid.response;

    if (!dataIsValid) {
        return errorResponse
    }

    let requestData = {
        "name": name,
        "email": email,
        "password": password,
        "honeypot": honeypot
    }

    // preparing the returned response
    let res = {
        response: false,
        message: "",
    }

    // making the request
    const signup = async () => {
        try {
            const response = await apiCredentials.post(apiEndpoints.userSignUp, requestData)

            let responseStatus = response.request.status;

            switch (responseStatus) {
                case 200:
                    let userIsLoggedIn = setReduxLogInUser(
                        response.data.user.name,
                        response.data.user.email,
                        response.data.user.access,
                        response.data.user.email_is_verified
                    )
                    res.response = userIsLoggedIn;
                    res.message = userIsLoggedIn ? "" : "Error: Registration failed."
                    break;
                case 400:
                case 401:
                case 409:
                    res.message = "Error: Registration failed."
                    break;
                default:
                    res.message = "Error: Please refresh the page and try again."
                    break;
            }
        }
        catch (error) {
            res.message = "Error: Please refresh the page and try again."
            console.warn(`Api handler signup encountered an error: ${error}`)
        }
        return res;
    }

    return signup();
};