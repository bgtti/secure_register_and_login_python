import { useState, useEffect, useRef } from "react";
import { PropTypes } from "prop-types";
import { useDispatch, useSelector } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { markMessageAs, answerMessage, changeMessageFlag, deleteMessage } from "../../../../config/apiHandler/admin/messageActions.js"
import { FLAG_TYPES } from "../../../../utils/constants.js";
import ActionAnswer from "./ActionAnswer.jsx";
import ActionChangeFlag from "./ActionChangeFlag.jsx";
import ActionDeleteMessage from "./ActionDelete.jsx";
import ActionMarkAs from "./ActionMarkAs.jsx";
import { getTodaysDate, dateToYYYYMMDD } from "../../../../utils/helpers.js";
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

//**** */=> MISSING: sender is spammer!!

/**
 * Component returns fragment with action that can be carried out on a message.
 * 
 * This component should be included inside the modal wrapper found at src>components>Modal through props.
 * This component is itself a wrapper as well, it's content being a fragment imported from a component in the same folder whose name starts with 'Action'. The 'action' passed as prop to this component will determine it's content.
 * 
 * @visibleName Admin Area: Messages: ModalMessageAction
 * @param {object} props
 * @param {string} props.action accepts one of ["answer", "delete", "flag", "markAs"]
 * @param {object} props.theMessage
 * @param {number} props.theMessage.id message id as a positive int
 * @param {string} props.theMessage.date //.. WHY
 * @param {string} props.theMessage.senderName //..WHY
 * @param {string} props.theMessage.senderEmail //..WHY
 * @param {bool} props.theMessage.senderIsUser //required for 'marked as'
 * @param {string} props.theMessage.message //..WHY
 * @param {string} props.theMessage.subject //required for answer recording
 * @param {string} props.theMessage.flagged //required for flag change
 * @param {bool} props.theMessage.answerNeeded //required for answer recording
 * @param {bool} props.theMessage.wasAnswered //required for 'marked as' & answer
 * @param {string} props.theMessage.answeredBy //required for answer recording
 * @param {string} props.theMessage.answerDate //required for answer recording
 * @param {string} props.theMessage.answer //required for answer recording
 * @param {bool} props.theMessage.isSpam //required to 'mark as'
 * @param {func} props.toggleModal 
 * @param {func} props.setUpdateData //..set to true when api request sent
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
    const { action: originalAction, theMessage, modalToggler, setUpdateData = "" } = props; //toggleModal instead of modalToggler ??????
    const { id, date, senderName, senderEmail, senderIsUser, subject, message, flagged, answerNeeded, wasAnswered, answeredBy, answerDate, answer, isSpam } = theMessage; //previously messageData

    const dispatch = useDispatch();


    //making sure action does not change when component re-renders
    const actionRef = useRef(originalAction);
    const action = actionRef.current;

    //setting the initial state
    function getOriginalState() {
        let oState;
        switch (action) {
            case "answer":
                const sub = subject === "no subject" ? "Contact Form Message" : subject
                const defaultSubjt = `Re: ${sub}`
                oState = {
                    answeredBy: wasAnswered ? answeredBy : useSelector((state) => state.user.email),
                    answerDate: wasAnswered ? dateToYYYYMMDD(answerDate) : getTodaysDate(),
                    answer: wasAnswered ? answer : "",
                    answerSend: wasAnswered ? false : true,
                    answerSubject: defaultSubjt
                };
                break
            case "markAs":
                oState = {
                    isSpam: isSpam,
                    answerNeeded: answerNeeded,
                    markSenderAsSpammer: false
                };
                break
            case "flag":
                oState = flagged;
                break
            case "delete":
                oState = false;
                break
            default:
                oState = false;
                console.error("Wrong action input in ModalMessageAction.")
        }
        return oState;
    }

    const originalState = getOriginalState();


    const [newState, setNewState] = useState(originalState)
    const [changesWereMade, setChangesWereMade] = useState(false) //possibly DELETE ==> no need?
    const [errorMessage, setErroMessage] = useState("")
    const [buttonText, setButtonText] = useState((action === "delete" ? "Delete" : "Save changes"))

    //if no changes are detected, do not make api call
    function stateHasChanged() {
        return JSON.stringify(originalState) !== JSON.stringify(newState);
    }

    //Check if an object has certain keys (used to make sure newState format is valid)
    function checkStateKeys(keys) {
        const hasKeys = keys.every(key => newState.hasOwnProperty(key));
        if (!hasKeys) { console.error("ModalMessageAction: newState rejected.") }
        return hasKeys
    }

    //Handle response
    const eText = "An error ocurred, please close this modal and try again."
    function responseSuccess() { setErroMessage(""); setUpdateData(true); modalToggler(); }
    function responseFail() { console.warn("ModalMessageAction: No message updates were possible."); setErroMessage(eText) }
    function warnError(action, error) { console.error(`Clickhandler case ${action} encountered an error`, error); setErroMessage(eText) }

    function clickHandler() {
        if (action !== "delete" && !stateHasChanged()) {
            return console.warn("No updates to message.") //=> TODO: THEN CLOSE MODAL (after asll cases are tested...)
        }

        switch (action) {
            case "answer":
                if (!checkStateKeys(["answeredBy", "answerDate", "answer", "answerSend", "answerSubject"])) { return }
                let obj = {
                    id: id,
                    answer: newState.answer,
                    subject: newState.answerSubject,
                    answeredBy: newState.answeredBy,
                    answerDate: newState.answerDate
                }
                dispatch(setLoader(true))
                answerMessage(obj, newState.answerSend)
                    .then(res => { res.success ? responseSuccess() : responseFail() })
                    .catch(error => { warnError(action, error) })
                    .finally(() => { dispatch(setLoader(false)); })
                break
            case "markAs":
                if (!checkStateKeys(["answerNeeded", "isSpam", "markSenderAsSpammer"])) { return }
                dispatch(setLoader(true))
                markMessageAs(id, newState.answerNeeded, newState.isSpam, newState.markSenderAsSpammer)
                    .then(res => { res.success ? responseSuccess() : responseFail() })
                    .catch(error => { warnError(action, error); })
                    .finally(() => { dispatch(setLoader(false)); })
                break
            case "flag":
                if (!(newState && FLAG_TYPES.includes(newState))) {
                    return console.error("ModalMessageAction: newState rejected.")
                }
                dispatch(setLoader(true))
                changeMessageFlag(id, newState)
                    .then(res => { res.success ? responseSuccess() : responseFail() })
                    .catch(error => { warnError(action, error); })
                    .finally(() => { dispatch(setLoader(false)); })
                break
            case "delete":
                dispatch(setLoader(true))
                deleteMessage(id)
                    .then(res => { res.success ? responseSuccess() : responseFail() })
                    .catch(error => { warnError(action, error) })
                    .finally(() => { dispatch(setLoader(false)); })
                break
            default:
                console.error(`Wrong input in ModalMessageAction clickHandler. Action = ${action}`)
        }
    }

    return (
        <>
            <p>{ACTION_TEXT.action}</p>
            <br />
            {
                action === "answer" && (
                    <ActionAnswer
                        currentState={newState}
                        changeState={setNewState}
                        changeBtnText={setButtonText}
                        wasAnswered={wasAnswered}
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
                        changeState={setNewState}
                    />
                )
            }
            {
                action === "markAs" && (
                    <ActionMarkAs
                        currentState={newState}
                        changeState={setNewState}
                        senderIsUser={senderIsUser}
                        wasAnswered={wasAnswered}
                    />
                )
            }
            {!changesWereMade && (
                <>
                    <br />
                    <div className="Modal-BtnContainer">
                        <button className={action === "delete" ? "Modal-ActionDanger" : "Modal-ActionBtn"} disabled={(errorMessage !== "")} onClick={clickHandler}>{buttonText}
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
        date: PropTypes.string.isRequired, //dont really need (?)
        senderName: PropTypes.string.isRequired, //dont really need (?)
        senderEmail: PropTypes.string.isRequired,
        subject: PropTypes.string.isRequired, //dont really need (?)
        message: PropTypes.string.isRequired, //dont really need (?)
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