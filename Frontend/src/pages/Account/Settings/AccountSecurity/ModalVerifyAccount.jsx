import { useEffect, useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { verifyAccount } from "../../../../config/apiHandler/authRegistration/verifyAccount.js"
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage.jsx";
import { getOTP } from "../../../../config/apiHandler/authSession/otp.js";
import InputOtp from "../../../../components/Auth/InputOtp.jsx";

/**
 * This component is a modal used to verify the user's account email address
 * 
 * @param {object} props
 * @param {object} props.user 
 * @param {string} props.user.email
 * @param {bool} props.user.acctVerified
 * @returns {React.ReactElement}
 */
function ModalVerifyAccount(props) {
    const { user } = props;

    const userAgent = navigator.userAgent; //info to be passed on to BE

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();


    const [otp, setOtp] = useState("");
    const [otpIsValid, setOtpIsValid] = useState(false);
    const [otpWasSent, setOtpWasSent] = useState(null);

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");

    // Action btn
    const btnDisabled = !otpIsValid || infoMessage !== "" || user.acctVerified

    // Ref to track initial mount: avoid sending duplicate API calls in strict mode
    const hasSentOtp = useRef(false);

    // Send OTP to user upon mount
    useEffect(() => {
        //only send request if email address has not yet been verified (avoid unecessary requests)
        if (user.acctVerified !== true && !hasSentOtp.current) {
            hasSentOtp.current = true; // Mark OTP as sent
            sendOtp()
        }
    }, []);

    //if a form error was shown, hide it when the user starts to correct the input
    useEffect(() => {
        if (infoMessage !== "") {
            setInfoMessage("")
        }
    }, [otp]);


    const sendOtp = (e) => {
        if (e) { e.preventDefault(); }

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
                    if (!res.response) { setInfoMessage(res.message); setOtpWasSent(false) }
                    else { setOtpWasSent(true) }
                }
            })
            .catch(error => { console.error("Error in otp function.", error); })
            .finally(() => { dispatch(setLoader(false)); })
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!otpIsValid) {
            setInfoMessage("Invalid OTP.")
            return
        }

        dispatch(setLoader(true));

        const handleResponse = (response) => {
            if (isComponentMounted()) {
                setInfoMessage(response.info)
            }
        };

        const handleError = (error) => {
            console.warn("clickHandler in modal encountered an error", error);
        };

        const handleFinally = () => {
            dispatch(setLoader(false));
        };

        verifyAccount(otp, userAgent)
            .then(response => handleResponse(response))
            .catch(error => { handleError(error) })
            .finally(handleFinally);
    };

    return (
        <>
            {otpWasSent === null ? (
                <>
                    <p>Sending email with one-time password...</p>
                </>
            ) : otpWasSent ? (
                <>
                    <p>A OTP was sent to {user.email}.</p>
                    <p>Please copy and paste it bellow.</p>
                    <p>The OTP is valid for 30 minutes.</p>
                </>
            ) : (
                <>
                    <p>We failed to send an OTP to {user.email}.</p>
                    <p>Please check if the email address exists and try again later.</p>
                    <p>Contact us in case you believe your email address is correct but we are failing to verify it.</p>
                </>
            )}


            {
                otpWasSent && (
                    <form onSubmit={handleSubmit} className="MAIN-form">
                        <br />
                        <InputOtp
                            otp={otp}
                            setOtp={setOtp}
                            setOtpIsValid={setOtpIsValid}
                        />
                        {
                            infoMessage !== "" && (
                                < ErrorMessage message={infoMessage} ariaDescribedby="api-response-error" />
                            )
                        }
                        {infoMessage === "" && <br />}

                        <div className="Modal-BtnContainer">

                            <button
                                disabled={user.acctVerified}
                                onClick={(e) => { sendOtp(e) }}>
                                Resend OTP
                            </button>
                            <button
                                className="Modal-ActionBtn"
                                disabled={btnDisabled}
                                type="submit">
                                Verify
                            </button>
                        </div>
                    </form>
                )
            }
        </>
    );
};

ModalVerifyAccount.propTypes = {
    user: PropTypes.shape({
        email: PropTypes.string.isRequired,
        acctVerified: PropTypes.bool.isRequired,
    }).isRequired,
};

export default ModalVerifyAccount;