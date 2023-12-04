import { useState } from "react";
import { nameValidation, emailValidation, passwordValidation } from "../../utils/validation";
import { INPUT_LENGTH } from "../../utils/constants";
import "./signup.css"

function SignUp() {
    const [formData, setFormData] = useState({
        name: "",
        nameIsValid: { response: false, message: "" },
        email: "",
        emailIsValid: { response: false, message: "" },
        password: "",
        passwordIsValid: { response: false, message: "" },
        confirmPassword: "",
        confirmPasswordIsValid: { response: false, message: "" },
    });

    const formIsValid = (formData.nameIsValid.response && formData.emailIsValid.response && formData.passwordIsValid.response && formData.confirmPasswordIsValid.response);

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
            // Add your form submission logic here, for example, send data to a server
            console.log('Form submitted:', formData);
            // Loader should start till server response
            // Server responds with success: decide whether to log user in or verify email
            // Server responds with failure, show error page
        }
    };

    return (
        <div className="SignUp">
            <h2>Sign Up</h2>
            <form onSubmit={handleSubmit} className='MAIN-form'>
                <div className="MAIN-form-display-table">
                    <label htmlFor="name">Name:<span className="SignUp-star">*</span></label>
                    <input
                        aria-invalid={formData.nameIsValid.message === "" ? "false" : "true"}
                        aria-describedby="name-error"
                        autoComplete="name"
                        id="name"
                        maxLength={`${INPUT_LENGTH.name.maxValue}`}
                        minLength={`${INPUT_LENGTH.name.minValue}`}
                        name="name"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        required
                        type="text"
                        value={formData.name}
                    />
                </div>
                {
                    formData.nameIsValid.message !== "" && (
                        <p className="MAIN-error-message" id="name-error">
                            <i>{formData.nameIsValid.message}</i>
                        </p>
                    )
                }
                <div className="MAIN-form-display-table">
                    <label htmlFor="email">Email:<span className="SignUp-star">*</span></label>
                    <input
                        aria-invalid={formData.emailIsValid.message === "" ? "false" : "true"}
                        aria-describedby="email-error"
                        autoComplete="email"
                        id="email"
                        maxLength={`${INPUT_LENGTH.email.maxValue}`}
                        minLength={`${INPUT_LENGTH.email.minValue}`}
                        name="email"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        required
                        type="text"
                        value={formData.email}
                    />
                </div>
                {
                    formData.emailIsValid.message !== "" && (
                        <p className="MAIN-error-message" id="email-error">
                            <i>{formData.emailIsValid.message}</i>
                        </p>
                    )
                }
                <div className="MAIN-form-display-table">
                    <label htmlFor="password">Password:<span className="SignUp-star">*</span></label>
                    <input
                        aria-invalid={formData.passwordIsValid.message === "" ? "false" : "true"}
                        aria-describedby="password-error"
                        autoComplete="new-password"
                        id="password"
                        maxLength={`${INPUT_LENGTH.password.maxValue}`}
                        minLength={`${INPUT_LENGTH.password.minValue}`}
                        name="password"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        required
                        type="password"
                        value={formData.password}
                    />
                </div>
                {
                    formData.passwordIsValid.message !== "" && (
                        <p className="MAIN-error-message" id="password-error">
                            <i>{formData.passwordIsValid.message}</i>
                        </p>
                    )
                }
                <div className="MAIN-form-display-table">
                    <label htmlFor="confirmPassword">Confirm Password:<span className="SignUp-star">*</span></label>
                    <input
                        aria-invalid={formData.confirmPasswordIsValid.message === "" ? "false" : "true"}
                        aria-describedby="confirm-password-error"
                        autoComplete="new-password"
                        id="confirmPassword"
                        maxLength={`${INPUT_LENGTH.password.maxValue}`}
                        minLength={`${INPUT_LENGTH.password.minValue}`}
                        name="confirmPassword"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        required
                        type="password"
                        value={formData.confirmPassword}
                    />
                </div>
                {
                    formData.confirmPasswordIsValid.message !== "" && (
                        <p className="MAIN-error-message" id="confirm-password-error">
                            <i>{formData.confirmPasswordIsValid.message}</i>
                        </p>
                    )
                }
                <button disabled={!formIsValid} type="submit">Create account</button>
            </form>
            <p className="MAIN-info-paragraph">
                Already have an account? <a href="/login">Log in</a> instead.
            </p>
        </div>
    );
}

export default SignUp;