import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import Flag from "../Flag/Flag";
import iconUserKnown from "../../assets/icon_user_type_user.svg"
import iconUserUnkown from "../../assets/icon_user_unkown.svg"
import iconMailSpam from "../../assets/icon_mail_top_danger.svg"
import { PATH_TO } from "../../router/routePaths"
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
 * @param {number} props.theMessage.userId
 * @param {string} props.theMessage.message
 * @param {string} props.theMessage.subject
 * @param {string} props.theMessage.flagged
 * @param {bool} props.theMessage.answerNeeded
 * @param {bool} props.theMessage.wasAnswered
 * @param {string} props.theMessage.answeredBy
 * @param {string} props.theMessage.answerDate
 * @param {string} props.theMessage.answer
 * @param {bool} props.theMessage.isSpam
 * @param {function} [props.clickHandler] 
 * 
 * @returns {React.ReactElement}
 * 
 * @example
 * //See example in: pages > Admin> Messages > Messages.jsx
 * 1. import Message from "[...]/components/Message/Message.jsx";
 * 2. declare function clickHandler(messageObj, action){...}
 * 3. display component inside return statement like 
 *      <Message
            isAdminComponent={true} //=> boolean
            theMessage={item} //=> message object
            clickHandler={clickHandler} //=> optional function, required if isAdminComponent (to handle action buttons), should accept the message obj and action
            //if inside a map method: key={index}
        />
 */
function Message(props) {
    const { theMessage, isAdminComponent, clickHandler = false } = props;
    const { id, date, senderName, senderEmail, senderIsUser, userId, subject, message, flagged, answerNeeded, wasAnswered, answeredBy, answerDate, answer, isSpam } = theMessage;

    const navigate = useNavigate();

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
            if (isSpam) { return ["Message marked as spam.", "FontBlue"] }
            if (wasAnswered) { return ["Message answered.", "FontDarker"] }
            if (answerNeeded) { return ["Answer needed!", "FontYellow"] }
            if (!answerNeeded) { return ["No answer needed.", "FontDarker"] }
            console.error(`Inconsistent message status: wasAnswered = ${wasAnswered}, answerNeeded = ${answerNeeded}`)
            return ["Status error.", "FontBlue"]
        } else {
            return [(wasAnswered ? "Message received a reply." : "message sent"), "FontDarker"]
        }
    }

    let messageStatus = getMessageStatus()

    return (
        <div className="Message">

            {/* Section 1: basic message info */}
            <section className={isAdminComponent ? "Message-Sect1" : ""} >
                <div>
                    <p>
                        {/* <b>Status: </b> */}
                        <span className={`Message-${messageStatus[1]}`}>{messageStatus[0]}</span>
                    </p>
                    <p>
                        {/* <b>Date: </b> */}
                        <span><b>{date.split(',')[0]}</b></span>
                        <span className="Message-FontDarker Message-FontSmall">  {date.split(',')[1]}</span>
                    </p>
                    <p>
                        {/* <b>Subject:</b>  */}
                        {
                            subject === "no subject" && (
                                <b className="Message-FontDarker Message-FontSmall">no subject</b>
                            )
                        }
                        {
                            subject !== "no subject" && (
                                <>
                                    <i className="Message-FontDarker MessageQuote">" </i>
                                    <b >{subject}</b>
                                    <i className="Message-FontDarker MessageQuote"> "</i>
                                </>
                            )
                        }
                    </p>
                    {
                        isAdminComponent && (
                            <p>
                                {/* <b>Sender:</b>  */}
                                <span className="Message-FontDarker Message-FontSmall">{senderName} ( {senderEmail} )</span>
                            </p>
                        )
                    }
                </div>
                {/* Icons */}
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



            {/* Section 2: 'show more' button */}
            <section>
                <button
                    className="Message-MarginTop Message-ShowMoreBtn"
                    onClick={toggleShowOptions}>
                    {showOptions ? "Show less..." : "Show more..."}
                </button>
            </section>

            {/* <hr /> */}

            {/* Message, answer, and action buttons */}
            {
                showOptions && (
                    <div>
                        <hr />
                        {/* Section 3: message text */}
                        <section>
                            <p className="Message-MarginTop Message-MarginBottom">
                                <b>Message</b>
                            </p>
                            <div className="Message-MessageBlock">
                                <p className="Message-WrapText">{message}</p>
                            </div>
                        </section>

                        {/* Section 4: message answer */}
                        {
                            wasAnswered && (
                                <>
                                    <hr />
                                    <section className="Message-Answer">
                                        <p className="Message-MarginTop Message-MarginBottom">
                                            <b>Answer</b>
                                        </p>
                                        <div className="Message-MessageBlock">
                                            <p className="Message-WrapText">{answer}</p>
                                        </div>

                                        <p className="Message-FontDarker Message-FontSmall Message-MarginTop">
                                            <i>Answered by: {answeredBy}</i>
                                        </p>
                                        <p className="Message-FontDarker Message-FontSmall">
                                            <i>Date: {answerDate}</i>
                                        </p>

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
                                        <p className="Message-MarginTop Message-MarginBottom">
                                            <b>Actions</b>
                                        </p>
                                        <div className="Message-BtnContainer Message-MarginTop">
                                            {senderIsUser && (
                                                <>
                                                    <button
                                                        onClick={() => { navigate(PATH_TO.adminArea_userInfo, { state: userId }) }}>
                                                        User info
                                                    </button>
                                                    <br />
                                                </>

                                            )}
                                            <div className="Message-BtnSubContainer Message-MarginTop">
                                                <button
                                                    onClick={() => { clickHandler(theMessage, "markAs") }}>
                                                    Mark as...
                                                </button>

                                                <button
                                                    onClick={() => { clickHandler(theMessage, "answer") }}>
                                                    {wasAnswered ? "Edit answer" : "Answer"}
                                                </button>

                                                <button
                                                    onClick={() => { clickHandler(theMessage, "flag") }}>
                                                    Change flag
                                                </button>

                                                <button
                                                    className="Message-DelBtn"
                                                    onClick={() => { clickHandler(theMessage, "delete") }}
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
        userId: PropTypes.number.isRequired,
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