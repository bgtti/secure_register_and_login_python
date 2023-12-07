import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { setLoader } from "../../redux/loader/loaderSlice"
import { setUser } from "../../redux/user/userSlice";
import { emailValidation, passwordValidationForLogin } from "../../utils/validation";
import { INPUT_LENGTH } from "../../utils/constants";
import api from "../../config/axios"
import APIURL from "../../config/apiUrls";
import "./login.css"

function LogIn() {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        email: "",
        emailIsValid: { response: false, message: "" },
        password: "",
        passwordIsValid: { response: false, message: "" },
        credentialsAreValid: { response: true, message: "" },
    });

    const formIsValid = (formData.emailIsValid.response && formData.passwordIsValid.response && formData.credentialsAreValid.response);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
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
            dispatch(setLoader(true));
            const logInUser = async () => {
                const requestData = {
                    "email": formData.email,
                    "password": formData.password
                }
                try {
                    const response = await api.post(APIURL.LOGIN, requestData);
                    if (response.status !== 200) {
                        if (response.status === 401) {
                            setFormData((prevData) => ({
                                ...prevData,
                                credentialsAreValid: { response: false, message: "Error: Invalid credentials." },
                            }));
                        } else {
                            setFormData((prevData) => ({
                                ...prevData,
                                credentialsAreValid: { response: false, message: "Error: Please refresh the page and try again." },
                            }));
                        }
                    } else {
                        const userData = {
                            id: response.data.user.id,
                            email: response.data.user.email,
                            name: response.data.user.name
                        }
                        dispatch(setUser(userData))
                        navigate("/dashboard");
                    }
                } catch (error) {
                    setFormData((prevData) => ({
                        ...prevData,
                        credentialsAreValid: { response: false, message: "Error: Please refresh the page and try again." },
                    }));
                }
                dispatch(setLoader(false));
            }
            logInUser();
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

                {
                    formData.credentialsAreValid.message !== "" && (
                        <p className="MAIN-error-message" id="password-error">
                            <i>{formData.credentialsAreValid.message}</i>
                        </p>
                    )
                }
            </form>
            <p className="MAIN-info-paragraph">
                Don't have an account yet? <a href="/signup">Sign up</a> instead.
            </p>
        </div>
    );
}

export default LogIn;