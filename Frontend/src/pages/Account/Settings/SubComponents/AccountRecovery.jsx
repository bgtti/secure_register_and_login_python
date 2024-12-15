import { useEffect, useState } from "react";
import Modal from "../../../../components/Modal/Modal";
import ModalRecoveryEmail from "../Modals/ModalRecoveryEmail";
/**
 * Component returns section with UI for a user's account deletion
 * 
 * @todo component functionality implementation missing
 * 
 * @returns {React.ReactElement}
 * 
 */
function AccountRecovery() {
    //State of modal that changes account credentials (boolean defines whether or not to show modal)
    const [modalRecoveryEmail, setModalRecoveryEmail] = useState(false)
    //Css class to hide/show modal
    // modalRecoveryEmail ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active"); 

    //Modal content
    const modalRecoveryEmailContent = modalRecoveryEmail && (
        <ModalRecoveryEmail modalToggler={toggleModal} />
    );

    //Modal state toggle
    function toggleModal() {
        setModalRecoveryEmail(!modalRecoveryEmail);
    }

    return (
        <section className="AccountSettings-Section1">
            {
                modalRecoveryEmail && (
                    <Modal
                        title={`Set Recovery Email`}
                        content={modalRecoveryEmailContent}
                        modalStatus={modalRecoveryEmail}
                        setModalStatus={setModalRecoveryEmail} />
                )
            }
            <h4>Account Recovery</h4>
            <p>Set a recovery email address. </p>
            <p>If you lose or forget your credentials, you can still gain access to the app.</p>
            <div>
                <button onClick={() => { toggleModal() }}>
                    Set recovery email
                </button>
            </div>
        </section>
    );
};

export default AccountRecovery;