import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { PATH_TO } from "../../../router/routePaths.js"
import InputToken from "../../../components/Auth/InputToken.jsx";

/**
 * Component returns Reset Password No Token page
 * 
 * When a password reset is requested, user should get an email with a button leading to the reset password page and a link to be pasted in the browser in case the button does not redirect.
 * This is the link page, where the user has to input the token manually on the page because the button with the full link including token did not work.
 * 
 * This component will re-direct to the Reset Password page.
 * 
 * @returns {React.ReactElement}
 */
function ResetPasswordNoToken() {
    const navigate = useNavigate();

    //Token
    const [token, setToken] = useState("");
    const [tokenIsValid, setTokenIsValid] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (tokenIsValid) {
            navigate(`${PATH_TO.resetPassword}${token}`);
        }
    };

    return (
        <div>

            <Helmet>
                <title>Reset Password Input Token</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>

            <h2>Reset Password: Token</h2>

            <p className="MAIN-info-paragraph">
                Provide the token you received per email bellow.
            </p>

            <br />

            <form onSubmit={handleSubmit} className='MAIN-form'>

                <InputToken
                    token={token}
                    setToken={setToken}
                    setTokenIsValid={setTokenIsValid}
                />

                <button
                    disabled={!tokenIsValid}
                    type="submit">
                    Submit Token
                </button>

            </form>
        </div>
    );
};

export default ResetPasswordNoToken;