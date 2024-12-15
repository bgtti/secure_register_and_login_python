import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { setLoader } from "../../../redux/loader/loaderSlice"
import { loginUser } from "../../../config/apiHandler/authMain/login"
import { getOTP } from "../../../config/apiHandler/authSession/otp.js";
import useIsComponentMounted from "../../../hooks/useIsComponentMounted.js";
import Honeypot from "../../../components/Honeypot/Honeypot";
import ErrorMessage from "../../../components/ErrorMessage/ErrorMessage";
import AuthErrorHint from "../../../components/Auth/AuthErrorHint.jsx";
import InputEmail from "../../../components/Auth/InputEmail.jsx";
import InputPassword from "../../../components/Auth/InputPassword";
import InputOtp from "../../../components/Auth/InputOtp.jsx";
import "./login.css"

/**
 * Component returns Log-in form
 * 
 * The form calls the apiHandler in login.js for authentication.
 * Successfull user authentication will re-direct the user to the dashboard.
 * Unsuccessful authentication will lead to error. Some errors will have feedback shown in this component, while others will lead to a re-direct to the error page. Check the axios configurations in the config folder to learn more about this behaviour.
 * 
 * @visibleName LogIn
 * @returns {React.ReactElement}
 * 
 * @todo When user inputs the wrong credentials 3+ times, a timer should be shown to reflect the temporary login block time. Check the login route( user model in the backend to confirm the temporary block time).
 */
