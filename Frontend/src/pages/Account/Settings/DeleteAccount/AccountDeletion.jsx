import { useEffect, useState } from "react";
import Modal from "../../../../components/Modal/Modal";
import ModalDeleteAccount from "./ModalDeleteAccount";
/**
 * Component returns section with UI for a user's account deletion
 * 
 * @todo component functionality implementation missing
 * 
 * @returns {React.ReactElement}
 * 
 */
function AccountDeletion() {
    //State of modal that changes account credentials (boolean defines whether or not to show modal)
    const [modalDeleteAcct, setModalDeleteAcct] = useState(false)
    //Css class to hide/show modal
    // modalDeleteAcct ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active"); 

    //Modal content
    const modalDeleteAcctContent = modalDeleteAcct && (
        <ModalDeleteAccount modalToggler={toggleModal} />
    );

    //Modal state toggle
    function toggleModal() {
        setModalDeleteAcct(!modalDeleteAcct);
    }

    return (
        <section className="AccountSettings-Section1">
            {
                modalDeleteAcct && (
                    <Modal
                        title={`Delete Account`}
                        content={modalDeleteAcctContent}
                        modalStatus={modalDeleteAcct}
                        setModalStatus={setModalDeleteAcct} />
                )
            }
            <h4>Delete Account</h4>
            <p>Please be certain you want to delete your account. </p>
            <p>Warning: This action cannot be undone.</p>
            <div>
                <button className="MAIN-DeleteBtn" onClick={() => { toggleModal() }}>
                    Delete account
                </button>
            </div>
        </section>
    );
};

export default AccountDeletion;