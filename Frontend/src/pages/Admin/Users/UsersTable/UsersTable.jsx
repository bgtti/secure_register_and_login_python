import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted";
import { getAllUsers } from "../../../../config/apiHandler/admin/users";
import { getLastMonthDate } from "../../../../utils/helpers";
import { setLoader } from "../../../../redux/loader/loaderSlice";
import Modal from "../../../../components/Modal/Modal";
import ModalUserAction from "../ModalUserAction/ModalUserAction";
import FilterTable from "./FilterTable/FilterTable"
import SearchTable from "./SearchTable/SearchTable";
import Table from "./Table/Table";
import Pagination from "../Pagination/Pagination"
import "./usersTable.css"

/**
 * Component shows table with all users, with modal for selected actions, as well as filter/search tabler options.
 * 
 * @returns {React.ReactElement}
 */
function UsersTable() {
    const dispatch = useDispatch();

    // Only set state if component is mounted
    const isComponentMounted = useIsComponentMounted();

    //All users to be displayed in Table component
    const [users, setUsers] = useState([]);

    //Pagination
    const [currentPage, setCurrentPage] = useState(1); // display this page of results
    const [totalPages, setTotalPages] = useState(1); // the total amount of pages of results

    //Table options for FilterTable component
    const [tableOptions, setTableOptions] = useState({
        itemsPerPage: "25",
        orderBy: "last_seen",
        orderSort: "descending",
        filterBy: "none",
        filterByFlag: "blue",
        filterByLastSeen: getLastMonthDate()
    })

    const FILTER_APPLIED = {
        is_blocked: "Filtering blocked users.",
        is_unblocked: "Filtering unblocked users.",
        flag: "Filtering users by flag colour.",
        flag_not_blue: "Filtering flagged users.",
        is_admin: "Fitering by user type admin.",
        is_user: "Fitering by user type regular.",
        last_seen: "Fitering by last seen online."
    }

    //Search options for SearchTable component
    const [searchOptions, setSearchOptions] = useState({
        searchBy: "none",
        searchWord: ""
    })

    //Store user selected from table's action buttons and the button's action
    const [userSelected, setUserSelected] = useState({ name: "", email: "", id: 0 })
    const [userAction, setUserAction] = useState("")

    //Actions allowed from this component (more actions are accepted by modalUserAction)
    const ACTIONS = ["delete", "block", "unblock"]

    //If a user is modified, request updated data
    const [updateData, setUpdateData] = useState(false)

    //Modal will open to perform selected action modal is displayed
    const [displayModal, setDisplayModal] = useState(false)

    //Modal setup: used in modal wrapper
    displayModal ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");
    const modalContent = displayModal && userAction !== "" && (
        <ModalUserAction user={userSelected} action={userAction} modalToggler={toggleModal} setUpdateData={setUpdateData} />
    );


    //Request data when component mounts, when data changes, or when user sets filter or search options
    useEffect(() => {
        getUsers();
    }, [searchOptions, tableOptions])

    useEffect(() => {
        if (updateData) {
            getUsers();
            setUpdateData(false);
        }
    }, [updateData])

    /**
     * Defines the userAction and userSelected states.
     * @param {number} id the id of the selected user
     * @param {string} action one of ACTIONS = ["delete", "block", "unblock"]
     * @returns {void}
     */
    function selectUserAction(id = 0, action = "") {
        if (id === 0 && action === "") {
            setUserSelected({ name: "", email: "", id: 0 });
            setUserAction("")
        } else {
            const user = users.find(user => user.id === id);
            user ? setUserSelected(user) : console.error("User not found. Could not select action.");
            ACTIONS.includes(action) ? setUserAction(action) : console.error("Invalid action. Could not select action.");
        }
    }

    /**
     * Toggles modalUserAction display
     */
    function toggleModal() {
        setDisplayModal(!displayModal);
    }

    /**
     * Fetch user table data
     * 
     * @param {number} [pageNr = 1] integer, must be positive
     * @returns {void} 
     * @example
     * //Input example:
     * getUsers() => will get the first page of the users table, according to the options saved in tableOptions & searchOptions state.
     */
    function getUsers(pageNr = 1) {
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

    //Filter and search options should only be shown if users actually exist
    let filterActive = tableOptions.filterBy !== "none";
    let searchActive = (searchOptions.searchWord !== "" && searchOptions.searchBy !== "none");
    let filterAndSearchActive = filterActive && searchActive;

    let usersMightExist = (users && users.length >= 0) || ((!users || users.length === 0) && (filterActive || searchActive))

    return (
        <div className="Users UsersTable">
            {
                displayModal && userAction !== "" && (
                    <Modal
                        title={`${userAction} user`}
                        content={modalContent}
                        modalStatus={displayModal}
                        setModalStatus={setDisplayModal} ></Modal>
                )
            }

            <h3>Users Table</h3>

            {/* Filter and Search only shown if users might exist in the database */}
            {
                usersMightExist && (
                    <div className="UsersTable-containerFilters">
                        <div className="UsersTable-btnFilters">
                            <FilterTable
                                tableOptions={tableOptions}
                                setTableOptions={setTableOptions}
                            />
                            <SearchTable
                                searchOptions={searchOptions}
                                setSearchOptions={setSearchOptions}
                            />
                        </div>
                        <div className="UsersTable-filterInfo">
                            <p><b>Current filters being applied:</b></p>
                            {
                                filterActive && (
                                    <p>{FILTER_APPLIED[tableOptions.filterBy]}</p>
                                )
                            }
                            {
                                searchActive && (
                                    <p>Filtering by {searchOptions.searchBy} with search keyword. </p>
                                )
                            }
                            {
                                !filterAndSearchActive && (
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
                            (!filterAndSearchActive) ? (
                                "No users found. Please reset the filters and try again."
                            ) : (
                                "You do not have any users yet."
                            )
                        }
                    </p>
                )
            }
        </div>
    );
}
export default UsersTable;