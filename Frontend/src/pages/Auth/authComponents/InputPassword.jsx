import { useEffect, useState } from "react";
import { PropTypes } from "prop-types";
import { passwordValidation, passwordValidationSimplified } from "../../../utils/validation";
import { INPUT_LENGTH } from "../../../utils/constants";
import RequiredFieldStar from "../../../components/RequiredFieldStar/RequiredFieldStar";
import ErrorMessage from "../../../components/ErrorMessage/ErrorMessage";

/**
 * Component returns InputPassword that should be the child component of a form
 * 
 * The form requires two states to be set on the parent: password and passwordIsValid. 
 * This component will use "password" and set the state of the parent. It will also set the state of passwordIsValid.
 * 
 * An optional boolean prop can be passed: simpleValidation will define whether a password should be validated with the simplified function or not.
 * Only pass "false" in the case a user's password is not yet registered (such as in a signup form).
 * Check out utils/validation for more information about the difference in validation.
 * 
 * This component also accepts an optional prop "autocomplete". 
 * When the password field is used for signing up, no need to use this (it defaults to "new-password").
 * When, however, in a login form, this should be best set to "current-password". 
 * 
 * @visibleName Password Field
 * 
 * @param {object} props
 * @param {string} props.autocomplete // optional, defaults to "new-password"
 * @param {string} props.password
 * @param {func} props.setPassword 
 * @param {func} props.setPasswordIsValid 
 * @param {bool} props.simpleValidation //will be true if no value is passed
 * @returns {React.ReactElement}
 * 
 */
function InputPassword(props) {
    const { password, setPassword, setPasswordIsValid, simpleValidation = true, autocomplete = "new-password" } = props;

    const validationFunc = (pw) => {
        if (simpleValidation) { return passwordValidationSimplified(pw) }
        else { return passwordValidation(pw) }
    }

    const [errorMessage, setErrorMessage] = useState("");

    const handleChange = (e) => {
        setPassword(e.target.value);
        if (errorMessage !== "") { setErrorMessage("") }
    };

    const handleBlur = (e) => {
        let validation = validationFunc(e.target.value);
        setErrorMessage(validation.message);
        setPasswordIsValid(validation.response);
    };

    //useEffect used to enable button (is password is indeed valid) as user is typing the password: smoother mouseless navigation
    useEffect(() => {
        if (password.length >= INPUT_LENGTH.password.minValue) {
            let validation = validationFunc(password);
            setPasswordIsValid(validation.response);
        }
    }, [password]);

    return (
        <>
            <div className="MAIN-form-display-table">
                <label htmlFor="password">Password:<RequiredFieldStar /></label>
                <input
                    aria-invalid={errorMessage === "" ? "false" : "true"}
                    aria-describedby="password-error"
                    autoComplete={autocomplete}
                    id="password"
                    maxLength={`${INPUT_LENGTH.password.maxValue}`}
                    minLength={`${INPUT_LENGTH.password.minValue}`}
                    name="password"
                    onBlur={handleBlur}
                    onChange={handleChange}
                    required
                    type="password"
                    value={password}
                />
            </div>
            {
                errorMessage !== "" && (
                    <ErrorMessage message={errorMessage} ariaDescribedby="password-error" />
                )
            }
        </>
    );
};
InputPassword.propTypes = {
    autocomplete: PropTypes.string,
    password: PropTypes.string.isRequired,
    setPassword: PropTypes.func.isRequired,
    setPasswordIsValid: PropTypes.func.isRequired,
};

export default InputPassword;