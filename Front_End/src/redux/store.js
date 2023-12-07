import loaderReducer from './loader/loaderSlice';
import userReducer from './user/userSlice';
import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
    reducer: {
        loader: loaderReducer,
        user: userReducer
    }
})