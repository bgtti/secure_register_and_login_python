import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { setLoader } from "../../../redux/loader/loaderSlice"
import { signupUser } from "../../../config/apiHandler/authRegistration/signup"
import useIsComponentMounted from "../../../hooks/useIsComponentMounted.js";
import Honeypot from "../../../components/Honeypot/Honeypot";
import ErrorMessage from "../../../components/ErrorMessage/ErrorMessage";
import AuthErrorHint from "../../../components/Auth/AuthErrorHint.jsx";
import InputName from "../../../components/Auth/InputName.jsx"
import InputEmail from "../../../components/Auth/InputEmail.jsx";
import InputPassword from "../../../components/Auth/InputPassword";
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

    const isComponentMounted = useIsComponentMounted();

    // Used for honeypot
    const [honeypotValue, setHoneypotValue] = useState("");

    // Used for actual fields
    const [email, setEmail] = useState("");
    const [emailIsValid, setEmailIsValid] = useState(false);
    const [name, setName] = useState("");
    const [nameIsValid, setNameIsValid] = useState(false);
    const [password, setPassword] = useState("");
    const [passwordIsValid, setPasswordIsValid] = useState(false);
    const [confirmPassword, setConfirmPassword] = useState("");
    const [confirmPasswordIsValid, setConfirmPasswordIsValid] = useState(false);

    // State set by api call
    const [errorMessage, setErrorMessage] = useState("");
    const [signupFailed, setSignupFailed] = useState(false);

    // Form is valid when all fields are valid and api call did not return error
    const formIsValid = (nameIsValid && emailIsValid && passwordIsValid && confirmPasswordIsValid && passwordIsValid === confirmPasswordIsValid && errorMessage === "")

    // Extra validation 
    const checkIfPasswordsMatch = (firstPwd, secondPwd) => {
        const arePasswordsEqual = (firstPwd === secondPwd);
        const message = arePasswordsEqual ? "" : "Passwords do not match."
        if (!arePasswordsEqual) { setErrorMessage(message); return false }
        else { return true }
    }

    //if a form error was shown, hide it when the user starts to correct the input
    useEffect(() => {
        if (errorMessage !== "") {
            setErrorMessage("")
        }
    }, [name, email, password, confirmPassword]);


    const handleSubmit = (e) => {
        e.preventDefault();
        if (!checkIfPasswordsMatch(password, confirmPassword)) {
            return
        }
        if (formIsValid) {
            const requestData = {
                name: name,
                email: email,
                password: password,
                honeypot: honeypotValue
            }
            dispatch(setLoader(true))
            signupUser(requestData)
                .then(res => {
                    if (isComponentMounted) {
                        if (res.response) {
                            navigate("/userAccount");
                        } else {
                            setSignupFailed(res.response);
                            setErrorMessage(res.message);
                        }
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

                <InputName
                    name={name}
                    setName={setName}
                    setNameIsValid={setNameIsValid}
                    cssClass={"MAIN-form-display-table"}
                />

                <InputEmail
                    email={email}
                    setEmail={setEmail}
                    setEmailIsValid={setEmailIsValid}
                    cssClass={"MAIN-form-display-table"}
                />
                <InputPassword
                    password={password}
                    setPassword={setPassword}
                    setPasswordIsValid={setPasswordIsValid}
                    simpleValidation={false}
                    cssClass={"MAIN-form-display-table"}
                />
                <InputPassword
                    autocomplete={"confirm-password"}
                    labelText={"Confirm Password"}
                    password={confirmPassword}
                    setPassword={setConfirmPassword}
                    setPasswordIsValid={setConfirmPasswordIsValid}
                    cssClass={"MAIN-form-display-table"}
                />

                <Honeypot setHoneypotValue={setHoneypotValue} />

                <button disabled={!formIsValid} type="submit">Create account</button>

                {
                    errorMessage !== "" && (
                        < ErrorMessage message={errorMessage} ariaDescribedby="api-response-error" />
                    )
                }
            </form>

            {
                errorMessage !== "" && signupFailed && (
                    < AuthErrorHint component={"signup"} />
                )
            }

            <p className="MAIN-info-paragraph">
                Already have an account? <a href="/login">Log in</a> instead.
            </p>
        </div>
    );
}

export default SignUp;