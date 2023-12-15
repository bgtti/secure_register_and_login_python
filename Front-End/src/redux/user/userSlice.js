import { createSlice } from "@reduxjs/toolkit"

const initialState = {
    id: "",
    email: "",
    name: ""
}

export const userSlice = createSlice({
    name: "user",
    initialState,
    reducers: {
        setUserId: (state, action) => {
            state.id = action.payload;
            state.email = state.email;
            state.name = state.name;
        },
        setUserEmail: (state, action) => {
            state.id = state.id;
            state.email = action.payload;
            state.name = state.name;
        },
        setUserName: (state, action) => {
            state.id = state.id;
            state.email = state.email;
            state.name = action.payload;
        },
        setUser: (state, action) => {
            state.id = action.payload.id;
            state.email = action.payload.email;
            state.name = action.payload.name;
        },
        setUserLogout: (state) => {
            state.id = "";
            state.email = "";
            state.name = "";
        },
    }
});

const userReducer = userSlice.reducer;

export const { setUserId, setUserEmail, setUserName, setUser, setUserLogout } = userSlice.actions;
export default userReducer;

// Example usage:

// const userData = {
//     id: "bb8c21ba800a4115b0532e97249fe8cb",
//     email: "tom@email.com",
//     name: "Tom"
// }
// dispatch(setUser(userData))

// Setting individual attributes require only the attribute value