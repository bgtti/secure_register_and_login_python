import { store } from "../store"
import { setUser, setUserLogout } from "../user/userSlice";
import { USER_ACCESS_TYPES } from "../../utils/constants"

/**
 * Function saves user information to the redux user slice if the supplied data is valid.
 * Returns true and changes user.loggedIn status to true if the supplied data is valid.
 * Returns false and changes user.loggedIn status to false if the supplied data is invalid.
 * 
 * This effectively logs the user in or out of protected routes.
 * 
 * The function should be used to wrap around protected route elements in Router.jsx
 * 
 * @param {string} name //"John"
 * @param {string} email //"john@fakemail.com"
 * @param {string} access //"user"
 * @returns {boolean}
 */
export function setReduxLogInUser(name, email, access) {
    let dataIsValid = name !== "" && email !== "" && USER_ACCESS_TYPES.includes(access);

    if (dataIsValid) {
        const userData = {
            loggedIn: true,
            access: access,
            email: email,
            name: name
        };
        store.dispatch(setUser(userData));
        return true;
    } else {
        store.dispatch(setUserLogout());
        return false;
    }
}

/**
 * Function logs out user from redux store.
 * 
 * Accepts no parameters and returns a boolean indicating success.
 * 
 * @returns {boolean}
 */
export function setReduxLogOutUser() {
    store.dispatch(setUserLogout());
    return false;
}