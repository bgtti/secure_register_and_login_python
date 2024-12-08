import { useNavigate } from "react-router-dom";
/**
 * Component returns div with UI of a sucessful email verification attempt
 * 
 * @returns {React.ReactElement}
 * 
 */
function VerifyEmailSucceeded() {
    const navigate = useNavigate();

    return (
        <div>

            <h3>Email verified successfully!</h3>
            <br />

            <p >
                You have successfully verified your account.
            </p>

            <br />

            <p >
                You are able to enable multi-factor authentication on your account if you wish to do so!
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

export default VerifyEmailSucceeded;