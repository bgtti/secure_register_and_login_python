import { useState } from "react";
import { PropTypes } from "prop-types";
import { INPUT_LENGTH } from "../../../utils/constants";
import { nameValidation, emailValidation, passwordValidation } from "../../../utils/validation";
import "./modalChangeAccount.css"

/**
 * This component is a modal used to change sensitive account informatiom.
 * 
 * @visibleName Modal Change Account Info
 * @param {object} props
 * @param {string} props.action one of:'name', 'email', 'password.
 * @param {func} props.modalToggler opens/closes modal
 * @returns {React.ReactElement}
 */
function ModalChangeAccount(props) {
    const { action, modalToggler } = props;

    const actionLowerCase = action.toLowerCase()

    let inputUsername = "john@example.com" //===> TODO
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
        inputIsValid: { response: false, message: "" }
    });

    const validateForm = (onChangeAction = true) => {
        let isValid;
        if (onChangeAction && (formData.inputField.length < inputLengthMin)) {
            isValid = { response: false, message: "" }
        } else {
            switch (actionLowerCase) {
                case "name":
                    isValid = nameValidation(formData.inputField)
                    break;
                case "email":
                    isValid = emailValidation(formData.inputField)
                    break;
                case "password":
                    if (formData.confirmPassword === "") {
                        isValid = { response: false, message: "" }
                    } else {
                        let pwMatch = (formData.inputField === formData.confirmPassword)
                        pwMatch ?
                            isValid = passwordValidation(formData.inputField) :
                            isValid = { response: false, message: "Passwords do not match" }
                    }
                    break;
                default:
                    isValid = { response: false, message: "Oops something went wrong" }
            }
        }

        setFormData((prevData) => ({
            ...prevData,
            inputIsValid: isValid,
        }));

        return
    }

    const formIsValid = formData.inputIsValid.response;


    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
        actionLowerCase === "password"
        validateForm()
    };

    const handleBlur = () => {
        validateForm(false)
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        //===> TODO
        validateForm(false)
        if (formIsValid) {
            console.log('Form submitted:', formData);
        }
    };

    return (
        <>
            <form onSubmit={handleSubmit} className="ModalChangeAccount MAIN-form">
                {
                    actionLowerCase !== "name" && (
                        <>
                            <p>Note: two-step verification required.</p>
                            <br />
                        </>
                    )
                }
                {/* Hidden field for username: helps password managers associate info. (Avoids browser warning) */}

                {
                    actionLowerCase !== "email" && (
                        <div class="MAIN-display-none">
                            <label for="username">Username</label>
                            <input
                                autoComplete="username"
                                id="username"
                                name="username"
                                readOnly
                                type="text"
                                value={inputUsername}
                            />
                        </div>
                    )
                }

                <div className="MAIN-form-display-table">
                    <label htmlFor="inputField">New {actionLowerCase}:<span className="MAIN-form-star">*</span></label>
                    <input
                        aria-invalid={formData.inputIsValid.message === "" ? "false" : "true"}
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
                                aria-invalid={formData.inputIsValid.message === "" ? "false" : "true"}
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
                    formData.inputIsValid.message !== "" && (
                        <p className="MAIN-error-message" id="error-message" aria-live="assertive">
                            <i>{formData.inputIsValid.message}</i>
                        </p>
                    )
                }
                <br />

                <div className="ModalChangeAccount-BtnContainer">
                    <button disabled={!formIsValid} type="submit" className="ModalChangeAccount-ActionBtn">Save</button>
                    <button onClick={modalToggler}>Cancel</button>
                </div>
            </form>
        </>
    );
};

ModalChangeAccount.propTypes = {
    action: PropTypes.oneOf(['name'.toLowerCase(), 'email'.toLowerCase(), 'password'.toLowerCase()]),
    modalToggler: PropTypes.func.isRequired
};

export default ModalChangeAccount;