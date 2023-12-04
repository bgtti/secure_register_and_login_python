import { useState } from "react";
import { emailValidation, passwordValidationForLogin } from "../../utils/validation";
import { INPUT_LENGTH } from "../../utils/constants";
import "./login.css"

function LogIn() {
    const [formData, setFormData] = useState({
        email: "",
        emailIsValid: { response: false, message: "" },
        password: "",
        passwordIsValid: { response: false, message: "" },
    });

    const formIsValid = (formData.emailIsValid.response && formData.passwordIsValid.response);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleBlur = (e) => {
        const { name, value } = e.target;
        if (name === "email") {
            setFormData((prevData) => ({
                ...prevData,
                emailIsValid: emailValidation(value),
            }));
        } else {
            if (name === "password") {
                setFormData((prevData) => ({
                    ...prevData,
                    passwordIsValid: passwordValidationForLogin(value),
                }));
            };
        };
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (formIsValid) {
            // Add your form submission logic here, for example, send data to a server
            console.log('Form submitted:', formData);
            // Loader should start till server response
            // Server responds with success: log in user
            // Server responds with failure, show error page
        }
    };

    return (
        <div className="LogIn">
            <h2>Log In</h2>
            <form onSubmit={handleSubmit} className='MAIN-form'>
                <div className="MAIN-form-display-table">
                    <label htmlFor="email">Email: </label>
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
                    <label htmlFor="password">Password: </label>
                    <input
                        aria-invalid={formData.passwordIsValid.message === "" ? "false" : "true"}
                        aria-describedby="password-error"
                        autoComplete="current-password"
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

                <button disabled={!formIsValid} type="submit">Log in</button>
            </form>
            <p className="MAIN-info-paragraph">
                Don't have an account yet? <a href="/signup">Sign up</a> instead.
            </p>
        </div>
    );
}

export default LogIn;