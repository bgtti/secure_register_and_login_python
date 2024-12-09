import { useState } from "react";
import { PropTypes } from "prop-types";
import { emailValidation } from "../../../utils/validation";
import { INPUT_LENGTH } from "../../../utils/constants";
import RequiredFieldStar from "../../../components/RequiredFieldStar/RequiredFieldStar";
import ErrorMessage from "../../../components/ErrorMessage/ErrorMessage";

/**
 * Component returns InputEmail that should be the child component of a form
 * 
 * The component requires two states to be set on the parent: email and emailIsValid. 
 * This component will use "email" and set the state of the parent. It will also set the state of emailIsValid.
 * 
 * This component also accepts an optional prop "autocomplete". 
 * When the email field is used for signing up, no need to use this.
 * When, however, in a login form, this should be best set to "username". 
 * It helps password managers dintinguish between a common email or a username/password match.
 * 
 * @visibleName InputEmail
 * 
 * @param {object} props
 * @param {string} props.autocomplete // optional, defaults to "email"
 * @param {string} props.email
 * @param {func} props.setEmail 
 * @param {func} props.setEmailIsValid 
 * @returns {React.ReactElement}
 * 
 */
function InputEmail(props) {
    const { email, setEmail, setEmailIsValid, autocomplete = "email" } = props;

    const [errorMessage, setErrorMessage] = useState("");

    const handleChange = (e) => {
        setEmail(e.target.value);
        if (errorMessage !== "") { setErrorMessage("") }
    };

    const handleBlur = (e) => {
        let validation = emailValidation(e.target.value);
        setErrorMessage(validation.message);
        setEmailIsValid(validation.response);
    };

    return (
        <>
            <div className="MAIN-form-display-table">
                <label htmlFor="email">Email:<RequiredFieldStar /></label>
                <input
                    aria-invalid={errorMessage === "" ? "false" : "true"}
                    aria-describedby="email-error"
                    autoComplete={autocomplete}
                    id="email"
                    maxLength={`${INPUT_LENGTH.email.maxValue}`}
                    minLength={`${INPUT_LENGTH.email.minValue}`}
                    name="email"
                    onBlur={handleBlur}
                    onChange={handleChange}
                    required
                    type="text"
                    value={email}
                />
            </div>
            {
                errorMessage !== "" && (
                    <ErrorMessage message={errorMessage} ariaDescribedby="email-error" />
                )
            }
        </>
    );
};
InputEmail.propTypes = {
    autocomplete: PropTypes.string,
    email: PropTypes.string.isRequired,
    setEmail: PropTypes.func.isRequired,
    setEmailIsValid: PropTypes.func.isRequired,
};

export default InputEmail;