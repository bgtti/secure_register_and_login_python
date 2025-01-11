import { PropTypes } from "prop-types";
import MailingList from "./MailingList";
import NightMode from "./NightMode";

/**
 * Component returns section with UI for a user's setting of account preferences
 * 
 * @returns {React.ReactElement}
 * 
 */
function AccountPreferences(props) {
    const { preferences } = props;

    return (
        <section >
            <h4>Preferences</h4>
            <div className="AccountSettings-Preferences">

                <MailingList
                    preferences={preferences}
                />

                <NightMode
                    preferences={preferences}
                />
            </div>
        </section>
    );
};
AccountPreferences.propTypes = {
    preferences: PropTypes.shape({
        mailingList: PropTypes.bool.isRequired,
        nightMode: PropTypes.bool.isRequired
    }).isRequired,
};

export default AccountPreferences;