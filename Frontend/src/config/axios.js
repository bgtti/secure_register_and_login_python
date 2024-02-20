import axios from "axios";
import { redirect } from "react-router-dom";
import apiEndpoints from "./apiEndPoints";

const urlBase = apiEndpoints.baseURL

// Axios instances:

/**
 * api is an Axios instance with an interceptor that will re-direct all error codes.
 * 
 * Ps: keep this in mind when writing try/catch blocks in api calls, since the page will navigate away when there is an error, and the code inside the catch block might not execute as planned.
 * 
 * ----------------------------------------------------
 * API calls in this application use the Axios library.
 * 
 * Two axios instances were created: this (api), and another one called apiCredentials.
 * The difference between them lies in the error handling from interceptors.
 * api has an interceptor that will redirect all errors to an error page. apiCredentials will send error 400, 401, and 409 back to the function, while redirecting other error types. apiCredentials should be used for SignUp and LogIn forms.
 * @see {@link https://axios-http.com/docs/intro}
 * -----------------------------------------------------
 * @example
 * 
 * Usage:
 * const response = await api.post(apiEndpoints.adminGetUsersTable, dataToPost)
 */
export const api = axios.create({
    baseURL: urlBase,
    timeout: 5000,
    withCredentials: true,
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': urlBase,
    }
});

/**
 * apiCredentials is an Axios instance with an interceptor that will re-direct most (but not all) errors to the error page. Errors 400, 401, and 409 will be sent back to the function.
 * 
 * Ps: keep this in mind when writing try/catch blocks in apiCredentials calls, since the page will navigate away when there is an error (eg 500), and the code inside the catch block might not execute as planned. Responses with error 400, 401, and 409 will be sent back to the function and should be handled inside the try-block (the catch block would only receive other error types).
 * 
 * ----------------------------------------------------
 * API calls in this application use the Axios library.
 * 
 * Two axios instances were created: this (api), and another one called apiCredentials.
 * The difference between them lies in the error handling from interceptors.
 * api has an interceptor that will redirect all errors to an error page. apiCredentials will send error 400, 401, and 409 back to the function, while redirecting other error types. apiCredentials should be used for SignUp and LogIn forms.
 * @see {@link https://axios-http.com/docs/intro}
 * -----------------------------------------------------
 * @example
 * 
 * Usage:
 * const response = await apiCredentials.post(apiEndpoints.logIn, userCredentials)
 */
export const apiCredentials = axios.create({
    baseURL: urlBase,
    timeout: 5000,
    withCredentials: true,
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': urlBase,
    }
}
);