import { useEffect, useState } from "react";
import { PropTypes } from "prop-types";
import { tokenFormatIsValid } from "../../utils/validation";
import { INPUT_LENGTH } from "../../utils/constants";
import RequiredFieldStar from "../RequiredFieldStar/RequiredFieldStar";
import ErrorMessage from "../ErrorMessage/ErrorMessage";

/**
 * Component returns InputToken that should be the child component of a form
 * 
 * The form requires two states to be set on the parent: token and tokenIsValid. 
 * This component will use "token" and set the state of the parent. It will also set the state of tokenIsValid.
 * 
 * @param {object} props
 * @param {string} [props.cssClass] //=> optional: defaults to "MAIN-form-display-table AuthToken-displayTable"
 * @param {string} props.token 
 * @param {func} props.setToken
 * @param {func} props.setTokenIsValid 
 * @returns {React.ReactElement}
 * 
 */
function InputToken(props) {
    const { token, setToken, setTokenIsValid, cssClass = "" } = props;

    // If this component is part of a form with many label/input pairs, it is recommended that only 
    // "MAIN-form-display-table" is passed as the argument to cssClass. Example: Signup form.
    const styleClass = cssClass === "" ? "MAIN-form-display-table AuthToken-displayTable" : cssClass;

    const [errorMessage, setErrorMessage] = useState("");

    const handleChange = (e) => {
        setToken(e.target.value);
        if (errorMessage !== "") { setErrorMessage("") }
    };

    const handleBlur = (e) => {
        let validation = tokenFormatIsValid(e.target.value);
        if (!validation) { setErrorMessage("Invalid token format") }
        setTokenIsValid(validation);
    };

    //useEffect used to enable button (is name is indeed valid) as user is typing the name: smoother mouseless navigation
    useEffect(() => {
        if (token.length > 1) {
            let validation = tokenFormatIsValid(token);
            setTokenIsValid(validation);
        }
    }, [token])

    return (
        <>
            <div className={`${styleClass}`}>
                <label htmlFor="token">Token:<RequiredFieldStar /></label>
                <input
                    aria-invalid={errorMessage === "" ? "false" : "true"}
                    aria-describedby="token-error"
                    autoComplete="token"
                    id="token"
                    maxLength={`${INPUT_LENGTH.signedToken.maxValue}`}
                    minLength={`${INPUT_LENGTH.signedToken.minValue}`}
                    name="token"
                    onBlur={handleBlur}
                    onChange={handleChange}
                    required
                    type="text"
                    value={token}
                />
            </div>
            {
                errorMessage !== "" && (
                    <ErrorMessage message={errorMessage} ariaDescribedby="token-error" />
                )
            }
        </>
    );
};
InputToken.propTypes = {
    cssClass: PropTypes.string,
    token: PropTypes.string.isRequired,
    setToken: PropTypes.func.isRequired,
    setTokenIsValid: PropTypes.func.isRequired,
};

export default InputToken;