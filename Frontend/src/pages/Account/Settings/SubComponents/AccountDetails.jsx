import { useState } from "react";
import { PropTypes } from "prop-types";
import Modal from "../../../../components/Modal/Modal";
import ModalAccountDetailChange from "../Modals/ModalAccountDetailChange";
import ModalVerifyEmail from "../Modals/ModalVerifyEmail";

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
 * @param {string} props.user.acctVerified
 * @returns {React.ReactElement}
 * 
 */
function AccountDetails(props) {
    const { user } = props;

    //State of modal that changes account credentials (boolean defines whether or not to show modal)
    const [modalChangeCreds, setModalChangeAcctCreds] = useState(false)

    //State of modal that verifies account
    const [modalVerifyEmail, setModalVerifyEmail] = useState(false)

    //Desired modal action of modalChangeCreds (ie: what credential to be changed)
    const [accountAction, setAccountAction] = useState("")

    //Css class to hide/show modal
    modalChangeCreds ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");

    //Modal content
    const modalChangeCredsContent = modalChangeCreds && accountAction !== "" && (
        <ModalAccountDetailChange action={accountAction} modalToggler={toggleModalCred} />
    );
    const modalVerifyEmailContent = modalVerifyEmail && (
        <ModalVerifyEmail modalToggler={toggleModalVerify} />
    );

    //Action selection
    function selectAccountAction(action) {
        ACCOUNT_ACTIONS.includes(action.toLowerCase()) ? setAccountAction(action) : setAccountAction("");
    }

    //Modal state toggle
    function toggleModalCred() {
        setModalChangeAcctCreds(!modalChangeCreds);
    }
    function toggleModalVerify() {
        setModalVerifyEmail(!modalChangeCreds);
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
                modalVerifyEmail && (
                    <Modal
                        title={`Verify Account`}
                        content={modalVerifyEmailContent}
                        modalStatus={modalVerifyEmail}
                        setModalStatus={setModalVerifyEmail} />
                )
            }
            <h4>Account Details</h4>
            <p><b>Name:</b> {user.name}</p>
            <div>
                <button onClick={() => { selectAccountAction("name"); toggleModalCred() }}>
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
                <button onClick={() => { selectAccountAction("password"); toggleModalCred() }}>
                    Change password
                </button>
            </div>

            <br />

            <p><b>Status:</b> {user.acctVerified ? "Verified" : "Email has not been verified"}</p>
            <div>
                <button disabled={user.acctVerified} onClick={() => { toggleModalVerify() }}>
                    Verify account
                </button>
            </div>
        </section>
    );
};
AccountDetails.propTypes = {
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        acctVerified: PropTypes.bool.isRequired
    }).isRequired,
};

export default AccountDetails;