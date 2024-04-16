import { useState } from "react";
import PropTypes from "prop-types";
import Flag from "../Flag/Flag";
import iconUserKnown from "../../assets/icon_user_type_user.svg"
import iconUserUnkown from "../../assets/icon_user_unkown.svg"
import iconMailSpam from "../../assets/icon_mail_top_danger.svg"
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
 * @param {bool} props.theMessage.senderIsUser
 * @param {string} props.theMessage.message
 * @param {string} props.theMessage.subject
 * @param {string} props.theMessage.flagged
 * @param {bool} props.theMessage.answerNeeded
 * @param {bool} props.theMessage.wasAnswered
 * @param {string} props.theMessage.answeredBy
 * @param {string} props.theMessage.answerDate
 * @param {string} props.theMessage.answer
 * @param {bool} props.theMessage.isSpam
 * @param {func} [props.clickHandlerNoAnswerNeeded] //Click handler needed if isAdminComponent, should accept message id
 * @param {func} [props.clickHandlerMarkAnswer] //Click handler needed if isAdminComponent, should accept message id
 * @param {func} [props.clickHandlerChangeFlag] //Click handler needed if isAdminComponent, should accept message id
 * @param {func} [props.clickHandlerDeleteMessage] //Click handler needed if isAdminComponent, should accept message id
 * 
 * @returns {React.ReactElement}
 */
