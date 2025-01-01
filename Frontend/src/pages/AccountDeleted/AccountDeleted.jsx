import { Helmet } from "react-helmet-async";
import { logOutDeletedUser } from "../../config/apiHandler/authRegistration/accountDeleted";

/**
 * Component returns a page confirming the user's account was deleted.
 * 
 * It logs the user out from the redux store.
 * 
 * @returns {React.ReactElement}
 * 
 */
function AccountDeleted() {
    logOutDeletedUser();

    return (
        <div >
            <Helmet>
                <title>Account Deleted</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>
            <h2>Account deleted</h2>
            <br />
            <p><b>Your account was deleted successfully!</b></p>
            <br />
            <p>You shall receive a confirmation of deletion shortly.</p>
            <br />
            <p>We are sorry to see you go and wish you all the best!</p>
        </div>
    );
}

export default AccountDeleted;