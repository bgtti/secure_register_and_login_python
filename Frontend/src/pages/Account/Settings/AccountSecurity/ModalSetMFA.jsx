import { useEffect, useState, useRef } from "react";
import { useDispatch } from "react-redux";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { setMfa } from "../../../../config/apiHandler/authSecurity/setMfa.js"
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage.jsx";
import Tooltip from "../../../../components/Tooltip/Tooltip"
import HiddenUsername from "../../../../components/Auth/HiddenUsername.jsx"
import InputPassword from "../../../../components/Auth/InputPassword.jsx";

/**
 * This component is a modal used to enable MFA
 * 
 * @param {object} props
 * @param {func} props.modalToggler opens/closes modal
 * @param {object} props.user 
 * @param {string} props.user.email
 * @returns {React.ReactElement}
 */
function ModalSetMFA(props) {
    const { modalToggler, user } = props;

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();

    const userAgent = navigator.userAgent; //info to be passed on to BE

    const [password, setPassword] = useState("");
    const [passwordIsValid, setPasswordIsValid] = useState(false);

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");
    const [apiCallSuccess, setApiCallSuccess] = useState(false);

    // Form is valid when all fields are valid and api call did not return error
    const formIsValid = (passwordIsValid && infoMessage === "")

    // Action btn
    const btnDisabled = (!passwordIsValid || infoMessage !== "" || apiCallSuccess)

    //if a form error was shown, hide it when the user starts to correct the input
    useEffect(() => {
        if (infoMessage !== "") {
            setInfoMessage("")
        }
    }, [password]);


    const handleSubmit = (e) => {
        e.preventDefault();

        if (!formIsValid) {
            setInfoMessage("Check your credentials.")
            return
        }

        const requestData = {
            password: password,
            userAgent: userAgent,
            enableMfa: true
        }

        dispatch(setLoader(true));

        const handleResponse = (response) => {
            if (isComponentMounted()) {
                setInfoMessage(response.message)
                if (response.response) { setApiCallSuccess(true) }
            }
        };

        const handleError = (error) => {
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
                <p>Multi-factor authentication (MFA) increases the security of your account.</p>
                <p>You will need to provide an <Tooltip text="OTP" message="OTP = one-time password. It is sent to you by email." /> along with your password to sign in.</p>
                <p>It is <b>highly</b> recommended that you set up a recovery email when enabling MFA
                    <Tooltip text="." message="In case you lose your password and/or access to your email account, a recovery email can help you regain access." />
                </p>
            </div>

            <br />

            <form onSubmit={handleSubmit} className="MAIN-form">

                <div>
                    <p>Confirm the password you use to log into your account before proceeding.</p>
                </div>

                <br />

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

                <br />

                <div className="Modal-BtnContainer">

                    <button
                        onClick={modalToggler}
                        type="button">
                        Cancel
                    </button>
                    <button
                        className="Modal-ActionBtn"
                        disabled={btnDisabled}
                        type="submit">
                        Enable MFA
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

ModalSetMFA.propTypes = {
    modalToggler: PropTypes.func.isRequired,
    user: PropTypes.shape({
        email: PropTypes.string.isRequired,
    }).isRequired,
};

export default ModalSetMFA;