import { setReduxLogOutUser } from "../../../redux/utilsRedux/setReduxUserState.js";

/**
 * Function does not make API call, just logs out user from the redux store when the user deletes the account.
 * 
 * This function is in the apiHandler to avoid changes in the redux store from the components.
 * The user could not be logged out from the same function that deletes the user due to component logic.
 * The component that deletes the user will navigate to a deletion page, where the logout takes place.
 * 
 * This function does not return any value.
 * 
 */
export function logOutDeletedUser() {

    // log out front end
    setReduxLogOutUser();
    return

}