import { useEffect, useState } from "react";
import { PropTypes } from "prop-types";
import Modal from "../../../../components/Modal/Modal";
import Tooltip from "../../../../components/Tooltip/Tooltip"
import ModalDisableMFA from "./ModalDisableMFA";
import ModalSetMFA from "./ModalSetMFA";
import ModalVerifyAccount from "./ModalVerifyAccount";

/**
 * Component returns section with UI for a user's account security
 * 
 * @param {object} props
 * @param {object} props.user 
 * @param {string} props.user.name
 * @param {string} props.user.email
 * @param {string} props.user.acctVerified
 * @returns {React.ReactElement}
 * 
 */
function AccountSecurity(props) {
    const { user } = props;

    //Verify account: set modal state
    const [modalVerifyAccount, setModalVerifyAccount] = useState(false)

    //MFA: set modal state
    const [modalSetMFA, setModalSetMFA] = useState(false)
    const [modalDisableMFA, setModalDisableMFA] = useState(false)

    //Verify account: state of text of account verification status
    const [acctVerificationStatus, setAcctVerificationStatus] = useState("")

    //MFA: state of text of tooltip
    const [mfaTooltipText, setMfaTooltipText] = useState("")

    // Verify account: set account verification status
    useEffect(() => {
        let verifyText;
        let mfaText;
        if (user.acctVerified) {
            verifyText = "account verified"
            mfaText = "Enable multi-factor authentication"
        } else {
            verifyText = "account not verified"
            if (!user.mfa) { mfaText = "Account must be verified before enabling multi-factor authentication" }
        }
        if (user.mfa) { mfaText = "Multi-factor authentication" }
        setAcctVerificationStatus(verifyText);
        setMfaTooltipText(mfaText);
    }, [user.acctVerified]);

    //Verify account: whether user may verify the account (disabling button)
    let acctCanBeVerified = user.acctVerified ? true : false

    //Verify account: modal content
    const modalVerifyAccountContent = modalVerifyAccount && (
        <ModalVerifyAccount user={user} modalToggler={toggleModalVerify} />
    );

    //MFA: modal content
    const modalSetMFAContent = modalSetMFA && (
        <ModalSetMFA user={user} modalToggler={toggleModalMFA} />
    );
    const modalDisableMFAContent = modalDisableMFA && (
        <ModalDisableMFA user={user} modalToggler={toggleModalMFADisable} />
    );

    //Verify account: Modal state toggle
    function toggleModalVerify() {
        setModalVerifyAccount(!modalVerifyAccount)
    }

    //MFA: Modal state toggle
    function toggleModalMFA() {
        setModalSetMFA(!modalSetMFA)
    }

    function toggleModalMFADisable() {
        setModalDisableMFA(!modalDisableMFA)
    }

    return (
        <section className="AccountSettings-Section1">
            {
                modalVerifyAccount && (
                    <Modal
                        title={`Verify Account`}
                        content={modalVerifyAccountContent}
                        modalStatus={modalVerifyAccount}
                        setModalStatus={setModalVerifyAccount} />
                )
            }
            {
                modalSetMFA && (
                    <Modal
                        title={`Enable Multi-factor auth`}
                        content={modalSetMFAContent}
                        modalStatus={modalSetMFA}
                        setModalStatus={setModalSetMFA} />
                )
            }
            {
                modalDisableMFA && (
                    <Modal
                        title={`EDisable Multi-factor auth`}
                        content={modalDisableMFAContent}
                        modalStatus={modalDisableMFA}
                        setModalStatus={setModalDisableMFA} />
                )
            }
            <h4>Account Safety</h4>

            <p><b><Tooltip text="Status:" message="Email address verification status" cssClass="Tooltip-text-bold" /></b> {acctVerificationStatus}</p>
            <div>
                <button
                    disabled={acctCanBeVerified}
                    onClick={toggleModalVerify}
                    title={acctCanBeVerified ? "Your account has already been verified" : ""}>
                    Verify account
                </button>
            </div>

            <br />

            <p><b><Tooltip text="MFA:" message={mfaTooltipText} cssClass="Tooltip-text-bold" /></b> {user.mfa ? "enabled" : "disabled"}</p>

            {
                user.mfa ? (
                    <div>
                        <button
                            className={user.mfa ? "MAIN-DeleteBtn" : "MAIN-display-none"}
                            disabled={!user.mfa}
                            onClick={toggleModalMFADisable}
                        >
                            Disable MFA
                        </button>
                    </div>
                ) : (
                    <div>
                        <button
                            className={user.mfa ? "MAIN-display-none" : ""}
                            disabled={!user.acctVerified || user.mfa}
                            onClick={toggleModalMFA}
                        >
                            Enable MFA
                        </button>
                    </div>
                )
            }

        </section>
    );
};
AccountSecurity.propTypes = {
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        acctVerified: PropTypes.oneOfType([
            PropTypes.bool,
            PropTypes.string
        ]).isRequired
    }).isRequired,
};

export default AccountSecurity;