import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { useDispatch } from "react-redux";
import { Helmet } from "react-helmet-async";
import { setLoader } from "../../../redux/loader/loaderSlice.js"
import useIsComponentMounted from "../../../hooks/useIsComponentMounted.js"
import { tokenFormatIsValid } from "../../../utils/validation"
import { confirmEmailChange } from "../../../config/apiHandler/authAccount/changeEmail.js"
import ChangeEmailFailed from "./Outcome/ChangeEmailFailed"
import ChangeEmailHalfPath from "./Outcome/ChangeEmailHalfPath"
import ChangeEmailSucceeded from "./Outcome/ChangeEmailSucceeded"
import "./changeEmail.css"


/**
 * Component returns Confirm Email Change Pages
 * 
 * This component will mount if user clicks on an email link to verify a request to change the email associated with the user's account. The request could have been sent to the user's current/old email address or to the user's desired new email address. Both should be verified.
 * 
 * The url path will differ between the link sent to the user's old and new email addresses: and this is used to identify which is the email being verified. A request is then sent to the server to check the token, and the response defines the information shown to the user.
 * 
 * Three different outcomes can be returned in the form of child component: one indicates a failure to verify the token, another indicates that 1 out of 2 tokens was successfully verified, and yet another indicated whether the email credential change was successful or not.
 * 
 * User should come to this page from /confirmEmailChange?token={tokenHere} or /confirmNewEmail?token={tokenHere}"
 * 
 * If you are testing this component, the link should look something like this:
 * http://localhost:5173/confirmEmailChange/token=56324f55
 * http://localhost:5173/confirmNewEmail/token=56324f55
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
function ChangeEmail() {

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();
    const location = useLocation();

    // Extract the url path 
    const currentPath = location.pathname;
    // Determine the route used to get here and inform if something could be wrong
    const isConfirmNewEmail = currentPath.includes('/confirmNewEmail');
    const isConfirmEmailChange = currentPath.includes('/confirmEmailChange');
    if (!isConfirmNewEmail && !isConfirmEmailChange) { console.error("Path error lead to email change component?") }
    // Extract the token from the url
    const tokenInUrl = currentPath.split("token=")[1];
    let token = tokenFormatIsValid(tokenInUrl)

    // Store API response in state
    const [tokenValid, setTokenValid] = useState(false);
    const [emailChangeComplete, setEmailChangeComplete] = useState(false);

    // 3 types of response: token validation failed, token validation succeeded and credentials can be changed, or token validation succeeded but another token still needs validation.
    const handleResponse = (response) => {
        console.log(response)
        if (isComponentMounted()) {
            if (response.success) {
                setTokenValid(true)
                if (response.credChanged) {
                    setEmailChangeComplete(true)
                }
            }
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
    const checkEmailChangeToken = () => {
        if (!token) { return }
        let pathTaken = isConfirmNewEmail ? "confirmNewEmail" : "confirmEmailChange"
        dispatch(setLoader(true));

        try {
            confirmEmailChange(pathTaken, tokenInUrl)
                .then(response => handleResponse(response))
                .catch(error => handleError(error))
                .finally(handleFinally)
        } catch (error) {
            console.log(error)
            dispatch(setLoader(false));
        }
    }

    // Make this request only once
    useEffect(() => {
        checkEmailChangeToken()
    }, []);


    return (
        <div className="ChangeEmail">
            <Helmet>
                <title>Email Change confirmation</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>

            <h2>Email change</h2>
            <br />

            {!tokenValid && <ChangeEmailFailed />}

            {tokenValid && emailChangeComplete && <ChangeEmailSucceeded />}

            {tokenValid && !emailChangeComplete && <ChangeEmailHalfPath
                verifiedNewEmail={isConfirmNewEmail} />}

        </div>
    );
};

export default ChangeEmail;