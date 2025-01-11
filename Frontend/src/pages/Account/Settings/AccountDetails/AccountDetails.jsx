import { useState } from "react";
import { PropTypes } from "prop-types";
import Modal from "../../../../components/Modal/Modal";
import ModalChangeEmail from "./ModalChangeEmail";
import ModalChangeName from "./ModalChangeName";
import ModalChangePassword from "./ModalChangePassword";

/**
 * Component returns section with UI for a user's account details
 * 
 * @param {object} props
 * @param {object} props.user 
 * @param {string} props.user.name
 * @param {string} props.user.email
 * @param {string} props.user.acctVerified //=> check if required
 * @returns {React.ReactElement}
 * 
 */
function AccountDetails(props) {
    const { user } = props;

    //State of modal that changes user's email
    const [modalChangeEmail, setModalChangeEmail] = useState(false)

    //State of modal that changes user's password
    const [modalChangePassword, setModalChangePassword] = useState(false)

    //State of modal that changes user's name
    const [modalChangeName, setModalChangeName] = useState(false)

    //Modal state toggle

    function toggleModalChangeEmail() {
        setModalChangeEmail(!modalChangeEmail);
    }

    function toggleModalChangePassword() {
        setModalChangePassword(!modalChangePassword);
    }

    function toggleModalChangeName() {
        setModalChangeName(!modalChangeName);
    }

    return (
        <section className="AccountSettings-Section1">
            {
                modalChangeEmail && (
                    <Modal
                        title={`Change Email`}
                        content={
                            <ModalChangeEmail modalToggler={toggleModalChangeEmail} user={user} />
                        }
                        modalStatus={modalChangeEmail}
                        setModalStatus={setModalChangeEmail} />
                )
            }
            {
                modalChangePassword && (
                    <Modal
                        title={`Change Password`}
                        content={
                            <ModalChangePassword modalToggler={toggleModalChangePassword} user={user} />
                        }
                        modalStatus={modalChangePassword}
                        setModalStatus={setModalChangePassword} />
                )
            }
            {
                modalChangeName && (
                    <Modal
                        title={`Change Name`}
                        content={
                            <ModalChangeName modalToggler={toggleModalChangeName} user={user} />
                        }
                        modalStatus={modalChangeName}
                        setModalStatus={setModalChangeName} />
                )
            }

            <h4>Account Details</h4>
            <p><b>Name:</b> {user.name}</p>

            <div>
                <button aria-label="Change Name Modal" onClick={toggleModalChangeName}>
                    Change name
                </button>
            </div>

            <br />

            <p><b>Email:</b> {user.email}</p>
            <div>
                <button aria-label="Change Email Modal" onClick={toggleModalChangeEmail}>
                    Change email
                </button>
            </div>

            <br />

            <p><b>Password:</b> ********</p>
            <div>
                <button aria-label="Change Password Modal" onClick={toggleModalChangePassword}>
                    Change password
                </button>
            </div>

        </section>
    );
};
AccountDetails.propTypes = {
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        acctVerified: PropTypes.oneOfType([
            PropTypes.bool,
            PropTypes.string
        ])
    }).isRequired,
};

export default AccountDetails;