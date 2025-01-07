import { useEffect, useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { changeEmail } from "../../../../config/apiHandler/authCredChange/changeEmail.js";
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage.jsx"
import HiddenUsername from "../../../../components/Auth/HiddenUsername.jsx";
import InputEmail from "../../../../components/Auth/InputEmail.jsx";
import InputPassword from "../../../../components/Auth/InputPassword";

/**
 * This component is a modal used to change the user's account email address.
 * 
 * How a user can change the email:
 * 1) User will be requested to input their password
 * 2) User will be requested to input the desired new email address
 * 3) The api request will then act according to the verification status:
 *      - If the user is not verified, the new email will just be saved
 *      - If the user is verified: the backend will initiate the change request by sending the user two confirmation emails: one to the new and another to the new email address. The process on the Front End then continues in pages > Auth > ChangeEmail
 * 
 * Rules:
 * - New email should not be the same as old email
 * - New email should not be the same as recovery email (just checked in BE) 
 * - New email should not already exist in the DB as an account email (just checked in BE) 
 * 
 * Reason for changing email differently in non-verified accounts: Since this app designed email verification as not compulsory, it is possible a user mistyped an email address or used one that does not exist. If this is the case, the user would never receive the verification code. 
 * If you want to change this logic, be sure to require verification upon account signup.
 * 
 * @param {object} props
 * @param {func} props.modalToggler // opens/closes modal
 * @param {object} props.user // the user as in the redux store
 * @param {string} props.user.email
 * @returns {React.ReactElement}
 */
function ModalChangeEmail(props) {
    const { modalToggler, user } = props;

    const userAgent = navigator.userAgent; //info to be passed on to BE

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();

    // Used for actual fields
    const [email, setEmail] = useState(""); //ie: new email
    const [emailIsValid, setEmailIsValid] = useState(false);
    const [password, setPassword] = useState(""); // to check current password
    const [passwordIsValid, setPasswordIsValid] = useState(false);

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");//success or error message

    //Form valid when..
    const formIsValid = emailIsValid && passwordIsValid && infoMessage === ""

    //Form was submitted successfully (status 200 or 202) button to submit will be disabled
    const formSubmitted = useRef(false)

    //if a form error was shown, hide it when the user starts to correct the input shouldSend
    useEffect(() => {
        if (infoMessage !== "") {
            setInfoMessage("")
        }
    }, [password, email]);

    //Handle form submission: API call to change email
    const handleSubmit = (e) => {
        e.preventDefault();

        if (!formIsValid) { setInfoMessage("Check credentials."); return }
        if (user.email === email) { setInfoMessage("No changes detected to email: current and new email addresses should be different."); return }
        if (formSubmitted.current === true) { setInfoMessage("Close this modal to request another email change."); return }

        let requestData = {
            "password": password,
            "newEmail": email,
            "userAgent": userAgent,
        }

        dispatch(setLoader(true));
        changeEmail(requestData)
            .then(res => {
                if (isComponentMounted()) {
                    setInfoMessage(res.message);
                    if (res.status === 200 || res.status === 202) { formSubmitted.current = true }
                }
            })
            .catch(error => { console.error("Error in change email function.", error); })
            .finally(() => { dispatch(setLoader(false)); })
    }


    return (
        <>
            <form onSubmit={handleSubmit} className="MAIN-form">

                <p><b>Account email: {user.email}</b></p>
                <div>
                    <p>Please input your current password to proceed. </p>
                    <p>Next, enter your desired new email.</p>
                    <p>Press 'Change Email' to {user.acctVerified ? "start the process" : "change your email"}.</p>
                </div>

                {
                    user.acctVerified && (
                        <div>
                            <p>You will then receive two confirmation emails:</p>
                            <p>- One sent to your currrent email address</p>
                            <p>- Another sent to your new email address</p>
                        </div>
                    )
                }

                <HiddenUsername
                    username={user.email} />

                <InputPassword
                    autocomplete="current-password"
                    cssClass="MAIN-form-display-table"
                    labelText={"Current Password"}
                    password={password}
                    setPassword={setPassword}
                    setPasswordIsValid={setPasswordIsValid}
                />

                {passwordIsValid && (
                    <InputEmail
                        cssClass={"MAIN-form-display-table"}
                        email={email}
                        labelText={"New Email"}
                        setEmail={setEmail}
                        setEmailIsValid={setEmailIsValid}
                    />
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
                    <button disabled={!formIsValid || formSubmitted.current} type="submit" className="Modal-ActionBtn">Change Email</button>
                    <button onClick={modalToggler} type="button">Cancel</button>
                </div>

            </form>
        </>
    );
};

ModalChangeEmail.propTypes = {
    modalToggler: PropTypes.func.isRequired,
    user: PropTypes.shape({
        email: PropTypes.string.isRequired,
    }).isRequired,
};

export default ModalChangeEmail;