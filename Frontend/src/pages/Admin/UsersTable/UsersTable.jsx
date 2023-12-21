import { useState, lazy, Suspense } from "react";
import Modal from "../../../components/Modal/Modal";
import ModalUserAction from "./ModalUserAction";
import Loader from "../../../components/Loader";
import UsersTableRow from "./UsersTableRow";
import "./usersTable.css"

const EXAMPLE = [
    {
        name: "John Alfred",
        email: "john@alfred",
        lastSeen: "14 Dec 2023",
        isBlocked: "false",
        uuid: "1234"
    },
    {
        name: "Maria Henrieta Johnson",
        email: "lala@expl.com",
        lastSeen: "10 Dec 2023",
        isBlocked: "false",
        uuid: "2345"
    },
    {
        name: "Frankenstein",
        email: "jeu@hh.com",
        lastSeen: "05 Nov 2023",
        isBlocked: "true",
        uuid: "3456"
    }
]

const USER_ACTIONS = ["delete", "block", "logs"]

// Lazy load UsersLogs component
const UsersLogs = lazy(() => import("./UsersLogs/UsersLogs.jsx"));

function UsersTable() {
    const users = EXAMPLE

    const [userSelected, setUserSelected] = useState({ name: "", email: "", uuid: "" })
    const [userAction, setUserAction] = useState("")
    const [modalUserAction, setModalUserAction] = useState(false)
    const [showUserLogs, setShowUserLogs] = useState(false)

    modalUserAction ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");

    const modalUserActionContent = modalUserAction && userAction !== "" && (
        <ModalUserAction user={userSelected} action={userAction} modalToggler={toggleModal} />
    );

    function selectUserAction(uuid = "", action = "") {
        if (uuid === "" && action === "") {
            setUserSelected({ name: "", email: "", uuid: "" });
            setUserAction("")
        } else {
            const user = users.find(user => user.uuid === uuid);
            user ? setUserSelected(user) : setUserSelected({ name: "", email: "", uuid: "" });
            USER_ACTIONS.includes(action.toLowerCase()) ? setUserAction(action) : setUserAction("");
        }
    }

    function toggleModal() {
        setModalUserAction(!modalUserAction);
    }

    return (
        <div className="UsersTable">
            {
                modalUserAction && userAction !== "" && (
                    <Modal
                        title={`${userAction} user`}
                        content={modalUserActionContent}
                        modalStatus={modalUserAction}
                        setModalStatus={setModalUserAction} ></Modal>
                )
            }
            <h3>{showUserLogs ? "User Logs" : "Users Table"}</h3>
            {
                !showUserLogs && (
                    <table className="MAIN-table" role="table">
                        <thead role="rowgroup">
                            <tr role="row">
                                <th role="columnheader">Name</th>
                                <th role="columnheader">Email</th>
                                <th role="columnheader">Last seen</th>
                                <th role="columnheader">Blocked</th>
                                <th role="columnheader">Actions</th>
                            </tr>
                        </thead>
                        <tbody role="rowgroup">
                            {users && (
                                users.map((user, index) => (
                                    <UsersTableRow
                                        user={user}
                                        key={index}
                                        toggleModal={toggleModal}
                                        setShowUserLogs={setShowUserLogs}
                                        selectUserAction={selectUserAction} />
                                ))
                            )}
                        </tbody>
                    </table>
                )
            }
            {
                showUserLogs && (
                    <Suspense fallback={<Loader />}>
                        <UsersLogs
                            user={userSelected}
                            setShowUserLogs={setShowUserLogs}
                            selectUserAction={selectUserAction}
                        />
                    </Suspense>
                )
            }
        </div>
    );
}
export default UsersTable;