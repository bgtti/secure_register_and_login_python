import { createSlice } from "@reduxjs/toolkit"

const initialState = {
    display: false
}

export const loaderSlice = createSlice({
    name: "loader",
    initialState,
    reducers: {
        setLoader: (state, action) => {
            state.display = action.payload;
        },
    }
});

const loaderReducer = loaderSlice.reducer;

export const { setLoader } = loaderSlice.actions;
export default loaderReducer;
