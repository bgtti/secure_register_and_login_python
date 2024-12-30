import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { setMfa } from "../../../../config/apiHandler/authSecurity/setMfa.js"
import { getOTP } from "../../../../config/apiHandler/authSession/otp.js";
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage.jsx";
import HiddenUsername from "../../../../components/Auth/HiddenUsername.jsx"
import InputPassword from "../../../../components/Auth/InputPassword.jsx";
import InputOtp from "../../../../components/Auth/InputOtp.jsx";

/**
 * This component is a modal used to disable MFA
 * 
 * @param {object} props
 * @param {func} props.modalToggler opens/closes modal
 * @param {object} props.user 
 * @param {string} props.user.email
 * @param {bool} props.user.mfa
 * @returns {React.ReactElement}
 */
function ModalDisableMFA(props) {
    const { modalToggler, user } = props;

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();

    const userAgent = navigator.userAgent; //info to be passed on to BE

    const [password, setPassword] = useState("");
    const [passwordIsValid, setPasswordIsValid] = useState(false);
    const [otp, setOtp] = useState("");
    const [otpIsValid, setOtpIsValid] = useState(false);
    const [otpWasSent, setOtpWasSent] = useState(false);

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");

    // Form is valid when all fields are valid and api call did not return error
    const formIsValid = (passwordIsValid && otpIsValid && infoMessage === "")

    // Action btn
    const btnDisabled = (!formIsValid || infoMessage !== "" || !user.mfa)

    //if a form error was shown, hide it when the user starts to correct the input
    useEffect(() => {
        if (infoMessage !== "") {
            setInfoMessage("")
        }
    }, [password, otp]);

    const sendOtp = (e) => {
        e.preventDefault();
        // get rid of previous error messages
        if (infoMessage !== "") { setInfoMessage("") }

        const requestData = {
            email: user.email,
            honeyPot: ""
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

        if (!formIsValid) {
            setInfoMessage("Check your credentials.")
            return
        }

        const requestData = {
            otp: otp,
            password: password,
            enableMfa: false,
            userAgent: userAgent
        }

        dispatch(setLoader(true));

        const handleResponse = (response) => {
            if (isComponentMounted()) {
                setInfoMessage(response.message)
            }
        };

        const handleError = (error) => {
            setInfoMessage("Failed to disable MFA. Please try again later.");
            console.warn("clickHandler in modal encountered an error", error);
        };

        const handleFinally = () => {
            dispatch(setLoader(false));
        };

        setMfa(requestData)
            .then(response => handleResponse(response))
            .catch(error => { handleError(error) })
            .finally(handleFinally);
    };

    return (
        <>
            <div>
                <p><i>Two-step verification required: OTP and password</i></p>
                <p>Multi-factor authentication (MFA) increases the security of your account.</p>
                <p>If you want to disable MFA, click to receive an OTP per email.</p>
                <p>Then copy and paste it bellow within 30 minutes and input your password.</p>
            </div>

            <br />

            <form onSubmit={handleSubmit} className="MAIN-form">
                {
                    otpWasSent && (
                        <>
                            <InputOtp
                                otp={otp}
                                setOtp={setOtp}
                                setOtpIsValid={setOtpIsValid}
                            />

                            {/* HiddenUsername should help browser find "current-password" */}
                            <HiddenUsername
                                username={user.email}
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

                <div className="Modal-BtnContainer">

                    <button
                        className={!otpWasSent ? "Modal-ActionBtn" : ""}
                        disabled={!user.mfa}
                        onClick={(e) => { sendOtp(e) }}
                        type="button">
                        {!otpWasSent ? "Send OTP" : "Resend OTP"}
                    </button>

                    {
                        otpWasSent ? (
                            <button
                                className="MAIN-DeleteBtn"
                                disabled={btnDisabled}
                                type="submit">
                                Disable MFA
                            </button>
                        ) : (
                            <button
                                onClick={modalToggler}
                                type="button">
                                Cancel
                            </button>
                        )
                    }

                </div>
                {
                    infoMessage !== "" && (
                        < ErrorMessage message={infoMessage} ariaDescribedby="api-response-error" />
                    )
                }
            </form>
        </>
    );
};

ModalDisableMFA.propTypes = {
    modalToggler: PropTypes.func.isRequired,
    user: PropTypes.shape({
        email: PropTypes.string.isRequired,
        mfa: PropTypes.bool.isRequired,
    }).isRequired,
};

export default ModalDisableMFA;