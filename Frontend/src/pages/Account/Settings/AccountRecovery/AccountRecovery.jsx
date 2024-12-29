import { useEffect, useState } from "react";
import { PropTypes } from "prop-types";
import Modal from "../../../../components/Modal/Modal";
import ModalSetRecoveryEmail from "./ModalSetRecoveryEmail";
import ModalViewRecoveryEmail from "./ModalViewRecoveryEmail";

/**
 * Component returns section with UI for a user's account recovery
 * 
 * @todo component functionality implementation missing
 * @param {object} props
 * @param {object} props.user 
 * @param {string} props.user.name
 * @param {string} props.user.email 
 * @param {string} props.user.acctVerified
 * @param {string} props.acctRecovery
 * @param {bool} props.acctRecovery.recoveryEmailAdded
 * @param {string} props.acctRecovery.recoveryEmailPreview
 * @returns {React.ReactElement}
 * 
 */
function AccountRecovery(props) {
    const { user, acctRecovery } = props;

    //State of modal that changes account credentials (boolean defines whether or not to show modal)
    const [modalSetRecoveryEmail, setModalSetRecoveryEmail] = useState(false)
    const [modalViewRecoveryEmail, setModalViewRecoveryEmail] = useState(false)

    //Css class to hide/show modal
    // modalSetRecoveryEmail ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active"); 

    //Modal content
    const modalSetRecoveryEmailContent = modalSetRecoveryEmail && (
        <ModalSetRecoveryEmail modalToggler={toggleModalSet} user={user} acctRecovery={acctRecovery} />
    );
    const modalViewRecoveryEmailContent = modalViewRecoveryEmail && (
        <ModalViewRecoveryEmail modalToggler={toggleModalView} user={user} acctRecovery={acctRecovery} />
    );

    //Modal state toggle
    function toggleModalSet() {
        setModalSetRecoveryEmail(!modalSetRecoveryEmail);
    }
    function toggleModalView() {
        setModalViewRecoveryEmail(!modalViewRecoveryEmail);
    }
    function toggleModalDelete() {
        console.log("delete")
    }

    return (
        <section className="AccountSettings-Section1">
            {
                modalSetRecoveryEmail && (
                    <Modal
                        title={`Set Recovery Email`}
                        content={modalSetRecoveryEmailContent}
                        modalStatus={modalSetRecoveryEmail}
                        setModalStatus={setModalSetRecoveryEmail}
                    />
                )
            }
            {
                modalViewRecoveryEmail && (
                    <Modal
                        title={`View Recovery Email`}
                        content={modalViewRecoveryEmailContent}
                        modalStatus={modalViewRecoveryEmail}
                        setModalStatus={setModalViewRecoveryEmail}
                    />
                )
            }

            <h4>Account Recovery</h4>

            {/* If the user has not yet set a recovery email */}
            {
                !acctRecovery.recoveryEmailAdded && (
                    <>
                        <p>Set a recovery email address. </p>
                        <p>If you lose or forget your credentials, you can still gain access to the app.</p>
                        {
                            !user.acctVerified && (
                                <p className="MAIN-yellow-paragraph">Verify your account in order to add a recovery email. </p>
                            )
                        }
                        <div>
                            <button
                                disabled={!user.acctVerified}
                                onClick={() => { toggleModalSet() }}
                            >
                                Set recovery email
                            </button>
                        </div>
                    </>
                )
            }
            {/* If the user already has a recovery email set */}
            {
                acctRecovery.recoveryEmailAdded && (
                    <>
                        <p>A recovery email address was set. </p>
                        <div>
                            <button
                                disabled={!user.acctVerified}
                                onClick={() => { toggleModalView() }}
                            >
                                View recovery email
                            </button>
                        </div>
                        <br />
                        <p>Recovery email: {acctRecovery.recoveryEmailPreview} </p>
                        <div>
                            <button
                                disabled={!user.acctVerified}
                                onClick={() => { toggleModalSet() }}
                            >
                                Change
                            </button>
                            <button
                                className="MAIN-DeleteBtn"
                                disabled={!user.acctVerified}
                                onClick={() => { toggleModalDelete() }}
                            >
                                Remove
                            </button>
                        </div>
                        <br />

                    </>
                )
            }
        </section>
    );
};
AccountRecovery.propTypes = {
    user: PropTypes.shape({
        // name: PropTypes.string.isRequired,
        // email: PropTypes.string.isRequired,
        acctVerified: PropTypes.oneOfType([
            PropTypes.bool,
            PropTypes.string
        ])
    }).isRequired,
    acctRecovery: PropTypes.shape({
        recoveryEmailPreview: PropTypes.string.isRequired,
        recoveryEmailAdded: PropTypes.bool.isRequired
    }).isRequired,
};

export default AccountRecovery;