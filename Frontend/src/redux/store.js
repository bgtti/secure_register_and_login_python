import accountRecoveryReducer from "./accountRecovery/accountRecoverySlice";
import loaderReducer from "./loader/loaderSlice";
import preferencesReducer from "./preferences/preferencesSlice";
import userReducer from "./user/userSlice";
import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
    reducer: {
        loader: loaderReducer,
        user: userReducer,
        preferences: preferencesReducer,
        accountRecovery: accountRecoveryReducer,
    }
})