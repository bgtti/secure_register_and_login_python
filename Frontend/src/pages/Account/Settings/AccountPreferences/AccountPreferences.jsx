import { useEffect, useState } from "react";
import { PropTypes } from "prop-types";
import Tooltip from "../../../../components/Tooltip/Tooltip"
/**
 * Component returns section with UI for a user's setting of account preferences
 * 
 * @todo component functionality implementation missing
 * @todo consider enable/disable otp
 * 
 * @returns {React.ReactElement}
 * 
 */
function AccountPreferences(props) {
    const { user, preferences } = props;

    //State of mailing list
    const [inMailingList, setInMailingList] = useState(preferences.mailingList)
    //State of night mode
    const [nightModeEnabled, setNightModeEnabled] = useState(preferences.nightMode)

    // MFA toggle only possible if the account has been verified
    let mfaToggleEnable = user.acctVerified === true;

    // Handlers for toggles
    const handleMailingListToggle = () => {
        setInMailingList((prev) => !prev);
    };

    const handleNightModeToggle = () => {
        setNightModeEnabled((prev) => !prev);
    };


    return (
        <section >
            <h4>Preferences</h4>
            <div className="AccountSettings-Preferences">

                <div>
                    <p><Tooltip text="Mailing List" message="Receive app news per email" /></p>
                    <div>
                        <label className="toggleBtn">
                            <input
                                checked={inMailingList}
                                onChange={handleMailingListToggle}
                                type="checkbox" />
                            <span className="slider round"></span>
                        </label>
                    </div>
                </div>

                <div>
                    <p>Night mode</p>
                    <div>
                        <label className="toggleBtn">
                            <input
                                checked={nightModeEnabled}
                                onChange={handleNightModeToggle}
                                type="checkbox" />
                            <span className="slider round"></span>
                        </label>
                    </div>
                </div>
            </div>
        </section>
    );
};
AccountPreferences.propTypes = {
    preferences: PropTypes.shape({
        mailingList: PropTypes.bool.isRequired,
        nightMode: PropTypes.bool.isRequired
    }).isRequired,
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        acctVerified: PropTypes.oneOfType([
            PropTypes.bool,
            PropTypes.string
        ])
    }).isRequired,
};

export default AccountPreferences;