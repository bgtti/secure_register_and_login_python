import { store } from "../store"
import { setPreferences, setResetPreferences, setMailingList, setNightMode } from "../preferences/preferencesSlice";
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
 * @param {bool} mailingList //whether user wants to receive notifications from the app
 * @param {bool} nightMode //whether user wants to see app in night mode
 * @returns {bool}
 */
export function setReduxPreferences(mailingList, nightMode) {
    // convert to boolean in case vallue arrives as string
    mailingList = stringToBool(mailingList)
    nightMode = stringToBool(nightMode)

    let dataIsValid = (typeof mailingList === "boolean") && (typeof nightMode === "boolean");

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

/**
 * Function saves user's mailing list preferences to the redux user slice if the supplied data is valid.
 * Returns true if the supplied data is valid.
 * Returns false and resets user preferences if the supplied data is invalid.
 * 
 * @param {bool} mailingList //whether user wants to receive notifications from the app
 * @returns {bool}
 */
export function setReduxMailingList(mailingList) {
    // convert to boolean in case vallue arrives as string
    mailingList = stringToBool(mailingList)

    let dataIsValid = (typeof mailingList === "boolean");

    if (dataIsValid) {
        store.dispatch(setMailingList(mailingList));
        return true;
    } else {
        console.error("Redux encountered an error: user mailing list preference data invalid, changes not saved.")
        return false;
    }
}

/**
 * Function saves user's night mode preferences to the redux user slice if the supplied data is valid.
 * Returns true if the supplied data is valid.
 * Returns false and resets user preferences if the supplied data is invalid.
 * 
 * @param {bool} nightMode //whether user wants to receive notifications from the app
 * @returns {bool}
 */
export function setReduxNightMode(nightMode) {
    // convert to boolean in case vallue arrives as string
    nightMode = stringToBool(nightMode)

    let dataIsValid = (typeof nightMode === "boolean");

    if (dataIsValid) {
        store.dispatch(setNightMode(nightMode));
        return true;
    } else {
        console.error("Redux encountered an error: user night mode preference data invalid, changes not saved.")
        return false;
    }
}