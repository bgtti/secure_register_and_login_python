import { useState, useEffect, lazy, Suspense } from "react";
import { getAllUsers } from "../../../config/apiHandler/admin.js"
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { setLoader } from "../../../redux/loader/loaderSlice"
import Modal from "../../../components/Modal/Modal";
import ModalUserAction from "./Modal/ModalUserAction.jsx";
import Loader from "../../../components/Loader";
import FilterUsersTable from "./FilterTable/FilterUsersTable.jsx";
import Table from "./Table/Table.jsx";
import "./usersTable.css"

/** 
 * @constant
 * @type {string[]}
 * @default 
 * ["delete", "block", "logs"]
*/
const USER_ACTIONS = ["delete", "block", "logs"]

const UsersLogs = lazy(() => import("./UsersLogs/UsersLogs.jsx"));

/**
 * Component for managing the component showing a table of all users, the component showing a user's log, or modal components to delete or block users.
 * 
 * UsersTable contains 4 child components: Table (shown by default), TableFilter (shown by default) UsersLogs (lazy loaded, shown if user selects it), Modal (shown if user selects it).
 * 
 * Attention: sensitive data. Admin access only.
 * 
 * Component passes props to children. Component accepts no props.
 * 
 * @todo implement pagination pages
 * @todo check table size since it is not adapting between width 970 and 600px
 * 
 * @visibleName Admin Area: Users' Table
 * @summary Table with all users. Manages user's log view, modals's display, and table filter.
 * @returns {React.ReactElement}
 */
function UsersTable() {
    const [users, setUsers] = useState([])
    const [userSelected, setUserSelected] = useState({ name: "", email: "", uuid: "" })
    const [userAction, setUserAction] = useState("")
    const [modalUserAction, setModalUserAction] = useState(false)
    const [showUserLogs, setShowUserLogs] = useState(false)

    const dispatch = useDispatch();
    const navigate = useNavigate();

    useEffect(() => {
        // dispatch(setLoader(true))
        // getAllUsers()
        //     .then(response => {
        //         setUsers(response.users);
        //     })
        // dispatch(setLoader(false));
        getUsers()

    }, [])

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

    /**
     * Toggles modal block user && modal delete user
     */
    function toggleModal() {
        setModalUserAction(!modalUserAction);
    }

    /**
     * Uses the function getAllUsers to make an api call to fetch user data.
     * Hover over getAllUsers to see the required parameters.
     */
    function getUsers(pageNr = 1, itemsPerPage = 25, orderBy = "last_seen", orderSort = "descending", filterBy = "none") {
        const data = {
            page_nr: pageNr,
            items_per_page: itemsPerPage,
            order_by: orderBy,
            order_sort: orderSort,
            filter_by: filterBy
        }
        dispatch(setLoader(true))
        getAllUsers(data)
            .then(response => {
                setUsers(response.users);
            })
        dispatch(setLoader(false));
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
                    <FilterUsersTable />
                )
            }
            {
                !showUserLogs && users && (
                    <Table
                        users={users}
                        toggleModal={toggleModal}
                        setShowUserLogs={setShowUserLogs}
                        selectUserAction={selectUserAction}
                    />
                )
            }
            {
                !users && (
                    <p>You do not have any users.</p>
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