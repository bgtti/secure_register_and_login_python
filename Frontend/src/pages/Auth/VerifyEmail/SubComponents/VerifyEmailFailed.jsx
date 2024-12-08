/**
 * Component returns div with UI of a failed email verification attempt
 * 
 * @returns {React.ReactElement}
 * 
 */
function EmailVerifyFailed() {

    return (
        <div>

            <h3>Invalid email verification link</h3>
            <br />

            <p >
                The link link you used probably already expired or is invalid.
            </p>

            <br />

            <p >
                Please log in and re-initiate this process. The link you receive will be valid for one hour. In case you encounter any issues, please contact support.
            </p>

        </div>
    );
};

export default EmailVerifyFailed;