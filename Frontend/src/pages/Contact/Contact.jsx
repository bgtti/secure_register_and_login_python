import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { setLoader } from "../../redux/loader/loaderSlice"
import { setUser } from "../../redux/user/userSlice";
import { loginUser } from "../../config/apiHandler/authSession/login"
import { emailValidation, nameValidation } from "../../utils/validation";
import { sendContactMessage } from "../../config/apiHandler/contact/contactUs"
import { INPUT_LENGTH } from "../../utils/constants";
import Honeypot from "../../components/Honeypot/Honeypot";
// import { api, apiCredentials } from "../../config/axios"
// import APIURL from "../../config/apiUrls";

/**
 * Component returns contact page
 * 
 * @summary Contact page
 * @returns {React.ReactElement}
 * 
 * @example
 * //...
 */
function Contact() {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    //upload user to pre-fill name and email fields
    const user = useSelector((state) => state.user);

    // Used for honeypot
    const [honeypotValue, setHoneypotValue] = useState("");

    const [formData, setFormData] = useState({
        name: "",
        nameIsValid: { response: false, message: "" },
        email: "",
        emailIsValid: { response: false, message: "" },
        message: "",
        messageIsValid: { response: false, message: "" },
        fieldsAreValid: { response: true, message: "" },
    });

    useEffect(() => {
        if (user.loggedIn) {
            setFormData((prevData) => ({
                ...prevData,
                name: user.name,
                nameIsValid: { response: true, message: "" },
                email: user.email,
                emailIsValid: { response: true, message: "" },
            }));
        }
    }, []);

    //useEffect used to enable button as user is typing the message: smoother mouseless navigation
    useEffect(() => {
        if (formData.message.length >= INPUT_LENGTH.contactMessage.minValue) {
            setFormData((prevData) => ({
                ...prevData,
                messageIsValid: { response: true, message: "" }
            }));
        }
    }, [formData.message]);

    const formIsValid = (formData.nameIsValid.response && formData.emailIsValid.response && formData.fieldsAreValid.response);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
        //Ensures that, if an error message had appeared before, that it disappears as user corrects input
        if (!formData.fieldsAreValid.response) {
            setFormData((prevData) => ({
                ...prevData,
                fieldsAreValid: { response: true, message: "" },
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
            if (formData.message.length >= INPUT_LENGTH.contactMessage.minValue && formData.message.length <= INPUT_LENGTH.contactMessage.maxValue) {
                setFormData((prevData) => ({
                    ...prevData,
                    messageIsValid: { response: true, message: "" }
                }));
            } else {
                setFormData((prevData) => ({
                    ...prevData,
                    messageIsValid: { response: false, message: `Message should be between ${INPUT_LENGTH.contactMessage.minValue} and ${INPUT_LENGTH.contactMessage.maxValue} characters long.` }
                }));
            }
        };
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (formIsValid) {
            const requestData = {
                name: formData.name,
                email: formData.email,
                message: formData.message,
                is_user: user.loggedIn,
                honeypot: honeypotValue
            }
            dispatch(setLoader(true))
            sendContactMessage(requestData)
                .then(res => {
                    setFormData((prevData) => ({
                        ...prevData,
                        fieldsAreValid: {
                            response: res.response,
                            message: res.message
                        },
                    }));
                })
                .catch(error => {
                    console.error("Error in contact function.", error);
                })
                .finally(() => {
                    dispatch(setLoader(false));
                })
        }
    };

    return (
        <div className="ContactUs">
            <Helmet>
                <title>Contact us</title>
                <meta name="description" content="Contact us" />
            </Helmet>
            <h2>Contact us</h2>
            <form onSubmit={handleSubmit} className="MAIN-form">
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
                    <label htmlFor="message">Message: <span className="MAIN-form-star"> *</span></label>
                    <textarea
                        id="message"
                        maxLength={`${INPUT_LENGTH.contactMessage.maxValue}`}
                        minLength={`${INPUT_LENGTH.contactMessage.minValue}`}
                        name="message"
                        onBlur={handleBlur}
                        onChange={handleChange}
                        required
                        value={formData.message}
                        cols="23"
                        rows="10">
                    </textarea>
                </div>
                {
                    formData.messageIsValid.message !== "" && (
                        <p className="MAIN-error-message" id="message-error">
                            <i>{formData.messageIsValid.message}</i>
                        </p>
                    )
                }

                <Honeypot setHoneypotValue={setHoneypotValue} />

                <button disabled={!formIsValid} type="submit">Send message</button>

                {
                    formData.fieldsAreValid.message !== "" && (
                        <p className="MAIN-error-message" id="password-error">
                            <i>{formData.fieldsAreValid.message}</i>
                        </p>
                    )
                }
            </form>
        </div>
    );
}

export default Contact;