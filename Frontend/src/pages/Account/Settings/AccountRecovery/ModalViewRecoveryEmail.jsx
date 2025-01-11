import { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { PropTypes } from "prop-types";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { getRecoveryEmail } from "../../../../config/apiHandler/authRecovery/getRecoveryEmail.js"
import ErrorMessage from "../../../../components/ErrorMessage/ErrorMessage";
import InputPassword from "../../../../components/Auth/InputPassword.jsx";
import HiddenUsername from "../../../../components/Auth/HiddenUsername.jsx"

/**
 * This component is a modal used to fetch and show the user's recovery email address.
 * 
 * @param {object} props
 * @param {func} props.modalToggler opens/closes modal
 * @param {object} props.user 
 * @param {string} props.user.email 
 * @returns {React.ReactElement}
 */
function ModalViewRecoveryEmail(props) {
    const { modalToggler, user } = props;

    const dispatch = useDispatch();

    const isComponentMounted = useIsComponentMounted();

    const userAgent = navigator.userAgent; //info to be passed on to BE

    // State for input components
    const [recoveryEmail, setRecoveryEmail] = useState("");
    const [password, setPassword] = useState("");
    const [passwordIsValid, setPasswordIsValid] = useState(false);

    // State set by api call
    const [infoMessage, setInfoMessage] = useState("");
    const [formSubmitted, setFormSubmitted] = useState(false);

    // Form is valid when all fields are valid and api call did not return error
    const formIsValid = (passwordIsValid && infoMessage === "")

    //if a form error was shown, hide it when the user starts to correct the input
    useEffect(() => {
        if (infoMessage !== "") {
            setInfoMessage("")
        }
    }, [password]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (formIsValid) {
            const requestData = {
                password: password,
                userAgent: userAgent
            }
            dispatch(setLoader(true))
            getRecoveryEmail(requestData)
                .then(res => {
                    if (isComponentMounted()) {
                        if (res.response) {
                            setRecoveryEmail(res.message);
                            setFormSubmitted(true);
                        }
                        else { setInfoMessage(res.message); }
                    }
                })
                .catch(error => {
                    console.error("Error in fetching recovery email.", error);
                })
                .finally(() => {
                    dispatch(setLoader(false));
                })
        }
    };

    return (
        <>
            <form onSubmit={handleSubmit} className="ModalAccountDetailChange MAIN-form">
                {
                    !formSubmitted && (
                        <>
                            <div>
                                <p>Recovery email addresses are considered sensitive information.</p>
                                <p>Please type your password to proceed. </p>
                            </div>

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

                {
                    formSubmitted && (
                        <>
                            <br />
                            <div>
                                <p>The following email address is set as your recovery email:</p>
                                <br />
                                <p><b>{recoveryEmail}</b></p>
                                <br />
                            </div>
                        </>
                    )
                }

                <div className="Modal-BtnContainer">

                    <button
                        className="Modal-ActionBtn"
                        disabled={!formIsValid || formSubmitted}
                        type="submit">
                        View
                    </button>

                    <button
                        onClick={modalToggler}>
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

ModalViewRecoveryEmail.propTypes = {
    modalToggler: PropTypes.func.isRequired,
    user: PropTypes.shape({
        email: PropTypes.string.isRequired
    }).isRequired,
    acctRecovery: PropTypes.shape({
        recoveryEmailAdded: PropTypes.bool.isRequired
    }).isRequired,
};

export default ModalViewRecoveryEmail;