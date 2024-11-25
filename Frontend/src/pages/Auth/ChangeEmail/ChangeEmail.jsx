
import { Helmet } from "react-helmet-async";
import { useSearchParams, useLocation } from "react-router-dom";
import { validateTokenFormat } from "../../../utils/validation"

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

    const [searchParams] = useSearchParams();

    const location = useLocation(); // Get the current location

    // Extract the path to determine the route
    const currentPath = location.pathname;
    const tokenInUrl = url.split("token=")[1];
    let token = validateTokenFormat(tokenInUrl)

    // TODO: define variable to control for token validity
    // TODO: define variable to control for change successfull

    // TODO: send request for validation to the BE
    // TODO: present response accordingly
    // TODO: if both email confirmations are successfull, display a button to take user to log in page


    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("clicked")
    };

    return (
        <div className="">
            <Helmet>
                <title>Email Change confirmation</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>

            <h2>Email change</h2>

            <p >
                This is the token: {token}
            </p>

            <p >
                This is the route used to arrive at this page: {currentPath}
            </p>

        </div>
    );
};

export default ChangeEmail;