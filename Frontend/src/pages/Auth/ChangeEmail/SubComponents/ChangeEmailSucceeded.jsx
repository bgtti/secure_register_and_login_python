import { useNavigate } from "react-router-dom";
/**
 * Component returns div with UI of a sucessful email change attempt
 * 
 * @returns {React.ReactElement}
 * 
 */
function ChangeEmailSucceeded() {
    const navigate = useNavigate();

    return (
        <div>

            <h3>Email changed successfully!</h3>
            <br />

            <p >
                You have successfully verified the email change in both accounts and your registered email address was changed.
            </p>

            <br />

            <p >
                You will receive two emails confirming the change shortly. You can now log in using your new email address!
            </p>

            <br />

            <button
                type="button"
                onClick={() => { navigate("/login") }}
                role="link">
                Go to log in page
            </button>

        </div>
    );
};

export default ChangeEmailSucceeded;