import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { useDispatch } from "react-redux";
import { Helmet } from "react-helmet-async";
import { setLoader } from "../../../redux/loader/loaderSlice.js"
import useIsComponentMounted from "../../../hooks/useIsComponentMounted.js"
import { tokenFormatIsValid } from "../../../utils/validation"
import { confirmEmailChange } from "../../../config/apiHandler/authAccount/changeEmail.js"
import "./changeEmail.css"


/**
 * Component returns Change Password page
 * 
 * This component will as the user for a new password, ask the user to repeat that password, and send the request to change password along with the token contained in the path.
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
function ChangePassword() {

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();
    const location = useLocation();

    // Extract the url path 
    const currentPath = location.pathname;
    // Extract the token from the url
    const tokenInUrl = currentPath.split("token=")[1];
    let token = tokenFormatIsValid(tokenInUrl)

    // Store API response in state
    const [tokenValid, setTokenValid] = useState(false);
    const [passwordChangeComplete, setPasswordChangeComplete] = useState(false);

    // 3 types of response: token validation failed, token validation succeeded and credentials were changed, or token validation succeeded but password could not be change (for some other reason).
    const handleResponse = (response) => {
        console.log(response)
        if (isComponentMounted()) {
            if (response.success) {
                setTokenValid(true)
                if (response.credChanged) {
                    setPasswordChangeComplete(true)
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
    const checkPasswordChange = () => {
        if (!token) { return }
        // dispatch(setLoader(true));
        // try {
        //     confirmEmailChange(pathTaken, tokenInUrl)
        //         .then(response => handleResponse(response))
        //         .catch(error => handleError(error))
        //         .finally(handleFinally)
        // } catch (error) {
        //     console.log(error)
        //     dispatch(setLoader(false));
        // }
    }


    return (
        <div className="ChangePassword">
            <Helmet>
                <title>Change Password</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>

            <h2>Change Password</h2>
            <br />

            {/* {!tokenValid && <ChangeEmailFailed />}

            {tokenValid && emailChangeComplete && <ChangeEmailSucceeded />}

            {tokenValid && !emailChangeComplete && <ChangeEmailHalfPath
                verifiedNewEmail={isConfirmNewEmail} />} */}

        </div>
    );
};

export default ChangePassword;