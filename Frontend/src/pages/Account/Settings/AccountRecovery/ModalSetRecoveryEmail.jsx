import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { setRecoveryEmail } from "../../../../config/apiHandler/authRecovery/setRecoveryEmail.js"
import { getOTP } from "../../../../config/apiHandler/authSession/otp.js";
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage";
import InputEmail from "../../../../components/Auth/InputEmail.jsx";
import InputPassword from "../../../../components/Auth/InputPassword.jsx";
import InputOtp from "../../../../components/Auth/InputOtp.jsx";
import HiddenUsername from "../../../../components/Auth/HiddenUsername.jsx"

/**
 * This component is a modal used to set a recovery email address.
 * 
 * @param {object} props
 * @param {func} props.modalToggler opens/closes modal
 * @param {object} props.user 
 * @param {string} props.user.email 
 * @param {string} props.acctRecovery
 * @param {bool} props.acctRecovery.recoveryEmailAdded
 * @returns {React.ReactElement}
 */
function ModalSetRecoveryEmail(props) {
    const { modalToggler, user, acctRecovery } = props;

    const dispatch = useDispatch();

    const isComponentMounted = useIsComponentMounted();

    const userAgent = navigator.userAgent; //info to be passed on to BE

    // State for input components
    const [email, setEmail] = useState("");
    const [emailIsValid, setEmailIsValid] = useState(false);
    const [otp, setOtp] = useState("");
    const [otpIsValid, setOtpIsValid] = useState(false);
    const [otpWasSent, setOtpWasSent] = useState(false);
    const [password, setPassword] = useState("");
    const [passwordIsValid, setPasswordIsValid] = useState(false);

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");
    const [recoverySet, setRecoverySet] = useState(false);

    // Form is valid when all fields are valid and api call did not return error
    const formIsValid = (emailIsValid && passwordIsValid && otpIsValid && infoMessage === "")

    //if a form error was shown, hide it when the user starts to correct the input
    useEffect(() => {
        if (infoMessage !== "") {
            setInfoMessage("")
        }
    }, [email, otp]);

    const sendOtp = (e) => {
        e.preventDefault();
        // get rid of previous error messages
        if (infoMessage !== "") { setInfoMessage("") }
        if (!emailIsValid) { setInfoMessage("Please check email input."); return }

        const requestData = {
            email: email,
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
        if (formIsValid) {
            const requestData = {
                email: email,
                password: password,
                otp: otp,
                userAgent: userAgent
            }
            dispatch(setLoader(true))
            setRecoveryEmail(requestData)
                .then(res => {
                    if (isComponentMounted()) {
                        setInfoMessage(res.message);
                        if (res.response) { setRecoverySet(true) }
                    }
                })
                .catch(error => {
                    console.error("Error in adding recovery email.", error);
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
                    <p><i>Two-step verification required: OTP and password</i></p>
                    <p>First, input the desired recovery email and request an OTP.</p>
                    <p>You will then receive the OTP in the recovery email.</p>
                    <p>Please copy and paste it bellow within 30 minutes.</p>
                    <p>Last, confirm the password you use to log into your account.</p>
                    <p>Click 'Save' to set the recovery email.</p>
                </div>
                <InputEmail
                    autocomplete="email"
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
                        className={recoverySet ? "MAIN-display-none" : ""}
                        disabled={formIsValid || recoverySet}
                        onClick={(e) => { sendOtp(e) }}
                        type="button">
                        {otpWasSent ? "Resend OTP" : "Send OTP"}
                    </button>

                    <button
                        className={!otpWasSent ? "MAIN-display-none" : "Modal-ActionBtn"}
                        disabled={(!formIsValid || recoverySet)}
                        type="submit">
                        Save
                    </button>

                    <button
                        className={!recoverySet ? "MAIN-display-none" : ""}
                        disabled={formIsValid}
                        onClick={modalToggler}
                        type="button">
                        Close
                    </button>
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

ModalSetRecoveryEmail.propTypes = {
    modalToggler: PropTypes.func.isRequired,
    user: PropTypes.shape({
        email: PropTypes.string.isRequired
    }).isRequired,
    acctRecovery: PropTypes.shape({
        recoveryEmailAdded: PropTypes.bool.isRequired
    }).isRequired,
};

export default ModalSetRecoveryEmail;