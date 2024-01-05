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
import Pagination from "./Pagination/Pagination.jsx";
import "./usersTable.css"

/** 
 * Constants for defining user actions on click events
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
    const dispatch = useDispatch();
    // State to store users and pagination:
    const [users, setUsers] = useState([])
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const itemsPerPage = 25;
    // State storing selected user action and modal display (block/delete user or show user's logs):
    const [userSelected, setUserSelected] = useState({ name: "", email: "", uuid: "" })
    const [userAction, setUserAction] = useState("")
    const [modalUserAction, setModalUserAction] = useState(false)
    const [showUserLogs, setShowUserLogs] = useState(false)

    //Pulling the first page of user data when page loads:
    useEffect(() => {
        getUsers()
    }, [])

    //Setting up the modal content and managing user action triggered by click events in child components:
    modalUserAction ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");
    const modalUserActionContent = modalUserAction && userAction !== "" && (
        <ModalUserAction user={userSelected} action={userAction} modalToggler={toggleModal} />
    );

    /**
     * Defines the userAction and userSelected states in UsersTable component
     * Should be combined with setShowUserLogs (to show/hide UsersLogs component) or toggleModal (to show/hide block user or delete user modals)
     * @param {string} uuid the uuid of the selected user
     * @param {string} action must be member of the constant USER_ACTIONS ("delete", "block", "logs")
     * @returns {void}
     */
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
     * Toggles the display (state) of modal block user or modal delete user, depending on which one is selected
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
                setTotalPages(response.totalPages);
                setCurrentPage(response.currentPage);
            })
        dispatch(setLoader(false));
    }

    /**
     * Accepts desired page as an argument and requests users for that page, setting users state in UsersTable.
     * @param {number} newPage must be positive int
     * @returns {void}
     */
    function handlePageChange(newPage) {
        if (Number.isInteger(newPage) && newPage >= 1 && newPage <= totalPages) {
            getUsers(newPage);
        }
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
                !showUserLogs && users && (
                    <>
                        <FilterUsersTable />
                        <Table
                            users={users}
                            toggleModal={toggleModal}
                            setShowUserLogs={setShowUserLogs}
                            selectUserAction={selectUserAction}
                        />
                        <Pagination
                            currentPage={currentPage}
                            totalPages={totalPages}
                            handlePageChange={handlePageChange}
                        />
                    </>
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