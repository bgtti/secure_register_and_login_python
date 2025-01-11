import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { getOTP } from "../../../../config/apiHandler/authSession/otp.js";
import { deleteOwnAccount } from "../../../../config/apiHandler/authRegistration/deleteAccount.js"
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage";
import InputPassword from "../../../../components/Auth/InputPassword.jsx";
import InputOtp from "../../../../components/Auth/InputOtp.jsx";
import HiddenUsername from "../../../../components/Auth/HiddenUsername.jsx"
/**
 * This component is a modal used delete the user's account.
 * 
 * @todo functionality missing
 * 
 * @visibleName Modal Initiate Email Verification
 * @param {object} props
 * @param {func} props.modalToggler opens/closes modal
 * @returns {React.ReactElement}
 */
function ModalDeleteAccount(props) {
    const { modalToggler, user } = props;

    const userAgent = navigator.userAgent; //info to be passed on to BE

    const dispatch = useDispatch();
    const navigate = useNavigate();
    const isComponentMounted = useIsComponentMounted();

    // State for input components
    const [otp, setOtp] = useState("");
    const [otpIsValid, setOtpIsValid] = useState(false);
    const [otpWasSent, setOtpWasSent] = useState(false);
    const [password, setPassword] = useState("");
    const [passwordIsValid, setPasswordIsValid] = useState(false);

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");

    // Form is valid when all fields are valid and api call did not return error
    const formIsValid = (passwordIsValid && otpIsValid && infoMessage === "")

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
        if (!passwordIsValid || (!otpIsValid && user.mfa)) { setInfoMessage("Check credentials"); return }

        const requestData = {
            password: password,
            otp: otp,
            userAgent: userAgent
        }

        dispatch(setLoader(true));

        const handleResponse = (response) => {
            if (isComponentMounted()) {
                if (response.response) { navigate("/accountDeleted"); }
                else { setInfoMessage(response.message) }
            }
        };

        const handleError = (error) => {
            if (isComponentMounted()) {
                console.warn("clickHandler in modal encountered an error", error);
            }
        };

        const handleFinally = () => {
            dispatch(setLoader(false));
        };

        deleteOwnAccount(requestData)
            .then(response => handleResponse(response))
            .catch(error => { handleError(error) })
            .finally(handleFinally);
    };



    return (
        <>
            <form onSubmit={handleSubmit} className="MAIN-form">
                <p><b>Warning: You are about to delete your account.</b></p>
                <p>This action cannot be undone.</p>

                {
                    user.mfa === true ? (
                        <>
                            <p>Multi-factor authentication is enabled in your account.</p>
                            <p>Click the button to receive an OTP per email to proceed.</p>
                        </>
                    ) : (
                        <>
                            <p>Type your password bellow to proceed.</p>
                        </>
                    )
                }

                {/* Form fields */}
                {
                    (!user.mfa || (user.mfa && otpWasSent)) && (
                        <>
                            <HiddenUsername
                                username={user.email}
                            />
                            <InputPassword
                                autocomplete="current-password"
                                password={password}
                                setPassword={setPassword}
                                setPasswordIsValid={setPasswordIsValid}
                            />
                            {user.mfa && (
                                <InputOtp
                                    otp={otp}
                                    setOtp={setOtp}
                                    setOtpIsValid={setOtpIsValid}
                                />
                            )}
                        </>
                    )
                }

                {/* Form buttons */}

                {
                    user.mfa && (
                        <div className="Modal-BtnContainer">
                            <button
                                className={!otpWasSent ? "Modal-ActionBtn" : ""}
                                // disabled={otpWasSent}
                                onClick={(e) => { sendOtp(e) }}
                                type="button">
                                {otpWasSent ? "Resend OTP" : "Send OTP"}
                            </button>
                            {
                                otpWasSent ? (
                                    <button
                                        className="MAIN-DeleteBtn"
                                        disabled={(!formIsValid)}
                                        type="submit">
                                        Delete account
                                    </button>
                                ) : (
                                    <button
                                        onClick={modalToggler}
                                        type="button">
                                        Keep account
                                    </button>
                                )
                            }
                        </div>
                    )
                }
                {
                    !user.mfa && (
                        <div className="Modal-BtnContainer">
                            <button
                                className="MAIN-DeleteBtn"
                                disabled={(!passwordIsValid)}
                                type="submit">
                                Delete account
                            </button>
                            <button
                                onClick={modalToggler}
                                type="button">
                                Keep account
                            </button>
                        </div>
                    )
                }
                {
                    infoMessage !== "" && (
                        < ErrorMessage message={infoMessage} ariaDescribedby="api-response-error" />
                    )
                }

            </form>
        </>
    );
};

ModalDeleteAccount.propTypes = {
    modalToggler: PropTypes.func.isRequired
};

export default ModalDeleteAccount;