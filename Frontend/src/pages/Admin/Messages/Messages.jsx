import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useDispatch } from "react-redux";
import useIsComponentMounted from "../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../redux/loader/loaderSlice";
import { PATH_TO } from "../../../router/routePaths.js";
import { getAllMessages } from "../../../config/apiHandler/admin/messages.js";
import Modal from "../../../components/Modal/Modal.jsx";
import ModalMessageAction from "./ModalMessageAction/ModalMessageAction.jsx";
import Message from "../../../components/Message/Message.jsx";
import Pagination from "../../../components/Pagination/Pagination.jsx";
import FilterMessages from "./FilterMessages/FilterMessages.jsx";
//import { getMessages } from "../../../../config/apiHandler/admin/userMessages.js" ///CHAANGE
import "./messages.css"


//=> TODO: pagination not working properly
//=> TODO: adapt filter "Filter" to include answered messages


const ACTIONS = {
    answer: "Admin answer",
    delete: "Delete message",
    flag: "Change message flag",
    markAs: "Mark message as..."
}

/**
 * Component returns all messages received through the contact form
 * 
 * @returns {React.ReactElement}
 */
function Messages() {

    const dispatch = useDispatch();

    // Only set state if component is mounted
    const isComponentMounted = useIsComponentMounted();

    // Store messages and pagination
    const [messages, setMessages] = useState([]);
    const [curPage, setCurPage] = useState([]);
    const [tPages, setTPages] = useState([]);

    // Filter
    const [filterOptions, setFilterOptions] = useState({
        itemsPerPage: 25,
        orderSort: "descending",
        filterBy: "answer_needed",
        showSpam: false,
    });

    // If messages do not exist, filter will not be displayed
    let messagesMightExist = (messages && messages.length >= 0) || ((!messages || messages.length === 0) && (filterOptions !== "all"))

    // Selected Action
    const [selectedAction, setSelectedAction] = useState("")
    const [selectedMessage, setSelectedMessage] = useState(false)

    // Some actions require more data to be passed on from the Mesage component to the modal executing the action. To mark a message as answered, markAnswered data is needed . To change a message flag, markColourChange is needed.
    const [markAnswered, setMarkAnswered] = useState({ answeredBy: "", answer: "" })
    const [markColourChange, setMarkColourChange] = useState({ currentFlagColour: "blue" })

    //If a message is modified, request updated data
    const [updateData, setUpdateData] = useState(false)

    //Modal
    const [displayModal, setDisplayModal] = useState(false)

    displayModal ? document.body.classList.add("Modal-active") : document.body.classList.remove("Modal-active");

    const modalCanBeDisplayed = (displayModal && selectedAction !== "" && selectedMessage)
    const modalContent = modalCanBeDisplayed && (
        <ModalMessageAction
            theMessage={selectedMessage}
            action={selectedAction}
            modalToggler={toggleModal}
            setUpdateData={setUpdateData} />
    );

    // Request messages upon component mount and after changes are made
    useEffect(() => {
        getMessages();
    }, [filterOptions])

    useEffect(() => {
        if (updateData) {
            setSelectedAction("");
            setSelectedMessage(false);
            getMessages();
            setUpdateData(false);
        }
    }, [updateData])

    /**
     * Toggles ModalMessageAction display
     */
    function toggleModal() {
        setDisplayModal(!displayModal);
    }

    /**
     * Fetch message data
     * 
     * @param {number} [pageNr = 1] integer, must be positive
     * @returns {void} 
     */
    function getMessages(pageNr = 1) {
        dispatch(setLoader(true))
        const queryObj = {
            pageNr: pageNr,
            itemsPerPage: filterOptions.itemsPerPage,
            orderSort: filterOptions.orderByDate,
            filterBy: filterOptions.filterBy,
            includeSpam: filterOptions.showSpam
        }
        getAllMessages(queryObj)
            .then(response => {
                if (isComponentMounted()) {
                    setMessages(response.messages);
                    setCurPage(response.currentPage);
                    setTPages(response.totalPages);
                    if (!response.data) { console.warn("No message data") }
                }
            })
            .catch(error => { console.warn("getAllMessages encountered an error", error); })
            .finally(() => { dispatch(setLoader(false)); })
    }

    /**
     * Fetch new page of message data
     * 
     * @param {number} [newPage] desired page number as integer, must be positive
     * @returns {void} 
     */
    function handlePagination(newPage) {
        if (Number.isInteger(newPage) && newPage >= 1 && newPage <= totalPages) {
            getMessages(newPage);
        }
    }

    // Click handlers to be sent to Message component
    function clickHandler(messageObj, action) {
        if (!ACTIONS.hasOwnProperty(action)) { console.error("Invalid message action."); return }
        setDisplayModal(true);
        setSelectedAction(action);
        setSelectedMessage(messageObj);
    }


    return (
        <div className="Messages">
            {
                modalCanBeDisplayed && (
                    <Modal
                        title={ACTIONS[selectedAction]}
                        content={modalContent}
                        modalStatus={displayModal}
                        setModalStatus={setDisplayModal} ></Modal>
                )
            }

            <h3>Messages</h3>

            {/* Filter only shown if messages might exist in the database */}

            <section>
                <FilterMessages
                    filterOptions={filterOptions}
                    setFilterOptions={setFilterOptions}
                />
            </section>

            <section className="Messages-MessageBoxSection">
                {
                    messages && messages.length > 0 && (
                        messages.map((item, index) => (
                            <Message
                                isAdminComponent={true}
                                theMessage={item}
                                clickHandler={clickHandler}
                                key={index}
                            />
                        ))
                    )
                }
                {
                    ((messages && messages.length == 0) || (!messages)) && (
                        <p><b>No message found.</b></p>
                    )
                }
            </section>

            {
                tPages > 1 && (
                    <Pagination
                        currentPage={curPage}
                        totalPages={tPages}
                        handlePageChange={handlePagination}
                    />
                )
            }
        </div>
    );
}
export default Messages;