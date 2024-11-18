import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Modal from "../../../components/Modal/Modal";
import ModalChangeAccount from "./ModalChangeAccount";
import "./accountSettings.css"

/** 
 * @constant
 * @type {string[]}
 * @default 
 * ["name","email","password"]
*/
const ACCOUNT_ACTIONS = ["name", "email", "password"]

/**
 * Component for managing the user's account.
 * 
 * 
 * Component accepts no props.
 * 
 * @visibleName User Area: Account Settings
 * @summary Component which allows users to change email and password.
 * @returns {React.ReactElement}
 */
function AccountSettings() {
    //upload user to pre-fill name and email fields
    const user = useSelector((state) => state.user);

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
        <div className="AccountSettings">
            {
                modalChangeAccount && accountAction !== "" && (
                    <Modal
                        title={`Change ${accountAction}`}
                        content={modalChangeAccountContent}
                        modalStatus={modalChangeAccount}
                        setModalStatus={setModalChangeAccount} ></Modal>
                )
            }
            <h3>Account Settings</h3>
            <section className="AccountSettings-Section1">
                <h4>Account</h4>
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
                    <button onClick={() => { selectAccountAction("password"); toggleModal() }}>
                        Change password
                    </button>
                </div>
            </section>

            <hr className="AccountSettings-hr" />

            <section >
                <h4>Preferences</h4>
                <div className="AccountSettings-Preferences">
                    <div>
                        <p>Mailing list</p>
                        <div>
                            <label className="toggleBtn">
                                <input type="checkbox" />
                                <span class="slider round"></span>
                            </label>
                        </div>
                    </div>

                    <div>
                        <p>Night mode</p>
                        <div>
                            <label className="toggleBtn">
                                <input type="checkbox" />
                                <span class="slider round"></span>
                            </label>
                        </div>
                    </div>

                </div>


            </section>
        </div>
    );
}

export default AccountSettings;