/**
 * Component returns section with UI for a user's setting of account preferences
 * 
 * @todo component functionality implementation missing
 * 
 * @returns {React.ReactElement}
 * 
 */
function AccountPreferences() {

    return (
        <section >
            <h4>Preferences</h4>
            <div className="AccountSettings-Preferences">
                <div>
                    <p>MFA</p>
                    <div>
                        <label className="toggleBtn">
                            <input type="checkbox" />
                            <span className="slider round"></span>
                        </label>
                    </div>
                </div>

                <div>
                    <p>Mailing list</p>
                    <div>
                        <label className="toggleBtn">
                            <input type="checkbox" />
                            <span className="slider round"></span>
                        </label>
                    </div>
                </div>

                <div>
                    <p>Night mode</p>
                    <div>
                        <label className="toggleBtn">
                            <input type="checkbox" />
                            <span className="slider round"></span>
                        </label>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default AccountPreferences;