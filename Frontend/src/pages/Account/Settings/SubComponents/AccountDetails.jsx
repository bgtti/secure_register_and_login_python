import { useState } from "react";
import { PropTypes } from "prop-types";
import Modal from "../../../../components/Modal/Modal";
import ModalAccountDetailChange from "../Modals/ModalAccountDetailChange";


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
 * @returns {React.ReactElement}
 * 
 */
function AccountDetails(props) {
    const { user } = props;

    //State of modal that changes account credentials (boolean defines whether or not to show modal)
    const [modalChangeCreds, setModalChangeAcctCreds] = useState(false)

    //Desired modal action (ie: what credential to be changed)
    const [accountAction, setAccountAction] = useState("")

    //Css class to hide/show modal
    modalChangeCreds ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");

    //Modal content
    const modalChangeCredsContent = modalChangeCreds && accountAction !== "" && (
        <ModalAccountDetailChange action={accountAction} modalToggler={toggleModal} />
    );

    //Action selection
    function selectAccountAction(action) {
        ACCOUNT_ACTIONS.includes(action.toLowerCase()) ? setAccountAction(action) : setAccountAction("");
    }

    //Modal state toggle
    function toggleModal() {
        setModalChangeAcctCreds(!modalChangeCreds);
    }

    return (
        <section className="AccountSettings-Section1">
            {
                modalChangeCreds && accountAction !== "" && (
                    <Modal
                        title={`Change ${accountAction}`}
                        content={modalChangeCredsContent}
                        modalStatus={modalChangeCreds}
                        setModalStatus={setModalChangeAcctCreds} ></Modal>
                )
            }
            <h4>Account Details</h4>
            <p><b>Name:</b> {user.name}</p>
            <div>
                <button onClick={() => { selectAccountAction("name"); toggleModal() }}>
                    Change name
                </button>
            </div>

            <br />

            <p><b>Email:</b> {user.email}</p>
            <div>
                <button onClick={() => { selectAccountAction("email"); toggleModal() }}>
                    Change email
                </button>
            </div>

            <br />

            <p><b>Password:</b> ********</p>
            <div>
                <button onClick={() => { selectAccountAction("password"); toggleModal() }}>
                    Change password
                </button>
            </div>

            <br />

            <p><b>Status:</b> your email has been verified</p>
            <div>
                <button onClick={() => { console.log("deleted") }}>
                    Verify account
                </button>
            </div>
        </section>
    );
};
AccountDetails.propTypes = {
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired
    }).isRequired,
};

export default AccountDetails;