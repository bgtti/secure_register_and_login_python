import { useState } from "react";
import { PropTypes } from "prop-types";
import { INPUT_LENGTH } from "../../../utils/constants";
import { nameValidation, emailValidation, passwordValidation } from "../../../utils/validation";
import "./modalChangeAccount.css"

function ModalChangeAccount(props) {
    const { action, modalToggler } = props;

    const actionLowerCase = action.toLowerCase()
    const actionCapitalized = actionLowerCase.charAt(0).toUpperCase() + actionLowerCase.slice(1);

    const inputLengthMax = actionLowerCase === "email" ? INPUT_LENGTH.email.maxValue : INPUT_LENGTH.password.maxValue;
    const inputLengthMin = actionLowerCase === "email" ? INPUT_LENGTH.email.minValue : INPUT_LENGTH.password.minValue;

    const [formData, setFormData] = useState({
        email: "",
        emailIsValid: { response: false, message: "" },
        password: "",
        passwordIsValid: { response: false, message: "" },
        confirmPassword: "",
        confirmPasswordIsValid: { response: false, message: "" },
    });

    const formIsValid = actionLowerCase === "email" ?
        (formData.emailIsValid.response) :
        (formData.passwordIsValid.response && formData.confirmPasswordIsValid.response);


    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };
    const handleBlur = (e) => {
        const { name, value } = e.target;
        if (name === "name") {
            setFormData((prevData) => ({
                ...prevData,
                nameIsValid: nameValidation(value),
            }));
        } else if (name === "email") {
            setFormData((prevData) => ({
                ...prevData,
                emailIsValid: emailValidation(value),
            }));
        } else {
            const checkIfPasswordsMatch = (firstPwd, secondPwd) => {
                const isPasswordRepeated = (firstPwd === secondPwd);
                const message = isPasswordRepeated ? "" : "Passwords do not match."
                setFormData((prevData) => ({
                    ...prevData,
                    confirmPasswordIsValid: { response: isPasswordRepeated, message: message },
                }));
            };
            if (name === "password") {
                setFormData((prevData) => ({
                    ...prevData,
                    passwordIsValid: passwordValidation(value),
                }));
                if (formData.confirmPasswordIsValid.response) {
                    checkIfPasswordsMatch(value, formData.confirmPassword);
                }
            } else {
                checkIfPasswordsMatch(formData.password, value);
            };
        };
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (formIsValid) {
            console.log('Form submitted:', formData);
        }
    };

    return (
        <>
            <form onSubmit={handleSubmit} className="ModalChangeAccount MAIN-form">
                <p>Note: two-step verification required.</p>
                <br />
                <div className="MAIN-form-display-table">
                    <label htmlFor={actionLowerCase}>New {actionLowerCase}:<span className="SignUp-star">*</span></label>
                    <input
                        aria-invalid={formData.emailIsValid.message === "" ? "false" : "true"}
                        aria-describedby={`${actionLowerCase}-error`}
                        autoComplete={actionLowerCase === "email" ? "email" : "new-password"}
                        id={actionLowerCase}
                        maxLength={inputLengthMax}
                        minLength={inputLengthMin}
                        name={actionLowerCase}
                        onBlur={handleBlur}
                        onChange={handleChange}
                        required
                        type={actionLowerCase}
                        value={actionLowerCase === "email" ? formData.email : formData.password}
                    />
                </div>
                {
                    actionLowerCase === "email" && formData.emailIsValid.message !== "" && (
                        <p className="MAIN-error-message" id="email-error">
                            <i>{formData.emailIsValid.message}</i>
                        </p>
                    )
                }
                {
                    actionLowerCase === "password" && formData.passwordIsValid.message !== "" && (
                        <p className="MAIN-error-message" id="password-error">
                            <i>{formData.passwordIsValid.message}</i>
                        </p>
                    )
                }
                {
                    actionLowerCase === "password" && (
                        <div className="MAIN-form-display-table">
                            <label htmlFor="confirmPassword">Confirm Password:<span className="SignUp-star">*</span></label>
                            <input
                                aria-invalid={formData.confirmPasswordIsValid.message === "" ? "false" : "true"}
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
                    actionLowerCase === "password" && formData.confirmPasswordIsValid.message !== "" && (
                        <p className="MAIN-error-message" id="confirm-password-error">
                            <i>{formData.confirmPasswordIsValid.message}</i>
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
    action: PropTypes.oneOf(['email'.toLowerCase(), 'account'.toLowerCase()]),
    modalToggler: PropTypes.func.isRequired
};

export default ModalChangeAccount;