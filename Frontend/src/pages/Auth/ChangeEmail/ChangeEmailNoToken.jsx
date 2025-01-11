import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { PATH_TO } from "../../../router/routePaths.js"
import InputToken from "../../../components/Auth/InputToken.jsx";

/**
 * Component returns Change Email No Token page
 * 
 * When an email change is requested, user should get 2 emails: an email with a button leading to the email change page (the url depends on whether it is the new or old email being changed) and a link to be pasted in the browser in case the button does not redirect.
 * This is the link page, where the user has to input the token manually on the page because the button with the full link including token did not work.
 * 
 * This component will re-direct to the appropriate email change page.
 * 
 * @returns {React.ReactElement}
 */
function ChangeEmailNoToken() {
    const navigate = useNavigate();
    const location = useLocation();

    // Extract the url path 
    const currentPath = location.pathname;

    // Determine the route used to get here
    // The url could be to confirm the new email address:
    const isConfirmNewEmail = currentPath.includes('/confirmNewEmail');
    // Or the url could be to confirm the current (old) email address:
    const isConfirmEmailChange = currentPath.includes('/confirmEmailChange');
    // Print an error to the console in case the path is something else
    if (!isConfirmNewEmail && !isConfirmEmailChange) { console.error("Path error lead to email change component?") }

    //Token
    const [token, setToken] = useState("");
    const [tokenIsValid, setTokenIsValid] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!tokenIsValid) { return }

        //navigate to the correct token validation page
        if (isConfirmNewEmail) {
            navigate(`${PATH_TO.emailChangeConfirmNewEmail}${token}`);
        } else {
            navigate(`${PATH_TO.emailChangeConfirmEmail}${token}`);
        }
    };

    return (
        <div>

            <Helmet>
                <title>Email Change Input Token</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>

            <h2>Email Change: Token</h2>

            <p className="MAIN-info-paragraph">
                Provide the token you received in your
                {isConfirmNewEmail ? " new " : " current "}
                email account bellow.
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

export default ChangeEmailNoToken;