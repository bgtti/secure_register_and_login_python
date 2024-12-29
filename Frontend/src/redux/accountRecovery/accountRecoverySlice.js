import { createSlice } from "@reduxjs/toolkit"

/**
 * Use the functions in utilsRedux to set the user state
 * (do not set userPreferencesSlice directly!)
 */

const initialState = {
    recoveryEmailAdded: false,
    recoveryEmailPreview: "",
    infoUpToDate: false //indicates whether status was updated by api call or initial state is being used
}

export const accountRecoverySlice = createSlice({
    name: "accountRecovery",
    initialState,
    reducers: {
        setRecovery: (state, action) => {
            state.recoveryEmailAdded = action.payload.recoveryEmailAdded;
            state.recoveryEmailPreview = action.payload.recoveryEmailPreview;
            state.infoUpToDate = action.payload.infoUpToDate
        },
        setResetRecovery: (state, action) => {
            state.recoveryEmailAdded = false;
            state.recoveryEmailPreview = "";
            state.infoUpToDate = action.payload.infoUpToDate
        },
    }
});

const accountRecoveryReducer = accountRecoverySlice.reducer;

export const { setRecovery, setResetRecovery } = accountRecoverySlice.actions;
export default accountRecoveryReducer;