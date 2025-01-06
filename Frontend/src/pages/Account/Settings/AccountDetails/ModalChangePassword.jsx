import { useState, useEffect, useRef } from "react";
import { useDispatch } from "react-redux";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { changePassword } from "../../../../config/apiHandler/authCredChange/changePassword.js";
import { getOTP } from "../../../../config/apiHandler/authSession/otp.js";
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage.jsx"
import HiddenUsername from "../../../../components/Auth/HiddenUsername.jsx";
import InputPassword from "../../../../components/Auth/InputPassword";
import InputOtp from "../../../../components/Auth/InputOtp.jsx";
import "./modalAccountDetailChange.css"

/**
 * This component is a modal used to change the user's password.
 * 
 * It works similarly to the password reset component, with the exception that this component only needs one API call and not two (if MFA is enabled, the second factor will be added to the first and only one request shall be sent).
 * 
 * How a user can change the password:
 * 1) User will be requested to input their old password
 * 2) User will then be requested to input the new password
 * 3) User will be requested to confirm the new password
 * 4) If user has MFA enabled, user will get an OTP sent to account email
 * 6) Clicking submit will change the user's password if all goes well.
 * 
 * Rules: 
 * - New password must not be same as old password (useless request otherwise)
 * - New password and Confirm Password must match and pass validation
 * 
 * @param {object} props
 * @param {func} props.modalToggler // opens/closes modal
 * @param {object} props.user // the user as in the redux store
 * @param {string} props.user.email
 * @returns {React.ReactElement}
 */
function ModalChangePassword(props) {
    const { modalToggler, user } = props;

    const userAgent = navigator.userAgent; //info to be passed on to BE 

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();

    // Used for actual fields
    const [oldPassword, setOldPassword] = useState(""); // ie: current password
    const [oldPasswordIsValid, setOldPasswordIsValid] = useState(false);
    const [password, setPassword] = useState(""); // ie: new password
    const [passwordIsValid, setPasswordIsValid] = useState(false);
    const [confirmPassword, setConfirmPassword] = useState(""); // ie: confirm new password
    const [confirmPasswordIsValid, setConfirmPasswordIsValid] = useState(false);

    //State only used if MFA is enabled
    const [otp, setOtp] = useState(""); //only required if MFA enaled
    const [otpIsValid, setOtpIsValid] = useState(false);//only required if MFA enaled
    const [otpWasSent, setOtpWasSent] = useState(false);//controls how often user may click on 'resend otp' button 

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");//success or error message

    // Form is valid when....
    const baseFieldsAreValid = (oldPasswordIsValid && passwordIsValid && confirmPasswordIsValid && infoMessage === "")
    const formIsValid = user.mfa ? (baseFieldsAreValid && otpIsValid) : baseFieldsAreValid //because otp is only necessary when mfa is enabled...
    const passwordsMatch = (password === confirmPassword)

    // Checks whether OTP was sent at least once (just used to change button text)
    const otpRequested = useRef(false)

    //Allow user to click on 'resend' OTP button again only 10 seconds after clicking it: avoid unnecessary api requests
    useEffect(() => {
        if (otpWasSent) {
            const timer = setTimeout(() => {
                setOtpWasSent(false); // Reset otpWasSent to false after 10 seconds
            }, 10000); // 10000ms = 10 seconds

            // Cleanup function to clear the timer if the component unmounts
            return () => clearTimeout(timer);
        }
    }, [otpWasSent]);

    //if a form error was shown, hide it when the user starts to correct the input shouldSend
    useEffect(() => {
        if (infoMessage !== "") {
            setInfoMessage("")
        }
    }, [oldPassword, password, confirmPassword, otp]);

    //API request that sends OTP per email to user
    const sendOtp = (e) => {
        if (e) { e.preventDefault(); }
        if (!otpRequested.current) { otpRequested.current = true }

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
            .catch(error => { console.error("Error in otp function.", error); })
            .finally(() => { dispatch(setLoader(false)); })
    };

    //Handle form submission: API call to change password
    const handleSubmit = (e) => {
        e.preventDefault();

        if (!formIsValid) { setInfoMessage("Check credentials."); return }
        if (!passwordsMatch) { setInfoMessage("Passwords do not match: New Password should be identical to Confirm Password."); return }
        if (oldPassword === password) { setInfoMessage("No changes detected to password: old and new passwords should be different."); return }

        let requestData = {
            "oldPassword": oldPassword,
            "newPassword": password,
            "pwChangeReason": "change", // means the user is logged in (different than in case of 'reset')
            "isFirstFactor": true, //even if user has mfa on, because api will validate all fields at once
            "userAgent": userAgent,
            "otp": otp
        }

        dispatch(setLoader(true));
        changePassword(requestData)
            .then(res => { if (isComponentMounted()) { setInfoMessage(res.message); } })
            .catch(error => { console.error("Error in change password function.", error); })
            .finally(() => { dispatch(setLoader(false)); })
    }


    return (
        <>
            <form onSubmit={handleSubmit} className="MAIN-form">

                <p>Please input your current password to proceed. </p>
                <p>Next, enter your desired new password and confirm it.</p>

                <HiddenUsername
                    username={user.email} />

                <InputPassword
                    autocomplete="current-password"
                    cssClass="MAIN-form-display-table"
                    labelText={"Current Password"}
                    password={oldPassword}
                    setPassword={setOldPassword}
                    setPasswordIsValid={setOldPasswordIsValid}
                />

                {oldPasswordIsValid && (
                    <>
                        <InputPassword
                            cssClass={"MAIN-form-display-table"}
                            labelText={"New Password"}
                            password={password}
                            setPassword={setPassword}
                            setPasswordIsValid={setPasswordIsValid}
                            simpleValidation={false}
                        />

                        <InputPassword
                            autocomplete={"confirm-password"}
                            cssClass={"MAIN-form-display-table"}
                            labelText={"Confirm Password"}
                            password={confirmPassword}
                            setPassword={setConfirmPassword}
                            setPasswordIsValid={setConfirmPasswordIsValid}
                        />
                    </>
                )}

                {baseFieldsAreValid && user.mfa && (
                    <>
                        <p>Since MFA is enabled, you need an OTP to confirm the change.</p>
                        <p>Please request the OTP, then copy and paste it below within 30 minutes.</p>
                        <p>Press "Submit" to change your password. The button will be enabled after all fields are valid.</p>

                        <InputOtp
                            otp={otp}
                            setOtp={setOtp}
                            setOtpIsValid={setOtpIsValid}
                            cssClass={"MAIN-form-display-table"}
                        />
                    </>
                )}

                {
                    infoMessage !== "" && (
                        < ErrorMessage message={infoMessage} ariaDescribedby="api-response-error" />
                    )
                }
                {
                    infoMessage === "" && (
                        <br />
                    )
                }

                <div className="Modal-BtnContainer">
                    <button disabled={!formIsValid} type="submit" className="Modal-ActionBtn">Change Password</button>
                    {user.mfa ? (
                        <button disabled={otpWasSent} onClick={(e) => { sendOtp(e) }} type="button">{otpRequested.current ? "Resend OTP" : "Send OTP"}</button>
                    ) : (
                        <button onClick={modalToggler} type="button">Cancel</button>
                    )
                    }
                </div>
            </form>
        </>
    );
};

ModalChangePassword.propTypes = {
    modalToggler: PropTypes.func.isRequired,
    user: PropTypes.shape({
        email: PropTypes.string.isRequired,
    }).isRequired,
};

export default ModalChangePassword;