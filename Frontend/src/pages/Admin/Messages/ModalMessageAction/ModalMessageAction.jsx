import { useState } from "react";
import { PropTypes } from "prop-types";
import { useDispatch, useSelector } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { markMessageNoAnswerNeeded, markMessageAnswered, changeMessageFlag, deleteMessage } from "../../../../config/apiHandler/admin/messageActions.js"
import { FLAG_TYPES } from "../../../../utils/constants.js";
import ActionAnswer from "./ActionAnswer.jsx";
import ActionChangeFlag from "./ActionChangeFlag.jsx";
import ActionDeleteMessage from "./ActionDelete.jsx";
import ActionMarkAs from "./ActionMarkAs.jsx";
// import "./modalUserAction.css"

const MESSAGE_ACTIONS = ["answer", "delete", "flag", "markAs"]

const ACTION_TITLE = {
    noAnswerNeeded: "No answer needed",
    answerNeeded: "Answer needed",
    markAnswered: "Message answered",
    changeFlag: "Change message flag",
    deleteMessage: "Delete message"
}

const ACTION_TEXT = {
    noAnswerNeeded: "Set message status to 'no answer needed'.",
    answerNeeded: "Set message status to 'answer needed'.",
    markAnswered: "Mark message as answered.",
    changeFlag: "Change message flag colour.",
    deleteMessage: "You are about to delete this message."
}

const MESSAGE_ACTION_MODAL_TITLE = {
    markAs: "Mark answer as...",
    answer: "Admin answer",
    flag: "Change message flag",
    delete: "Delete message"
}

const MARK_AS_OPTS = {
    markSpam: "Message is spam",
    markNotSpam: "Message is not spam",
    markAnswerNeeded: "Answer is needed",
    markNoAnswerNeeded: "No answer is needed"
}


/**
 * Component returns fragment with action that can be carried out on a message.
 * 
 * This component should be included inside the modal wrapper found at src>components>Modal through props.
 * 
 * @visibleName Admin Area: Messages: ModalMessageAction
 * @param {object} props
 * @param {string} props.action accepts one of ["answer", "delete", "flag", "markAs"]
 * @param {object} props.theMessage
 * @param {number} props.theMessage.id message id as a positive int
 * @param {string} props.theMessage.date //..
 * @param {string} props.theMessage.senderName //..
 * @param {string} props.theMessage.senderEmail
 * @param {bool} props.theMessage.senderIsUser
 * @param {string} props.theMessage.message //..
 * @param {string} props.theMessage.subject //..
 * @param {string} props.theMessage.flagged
 * @param {bool} props.theMessage.answerNeeded
 * @param {bool} props.theMessage.wasAnswered
 * @param {string} props.theMessage.answeredBy
 * @param {string} props.theMessage.answerDate
 * @param {string} props.theMessage.answer
 * @param {bool} props.theMessage.isSpam
 * @param {func} props.toggleModal 
 * @param {func} props.setUpdateData //..
 * @returns {React.ReactElement}
 * 
 * @example
 * import Modal from ".../components/Modal/Modal"
 * import { useState} from "react";
 * //inside the functional component:
 * const [showModal, setShowModal] = useState(false)
 * function toggleModal() { setShowModal(!showModal)}
 * const modalInfo = <ModalMessageAction id={12} action="noAnswerNeeded" modalToggler={toggleModal} setUpdateData={setUpdateData}/> //<- refers to this component!
 * return (
 * <Modal title="Mark as no answer needed" content={modalInfo} modalStatus={showModal} setModalStatus={setShowModal} ></Modal> //<-the modal wrapper component with this component passed as a prop
 * )
 */
