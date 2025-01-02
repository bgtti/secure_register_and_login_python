import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { useLocation } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { setLoader } from "../../../redux/loader/loaderSlice"
import { changePassword } from "../../../config/apiHandler/authCredChange/changePassword.js";
import useIsComponentMounted from "../../../hooks/useIsComponentMounted.js";
import { PATH_TO } from "../../../router/routePaths.js"
import { tokenFormatIsValid } from "../../../utils/validation.js"
import ErrorMessage from "../../../components/ErrorMessage/ErrorMessage";
import Honeypot from "../../../components/Honeypot/Honeypot";
import HiddenUsername from "../../../components/Auth/HiddenUsername.jsx";
import InputPassword from "../../../components/Auth/InputPassword";
import InputOtp from "../../../components/Auth/InputOtp.jsx";

/**
 * Component returns Reset Password page
 * 
 * When a password reset is requested, user should get an email with a link leading to this page.
 * The user will be prompted to give a news password.
 * If MFA is enable on the user's account, the server will respond with 202 and the user will also be asked to input an OTP sent to the user's recovery email address.
 * 
 * @returns {React.ReactElement}
 */
function ResetPassword() {
    const dispatch = useDispatch();
    const isComponentMounted = useIsComponentMounted();

    //info to be passed on to BE
    const userAgent = navigator.userAgent;

    // Extract the token from the url
    const location = useLocation();

    // Extract the url path 
    const currentPath = location.pathname;
    const tokenInUrl = currentPath.split("token=")[1];

    // Used for honeypot
    const [honeypotValue, setHoneypotValue] = useState("");

    // Used for actual fields
    const [password, setPassword] = useState("");
    const [passwordIsValid, setPasswordIsValid] = useState(false);
    const [confirmPassword, setConfirmPassword] = useState("");
    const [confirmPasswordIsValid, setConfirmPasswordIsValid] = useState(false);
    const [otp, setOtp] = useState("");
    const [otpIsValid, setOtpIsValid] = useState(false);

    // If mfa enabled: State set by api call
    const [mfaStep2, setMfaStep2] = useState(false);
    const [mfaInfo, setMfaInfo] = useState(false);

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


    const handleSubmit = (e) => {
        e.preventDefault();
        if (!formIsValid) { setInfoMessage("Check credentials."); }
        if (!tokenFormatIsValid(tokenInUrl)) { setInfoMessage("Token format invalid."); }

        let requestData = {
            "newPassword": password,
            "pwChangeReason": "reset",
            "isFirstFactor": !mfaStep2,
            "honeypot": honeypotValue,
            "userAgent": userAgent,
            "signedToken": tokenInUrl,
            "otp": otp
        }

        dispatch(setLoader(true))
        changePassword(requestData)
            .then(res => {
                if (isComponentMounted()) {
                    if (res.status === 202) { setMfaStep2(true); setMfaInfo(res.message) }
                    else { setInfoMessage(res.message); }
                }
            })
            .catch(error => { console.error("Error in reset password function.", error); })
            .finally(() => { dispatch(setLoader(false)); })
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

                <HiddenUsername
                    username="" />

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
                                <p className="MAIN-info-paragraph">{mfaInfo}</p>
                                <p className="MAIN-info-paragraph">Please copy and paste it bellow within 30 minutes to complete the process.</p>
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
                mfaStep2 && (
                    <p>Did not receive OTP? <a href={PATH_TO.contact}>contact us</a></p>
                )
            }

        </div>
    );
};

export default ResetPassword;