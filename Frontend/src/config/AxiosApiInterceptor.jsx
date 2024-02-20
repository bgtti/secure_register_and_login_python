import { useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { api, apiCredentials } from './axios';

/**
 * Component used to add axios request interceptors to catch and handle error responses.
 * The interceptors were added to a React component (this) in order to use React Router's useNavigate hook. This component was then placed in Router.jsx.
 * 
 * Two interceptors are used: in api and apiCredentials. The interceptor in api will redirect all errors to the error page. The interceptor in apiCredentials will return the response to the function making the request in case of error 400, 401, and 409 and only redirect to the error page in case of other errors. 
 * 
 * The reason for apiCredentials not redirecting all error is so that certain errors can be handled locally by components such as SignUp and LogIn to give better feedback. Example: a password validation failure, or attempting to create an account that already exists.
 * 
 * @visibleName Axios interceptors
 * @returns {React.ReactElement}
 */
function AxiosApiInterceptor() {

    const navigate = useNavigate();

    useEffect(() => {
        const navigateToError = api.interceptors.response.use(
            (response) => response,
            (error) => {
                let errorCode = error.response.request.status.toString()
                if (errorCode === "401") {
                    navigate("/login");
                } else if (errorCode === "418") {
                    navigate("/botError");
                } else {
                    navigate("/errorPage", { state: errorCode });
                }
                return Promise.reject(error);
            }
        );
        const navigateCredentialsError = apiCredentials.interceptors.response.use(
            (response) => response,
            (error) => {

                let errorCode = error.response.request.status.toString()

                if (errorCode === "400" || errorCode === "401" || errorCode === "403" || errorCode === "409") {
                    return error;
                } else if (errorCode === "418") {
                    navigate("/botError");
                } else {
                    navigate("/errorPage", { state: errorCode });
                }
                return Promise.reject(error);
            }
        );
    }, []);

    return <></>;
}

export default AxiosApiInterceptor;

// Combining useNavigate with axios interceptor required a bit of research. Navigating to the error page requires sending the state to the component (or props). These are the sources I used to base the current solution:
//source 1: https://stackoverflow.com/questions/71548673/react-router-v6-how-to-use-navigate-axios-interceptors
//source 2: https://stackoverflow.com/questions/74085802/what-is-the-correct-way-to-use-usenavigate-inside-axios-interceptor
