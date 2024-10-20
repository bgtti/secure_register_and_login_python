import { useState } from "react";
import { PropTypes } from "prop-types";
import { useDispatch, useSelector } from "react-redux";
import useIsComponentMounted from "../../../../hooks/useIsComponentMounted.js";
import { setLoader } from "../../../../redux/loader/loaderSlice.js"
import { markMessageNoAnswerNeeded, markMessageAnswered, changeMessageFlag, deleteMessage } from "../../../../config/apiHandler/admin/messageActions.js"
import { FLAG_TYPES } from "../../../../utils/constants.js";
// import "./modalUserAction.css"

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
 * @param {string} props.action accepts only one of ["noAnswerNeeded", "answerNeeded", "markAnswered", "changeFlag", "deleteMessage"]
 * @param {number} props.id message id as an int
 * @param {string} [props.flag] pass flag color as a parameter if action === "changeFlag"
 * @param {string} [props.answeredBy] pass answeredBy as a parameter if action === "markAnswered"
 * @param {string} [props.answer] pass answer as a parameter if action === "markAnswered"
 * @param {func} props.toggleModal 
 * @param {func} props.setUpdateData 
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
    const { action, id, flag = "blue", answeredBy = "", answer = "", modalToggler, setUpdateData } = props;

    const isComponentMounted = useIsComponentMounted();
    const dispatch = useDispatch();

    const [errorMessage, setErroMessage] = useState("")
    const [changesWereMade, setChangesWereMade] = useState(false)

    const [messageFlag, setMessageFlag] = useState(flag)//only used when changing flag color

    const [messageAnsweredBy, setMessageAnsweredBy] = useState(answeredBy)//only used when marking message as answered
    const [messageAnsweredText, setMessageAnsweredText] = useState(answer)//only used when marking message as answered

    function clickHandler() {
        dispatch(setLoader(true));

        const handleResponse = (response, successMessage) => {
            if (isComponentMounted()) {
                setErroMessage(response.success ? successMessage : "An error occurred. Please reload the page and try again.");
                if (response.success) {
                    setChangesWereMade(true);
                    setUpdateData(true);
                }
            }
        };

        const handleError = (error) => {
            console.warn("clickHandler in modal encountered an error", error);
        };

        const handleFinally = () => {
            dispatch(setLoader(false));
        };

        let requestAction;
        let responseActionMessage;

        switch (action) {
            case "noAnswerNeeded":
                requestAction = function () { return markMessageNoAnswerNeeded(id, true) };
                responseActionMessage = "Message marked as no answer needed!";
                break
            case "answerNeeded":
                requestAction = function () { return markMessageNoAnswerNeeded(id, false) };
                responseActionMessage = "Message marked as answer needed!";
                break
            case "markAnswered":
                requestAction = function () { return markMessageAnswered(id, messageAnsweredBy, messageAnsweredText) };
                responseActionMessage = "Message marked as answered!";
                break
            case "changeFlag":
                requestAction = function () { return changeMessageFlag(id, messageFlag) };
                responseActionMessage = "Message flag changed successfully!";
                break
            case "deleteMessage":
                requestAction = function () { return deleteMessage(id) };
                responseActionMessage = "Message deleted successfully!";
                break
            default:
                requestAction = function () { return console.error("Wrong action input in ModalMessageAction.") };
                responseActionMessage = "An error occurred: action input invalid.";
        }
        try {
            requestAction()
                .then(response => handleResponse(response, responseActionMessage))
                .catch(handleError)
                .finally(handleFinally);
        } catch {
            console.error("Error in ModalMessageAction", error);
            dispatch(setLoader(false));
        }
    }

    return (
        <>
            <p>{ACTION_TEXT.action}</p>
            <br />

            {
                action === "changeFlag" && (
                    <>
                        <p>Select the flag colour of the message:</p>
                        <br />
                        <p><b className="ModalMessageAction-Bold" >Flag: </b> {flag}</p>
                        <br />
                        <div className="MAIN-form-display-table ModalMessageAction-displayTable">
                            <label htmlFor="changeFlag">Select new flag colour:</label>
                            <select
                                className="ModalMessageAction-Select"
                                name="changeFlag"
                                id="changeFlag"
                                defaultValue={messageFlag}
                                disabled={changesWereMade ? true : false}
                                onChange={(e) => { setMessageFlag(e.target.value) }}>
                                {
                                    FLAG_TYPES.map((item, index) => (
                                        <option value={item} key={index}>{item}</option>
                                    ))
                                }
                            </select>
                        </div>
                    </>
                )
            }

            {
                action === "markAnswered" && (
                    <>
                        <br />
                        <div className="MAIN-form-display-table ModalMessageAction-displayTable">
                            <label htmlFor="answeredBy">Select new flag colour:</label>
                            <input
                                id="answeredBy"
                                defaultValue={messageAnsweredBy}
                                disabled={changesWereMade ? true : false}
                                name="answeredBy"
                                type="text"
                                onChange={(e) => { setMessageAnsweredBy(e.target.value) }} />
                        </div>
                        <br />

                        <div className="MAIN-form-display-table ModalMessageAction-displayTable">
                            <label htmlFor="answerText">Select new flag colour:</label>
                            <input
                                id="answerText"
                                defaultValue={messageAnsweredText}
                                disabled={changesWereMade ? true : false}
                                name="answerText"
                                type="text"
                                onChange={(e) => { setMessageAnsweredText(e.target.value) }} />
                        </div>
                    </>
                )
            }

            {
                action === "deleteMessage" && (
                    <>
                        <br />
                        <p>This action cannot be undone.</p>
                    </>
                )
            }

            {!changesWereMade && (
                <>
                    <br />
                    <div className="ModalMessageAction-BtnContainer">
                        <button className="ModalMessageAction-ActionBtn" disabled={(errorMessage !== "")} onClick={clickHandler}>{action === "deleteMessage" ? "Delete" : "Save changes"}
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
    action: PropTypes.oneOf(["noAnswerNeeded", "answerNeeded", "markAnswered", "changeFlag", "deleteMessage"]),
    id: PropTypes.number.isRequired,
    flag: PropTypes.string,
    answeredBy: PropTypes.string,
    answer: PropTypes.string,
    modalToggler: PropTypes.func.isRequired,
    setUpdateData: PropTypes.func.isRequired,
};

export default ModalMessageAction;