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
        // console.log("hello")
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

    // function clickHandlerNoAnswerNeeded(/**Number*/ id, /**Bool*/ markNoAnswer) {
    //     markNoAnswer ? setSelectedAction(ACTIONS.noAnswerNeeded) : setSelectedAction(ACTIONS.answerNeeded);
    //     setSelectedMessageId(id);
    //     setDisplayModal(true);
    // }
    // function clickHandlerMarkAnswer(/**Number*/ id, /**String*/ answeredBy = "", /**String*/ answer = "") {
    //     setSelectedAction(ACTIONS.markAnswered);
    //     setSelectedMessageId(id);
    //     setMarkAnswered({ answeredBy: answeredBy, answer: answer });
    //     setDisplayModal(true);
    // }
    // function clickHandlerChangeFlag(/**Number*/ id, /**String*/ currentFlagColour) {
    //     setSelectedAction(ACTIONS.changeFlag);
    //     setSelectedMessageId(id);
    //     setMarkColourChange({ currentFlagColour: currentFlagColour })
    //     setDisplayModal(true);
    // }
    // function clickHandlerDeleteMessage(/**Number*/ id) {
    //     setSelectedAction(ACTIONS.deleteMessage);
    //     setSelectedMessageId(id);
    //     setDisplayModal(true);
    // }

    let aMessage = {
        "id": 1,
        "date": "Tue, 09 Jan 2024 21:07:38 GMT",
        "senderName": "John",
        "senderEmail": "john@example.com",
        "subject": "oops",
        "message": "Hi, I have a problem logging in.",
        "flagged": "blue",
        "answerNeeded": true,
        "senderIsUser": true,
        "wasAnswered": false,
        "answeredBy": "",
        "answerDate": "",
        "answer": "",
        "isSpam": false,
        "userId": 5
    }
    let a2Message = {
        "id": 1,
        "date": "Tue, 09 Jan 2024 21:07:38 GMT",
        "senderName": "John",
        "senderEmail": "john@example.com",
        "subject": "helooo",
        "message": "Hi, I have a problem logging in.",
        "flagged": "blue",
        "answerNeeded": false,
        "wasAnswered": true,
        "senderIsUser": false,
        "answeredBy": "j@hhhshsidndd.com",
        "answerDate": "Tue, 09 Jan 2024 21:07:38 GMT",
        "answer": "kdbkdvbs djhcbvhcd shbkhb sajhsbashcabv shcbdchkbcd kbkdbkdc hvhdvdlhvdc askhbckhcd",
        "isSpam": true,
        "userId": 0
    }
    let a3Message = {
        "id": 3,
        "date": "Tue, 09 Jan 2024 21:07:38 GMT",
        "senderName": "John",
        "senderEmail": "john@example.com",
        "subject": "zyagss",
        "message": "Hi, I have a problem logging in.",
        "flagged": "red",
        "answerNeeded": false,
        "wasAnswered": false,
        "senderIsUser": true,
        "answeredBy": "",
        "answerDate": "",
        "answer": "",
        "isSpam": false,
        "userId": 8
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
                {/* <Message
                    isAdminComponent={true}
                    theMessage={aMessage}
                    clickHandler={clickHandler}
                />
                <Message
                    isAdminComponent={true}
                    theMessage={a2Message}
                    clickHandler={clickHandler}
                />
                <Message
                    isAdminComponent={true}
                    theMessage={a3Message}
                    clickHandler={clickHandler}
                /> */}
            </section>

            {/* {
                messages && messages.length <0 && (
                    messages.map((item, index) => (
                        <Message
                            isAdminComponent={true}
                            theMessage={item}
                            clickHandler={clickHandler}
                            key={index}
                        />
                    ))
                )
            } */}


            {/* {
                messages && messages.length > 0 && (
                    <>
                        {messages && (
                            messages.map((message, index) => (
                                <UserMessageContainer
                                    theMessage={message}
                                    key={index}
                                />
                            ))
                        )}
                    </>
                )
            }
            {
                ((messages && messages.length == 0) || (!messages)) && (
                    <p><b>No message found.</b></p>
                )
            } */}
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