import { store } from "../store"
import { setPreferences, setResetPreferences } from "../preferences/preferencesSlice";
import { stringToBool } from "../../utils/helpers"

// ABOUT THIS FILE
// use the functions herein to set or modify the user preference state
// these functions should ideally be called from within api handlers: not from the components
// this will make debugging easier by having only one source of truth!

/**
 * Function saves user preferences to the redux user slice if the supplied data is valid.
 * Returns true if the supplied data is valid.
 * Returns false and resets user preferences if the supplied data is invalid.
 * 
 * @param {bool} mfa // whether multi-factor authentication is required
 * @param {bool} mailingList //whether user wants to receive notifications from the app
 * @param {bool} nightMode //whether user wants to see app in night mode
 * @returns {bool}
 */
export function setReduxPreferences(mfa, mailingList, nightMode) {
    // convert to boolean in case vallue arrives as string
    mailingList = stringToBool(mailingList)
    nightMode = stringToBool(nightMode)

    let dataIsValid = (typeof mailingList === "boolean") && (typeof mailingList === "boolean");

    if (dataIsValid) {
        const prefData = {
            mailingList: mailingList,
            nightMode: nightMode,
        };
        store.dispatch(setPreferences(prefData));
        return true;
    } else {
        console.error("Redux encountered an error: user preference data invalid, defaults used.")
        store.dispatch(setResetPreferences());
        return false;
    }
}