import { store } from "../store"
import { setRecovery, setResetRecovery } from "../accountRecovery/accountRecoverySlice";
import { stringToBool } from "../../utils/helpers"

// ABOUT THIS FILE
// use the functions herein to set or modify the user account recovery state
// these functions should ideally be called from within api handlers: not from the components
// this will make debugging easier by having only one source of truth!

/**
 * Function saves user preferences to the redux user slice if the supplied data is valid.
 * Returns true if the supplied data is valid.
 * Returns false and resets user account recovery status if the supplied data is invalid.
 * 
 * @param {bool} recoveryEmailAdded // whether user has set a recovery email
 * @param {string} recoveryEmailPreview //anonymized version of recovery email or empty string
 * @returns {bool}
 */
export function setReduxAccountRecovery(recoveryEmailAdded, recoveryEmailPreview = "") {
    // convert to boolean in case value arrives as string
    recoveryEmailAdded = stringToBool(recoveryEmailAdded)

    let dataIsValid = (typeof recoveryEmailAdded === "boolean") && (typeof recoveryEmailPreview === "string");

    if (dataIsValid) {
        const prefData = {
            recoveryEmailAdded: recoveryEmailAdded,
            recoveryEmailPreview: recoveryEmailPreview,
            infoUpToDate: true //indicates api call retrieved information
        };
        store.dispatch(setRecovery(prefData));
        return true;
    } else {
        console.error("Redux encountered an error: user account recovery data invalid, defaults used.")
        store.dispatch(setResetRecovery(true));
        return false;
    }
}