import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import Honeypot from "../../components/Honeypot/Honeypot";
import { setLoader } from "../../redux/loader/loaderSlice"
import { signupUser } from "../../config/apiHandler/signup"
import { nameValidation, emailValidation, passwordValidation } from "../../utils/validation";
import { INPUT_LENGTH } from "../../utils/constants";
import "./signup.css"

/**
 * Component returns Sign-up form
 * 
 * The form calls the apiHandler in signup.js for authentication.
 * Successfull user authentication will re-direct the user to the dashboard.
 * Unsuccessful authentication will lead to error. Some errors will have feedback shown in this component, while others will lead to a re-direct to the error page. Check the axios configurations in the config folder to learn more about this behaviour.
 * 
 * @visibleName SignUp
 * @returns {React.ReactElement}
 * 
 */
function SignUp() {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    // Used for honeypot
    const [honeypotValue, setHoneypotValue] = useState("");

    const [formData, setFormData] = useState({
        name: "",
        nameIsValid: { response: false, message: "" },
        email: "",
        emailIsValid: { response: false, message: "" },
        password: "",
        passwordIsValid: { response: false, message: "" },
        confirmPassword: "",
        confirmPasswordIsValid: { response: false, message: "" },
        credentialsAreValid: { response: true, message: "" },
    });

    const formIsValid = (formData.nameIsValid.response && formData.emailIsValid.response && formData.passwordIsValid.response && formData.confirmPasswordIsValid.response && formData.credentialsAreValid.response);

    //useEffect used to enable button as user is typing the password: smoother mouseless navigation
    useEffect(() => {
        if (formData.confirmPassword.length >= INPUT_LENGTH.password.minValue) {
            setFormData((prevData) => ({
                ...prevData,
                confirmPasswordIsValid: { response: true, message: "" }
            }));
        }
    }, [formData.confirmPassword]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
        //Ensures that, if an error message had appeared before, that it disappears as user corrects input
        if (!formData.credentialsAreValid.response) {
            setFormData((prevData) => ({
                ...prevData,
                credentialsAreValid: { response: true, message: "" },
            }));
        }
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
            const requestData = {
                name: formData.name,
                email: formData.email,
                password: formData.password,
                honeypot: honeypotValue
            }
            dispatch(setLoader(true))
            signupUser(requestData)
                .then(res => {
                    if (res.response) {
                        navigate("/dashboard");
                    } else {
                        setFormData((prevData) => ({
                            ...prevData,
                            credentialsAreValid: {
                                response: res.response,
                                message: res.message
                            },
                        }));
                    }
                })
                .catch(error => {
                    console.error("Error in signup function.", error);
                })
                .finally(() => {
                    dispatch(setLoader(false));
                })
        }
    };

    return (
        <div className="SignUp">
            <Helmet>
                <title>Sign up</title>
                <meta name="description" content="Sign up" />
            </Helmet>
            <h2>Sign Up</h2>
            <form onSubmit={handleSubmit} className='MAIN-form'>

                <div className="MAIN-form-display-table">
                    <label htmlFor="name">Name:<span className="MAIN-form-star"> *</span></label>
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
                    <label htmlFor="email">Email:<span className="MAIN-form-star"> *</span></label>
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
                    <label htmlFor="password">Password:<span className="MAIN-form-star"> *</span></label>
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
                    <label htmlFor="confirmPassword">Confirm Password:<span className="MAIN-form-star"> *</span></label>
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

                <Honeypot setHoneypotValue={setHoneypotValue} />

                <button disabled={!formIsValid} type="submit">Create account</button>

                {
                    formData.credentialsAreValid.message !== "" && (
                        <p className="MAIN-error-message" id="password-error">
                            <i>{formData.credentialsAreValid.message}</i>
                        </p>
                    )
                }
            </form>

            {
                formData.credentialsAreValid.message !== "" && (
                    <div className="SignUp-errorHints">
                        <h3>What could have gone wrong...</h3>
                        <p><b>Check your password</b> and make sure it has 8 or more characters and that it is not easy to guess.</p>
                        <p>Passwords commonly used on the web might be rejected, such as "12345678". Tip: use a password manager or come up with a long sentence you can remember later.</p>
                        <p><b>Check for spaces and invalid characters</b> such as spaces in the email field. Emails also contain the @ character. Make sure you have not mixed up the name and email fields by mistake.</p>
                        <p><b>Check your inbox</b> - if you already have an account, you should have received an email to help you log-in.</p>
                        <p><b>Refresh the page</b> and try again to see if the problem resolves.</p>
                        <p><b>If none of the above works</b> let us know. The error could indicate a problem on our end.</p>
                    </div>
                )
            }

            <p className="MAIN-info-paragraph">
                Already have an account? <a href="/login">Log in</a> instead.
            </p>
        </div>
    );
}

export default SignUp;