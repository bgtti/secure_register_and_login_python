import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { Helmet } from "react-helmet-async";
import { setLoader } from "../../../redux/loader/loaderSlice.js"
import useIsComponentMounted from "../../../hooks/useIsComponentMounted.js";
import { getTokenPasswordReset } from "../../../config/apiHandler/authCredChange/getTokenPasswordReset.js"
import ErrorMessage from "../../../components/ErrorMessage/ErrorMessage.jsx";
import Honeypot from "../../../components/Honeypot/Honeypot.jsx";
import InputEmail from "../../../components/Auth/InputEmail.jsx";

/**
 * Component returns Reset Password page
 * 
 * When a password reset is requested, user should get an email with a link leading to a new password input page
 * 
 * @visibleName LogIn
 * @returns {React.ReactElement}
 * 
 * @todo api request
 */
function ForgotPassword() {
    const dispatch = useDispatch();
    const isComponentMounted = useIsComponentMounted();

    const userAgent = navigator.userAgent; //info to be passed on to BE

    // Used for honeypot
    const [honeypotValue, setHoneypotValue] = useState("");

    // Used for actual fields
    const [email, setEmail] = useState("");
    const [emailIsValid, setEmailIsValid] = useState(false);

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");
    const [apiSuccess, setApiSuccess] = useState(false);

    //if a form error was shown, hide it when the user starts to correct the input
    useEffect(() => {
        if (infoMessage !== "") {
            setInfoMessage("")
        }
    }, [email]);


    const handleSubmit = (e) => {
        e.preventDefault();
        if (!emailIsValid) { setInfoMessage("Email is not valid."); }
        let requestData = {
            "honeypot": honeypotValue,
            "email": email,
            "userAgent": userAgent
        }
        dispatch(setLoader(true))
        getTokenPasswordReset(requestData)
            .then(res => {
                if (isComponentMounted()) {
                    if (res.response) { setApiSuccess(true); }
                    else { setInfoMessage(res.message); }
                }
            })
            .catch(error => {
                console.error("Error in forgot password function.", error);
            })
            .finally(() => {
                dispatch(setLoader(false));
            })
    };

    return (
        <div>

            <Helmet>
                <title>Request a Password Reset</title>
                <meta name="description" content="Reset Password" />
            </Helmet>

            <h2>Request a Password Reset</h2>


            <p className="MAIN-info-paragraph">
                Provide the email address that you used to sign up for your account.
            </p>

            <p className="MAIN-info-paragraph">
                If the email addressyou provide is registered with us, you shall receive an email with instructions on how to reset your password.
            </p>

            <br />

            <form onSubmit={handleSubmit} className='MAIN-form'>
                <InputEmail
                    autocomplete="username"
                    disabled={apiSuccess}
                    email={email}
                    setEmail={setEmail}
                    setEmailIsValid={setEmailIsValid}
                    cssClass={"MAIN-form-display-table"}
                />

                <Honeypot setHoneypotValue={setHoneypotValue} />

                <button
                    disabled={!emailIsValid || apiSuccess}
                    type="submit">
                    Reset password
                </button>

                {
                    infoMessage !== "" && (
                        < ErrorMessage message={infoMessage} ariaDescribedby="api-response-error" />
                    )
                }
            </form>

            {apiSuccess && (
                <div>
                    <p className="MAIN-info-paragraph"><b>Request to reset password submitted!</b></p>
                    <p className="MAIN-info-paragraph">Check your email account to proceed.</p>
                </div>
            )}



        </div>
    );
};

export default ForgotPassword;