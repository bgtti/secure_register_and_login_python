import { PropTypes } from "prop-types";
import "./errorMessage.css"
/**
 * Component returns p tag with a message in italics (yellow)
 * 
 * Can be placed under a form input to display an error message.
 * 
 * Accepts two parameter: message (required) and ariaDescribedby (optional)
 * Not passing a parameter to ariaDescribedby may lead to errors if more than one ErrorMessage component is being rendered at the same time.
 * The reason is that ariaDescribedby will be used as the component's id, and an id should be unique. 
 * 
 * @visibleName Error Message
 * 
 * @param {object} props
 * @param {string} props.message // error message to be shown to user
 * @param {string} props.ariaDescribedby //aria-describedby of the input field yielding the error (for acessability purposes). 
 * @returns {React.ReactElement}
 * @example
 * import ErrorMessage from "../../../components/ErrorMessage/ErrorMessage";
 * let errorMessage = "Email format not accepted." //==> param!
 * let showError = true
 * //some code...
 * <div>
        <label htmlFor="email">Email:</label>
        <input
            aria-invalid={showError}
            aria-describedby="email-error" //==> param!
            autoComplete="email"
            type="text"
            //...etc
        />
    </div>
 * {showError && (
        <ErrorMessage message={errorMessage} ariaDescribedby="email-error"/> // this component!
    )}
    //rest of the return statement...
 */
function ErrorMessage(props) {
    const { message, ariaDescribedby = "error" } = props;

    return (
        <p aria-live="polite" className="Error-Message" id={ariaDescribedby} >
            <i>{message}</i>
        </p>
    );
};
ErrorMessage.propTypes = {
    message: PropTypes.string.isRequired,
    ariaDescribedby: PropTypes.string,
};

export default ErrorMessage;