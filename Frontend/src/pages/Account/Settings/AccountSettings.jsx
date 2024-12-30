import { useEffect, useRef } from "react";
import { useSelector } from "react-redux";
import { getRecoveryStatus } from "../../../config/apiHandler/authRecovery/getRecoveryStatus"
import AccountDeletion from "./DeleteAccount/AccountDeletion";
import AccountDetails from "./AccountDetails/AccountDetails";
import AccountPreferences from "./AccountPreferences/AccountPreferences";
import AccountRecovery from "./AccountRecovery/AccountRecovery";
import "./accountSettings.css"

/**
 * Component for managing the user's account.
 * 
 * @visibleName User Area: Account Settings
 * @summary Component which allows users to change email and password.
 * @returns {React.ReactElement}
 */
function AccountSettings() {

    const user = useSelector((state) => state.user);
    const preferences = useSelector((state) => state.preferences);
    const acctRecovery = useSelector((state) => state.accountRecovery);

    // Get account recovery information if redux was not updated in this session
    // Update recovery info upon mount if necessary
    // Ref to track update: avoid duplicate calls (in strict mode)
    const hasFetched = useRef(false);
    useEffect(() => {
        if (!acctRecovery.infoUpToDate && !hasFetched.current) {
            hasFetched.current = true;
            getRecoveryStatus().catch(error => {
                console.error("Error in getRecoveryStatus function.", error);
            });
        }
    }, []);

    //Load recovery: recovery status and if recovery email, then, it...

    return (
        <div className="AccountSettings">

            <h3>Account Settings</h3>

            <AccountDetails
                user={user} />

            <hr className="AccountSettings-hr" />

            <AccountPreferences
                user={user}
                preferences={preferences} />

            <hr className="AccountSettings-hr" />
            <AccountRecovery
                user={user}
                acctRecovery={acctRecovery}
            />

            <hr className="AccountSettings-hr" />
            <AccountDeletion />
        </div>
    );
}

export default AccountSettings;