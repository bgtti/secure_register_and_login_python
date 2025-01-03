import { createSlice } from "@reduxjs/toolkit"

/**
 * Use the functions in utilsRedux to set the user state
 * (do not set userPreferencesSlice directly!)
 */

const initialState = {
    mfa: false,
    mailingList: false,
    nightMode: true,
}

export const preferencesSlice = createSlice({
    name: "preferences",
    initialState,
    reducers: {
        setPreferences: (state, action) => {
            state.mfa = action.payload.mfa;
            state.mailingList = action.payload.mailingList;
            state.nightMode = action.payload.nightMode;
        },
        setResetPreferences: (state) => {
            state.mfa = false;
            state.mailingList = false;
            state.nightMode = true;
        },
    }
});

const preferencesReducer = preferencesSlice.reducer;

export const { setPreferences, setResetPreferences } = preferencesSlice.actions;
export default preferencesReducer;