function Login() {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const isComponentMounted = useIsComponentMounted();

    // Used for honeypot
    const [honeypotValue, setHoneypotValue] = useState("");

    // State to define whether user prefers OTP or password to log in
    const [otpActive, setOtpActive] = useState(false);

    // Used for actual fields
    const [email, setEmail] = useState("");
    const [emailIsValid, setEmailIsValid] = useState(false);
    const [password, setPassword] = useState("");
    const [passwordIsValid, setPasswordIsValid] = useState(false);
    const [otp, setOtp] = useState("");
    const [otpIsValid, setOtpIsValid] = useState(false);
    const [otpWasSent, setOtpWasSent] = useState(false);

    // State set by api call
    const [errorMessage, setErrorMessage] = useState("");
    const [loginFailed, setLoginFailed] = useState(false);

    // If mfa enabled: State set by api call
    const [mfaStep2, setMfaStep2] = useState(false);
    const [mfaMessage, setMfaMessage] = useState("");

    // Form is valid when all fields are valid and api call did not return error
    const formIsValid = otpActive ? (emailIsValid && otpIsValid && errorMessage === "") : (emailIsValid && passwordIsValid && errorMessage === "")

    //if a form error was shown, hide it when the user starts to correct the input
    useEffect(() => {
        if (errorMessage !== "") {
            setErrorMessage("")
        }
    }, [email, password, otp]);

    const sendOtp = (e) => {
        e.preventDefault();
        // get rid of previous error messages
        if (errorMessage !== "") { setErrorMessage("") }
        if (!emailIsValid) {
            setErrorMessage("Please check email input.");
            return
        }
        const requestData = {
            email: email,
            honeyPot: honeypotValue
        }

        dispatch(setLoader(true))
        getOTP(requestData)
            .then(res => {
                if (isComponentMounted()) {
                    if (res.response) { setOtpWasSent(true); }
                    else {
                        setLoginFailed(res.response);
                        setErrorMessage(res.message);
                    }
                }
            })
            .catch(error => {
                console.error("Error in otp function.", error);
            })
            .finally(() => {
                dispatch(setLoader(false));
            })
    };

    // TODO test this component with mfa
    const handleSubmit = (e) => {
        e.preventDefault();
        if (formIsValid) {
            //When MFA is enabled, this function should be called twice: one for each auth method
            let method;
            if (mfaStep2) { if (otpActive) { method = "password" } else { method = "otp" } }
            else { if (otpActive) { method = "otp" } else { method = "password" } }
            const requestData = {
                email: email,
                password: otpActive ? otp : password,
                method: method,
                honeyPot: honeypotValue
            }
            dispatch(setLoader(true))
            loginUser(requestData)
                .then(res => {
                    if (isComponentMounted()) {
                        if (res.response) {
                            if (res.response.status === 202) {
                                setMfaStep2(true)
                                setMfaMessage(res.response.message)
                            } else {
                                navigate("/userAccount");
                            }
                        } else {
                            setLoginFailed(res.response);
                            setErrorMessage(res.message);
                        }
                    }
                })
                .catch(error => {
                    console.error("Error in login function.", error);
                })
                .finally(() => {
                    dispatch(setLoader(false));
                })
        }
    };

    // Auth components
    const passwordComponent = (
        <InputPassword
            autocomplete="current-password"
            password={password}
            setPassword={setPassword}
            setPasswordIsValid={setPasswordIsValid}
        />
    )

    const otpComponent = (
        <InputOtp
            otp={otp}
            setOtp={setOtp}
            setOtpIsValid={setOtpIsValid}
        />
    )

    return (
        <div className="LogIn">

            <Helmet>
                <title>Log in</title>
                <meta name="description" content="Log in" />
            </Helmet>

            <h2>Log In</h2>

            <form onSubmit={handleSubmit} className='MAIN-form LogIn-form'>

                <div className="MAIN-form-display-table Login-opt-container">
                    <label htmlFor="Login-Options">Select: </label>

                    <span className="LogIn-Opts" id="Login-Options">
                        <button
                            className={otpActive ? "" : "Login-Opt-Active"}
                            onClick={(e) => { e.preventDefault(); setOtpActive(false) }}>
                            Password
                        </button>
                        <button
                            className={otpActive ? "Login-Opt-Active" : ""}
                            onClick={(e) => { e.preventDefault(); setOtpActive(true) }}>
                            OTP
                        </button>
                    </span>
                </div>

                <InputEmail
                    autocomplete="username"
                    email={email}
                    setEmail={setEmail}
                    setEmailIsValid={setEmailIsValid}
                />

                {!otpActive && passwordComponent}
                {otpActive && otpWasSent && otpComponent}

                {
                    mfaStep2 && (
                        <div className="LogIn-ExtraOpts">
                            <p>{mfaMessage}</p>
                        </div>
                    )
                }

                {otpActive && mfaStep2 && passwordComponent}
                {!otpActive && mfaStep2 && otpComponent}

                <Honeypot setHoneypotValue={setHoneypotValue} />

                <div className="LogIn-Btns-Container">
                    <button
                        className={(otpActive && !otpWasSent) ? "MAIN-display-none" : ""} disabled={!formIsValid}
                        type="submit">
                        Log in
                    </button>

                    {otpActive && (
                        <button
                            disabled={formIsValid}
                            onClick={(e) => { sendOtp(e) }}>
                            {otpWasSent ? "Resend OTP" : "Send OTP"}
                        </button>
                    )}
                </div>

                {
                    errorMessage !== "" && (
                        < ErrorMessage message={errorMessage} ariaDescribedby="api-response-error" />
                    )
                }

            </form>

            {
                errorMessage !== "" && loginFailed && (
                    < AuthErrorHint component={"login"} />
                )
            }

            {
                otpActive ? (
                    <div className="LogIn-ExtraOpts">
                        <p><i>You will only receive an OTP per email if the account is registered.</i></p>
                        <p><i>The server will reject invalid OTPs and non-registered emails attempting alike.</i></p>
                        <p><i>PS: If you have MFA enabled, a password will still be required.</i></p>
                    </div>
                ) : (
                    <div className="LogIn-ExtraOpts">
                        <p>Forgot your password? <a href="/resetPassword">Reset password</a>.</p>
                        <p>Don't have an account yet? <a href="/signup">Sign up</a>.</p>
                    </div>
                )
            }

        </div>
    );
};

export default Login;