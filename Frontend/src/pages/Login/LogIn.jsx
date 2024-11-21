import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { setLoader } from "../../redux/loader/loaderSlice"
import { loginUser } from "../../config/apiHandler/login"
import { emailValidation, passwordValidationForLogin } from "../../utils/validation";
import { INPUT_LENGTH } from "../../utils/constants";
import Honeypot from "../../components/Honeypot/Honeypot";
import "./login.css"

/**
 * Component returns Log-in form
 * 
 * The form calls the apiHandler in login.js for authentication.
 * Successfull user authentication will re-direct the user to the dashboard.
 * Unsuccessful authentication will lead to error. Some errors will have feedback shown in this component, while others will lead to a re-direct to the error page. Check the axios configurations in the config folder to learn more about this behaviour.
 * 
 * @visibleName LogIn
 * @returns {React.ReactElement}
 * 
 * @todo When user inputs the wrong credentials 3+ times, a timer should be shown to reflect the temporary login block time. Check the login route( user model in the backend to confirm the temporary block time).
 */
function LogIn() {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    // Used for honeypot
    const [honeypotValue, setHoneypotValue] = useState("");

    // Used for actual fields
    const [formData, setFormData] = useState({
        email: "",
        emailIsValid: { response: false, message: "" },
        password: "",
        passwordIsValid: { response: false, message: "" },
        credentialsAreValid: { response: true, message: "" },
    });

    const formIsValid = (formData.emailIsValid.response && formData.passwordIsValid.response && formData.credentialsAreValid.response);

    //useEffect used to enable button as user is typing the password: smoother mouseless navigation
    useEffect(() => {
        if (formData.password.length >= INPUT_LENGTH.password.minValue) {
            setFormData((prevData) => ({
                ...prevData,
                passwordIsValid: { response: true, message: "" }
            }));
        }
    }, [formData.password]);

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
            const requestData = {
                email: formData.email,
                password: formData.password,
                honeyPot: honeypotValue
            }
            dispatch(setLoader(true))
            loginUser(requestData)
                .then(res => {
                    if (res.response) {
                        navigate("/userAccount");
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
                    console.error("Error in login function.", error);
                })
                .finally(() => {
                    dispatch(setLoader(false));
                })
        }
    };

    return (
        <div className="LogIn">
            <Helmet>
                <title>Log in</title>
                <meta name="description" content="Log in" />
            </Helmet>
            <h2>Log In</h2>
            <form onSubmit={handleSubmit} className='MAIN-form'>
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

                <Honeypot setHoneypotValue={setHoneypotValue} />

                <button disabled={!formIsValid} type="submit">Log in</button>

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
                    <div className="LogIn-errorHints">
                        <h3>What could have gone wrong...</h3>
                        <p><b>Check your credentials</b> to make sure you have the correct email/password combination. The email should not contain empty spaces.</p>
                        <p><b>Multiple failed log-in attemps</b> will block you from logging in temporarily. You should wait a couple of mintes after 3 failed attempts before you can try again. The temporary blockage time increases with the number of failed attempts.</p>
                        <p><b>Check your inbox</b> - you will be notified in case you have been blocked by an admin or due to multiple failed log-in attempts.</p>
                        <p><b>Refresh the page</b> and try again to see if the problem resolves.</p>
                        <p><b>Make sure you have an account</b> and sign up in case you do not.</p>
                        <p><b>The error could be </b> to make sure you have the correct email/password combination. The email should not contain empty spaces.</p>
                        <p><b>If none of the above works</b> let us know. The error could indicate a problem on our end.</p>
                    </div>
                )
            }

            <p className="MAIN-info-paragraph">
                Don't have an account yet? <a href="/signup">Sign up</a> instead.
            </p>
        </div>
    );
};

export default LogIn;