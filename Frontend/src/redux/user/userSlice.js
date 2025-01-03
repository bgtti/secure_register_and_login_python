import { createSlice } from "@reduxjs/toolkit"

/**
 * Use the functions in utilsRedux to set the user state
 * (do not set userSlice directly!)
 */

const initialState = {
    loggedIn: false,
    access: "",
    email: "",
    name: "",
    acctVerified: false,
}

export const userSlice = createSlice({
    name: "user",
    initialState,
    reducers: {
        setUserName: (state, action) => {
            state.loggedIn = state.loggedIn;
            state.access = state.access;
            state.email = state.email;
            state.name = action.payload;
            state.acctVerified = state.acctVerified;
        },
        setUserAcctVerification: (state, action) => {
            state.loggedIn = state.loggedIn;
            state.access = state.access;
            state.email = state.email;
            state.name = state.name;
            state.acctVerified = action.payload; // should be either: true, false, or "pending"
        },
        setUser: (state, action) => {
            state.loggedIn = action.payload.loggedIn;
            state.access = action.payload.access;
            state.email = action.payload.email;
            state.name = action.payload.name;
            state.acctVerified = action.payload.acctVerified;
        },
        setUserLogout: (state) => {
            state.loggedIn = false;
            state.access = "";
            state.email = "";
            state.name = "";
            state.acctVerified = false;
        },
    }
});

const userReducer = userSlice.reducer;

export const { setUserName, setUserAcctVerification, setUser, setUserLogout } = userSlice.actions;
export default userReducer;

// Example usage:

// const userData = {
//     id: "bb8c21ba800a4115b0532e97249fe8cb",
//     email: "tom@email.com",
//     name: "Tom",
//     acctVerified = false
// }
// dispatch(setUser(userData))

// Setting individual attributes require only the attribute value