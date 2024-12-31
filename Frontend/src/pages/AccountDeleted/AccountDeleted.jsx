import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
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
    logOutDeletedUser()

    return (
        <div >
            <Helmet>
                <title>Account Deleted</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>
            <h2>Account deleted</h2>
            <br />
            <p>Your account was deleted successfully!</p>
        </div>
    );
}

export default AccountDeleted;