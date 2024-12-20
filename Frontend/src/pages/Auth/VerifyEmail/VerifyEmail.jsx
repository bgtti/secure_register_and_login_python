import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { useDispatch } from "react-redux";
import { Helmet } from "react-helmet-async";
import { setLoader } from "../../../redux/loader/loaderSlice.js"
import useIsComponentMounted from "../../../hooks/useIsComponentMounted.js"
import { tokenFormatIsValid } from "../../../utils/validation"
import { confirmEmailVerification } from "../../../config/apiHandler/authRegistration/verifyEmail.js"
import VerifyEmailFailed from "./SubComponents/VerifyEmailFailed.jsx"
import VerifyEmailSucceeded from "./SubComponents/VerifyEmailSucceeded.jsx"


/**
 * Component returns Verify Email Change Page
 * 
 * This component will mount if user clicks on an email link to verify their ownership of the email address.
 * 
 * Example of token that may be received: 
 * Il94YzZPcElIUFdjRi0wZ3MyelU2NW91Unl0b3lJMlN3RWpkTGctblBvT3Mi.Z03aPA.CtQImrnVkLtUH0VpAyRrdzIcuGU
 * 
 * @requires parameter in the url named "token"
 * 
 * @visibleName Token verification for email change
 * @returns {React.ReactElement}
 * 
 */
function VerifyEmail() {

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();
    const location = useLocation();

    // Extract the url path 
    const currentPath = location.pathname;
    // Extract the token from the url
    const tokenInUrl = currentPath.split("token=")[1];
    let token = tokenFormatIsValid(tokenInUrl)

    // Store API response in state
    const [tokenValid, setTokenValid] = useState(null);

    // 2 types of response: token validation failed or token validation succeeded.
    const handleResponse = (response) => {
        console.log(response)
        if (isComponentMounted()) {
            setTokenValid(response.success)
        }
    }

    // Handle caught errors from request
    const handleError = (error) => {
        console.warn("An error occurred. ", error);
    };

    // Whether there was an error or not, execute after api request
    const handleFinally = () => {
        dispatch(setLoader(false));
    };

    // API request: check token and email credential change status
    const checkEmailVerificationToken = () => {
        if (!token) { setTokenValid(false); return }

        dispatch(setLoader(true));

        confirmEmailVerification(tokenInUrl)
            .then(response => handleResponse(response))
            .catch(error => handleError(error))
            .finally(handleFinally)
    }

    //Make this request only once
    useEffect(() => {
        checkEmailVerificationToken()
    }, []);


    return (
        <div className="VerifyEmail">
            <Helmet>
                <title>Email Verification</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>

            <h2>Email Verification</h2>
            <br />
            {tokenValid === null ? (
                <>
                    <p>Validating token...</p>
                </>
            ) : tokenValid ? (
                <VerifyEmailSucceeded />
            ) : (
                <VerifyEmailFailed />
            )}

        </div>
    );
};

export default VerifyEmail;