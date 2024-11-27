import PropTypes from "prop-types";
/**
 * Component returns div with UI of a successful token verification (step 1/2) of changing the email
 * @param {object} props
 * @param {boolean} props.verifiedNewEmail
 * @returns {React.ReactElement}
 * 
 */
function ChangeEmailHalfPath() {
    const { verifiedNewEmail } = props;

    let missingEmail = ""
    let stepCompleted = ""

    if (verifiedNewEmail) {
        missingEmail = "current"
        stepCompleted = "3"
    } else {
        missingEmail = "new"
        stepCompleted = "2"
    }

    return (
        <div>

            <h3>1 out of 2 links verified!</h3>
            <br />

            <p >
                The email change process is <b>not complete yet</b>: please click on the link we sent to your <b>{missingEmail}</b> email address as well.
            </p>

            <br />

            <p >
                Email change requests are a three-step process:
            </p>
            <ol>
                <li><b>Step 1:</b> request the email change in account settings</li>
                <li><b>Step 2:</b> click the link sent to your <b>current email</b> address to verify the change, and</li>
                <li><b>Step 3:</b> click the link sent to your <b>new email</b> address to verify its valid.</li>
            </ol>

            <br />

            <p >
                You have completed steps 1 and {stepCompleted} already.
                No changes will be made to your account until both email verifications are completed.
            </p>

        </div>
    );
};
ChangeEmailHalfPath.propTypes = {
    verifiedNewEmail: PropTypes.bool.isRequired,
};

export default ChangeEmailHalfPath;