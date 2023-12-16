import { useState } from "react";
import Modal from "../../../components/Modal/Modal";
import ModalChangeAccount from "./ModalChangeAccount";
import "./adminSettings.css"

const ACCOUNT_ACTIONS = ["password", "email"]
function AdminSettings() {
    const [modalChangeAccount, setModalChangeAccount] = useState(false)
    const [accountAction, setAccountAction] = useState("")

    modalChangeAccount ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");

    const modalChangeAccountContent = modalChangeAccount && accountAction !== "" && (
        <ModalChangeAccount action={accountAction} modalToggler={toggleModal} />
    );

    function selectAccountAction(action) {
        ACCOUNT_ACTIONS.includes(action.toLowerCase()) ? setAccountAction(action) : setAccountAction("");
    }
    function toggleModal() {
        setModalChangeAccount(!modalChangeAccount);
    }

    return (
        <div className="AdminSettings">
            {
                modalChangeAccount && accountAction !== "" && (
                    <Modal
                        title={`Change admin ${accountAction}`}
                        content={modalChangeAccountContent}
                        modalStatus={modalChangeAccount}
                        setModalStatus={setModalChangeAccount} ></Modal>
                )
            }
            <h3>Admin Settings</h3>
            <section className="AdminSettings-Section1">
                <h4>Account</h4>
                <p>Email: admin@admin.com</p>
                <div>
                    <button onClick={() => { selectAccountAction("email"); toggleModal() }}>
                        Change email
                    </button>
                    <button onClick={() => { selectAccountAction("password"); toggleModal() }}>
                        Change password
                    </button>
                </div>
            </section>
        </div>
    );
}

export default AdminSettings;