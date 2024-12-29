import { PropTypes } from "prop-types";

/**
 * Component returns div with hidden username field
 * 
 * A Browser waning claims "[DOM] Password forms should have (optionally hidden) username fields for accessibility""
 * @info https://www.chromium.org/developers/design-documents/create-amazing-password-forms/
 * 
 * Use this component to get rid of the browser warning.
 * In certain forms, pass a prop "username" with the user's email to help password managers and assistive technology do their jobs
 * 
 * @param {string} props.username // the user's login email address
 * 
 * @returns {React.ReactElement}
 * 
 */
function HiddenUsername(props) {
    const { username = "leave this field empty" } = props

    return (
        <div className="MAIN-display-none">
            <label htmlFor="username">Username:</label>
            <input
                aria-hidden="true"
                autoComplete="username"
                id="username"
                name="username"
                readOnly
                type="text"
                value={username}
            />
        </div>
    );
};
HiddenUsername.propTypes = {
    username: PropTypes.string,
};

export default HiddenUsername;