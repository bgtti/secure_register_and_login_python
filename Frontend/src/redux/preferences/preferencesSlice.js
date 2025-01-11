import { createSlice } from "@reduxjs/toolkit"

/**
 * Use the functions in utilsRedux to set the user state
 * (do not set userPreferencesSlice directly!)
 */

const initialState = {
    mailingList: false,
    nightMode: true,
}

export const preferencesSlice = createSlice({
    name: "preferences",
    initialState,
    reducers: {
        setPreferences: (state, action) => {
            state.mailingList = action.payload.mailingList;
            state.nightMode = action.payload.nightMode;
        },
        setMailingList: (state, action) => {
            state.mailingList = action.payload;
            state.nightMode = state.nightMode;
        },
        setNightMode: (state, action) => {
            state.mailingList = state.mailingList;
            state.nightMode = action.payload;
        },
        setResetPreferences: (state) => {
            state.mailingList = false;
            state.nightMode = true;
        },
    }
});

const preferencesReducer = preferencesSlice.reducer;

export const { setPreferences, setResetPreferences, setMailingList, setNightMode } = preferencesSlice.actions;
export default preferencesReducer;