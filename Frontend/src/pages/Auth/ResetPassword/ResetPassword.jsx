import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { Helmet } from "react-helmet-async";
import { setLoader } from "../../../redux/loader/loaderSlice"
import { getOTP } from "../../../config/apiHandler/authSession/otp.js";
import useIsComponentMounted from "../../../hooks/useIsComponentMounted.js";
import ErrorMessage from "../../../components/ErrorMessage/ErrorMessage";
import Honeypot from "../../../components/Honeypot/Honeypot";
import InputEmail from "../../../components/Auth/InputEmail.jsx";
import InputPassword from "../../../components/Auth/InputPassword";
import InputOtp from "../../../components/Auth/InputOtp.jsx";

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
function ResetPassword() {
    const dispatch = useDispatch();
    const isComponentMounted = useIsComponentMounted();

    const userAgent = navigator.userAgent; //info to be passed on to BE

    // Used for honeypot
    const [honeypotValue, setHoneypotValue] = useState("");

    // Used for actual fields
    const [password, setPassword] = useState("");
    const [passwordIsValid, setPasswordIsValid] = useState(false);
    const [confirmPassword, setConfirmPassword] = useState("");
    const [confirmPasswordIsValid, setConfirmPasswordIsValid] = useState(false);
    const [otp, setOtp] = useState("");
    const [otpIsValid, setOtpIsValid] = useState(false);
    const [otpWasSent, setOtpWasSent] = useState(false);

    // If mfa enabled: State set by api call
    const [mfaStep2, setMfaStep2] = useState(false);
    const [mfaMessage, setMfaMessage] = useState("");

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");

    // Form is valid when all fields are valid and api call did not return error
    const formIsValid = mfaStep2 ? (passwordIsValid && confirmPasswordIsValid && otpIsValid && infoMessage === "") : (passwordIsValid && confirmPasswordIsValid && infoMessage === "")

    //if a form error was shown, hide it when the user starts to correct the input
    useEffect(() => {
        if (infoMessage !== "") {
            setInfoMessage("")
        }
    }, [password, confirmPassword, otp]);

    //allow user to click on 'resend' OTP again only 10 seconds after clicking it
    useEffect(() => {
        if (otpWasSent) {
            const timer = setTimeout(() => {
                setOtpWasSent(false); // Reset otpWasSent to false after 10 seconds
            }, 10000); // 10000ms = 10 seconds

            // Cleanup function to clear the timer if the component unmounts
            return () => clearTimeout(timer);
        }
    }, [otpWasSent]);

    const sendOtp = (e) => {
        e.preventDefault();
        // get rid of previous error messages
        if (infoMessage !== "") { setErrorMessage("") }
        if (!formIsValid) {
            setInfoMessage("Please check email input.");
            return
        }
        const requestData = {
            email: email, //how to get email....? must be recovery
            honeyPot: honeypotValue
        }

        dispatch(setLoader(true))
        getOTP(requestData)
            .then(res => {
                if (isComponentMounted()) {
                    if (res.response) { setOtpWasSent(true); }
                    else { setInfoMessage(res.message); }
                }
            })
            .catch(error => {
                console.error("Error in otp function.", error);
            })
            .finally(() => {
                dispatch(setLoader(false));
            })
    };


    const handleSubmit = (e) => {
        e.preventDefault();
        if (!formIsValid) { setInfoMessage("Check credentials."); }
        console.log("sent")
        // dispatch(setLoader(true))
        // loginUser(requestData)
        //     .then(res => {
        //         if (isComponentMounted()) {
        //             if (res.response) {
        //                 if (res.status === 202) {
        //                     setMfaStep2(true)
        //                     setMfaMessage(res.message)
        //                 } else {
        //                     navigate("/userAccount");
        //                 }
        //             } else {
        //                 setLoginFailed(res.response);
        //                 setErrorMessage(res.message);
        //             }
        //         }
        //     })
        //     .catch(error => {
        //         console.error("Error in login function.", error);
        //     })
        //     .finally(() => {
        //         dispatch(setLoader(false));
        //     })
    };

    const otpComponent = (
        <InputOtp
            otp={otp}
            setOtp={setOtp}
            setOtpIsValid={setOtpIsValid}
            cssClass={"MAIN-form-display-table"}
        />
    )

    return (
        <div>

            <Helmet>
                <title>Reset Password</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>

            <h2>Reset Password</h2>

            <p className="MAIN-info-paragraph">
                Provide a new password and confirm it bellow.
            </p>

            <p className="MAIN-info-paragraph">
                If you have MFA set in your account, you will be requested to provide an OTP that will be sent to your recovery email address. If you lost access to your recovery email address, please contact support.
            </p>

            <br />

            <form onSubmit={handleSubmit} className='MAIN-form'>

                <InputPassword
                    cssClass={"MAIN-form-display-table"}
                    disableField={mfaStep2}
                    labelText={"New Password"}
                    password={password}
                    setPassword={setPassword}
                    setPasswordIsValid={setPasswordIsValid}
                    simpleValidation={false}
                />

                <InputPassword
                    autocomplete={"confirm-password"}
                    cssClass={"MAIN-form-display-table"}
                    disableField={mfaStep2}
                    labelText={"Confirm Password"}
                    password={confirmPassword}
                    setPassword={setConfirmPassword}
                    setPasswordIsValid={setConfirmPasswordIsValid}
                />

                {
                    mfaStep2 && (
                        <>
                            <div>
                                <p className="MAIN-info-paragraph">An OTP was sent to your recovery email: b***@***.com</p>
                                <p className="MAIN-info-paragraph">Please copy and paste it bellow within 30 minutes.</p>
                            </div>

                            {otpComponent}
                        </>
                    )
                }

                <Honeypot setHoneypotValue={setHoneypotValue} />

                <button
                    disabled={!formIsValid}
                    type="submit">
                    Reset password
                </button>

                {
                    infoMessage !== "" && (
                        < ErrorMessage message={infoMessage} ariaDescribedby="api-response-error" />
                    )
                }
            </form>

            {
                mfaStep2 && !otpWasSent && (
                    <p>Did not receive OTP? <a href="#" onClick={sendOtp}>Resend OTP</a></p>
                )
            }
            {
                mfaStep2 && otpWasSent && (
                    <p className="MAIN-info-paragraph"><i>
                        OTP was resent, please check your recovery email.
                    </i></p>
                )
            }

        </div>
    );
};

export default ResetPassword;