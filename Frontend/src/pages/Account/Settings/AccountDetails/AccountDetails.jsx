import { useEffect, useState } from "react";
import { PropTypes } from "prop-types";
import Modal from "../../../../components/Modal/Modal";
import ModalAccountDetailChange from "./ModalAccountDetailChange";
import ModalChangeName from "./ModalChangeName";
import ModalChangePassword from "./ModalChangePassword";

/** 
 * @constant
 * @type {string[]}
 * @default 
 * // Use to define action the modal should take 
 * //(ie: what account credential should be changed)
 * ACCOUNT_ACTIONS =["name","email","password"]
*/
const ACCOUNT_ACTIONS = ["name", "email", "password"]


/**
 * Component returns section with UI for a user's account deletion
 * 
 * @todo component functionality implementation of change password missing
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

    //State of modal that changes account credentials (boolean defines whether or not to show modal)
    const [modalChangeCreds, setModalChangeAcctCreds] = useState(false)

    //State of modal that changes user's name
    const [modalChangeName, setModalChangeName] = useState(false)

    //State of modal that changes user's password
    const [modalChangePassword, setModalChangePassword] = useState(false)

    //Desired modal action of modalChangeCreds (ie: what credential to be changed)
    const [accountAction, setAccountAction] = useState("")

    //Css class to hide/show modal
    modalChangeCreds ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");
    // TODO: css class for other model..?

    //Modal content
    const modalChangeCredsContent = modalChangeCreds && accountAction !== "" && (
        <ModalAccountDetailChange action={accountAction} modalToggler={toggleModalCred} />
    );
    const modalChangeNameContent = modalChangeName && (
        <ModalChangeName modalToggler={toggleModalChangeName} user={user} />
    );
    const modalChangePasswordContent = modalChangePassword && (
        <ModalChangePassword modalToggler={toggleModalChangePassword} user={user} />
    );

    //Action selection
    function selectAccountAction(action) {
        ACCOUNT_ACTIONS.includes(action.toLowerCase()) ? setAccountAction(action) : setAccountAction("");
    }

    //Modal state toggle
    function toggleModalCred() {
        setModalChangeAcctCreds(!modalChangeCreds);
    }

    function toggleModalChangeName() {
        setModalChangeName(!modalChangeName);
    }

    function toggleModalChangePassword() {
        setModalChangePassword(!modalChangePassword);
    }

    return (
        <section className="AccountSettings-Section1">
            {
                modalChangeCreds && accountAction !== "" && (
                    <Modal
                        title={`Change ${accountAction}`}
                        content={modalChangeCredsContent}
                        modalStatus={modalChangeCreds}
                        setModalStatus={setModalChangeAcctCreds} />
                )
            }
            {
                modalChangeName && (
                    <Modal
                        title={`Change Name`}
                        content={modalChangeNameContent}
                        modalStatus={modalChangeName}
                        setModalStatus={setModalChangeName} />
                )
            }
            {
                modalChangePassword && (
                    <Modal
                        title={`Change Password`}
                        content={modalChangePasswordContent}
                        modalStatus={modalChangePassword}
                        setModalStatus={setModalChangePassword} />
                )
            }

            <h4>Account Details</h4>
            <p><b>Name:</b> {user.name}</p>

            <div>
                <button onClick={() => { toggleModalChangeName() }}>
                    Change name
                </button>
            </div>

            <br />

            <p><b>Email:</b> {user.email}</p>
            <div>
                <button onClick={() => { selectAccountAction("email"); toggleModalCred() }}>
                    Change email
                </button>
            </div>

            <br />

            <p><b>Password:</b> ********</p>
            <div>
                <button onClick={toggleModalChangePassword}>
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