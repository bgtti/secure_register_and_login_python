import { useSelector } from "react-redux";
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

    return (
        <div className="AccountSettings">

            <h3>Account Settingsssss</h3>

            <AccountDetails
                user={user} />

            <hr className="AccountSettings-hr" />

            <AccountPreferences
                user={user}
                preferences={preferences} />

            <hr className="AccountSettings-hr" />
            <AccountRecovery />

            <hr className="AccountSettings-hr" />
            <AccountDeletion />
        </div>
    );
}

export default AccountSettings;