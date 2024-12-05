import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { Helmet } from "react-helmet-async";
import { setLoader } from "../../../redux/loader/loaderSlice"
import { emailValidation, passwordValidationForLogin } from "../../../utils/validation";
import { INPUT_LENGTH } from "../../../utils/constants";
import Honeypot from "../../../components/Honeypot/Honeypot";

/**
 * Component returns Reset Password page
 * 
 * When a password reset is requested, user should get an email with a link leading to a new password input page
 * 
 * @visibleName LogIn
 * @returns {React.ReactElement}
 * 
 * @todo api request
 */
function ResetPassword() {
    const dispatch = useDispatch();

    // Used for honeypot
    const [honeypotValue, setHoneypotValue] = useState("");

    // Used for actual fields
    const [formData, setFormData] = useState({
        email: "",
        emailIsValid: { response: false, message: "" },
    });

    //useEffect used to enable button as user is typing the password: smoother mouseless navigation

    const handleChange = (e) => {
        let inputValue = e.target.value
        setFormData((prevData) => ({
            ...prevData,
            email: inputValue,
        }));

        //Only validate after the user has typed a certain number of characters after the "@"
        if (inputValue.includes("@") && inputValue.split("@")[1]?.length >= 3) {
            setFormData((prevData) => ({
                ...prevData,
                emailIsValid: emailValidation(inputValue),
            }))
        }

        //Ensures that, if an error message had appeared before, that it disappears as user corrects input
        if (!formData.emailIsValid.response) {
            setFormData((prevData) => ({
                ...prevData,
                emailIsValid: { response: false, message: "" },
            }));
        }
    };

    const handleBlur = (e) => {
        setFormData((prevData) => ({
            ...prevData,
            emailIsValid: emailValidation(e.target.value),
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (formData.emailIsValid) {
            const requestData = {
                email: formData.email,
                honeyPot: honeypotValue
            }
            console.log(requestData)
            // dispatch(setLoader(true))
            // loginUser(requestData)
            //     .then(res => {
            //         if (res.response) {
            //             navigate("/userAccount");
            //         } else {
            //             setFormData((prevData) => ({
            //                 ...prevData,
            //                 credentialsAreValid: {
            //                     response: res.response,
            //                     message: res.message
            //                 },
            //             }));
            //         }
            //     })
            //     .catch(error => {
            //         console.error("Error in login function.", error);
            //     })
            //     .finally(() => {
            //         dispatch(setLoader(false));
            //     })
        }
    };

    return (
        <div className="LogIn">
            <Helmet>
                <title>Reset Password</title>
                <meta name="description" content="Reset Password" />
            </Helmet>
            <h2>Reset Password</h2>
            <p className="MAIN-info-paragraph">
                Provide the email address that you used to sign up for your account.
            </p>
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

                <Honeypot setHoneypotValue={setHoneypotValue} />

                <button disabled={!formData.emailIsValid.response} type="submit">Reset password</button>

            </form>

            <p className="MAIN-info-paragraph">
                If the email you provided is registered with us, you shall receive a link to change your password.
            </p>
        </div>
    );
};

export default ResetPassword;