
import { Helmet } from "react-helmet-async";
import { useSearchParams, useLocation } from "react-router-dom";
import { tokenFormatIsValid } from "../../../utils/validation"
import ChangeEmailFailed from "./Outcome/ChangeEmailFailed"
import ChangeEmailSucceeded from "./Outcome/ChangeEmailSucceeded"
import ChangeEmailHalfPath from "./Outcome/ChangeEmailHalfPath"
import "./changeEmail.css"

/**
 * @plan
 * 
 * User should come to this page from /confirmEmailChange?token={tokenHere} or /confirmNewEmail?token={tokenHere}"
 * the url they arrive from will determine the request from the server (api endpoint)
 * display to user accordingly:
 * 
 * options are:
 * - token expired or invalid => re-start process or contact support
 * - one of the confirmation emails (specify which) was confirmed, but the other not yet so change didnt take effect
 * - both email links were confirmed and changes will take effect immediately: log in button appears
 * http://localhost:5173/confirmEmailChange/token=56324f55
 * http://localhost:5173/confirmNewEmail/token=56324f55
 * 
 */


/**
 * Component returns Confirm Email Change Pages
 * 
 * TODO more info
 * 
 * @requires parameter in the url named "token"
 * 
 * @visibleName //... @todo
 * @returns {React.ReactElement}
 * 
 * @todo this component
 */
function ChangeEmail() {

    // const [searchParams] = useSearchParams();

    const location = useLocation(); // Get the current location

    // Extract the path 
    const currentPath = location.pathname;
    // Determine the route used to get here
    const isConfirmNewEmail = currentPath.includes('/confirmNewEmail');
    const isConfirmEmailChange = currentPath.includes('/confirmEmailChange');

    if (!isConfirmNewEmail && !isConfirmEmailChange) { console.error("Path error lead to email change component?") }

    // Extract the token from the url
    const tokenInUrl = currentPath.split("token=")[1];
    let token = tokenFormatIsValid(tokenInUrl)

    // TODO: send request for validation to the BE
    // TODO: present response accordingly
    // TODO: if both email confirmations are successfull, display a button to take user to log in page




    return (
        <div className="ChangeEmail">
            <Helmet>
                <title>Email Change confirmation</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>

            <p>
                {isConfirmNewEmail && 'Confirm New Email'}
                {isConfirmEmailChange && 'Confirm Email Change'}
            </p>

            <h2>Email change</h2>
            <br />

            <p >
                This is the token: {token}
            </p>

            <p >
                This is the route used to arrive at this page: {currentPath}
            </p>

            {/* <ChangeEmailFailed /> */}
            {/* <ChangeEmailSucceeded /> */}
            {/* <ChangeEmailHalfPath 
            verifiedNewEmaile={isConfirmNewEmail}/> */}

        </div>
    );
};

export default ChangeEmail;