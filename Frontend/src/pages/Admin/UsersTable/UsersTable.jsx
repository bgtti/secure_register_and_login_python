import { useState, useEffect, lazy, Suspense, useRef } from "react";
import { getAllUsers } from "../../../config/apiHandler/admin/users.js"
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { setLoader } from "../../../redux/loader/loaderSlice"
import { getLastMonthDate } from "../../../utils/helpers";
import useIsComponentMounted from "../../../hooks/useIsComponentMounted.js";
import Modal from "../../../components/Modal/Modal";
import ModalUserAction from "./Modal/ModalUserAction.jsx";
import Loader from "../../../components/Loader";
import FilterUsersTable from "./FilterTable/FilterUsersTable.jsx";
import SearchUser from "./SearchUser/SearchUser.jsx";
import Table from "./Table/Table.jsx";
import Pagination from "./Pagination/Pagination.jsx";
import "./usersTable.css"

// *** CONSTANTS ***
/** 
 * Constants for defining set filter message
 * @constant
 * @type {string{}}
*/
const FILTER_APPLIED = {
    is_blocked: "Filtering blocked users.",
    is_unblocked: "Filtering unblocked users.",
    flag: "Filtering users by flag colour.",
    flag_not_blue: "Filtering flagged users.",
    is_admin: "Fitering by user type admin.",
    is_user: "Fitering by user type regular.",
    last_seen: "Fitering by last seen online."
}

/** 
 * Constants for defining user actions on click events
 * @constant
 * @type {string[]}
 * @default 
 * ["delete", "block", "logs"]
*/
const USER_ACTIONS = ["delete", "block", "unblock", "flag", "type change", "logs", "userInfo"]

// *** LAZY LOADS ***

const UsersLogs = lazy(() => import("./UsersLogs/UsersLogs.jsx"));
const UserInformation = lazy(() => import("./UserInformation/UserInformation.jsx"));

// *** COMPONENT ***

/**
 * Component for managing the component showing a table of all users, the component showing a user's log, or modal components to delete or block users.
 * 
 * UsersTable contains 4 child components: Table (shown by default), TableFilter (shown by default) UsersLogs (lazy loaded, shown if user selects it), Modal (shown if user selects it).
 * 
 * Attention: sensitive data. Admin access only.
 * 
 * Component passes props to children. Component accepts no props.
 * 
 * @todo implement API call for search user
 * @todo docstrings for search user
 * 
 * @visibleName Admin Area: Users' Table
 * @summary Table with all users. Manages user's log view, modals's display, and table filter.
 * @returns {React.ReactElement}
 */