function Message(props) {
    const { theMessage, isAdminComponent, clickHandlerNoAnswerNeeded, clickHandlerMarkAnswer, clickHandlerChangeFlag, clickHandlerDeleteMessage } = props;
    const { id, date, senderName, senderEmail, senderIsUser, subject, message, flagged, answerNeeded, wasAnswered, answeredBy, answerDate, answer, isSpam } = theMessage;

    const [showOptions, setShowOptions] = useState(false);
    function toggleShowOptions() {
        setShowOptions(!showOptions);
    }

    function messageData() {
        let dataObj = {
            id: id,
            senderEmail: senderEmail,
            senderIsUser: senderIsUser,
            flagged: flagged,
            answerNeeded: answerNeeded,
            wasAnswered: wasAnswered,
            answeredBy: answeredBy,
            answerDate: answerDate,
            answer: answer,
            isSpam: isSpam
        }
    }

    function getMessageStatus() {
        if (isAdminComponent) {
            if (isSpam) { return ["marked as spam", "FontBlue"] }
            if (wasAnswered) { return ["answered", "FontDarker"] }
            if (answerNeeded) { return ["answer needed", "FontYellow"] }
            if (!answerNeeded) { return ["no answer needed", "FontDarker"] }
            console.error(`Inconsistent message status: wasAnswered = ${wasAnswered}, answerNeeded = ${answerNeeded}`)
            return ["status error", "FontBlue"]
        } else {
            return [(wasAnswered ? "message received a reply" : "message sent"), "FontDarker"]
        }
    }

    let messageStatus = getMessageStatus()

    return (
        <div className="Message">

            {/* Section 1: basic message info */}
            <section className={isAdminComponent ? "Message-Sect1" : ""} >
                <div>
                    <p><b>Date:</b> <span className="Message-FontDarker">{date}</span></p>
                    {
                        isAdminComponent && (
                            <p><b>Sender:</b> <span className="Message-FontDarker">{senderName} | {senderEmail}</span> </p>
                        )
                    }
                    <p><b>Status:</b> <span className={`Message-${messageStatus[1]}`}>{messageStatus[0]}</span></p>
                </div>
                {
                    isAdminComponent && (
                        <div className="Message-IconContainer">
                            {isSpam && (
                                <div className="MAIN-iconContainerCircle">
                                    <img
                                        className="Message-spamIcon"
                                        alt={"This message was marked as spam"}
                                        role="img"
                                        title={"Marked as spam"}
                                        src={iconMailSpam}
                                    />
                                </div>
                            )}

                            <div className="MAIN-iconContainerCircle">
                                <img
                                    className={senderIsUser ? "Message-userIcon" : "Message-userIconUnkown"}
                                    alt={senderIsUser ? "Sender is a subscribed user." : "Sender is unkown (not a subscribed user)."}
                                    role="img"
                                    title={senderIsUser ? "Sender is a subscribed user" : "Sender is unkown"}
                                    src={senderIsUser ? iconUserKnown : iconUserUnkown}
                                />
                            </div>
                            <div className="MAIN-iconContainerCircle Message-flagContainer">
                                <Flag flag={flagged} />
                            </div>
                        </div>
                    )
                }
            </section >

            <hr />

            {/* Section 2: message subject and 'show more' button */}
            <section>
                <p className="Message-MarginTop"><b>Subject:</b> {subject}</p>
                <button
                    className="Message-MarginTop Message-ShowMoreBtn"
                    onClick={toggleShowOptions}>
                    {showOptions ? "Show less..." : "Show more..."}
                </button>
            </section>

            {/* Message, answer, and action buttons */}
            {
                showOptions && (
                    <div>
                        <hr />

                        {/* Section 3: message text */}
                        <section>
                            <p className="Message-MarginTop"><b>Message:</b></p>
                            <p className="Message-MarginTop Message-WrapText">{message}</p>
                        </section>

                        {/* Section 4: message answer */}
                        {
                            wasAnswered && (
                                <>
                                    <hr />
                                    <section>
                                        <p><b>Answer:</b></p>
                                        <p className="Message-MarginTop"><b>By:</b> <span className="Message-FontDarker">{answeredBy}</span></p>
                                        <p><b>Date:</b> <span className="Message-FontDarker">{answerDate}</span></p>
                                        <p className="Message-MarginTop Message-WrapText">{answer}</p>
                                    </section>
                                </>
                            )
                        }

                        {/* Section 5: action buttons */}
                        {
                            isAdminComponent && (
                                <>
                                    <hr />
                                    <div>
                                        <p><b>Actions:</b></p>
                                        <div className="Message-BtnContainer Message-MarginTop">
                                            {senderIsUser && (
                                                <>
                                                    <button
                                                        onClick={() => { console.log("hello") }}>
                                                        User info
                                                    </button>
                                                    <br />
                                                </>

                                            )}
                                            <div className="Message-BtnSubContainer Message-MarginTop">
                                                <button
                                                    onClick={() => { console.log("hello") }}>
                                                    Mark as...
                                                </button>

                                                <button
                                                    onClick={() => { console.log("hello") }}>
                                                    {wasAnswered ? "Edit answer" : "Record answer"}
                                                </button>

                                                <button
                                                    onClick={() => { console.log("hello") }}>
                                                    Change flag
                                                </button>

                                                <button
                                                    className="Message-DelBtn"
                                                    onClick={() => { console.log("hello") }}
                                                >
                                                    Delete message
                                                </button>
                                            </div>





                                            {/* 
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

                                            <button onClick={() => { console.log("spam") }}>Mark as spam</button>

                                            <button onClick={() => { clickHandlerDeleteMessage(id) }} className="Message-DelBtn">Delete message</button> */}
                                        </div>
                                    </div>
                                </>
                            )
                        }
                    </div>
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
        subject: PropTypes.string.isRequired,
        message: PropTypes.string.isRequired,
        flagged: PropTypes.string.isRequired,
        answerNeeded: PropTypes.bool.isRequired,
        wasAnswered: PropTypes.bool.isRequired,
        answeredBy: PropTypes.string.isRequired,
        answerDate: PropTypes.string.isRequired,
        answer: PropTypes.string.isRequired,
        senderIsUser: PropTypes.bool.isRequired,
        isSpam: PropTypes.bool.isRequired
    }).isRequired,
    clickHandlerNoAnswerNeeded: PropTypes.func,
    clickHandlerMarkAnswer: PropTypes.func,
    clickHandlerChangeFlag: PropTypes.func,
    clickHandlerDeleteMessage: PropTypes.func,
};
export default Message;