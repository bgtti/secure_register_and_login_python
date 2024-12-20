import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { setRecoveryEmail } from "../../../../config/apiHandler/authRecovery/recoveryEmail.js"
import { getOTP } from "../../../../config/apiHandler/authSession/otp.js";
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage";
import InputEmail from "../../../../components/Auth/InputEmail.jsx";
import InputPassword from "../../../../components/Auth/InputPassword.jsx";
import InputOtp from "../../../../components/Auth/InputOtp.jsx";
// import "./modalAccountDetailChange.css"

/**
 * This component is a modal used to change sensitive account information.
 * 
 * @param {object} props
 * @param {func} props.modalToggler opens/closes modal
 * @returns {React.ReactElement}
 */
function ModalRecoveryEmail(props) {
    const { modalToggler } = props;

    const dispatch = useDispatch();

    const isComponentMounted = useIsComponentMounted();

    const userAgent = navigator.userAgent; //info to be passed on to BE

    //TODO: get recovery email/ see if it exists

    // State for input components
    const [email, setEmail] = useState("");
    const [emailIsValid, setEmailIsValid] = useState(false);
    const [otp, setOtp] = useState("");
    const [otpIsValid, setOtpIsValid] = useState(false);
    const [otpWasSent, setOtpWasSent] = useState(false);
    const [password, setPassword] = useState("");
    const [passwordIsValid, setPasswordIsValid] = useState(false);

    // State set by api call
    const [errorMessage, setErrorMessage] = useState("");
    const [formSubmitted, setFormSubmitted] = useState(false);

    // Form is valid when all fields are valid and api call did not return error
    const formIsValid = (emailIsValid && passwordIsValid && otpIsValid && errorMessage === "")

    //if a form error was shown, hide it when the user starts to correct the input
    useEffect(() => {
        if (errorMessage !== "") {
            setErrorMessage("")
        }
    }, [email, otp]);

    const sendOtp = (e) => {
        e.preventDefault();
        // get rid of previous error messages
        if (errorMessage !== "") { setErrorMessage("") }
        if (!emailIsValid) { setErrorMessage("Please check email input."); return }

        const requestData = {
            email: email,
            honeyPot: ""
        }

        dispatch(setLoader(true))
        getOTP(requestData)
            .then(res => {
                if (isComponentMounted()) {
                    if (res.response) { setOtpWasSent(true); }
                    else {
                        setApiReqFailed(res.response);
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

    const handleSubmit = (e) => {
        e.preventDefault();
        if (formIsValid) {
            const requestData = {
                email: email,
                password: password,
                otp: otp,
                honeypot: ""
            }
            dispatch(setLoader(true))
            setRecoveryEmail(requestData)
                .then(res => {
                    if (isComponentMounted()) {
                        if (res.response) {
                            setErrorMessage("Recovery email set successfully!");
                            setFormSubmitted(true)
                        } else {
                            setApiReqFailed(true);
                            setErrorMessage(res.message);
                        }
                    }
                })
                .catch(error => {
                    console.error("Error in adding account email.", error);
                })
                .finally(() => {
                    dispatch(setLoader(false));
                })
        }
    };


    return (
        <>
            <form onSubmit={handleSubmit} className="ModalAccountDetailChange MAIN-form">
                <div>
                    <p>Note: two-step verification required.</p>
                    <p>You will receive an OTP to confirm this email.</p>
                </div>
                <InputEmail
                    autocomplete="username"
                    email={email}
                    setEmail={setEmail}
                    setEmailIsValid={setEmailIsValid}
                />
                {
                    otpWasSent && (
                        <>
                            <InputOtp
                                otp={otp}
                                setOtp={setOtp}
                                setOtpIsValid={setOtpIsValid}
                            />

                            <InputPassword
                                autocomplete="current-password"
                                password={password}
                                setPassword={setPassword}
                                setPasswordIsValid={setPasswordIsValid}
                            />
                        </>
                    )
                }

                <div className="ModalAccountDetailChange-BtnContainer">
                    <button
                        className={!otpWasSent ? "MAIN-display-none" : ""}
                        disabled={(!formIsValid || formSubmitted)}
                        type="submit">
                        Save
                    </button>

                    <button
                        className={formSubmitted ? "MAIN-display-none" : ""}
                        disabled={formIsValid}
                        onClick={(e) => { sendOtp(e) }}>
                        {otpWasSent ? "Resend OTP" : "Send OTP"}
                    </button>

                    <button
                        className={!formSubmitted ? "MAIN-display-none" : ""}
                        disabled={formIsValid}
                        onClick={modalToggler}>
                        Close
                    </button>
                </div>

                {
                    errorMessage !== "" && (
                        < ErrorMessage message={errorMessage} ariaDescribedby="api-response-error" />
                    )
                }
            </form>
        </>
    );
};

ModalRecoveryEmail.propTypes = {
    modalToggler: PropTypes.func.isRequired
};

export default ModalRecoveryEmail;