function UsersTable() {
    const dispatch = useDispatch();

    // Only set state if component is mounted
    const isComponentMounted = useIsComponentMounted();

    // The following state is used to store users and pagination. The values are set from the response in the API request either at component mount (through the useEffect) or requests through the Pagination, FilterUsersTable, and SearchUser components which call the getUsers function (defined bellow) when called by admin users through click events.
    const [users, setUsers] = useState([]);
    const [currentPage, setCurrentPage] = useState(1); // display this page of results
    const [totalPages, setTotalPages] = useState(1); // the total amount of pages of results

    // The following items (tableOptions) are controlled by the FilterUsersTable component. Only specific (enum) values are allowed. Check the component for more information on allowed values. 
    const [tableOptions, setTableOptions] = useState({
        itemsPerPage: "25",
        orderBy: "last_seen",
        orderSort: "descending",
        filterBy: "none",
        filterByFlag: "blue",
        filterByLastSeen: getLastMonthDate()
    })

    // The following items (searchOptions) are controlled by the by the SearchUser component. Only specific values are allowed for 'searchBy'. Check the component for more information
    const [searchOptions, setSearchOptions] = useState({
        searchBy: "none",
        searchWord: ""
    })

    // The following state is used for storing selected user action and modal display (block/delete user or show user's logs). They are set from the Table component.
    const [userSelected, setUserSelected] = useState({ name: "", email: "", id: 0 })
    const [userAction, setUserAction] = useState("")
    const [modalUserAction, setModalUserAction] = useState(false)
    const [showUserInfo, setShowUserInfo] = useState(false) //lazy loaded component
    const [showUserLogs, setShowUserLogs] = useState(false) //lazy loaded component

    // If changes are made to the user's table (blocking/unblocking/deleting a user), reload user's table
    const [reloadUsersTable, setReloadUsersTable] = useState(false)

    //Pulling new user data when user changes tableOptions or searches:
    useEffect(() => {
        getUsers();
    }, [searchOptions, tableOptions])

    //Pulling new user data when a user from table is changed:
    useEffect(() => {
        if (reloadUsersTable) {
            getUsers();
            setReloadUsersTable(false);
        }
    }, [reloadUsersTable])

    // Setting up the modal content and managing user action triggered by click events in child components:
    modalUserAction ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");
    const modalUserActionContent = modalUserAction && userAction !== "" && (
        <ModalUserAction user={userSelected} action={userAction} modalToggler={toggleModal} setReloadUsersTable={setReloadUsersTable} />
    );

    /**
     * Defines the userAction and userSelected states in UsersTable component.
     * Should be combined with setShowUserLogs (to show/hide UsersLogs component) or toggleModal (to show/hide block user or delete user modals)
     * @param {number} id the id of the selected user
     * @param {string} action one of constant USER_ACTIONS -> ["delete", "block", "unblock", "logs", "userInfo"]
     * @returns {void}
     */
    function selectUserAction(id = 0, action = "") {
        if (id === 0 && action === "") {
            setUserSelected({ name: "", email: "", id: 0 });
            setUserAction("")
        } else {
            const user = users.find(user => user.id === id);
            user ? setUserSelected(user) : setUserSelected({ name: "", email: "", id: 0 });
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
     * Uses the function getAllUsers (from apiHandler) to make an api call to fetch user data. If component is mounted, will update the state, showing the users in table format.
     * 
     * This function is currently being called when the following state updates: tableOptions & searchOptions.
     * 
     * This function takes the optional parameter of page number, and will use the state to send the required parameters of the getAllUsers.
     * 
     * @param {number} [pageNr = 1] integer, must be positive
     * @returns {void} 
     * @example
     * //Input example:
     * getUsers() => will get the first page of the users table, according to the options saved in tableOptions & searchOptions state.
     */
    function getUsers(pageNr = 1) {
        //check data consistency
        let searchByIsConsistent = ((searchOptions.searchWord === "" && searchOptions.searchBy === "none") || (searchOptions.searchWord !== "" && searchOptions.searchBy !== "none"));
        if (!searchByIsConsistent) {
            console.warn(`Data inconsistency: searchBy = ${searchOptions.searchBy} & searchWord = ${searchOptions.searchWord}`)
        }
        const data = {
            pageNr: pageNr,
            itemsPerPage: tableOptions.itemsPerPage,
            orderBy: tableOptions.orderBy,
            orderSort: tableOptions.orderSort,
            filterBy: tableOptions.filterBy,
            filterByFlag: tableOptions.filterByFlag,
            filterByLastSeen: tableOptions.filterByLastSeen,
            searchBy: searchOptions.searchWord === "" ? "none" : searchOptions.searchBy,
            searchWord: searchOptions.searchBy === "none" ? "" : searchOptions.searchWord
        }
        dispatch(setLoader(true))
        getAllUsers(data)
            .then(response => {
                if (isComponentMounted()) {
                    if (response.data) {
                        setUsers(response.users);
                        setCurrentPage(response.currentPage);
                        setTotalPages(response.totalPages);
                    } else {
                        setUsers([]);
                        setCurrentPage(1);
                        setTotalPages(1);
                    }
                }
            })
            .catch(error => {
                console.warn("getUsers (in UsersTable) encountered an error", error);
            })
            .finally(() => {
                dispatch(setLoader(false));
            })
    };

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
                !showUserLogs && !showUserInfo && (
                    <>
                        {
                            ((users && users.length >= 0) || ((!users || users.length === 0) && (tableOptions.filterBy !== "none"))) && (
                                <div className="UsersTable-containerFilters">
                                    <div className="UsersTable-btnFilters">
                                        <FilterUsersTable
                                            tableOptions={tableOptions}
                                            setTableOptions={setTableOptions}
                                        />
                                        <SearchUser
                                            searchOptions={searchOptions}
                                            setSearchOptions={setSearchOptions}
                                        />
                                    </div>
                                    <div className="UsersTable-filterInfo">
                                        <p><b>Current filters being applied:</b></p>
                                        {
                                            tableOptions.filterBy !== "none" && (
                                                <p>{FILTER_APPLIED[tableOptions.filterBy]}</p>
                                            )
                                        }
                                        {
                                            searchOptions.searchBy !== "none" && searchOptions.searchWord !== "" && (
                                                <p>Filtering by {searchOptions.searchBy} with search keyword. </p>
                                            )
                                        }
                                        {
                                            tableOptions.filterBy === "none" && (searchOptions.searchWord === "" || searchOptions.searchBy === "none") && (
                                                <p>No filters active. Showing result for all users.</p>
                                            )
                                        }
                                    </div>
                                </div>
                            )
                        }
                        {
                            users && users.length > 0 && (
                                <>
                                    <Table
                                        users={users}
                                        toggleModal={toggleModal}
                                        setShowUserInfo={setShowUserInfo}
                                        selectUserAction={selectUserAction}
                                    />
                                    {
                                        totalPages > 1 && (
                                            <Pagination
                                                currentPage={currentPage}
                                                totalPages={totalPages}
                                                handlePageChange={handlePageChange}
                                            />
                                        )
                                    }
                                </>
                            )
                        }
                        {
                            (!users || users.length === 0) && (
                                <p className="UsersTable-noTable">
                                    {
                                        (tableOptions.filterBy !== "none" || tableOptions.searchBy !== "none") ? (
                                            "No users found. Please reset the filter and try again."
                                        ) : (
                                            "You do not have any users yet."
                                        )
                                    }
                                </p>
                            )
                        }
                    </>
                )
            }
            {/* Clicking the more info button on a user in the table will lead to the user's UserInformation page: */}
            {
                showUserInfo && (
                    <Suspense fallback={<Loader />}>
                        <UserInformation
                            userId={userSelected.id}
                            setShowUserInfo={setShowUserInfo}
                            setShowUserLogs={setShowUserLogs}
                            selectUserAction={selectUserAction}
                            toggleModal={toggleModal}
                        />
                    </Suspense>
                )
            }
            {/* Inside the UserInformation page, clicking on the show logs button will lead to the User's logs page: */}
            {
                showUserLogs && (
                    <Suspense fallback={<Loader />}>
                        <UsersLogs
                            user={userSelected}
                            setShowUserInfo={setShowUserInfo}
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