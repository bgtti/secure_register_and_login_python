import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { PropTypes } from "prop-types";
import { INPUT_LENGTH } from "../../../../utils/constants";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { acctNameChange } from "../../../../config/apiHandler/authAccount/changeName.js"
import { acctEmailChange } from "../../../../config/apiHandler/authAccount/changeEmail.js";
import { nameValidation, emailValidation, passwordValidation } from "../../../../utils/validation.js"
import "./modalAccountDetailChange.css"

/**
 * This component is a modal used to change sensitive account information.
 * 
 * Used for: user's name, email, and password change
 * 
 * @todo improvement and pw change missing
 * 
 * @visibleName Modal Change Account Detail Change
 * @param {object} props
 * @param {string} props.action one of:'name', 'email', 'password.
 * @param {func} props.modalToggler opens/closes modal
 * @returns {React.ReactElement}
 */
function ModalAccountDetailChange(props) {
    const { action, modalToggler } = props;

    const userAgent = navigator.userAgent; //info to be passed on to BE

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();

    const actionLowerCase = action.toLowerCase()

    const user = useSelector((state) => state.user);

    let inputLengthMax = INPUT_LENGTH[actionLowerCase].maxValue;
    let inputLengthMin = INPUT_LENGTH[actionLowerCase].minValue;
    let inputType = actionLowerCase === "name" ? "text" : actionLowerCase;
    const inputAutoComplete = {
        name: "off",
        email: "email",
        password: "new-password",
    };

    const [formData, setFormData] = useState({
        inputField: "",
        confirmPassword: "", //used only if action is password: second input field value here
        isValid: false
    });

    const [formError, setFormError] = useState({
        occurred: true,
        show: false,
        message: "",
    });

    const [formSubmitted, setFormSubmitted] = useState(false);

    const formIsValid = !formError.occurred; // ==> TODO: NO

    const checkPwMatch = () => {
        if (formData.confirmPassword.length === 0) {
            return { response: false, message: "Please confirm password" }
        }
        let res;
        let pwMatch = (formData.inputField === formData.confirmPassword)
        pwMatch ?
            res = { response: true, message: "" } :
            res = { response: false, message: "Passwords do not match" }
        return res
    }

    const validateInput = (field) => {
        switch (actionLowerCase) {
            case "name":
                return nameValidation(formData.inputField)
            case "email":
                return emailValidation(formData.inputField)
            case "password":
                if (field === "confirmPassword") {
                    return checkPwMatch()
                } else {
                    return passwordValidation(formData.inputField)
                }
            default:
                return { response: false, message: "" }
        }
    }

    const validateForm = (showError, field = "inputField") => {
        let validity = validateInput(field);

        setFormError(() => ({
            occurred: validity.response,
            message: validity.message,
            show: showError
        }));

        if (actionLowerCase === "password") {
            let pwValid = passwordValidation(formData.inputField)
            let confirmPwisValid = checkPwMatch()
            let formIsValid = pwValid.response && confirmPwisValid.response

            setFormData((prevData) => ({
                ...prevData,
                isValid: formIsValid,
            }));
        } else {
            setFormData((prevData) => ({
                ...prevData,
                isValid: validity.response,
            }));
        }
    }


    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
        if ((name === "confirmPassword" && value.length >= inputLengthMin) || (name !== "confirmPassword" && value.length > 3)) {
            validateForm(true, name) //show error
        } else {
            validateForm(false, name)//dont show error
        }
    };

    const handleBlur = (e) => {
        validateForm(true, e.target.name)
    };

    const checkIfDataChanged = () => {
        if (actionLowerCase === "password") { return true } //password data is not checked
        return user[actionLowerCase] !== formData.inputField;
    }

    const handleSubmit = (e) => { //===> TODO: improve
        e.preventDefault();

        validateForm(true)
        let dataChanged = checkIfDataChanged()

        if (!formData.isValid || !dataChanged) {
            console.log('not submitting'); //===> TODO: handle
        }

        dispatch(setLoader(true));

        const errorMsg = "An error occurred. Please close modal and try again."

        const handleResponse = (response, successMessage) => {
            if (isComponentMounted()) {
                let errorInfo = errorMsg
                if (!response.success && response.info) { errorInfo = response.info }
                setFormError(() => ({
                    occurred: response.success,
                    message: (response.success ? successMessage : errorInfo),
                    show: true
                }));
            }
        };

        const handleError = (error) => {
            console.warn("clickHandler in modal encountered an error", error);
        };

        const handleFinally = () => {
            setFormSubmitted(true)
            dispatch(setLoader(false));
        };

        let requestAction;
        let responseActionMessage;

        switch (actionLowerCase) {
            case "name":
                requestAction = function () { return acctNameChange(formData.inputField) };
                responseActionMessage = "Name changed successfully!";
                break
            case "email":
                requestAction = function () { return acctEmailChange(formData.inputField) }; //===> TODO: missing
                responseActionMessage = "Please check your email to confirm the change.";
                break
            case "password":
                requestAction = function () { return console.log("pw") }; //===> TODO: missing
                responseActionMessage = "Please check your email to confirm the change.";
                break
            default:
                requestAction = function () { return console.error("Wrong action input in ModalChangeAcct.") };
                responseActionMessage = "An error occurred: action input invalid.";
        }

        try {
            requestAction()
                .then(response => handleResponse(response, responseActionMessage))
                .catch(error => { handleError(error) })
                .finally(handleFinally);
        } catch (error) {
            console.error("Error in ModalChangeAcct", error);
            dispatch(setLoader(false));
        }
    };

    return (
        <>
            <form onSubmit={handleSubmit} className="ModalAccountDetailChange MAIN-form">
                {
                    actionLowerCase === "password" && (
                        <>
                            <p>Note: two-step verification required.</p>
                            <p>You will receive a confirmation email.</p>
                        </>
                    )
                }
                {
                    actionLowerCase === "email" && (
                        <>
                            <p>Note: three-step verification required.</p>
                            <p>Check your email after clicking "save".</p>
                        </>
                    )
                }
                {/* Hidden field for username: helps password managers associate info. (Avoids browser warning) */}

                {
                    actionLowerCase !== "email" && (
                        <div className="MAIN-display-none">
                            <label htmlFor="username">Username</label>
                            <input
                                autoComplete="username"
                                id="username"
                                name="username"
                                readOnly
                                type="text"
                                value={user.email}
                            />
                        </div>
                    )
                }

                {
                    actionLowerCase !== "password" &&
                    (<p >
                        Account {actionLowerCase}: {user[actionLowerCase]}
                    </p>)
                }

                <div className="MAIN-form-display-table">
                    <label htmlFor="inputField">New {actionLowerCase}:<span className="MAIN-form-star">*</span></label>
                    <input
                        aria-invalid={formError.occurred}
                        aria-describedby={`${actionLowerCase}-error`}
                        autoComplete={inputAutoComplete[actionLowerCase]}
                        id="inputField"
                        maxLength={inputLengthMax}
                        minLength={inputLengthMin}
                        name="inputField"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        required
                        type={inputType}
                        value={formData.inputField}
                    />
                </div>
                {
                    actionLowerCase === "password" && (
                        <div className="MAIN-form-display-table">
                            <label htmlFor="confirmPassword">Confirm password:<span className="MAIN-form-star">*</span></label>
                            <input
                                aria-invalid={formError.occurred}
                                aria-describedby="confirm-password-error"
                                autoComplete="new-password"
                                id="confirmPassword"
                                maxLength={inputLengthMax}
                                minLength={inputLengthMin}
                                name="confirmPassword"
                                onBlur={handleBlur}
                                onChange={handleChange}
                                required
                                type="password"
                                value={formData.confirmPassword}
                            />
                        </div>
                    )
                }
                {
                    formError.message !== "" && formError.show && (
                        <p className="MAIN-error-message" id="error-message" aria-live="assertive">
                            <i>{formError.message}</i>
                        </p>
                    )
                }
                <br />

                <div className="ModalAccountDetailChange-BtnContainer">
                    <button disabled={formSubmitted} type="submit" className="ModalAccountDetailChange-ActionBtn">Save</button>
                    <button onClick={modalToggler}>{formSubmitted ? "Close" : "Cancel"}</button>
                </div>
            </form>
        </>
    );
};

ModalAccountDetailChange.propTypes = {
    action: PropTypes.oneOf(['name'.toLowerCase(), 'email'.toLowerCase(), 'password'.toLowerCase()]),
    modalToggler: PropTypes.func.isRequired
};

export default ModalAccountDetailChange;