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
    mfa: false
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
            state.mfa = state.mfa;
        },
        setUserAcctVerification: (state, action) => {
            state.loggedIn = state.loggedIn;
            state.access = state.access;
            state.email = state.email;
            state.name = state.name;
            state.acctVerified = action.payload; // should be either: true, or false
            state.mfa = state.mfa;
        },
        setUserMfa: (state, action) => {
            state.loggedIn = state.loggedIn;
            state.access = state.access;
            state.email = state.email;
            state.name = state.name;
            state.acctVerified = state.acctVerified;
            state.mfa = action.payload; // should be either: true, or false
        },
        setUser: (state, action) => {
            state.loggedIn = action.payload.loggedIn;
            state.access = action.payload.access;
            state.email = action.payload.email;
            state.name = action.payload.name;
            state.acctVerified = action.payload.acctVerified;
            state.mfa = action.payload.mfa;
        },
        setUserLogout: (state) => {
            state.loggedIn = false;
            state.access = "";
            state.email = "";
            state.name = "";
            state.acctVerified = false;
            state.mfa = false;
        },
    }
});

const userReducer = userSlice.reducer;

export const { setUserName, setUserAcctVerification, setUserMfa, setUser, setUserLogout } = userSlice.actions;
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