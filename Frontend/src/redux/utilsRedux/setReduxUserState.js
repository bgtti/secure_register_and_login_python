import { store } from "../store"
import { setUser, setUserLogout, setUserName, setUserAcctVerification } from "../user/userSlice";
import { USER_ACCESS_TYPES, ACCT_VERIFICATION_STATUS } from "../../utils/constants"
import { stringToBool } from "../../utils/helpers"

// ABOUT THIS FILE
// use the functions herein to set or modify the user state
// these functions should ideally be called from within api handlers: not from the components
// this will make debugging easier by having only one source of truth!



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
 * @param {string|bool} acctVerified //[true, false, "pending", "true", "false"]
 * @returns {boolean}
 */
export function setReduxLogInUser(name, email, access, acctVerified) {
    let verified;
    if (acctVerified === "pending") { verified = acctVerified }
    else { verified = stringToBool(acctVerified) }//convert to boolean if string

    let dataIsValid = name !== "" && email !== "" && USER_ACCESS_TYPES.includes(access) && ACCT_VERIFICATION_STATUS.includes(verified);

    if (dataIsValid) {
        const userData = {
            name: name,
            loggedIn: true,
            access: access,
            email: email,
            acctVerified: verified,
        };
        store.dispatch(setUser(userData));
        return true;
    } else {
        console.error("Redux encountered an error: user data invalid")
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

/**
 * Function changes user's name in the redux store.
 * 
 * Accepts no parameters and returns a boolean indicating success.
 * 
 * @param {string} name //"John"
 * @returns {boolean}
 */
export function setReduxUserName(name) {
    let dataIsValid = name !== ""
    if (dataIsValid) {
        const userData = {
            name: name,
        };
        store.dispatch(setUserName(userData));
        return true;
    } else {
        console.error("Redux encountered an error: user's name invalid")
        store.dispatch(setUserLogout());
        return false;
    }
}

/**
 * Function changes user's name in the redux store.
 * 
 * Accepts no parameters and returns a boolean indicating success.
 * 
 * @param {string} acctVerified //[true, false, "pending"]
 * @returns {boolean}
 */
export function setReduxUserAcctVerification(acctVerified) {
    let verified;
    if (acctVerified === "pending") { verified = acctVerified }
    else { verified = stringToBool(acctVerified) }//convert to boolean if string
    let dataIsValid = ACCT_VERIFICATION_STATUS.includes(verified);
    if (dataIsValid) {
        const userData = {
            acctVerified: verified,
        };
        store.dispatch(setUserAcctVerification(userData));
        return true;
    } else {
        console.error("Redux encountered an error: user's verification status invalid")
        store.dispatch(setUserLogout());
        return false;
    }
} 