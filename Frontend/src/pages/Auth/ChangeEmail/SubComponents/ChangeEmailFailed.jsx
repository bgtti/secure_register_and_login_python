/**
 * Component returns div with UI of a failed email change attempt
 * 
 * @returns {React.ReactElement}
 * 
 */
function ChangeEmailFailed() {

    return (
        <div>

            <h3>Invalid email verification link</h3>
            <br />

            <p >
                The link link you used probably already expired or is invalid.
            </p>

            <br />

            <p >
                When you initiate the process to change your account email, two emails will be sent to you:
            </p>
            <ol>
                <li>- One to the email account you currently use to log in, and</li>
                <li>- One to the new email address you provided.</li>
            </ol>

            <br />

            <p >
                You need to validate both emails by clicking on the button they contain so as to have your change request approved.
            </p>

            <br />

            <p >
                To change the email registered with us, please log in and re-initiate this process. In case you encounter any issues, please contact support.
            </p>

        </div>
    );
};

export default ChangeEmailFailed;