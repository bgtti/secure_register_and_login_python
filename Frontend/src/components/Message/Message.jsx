import PropTypes from "prop-types";
import Flag from "../Flag/Flag";
import "./message.css"

/**
 * Component returns a message box with its content.
 * Messages sent through the site's contact form can be individually displayed using this message box.
 * 
 * @visibleName Message Box
 * @param {object} props
 * @param {bool} props.isAdminComponent // indicates whether this component will be used in the adminArea or visible to all users
 * @param {object} props.theMessage
 * @param {number} props.theMessage.id // number should be int
 * @param {string} props.theMessage.date
 * @param {string} props.theMessage.senderName
 * @param {string} props.theMessage.senderEmail
 * @param {string} props.theMessage.message
 * @param {string} props.theMessage.flagged
 * @param {bool} props.theMessage.answerNeeded
 * @param {bool} props.theMessage.wasAnswered
 * @param {string} props.theMessage.answeredBy
 * @param {string} props.theMessage.answerDate
 * @param {string} props.theMessage.answer
 * @param {func} [props.clickHandlerNoAnswerNeeded] //Click handler needed if isAdminComponent, should accept message id
 * @param {func} [props.clickHandlerMarkAnswer] //Click handler needed if isAdminComponent, should accept message id
 * @param {func} [props.clickHandlerChangeFlag] //Click handler needed if isAdminComponent, should accept message id
 * @param {func} [props.clickHandlerDeleteMessage] //Click handler needed if isAdminComponent, should accept message id
 * 
 * @returns {React.ReactElement}
 */
function Message(props) {
    const { theMessage, isAdminComponent, clickHandlerNoAnswerNeeded, clickHandlerMarkAnswer, clickHandlerChangeFlag, clickHandlerDeleteMessage } = props;
    const { id, date, senderName, senderEmail, message, flagged, answerNeeded, wasAnswered, answeredBy, answerDate, answer } = theMessage;

    function getMessageStatus() {
        if (isAdminComponent) {
            if (wasAnswered) { return "answered" }
            if (answerNeeded) { return "answer needed" }
            if (!answerNeeded) { return "no answer needed" }
            console.error(`Inconsistent message status: wasAnswered = ${wasAnswered}, answerNeeded = ${answerNeeded}`)
            return "status error"
        } else {
            return (wasAnswered ? "message received a reply" : "message sent")
        }
    }

    let messageStatus = getMessageStatus()

    return (
        <div className="Message">
            <section className={isAdminComponent ? "Message-Sect1" : ""} >
                <div>
                    <p><b>Date:</b> <span className="Message-FontDarker">{date}</span></p>
                    {
                        isAdminComponent && (
                            <p><b>Sender:</b> <span className="Message-FontDarker">{senderName} | {senderEmail}</span> </p>
                        )
                    }
                    <p><b>Status:</b> <span className={answerNeeded && isAdminComponent ? "Message-StrongFontColour" : "Message-FontDarker"}>{messageStatus}</span></p>
                </div>
                {
                    isAdminComponent && (
                        <div className="Message-FlagContainer">
                            <div className="MAIN-iconContainerCircle">
                                <Flag flag={flagged} />
                            </div>
                        </div>
                    )
                }

            </section >

            <hr />

            <section>
                <p><b>Message</b></p>
                <p className="Message-MarginTop Message-WrapText">{message}</p>
            </section>

            {
                wasAnswered && (
                    <>
                        <hr />
                        <section>
                            <p><b>Answer</b></p>
                            <p className="Message-MarginTop"><b>By:</b> <span className="Message-FontDarker">{answeredBy}</span></p>
                            <p><b>Date:</b> <span className="Message-FontDarker">{answerDate}</span></p>
                            <p className="Message-MarginTop Message-WrapText">{answer}</p>
                        </section>
                    </>
                )
            }

            {
                isAdminComponent && (
                    <>
                        <hr />
                        <div>
                            <p><b>Actions</b></p>
                            <div className="Message-BtnContainer Message-MarginTop">
                                {
                                    !answerNeeded && !wasAnswered && (
                                        <button onClick={() => { clickHandlerNoAnswerNeeded(id, false) }}>Answer needed</button>
                                    )
                                }
                                {
                                    answerNeeded && !wasAnswered && (
                                        <button onClick={() => { clickHandlerNoAnswerNeeded(id, true) }}>No answer needed</button>
                                    )
                                }
                                {
                                    wasAnswered && (
                                        <button disabled >No answer needed</button>
                                    )
                                }
                                <button onClick={() => { clickHandlerMarkAnswer(id, answeredBy, answer) }}>{wasAnswered ? "Edit answer" : "Mark as answered"}</button>
                                <button onClick={() => { clickHandlerChangeFlag(id, flagged) }}>Change message flag</button>
                                <button onClick={() => { clickHandlerDeleteMessage(id) }} className="Message-DelBtn">Delete message</button>
                            </div>
                        </div>
                    </>
                )
            }

        </div >
    );
};
Message.propTypes = {
    isAdminComponent: PropTypes.bool.isRequired,
    theMessage: PropTypes.shape({
        id: PropTypes.number.isRequired,
        date: PropTypes.string.isRequired,
        senderName: PropTypes.string.isRequired,
        senderEmail: PropTypes.string.isRequired,
        message: PropTypes.string.isRequired,
        flagged: PropTypes.string.isRequired,
        answerNeeded: PropTypes.bool.isRequired,
        wasAnswered: PropTypes.bool.isRequired,
        answeredBy: PropTypes.string.isRequired,
        answerDate: PropTypes.string.isRequired,
        answer: PropTypes.string.isRequired
    }).isRequired,
    clickHandlerNoAnswerNeeded: PropTypes.func,
    clickHandlerMarkAnswer: PropTypes.func,
    clickHandlerChangeFlag: PropTypes.func,
    clickHandlerDeleteMessage: PropTypes.func,
};
export default Message;