function ModalMessageAction(props) {
    const { action, theMessage, modalToggler, setUpdateData = "" } = props; //toggleModal instead of modalToggler ??????
    const { id, date, senderName, senderEmail, senderIsUser, subject, message, flagged, answerNeeded, wasAnswered, answeredBy, answerDate, answer, isSpam } = theMessage; //previously messageData

    let originalState;

    switch (action) {
        case "answer":
            originalState = {
                answeredBy: wasAnswered ? answeredBy : useSelector((state) => state.user.email),
                answerDate: wasAnswered ? answerDate : new Date().toJSON().slice(0, 10),
                answer: wasAnswered ? answer : ""
            };
            break
        case "markAs":
            originalState = {
                isSpam: isSpam,
                answerNeeded: answerNeeded,
                markSenderAsSpammer: false
            };
            break
        case "flag":
            originalState = flagged;
            break
        case "delete":
            originalState = false;
            break
        default:
            originalState = false;
            console.error("Wrong action input in ModalMessageAction.")
    }

    const [newState, setNewState] = useState(originalState)
    const [changesWereMade, setChangesWereMade] = useState(false)
    const [errorMessage, setErroMessage] = useState("")

    function stateHasChanged() {
        if (JSON.stringify(originalState) === JSON.stringify(newState)) { return true }
        else { return false }
    }

    function clickHandler() {
        console.log(`action = ${action}`)
        console.log(`state changed = ${stateHasChanged()}`)
        console.log(`new state = ${newState}`)
        console.log(`************************************`)
    }



    return (
        <>
            <p>{ACTION_TEXT.action}</p>
            <br />
            {
                action === "answer" && (
                    <ActionAnswer
                        changesWereMade={changesWereMade}
                        wasAnswered={wasAnswered}
                        answeredBy={answeredBy}
                        answerDate={answerDate}
                        answer={answer}
                    />
                )
            }
            {
                action === "delete" && (
                    <ActionDeleteMessage
                        isSpam={isSpam}
                        senderName={senderName}
                        senderEmail={senderEmail}
                    />
                )
            }

            {
                action === "flag" && (
                    <ActionChangeFlag
                        messageFlag={flagged}
                        changesWereMade={changesWereMade}
                        setMessageFlag={setNewState}
                    />

                )
            }
            {
                action === "markAs" && (
                    <ActionMarkAs
                        changesWereMade={changesWereMade}
                        isSpam={isSpam}
                        answerNeeded={answerNeeded}
                        wasAnswered={wasAnswered}
                        senderIsUser={senderIsUser}
                    />
                )
            }

            {!changesWereMade && (
                <>
                    <br />
                    <div className="Modal-BtnContainer">
                        <button className={action === "delete" ? "Modal-ActionDanger" : "Modal-ActionBtn"} disabled={(errorMessage !== "")} onClick={clickHandler}>{action === "delete" ? "Delete" : "Save changes"}
                        </button>
                        <button disabled={(errorMessage !== "")} onClick={modalToggler}>Cancel</button>
                    </div>
                </>
            )}

            {
                errorMessage !== "" && (
                    <>
                        <br />
                        <p className="MAIN-error-message">
                            <i>{errorMessage}</i>
                        </p>
                    </>
                )
            }
        </>
    );
};

ModalMessageAction.propTypes = {
    action: PropTypes.oneOf(["answer", "delete", "flag", "markAs"]),
    theMessage: PropTypes.shape({
        id: PropTypes.number.isRequired,
        date: PropTypes.string.isRequired, //dont really need
        senderName: PropTypes.string.isRequired, //dont really need
        senderEmail: PropTypes.string.isRequired,
        subject: PropTypes.string.isRequired, //dont really need
        message: PropTypes.string.isRequired, //dont really need
        flagged: PropTypes.string.isRequired,
        answerNeeded: PropTypes.bool.isRequired,
        wasAnswered: PropTypes.bool.isRequired,
        answeredBy: PropTypes.string.isRequired,
        answerDate: PropTypes.string.isRequired,
        answer: PropTypes.string.isRequired,
        senderIsUser: PropTypes.bool.isRequired,
        isSpam: PropTypes.bool.isRequired
    }).isRequired,
    modalToggler: PropTypes.func.isRequired,
    // setUpdateData: PropTypes.func.isRequired,
};

export default ModalMessageAction;