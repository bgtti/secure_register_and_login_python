/**
 * Component returns section with UI for a user's account deletion
 * 
 * @todo component functionality implementation missing
 * 
 * @returns {React.ReactElement}
 * 
 */
function AccountDeletion() {

    return (
        <section className="AccountSettings-Section1">
            <h4>Delete Account</h4>
            <p>Please be certain you want to delete your account. </p>
            <p>Warning: This action cannot be undone.</p>
            <div>
                <button className="MAIN-DeleteBtn" onClick={() => { console.log("deleted") }}>
                    Delete account
                </button>
            </div>
        </section>
    );
};

export default AccountDeletion;