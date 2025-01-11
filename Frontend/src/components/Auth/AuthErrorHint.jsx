import { PropTypes } from "prop-types";
import "./authComponents.css"

/** 
 * @constant
 * @type {string[]}
 * @default 
 * // Use to define the modal's output (depends on which component called it) 
 * COMPONENTS = ["signup", "login"]
*/
const COMPONENTS = ["signup", "login"]

/**
 * Component returns div tag with hints about why a login or signup attempt might have failed.
 * 
 * Requires one prop: the lowercase name of the component calling it.
 * This component was built to be attached to either the Signup or the Login component.
 * 
 * @visibleName AuthErrorHint
 * 
 * @param {object} props
 * @param {string} props.component //one of: ["signup", "login"]. 
 * @returns {React.ReactElement}
 */
function AuthErrorHint(props) {
    const { component } = props;

    // Note that error hint text is vague by design. 
    // It should not inform whether it was the email or the password that caused the error.
    // OWASP recommends ambiguity as not to give bad actors enough information as to determine if a certain account exists.

    const errorHints = {
        login: (
            <>
                <p><b>Check your credentials:</b> Make sure you have the correct email/password combination. The email should not contain empty spaces.</p>
                <p><b>Check your inbox:</b> You will be notified if you have been blocked by an admin or due to multiple failed log-in attempts.</p>
                <p><b>Multiple failed log-in attempts:</b> You will be temporarily blocked after 3 failed attempts. Wait a few minutes before trying again; the wait time increases with further failed attempts.</p>
                <p><b>Make sure you have an account:</b> Sign up if you don’t already have one.</p>
            </>
        ),
        signup: (
            <>
                <p><b>Check your password:</b> Ensure it has 8+ characters and isn’t easy to guess. Common passwords like "12345678" might be rejected. Tip: use a password manager or create a memorable, long sentence.</p>
                <p><b>Check for spaces and invalid characters:</b> Ensure the email field has no spaces and includes the "@" character. Avoid mixing up the name and email fields.</p>
                <p><b>Check your inbox:</b> If you already have an account, you should have received an email to help you log in.</p>
            </>
        ),
        default: (
            <>
                <p><b>Check your credentials:</b> Ensure they are correct.</p>
                <p><b>Check for spaces and invalid characters:</b> The email field should have no spaces and must include the "@" character. Avoid mixing up fields.</p>
                <p><b>Check your inbox:</b> If you already have an account, you should have received an email to help you log in.</p>
            </>
        ),
    };

    const text = errorHints[component] || errorHints.default;

    return (
        <div aria-label="Authentication Error Hints" className="AuthErrorHint">
            <h3>What could have gone wrong...</h3>
            {text}
            <p><b>If none of the above works</b> let us know. The error could indicate a problem on our end.</p>
        </div>
    );
};
AuthErrorHint.propTypes = {
    component: PropTypes.oneOf(COMPONENTS)
};

export default AuthErrorHint;