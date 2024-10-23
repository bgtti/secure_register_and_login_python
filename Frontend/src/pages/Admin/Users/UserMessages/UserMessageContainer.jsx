import PropTypes from "prop-types";
import Flag from "../../../../components/Flag/Flag";
import "./userMessageContainer.css"

/**
 * Component returns HTML div with details of the message.
 * 
 * @visibleName Admin Area: User's Messages: Message Container
 * @param {object} props
 * @param {object} props.theMessage 
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
 * @returns {React.ReactElement}
 */
function UserMessageContainer(props) {
    const { theMessage } = props;
    const { date, senderName, senderEmail, message, flagged, answerNeeded, wasAnswered, answeredBy, answerDate, answer } = theMessage;

    return (
        <div className="UserMessageContainer">
            <div className="UserMessageContainer-Sect1">
                <div>
                    <p>
                        <b>Date: </b>
                        <span><b>{date.split(',')[0]}</b></span>
                        <span className="UserMessageContainer-FontDarker">, {date.split(',')[1]}</span>
                    </p>
                    <p>
                        {answerNeeded && (
                            <b className="UserMessageContainer-FontYellow">Answer needed!</b>
                        )}
                        {!answerNeeded && (
                            <span className="UserMessageContainer-FontDarker">No answer needed.</span>
                        )}
                    </p>
                    <p>
                        {!wasAnswered && answerNeeded && (
                            <b className="UserMessageContainer-FontYellow">Message not answered.</b>
                        )}
                        {!wasAnswered && !answerNeeded && (
                            <b className="UserMessageContainer-FontDarker">Message not answered.</b>
                        )}
                        {wasAnswered && (
                            <span className="UserMessageContainer-FontDarker">Message answered.</span>
                        )}
                    </p>

                </div>
                <div className="MAIN-iconContainerCircle UserMessageContainer-flagContainer">
                    <div className="MAIN-iconContainerCircle ">
                        <Flag flag={flagged} />
                    </div>
                </div>
            </div>

            <hr />

            <div className="UserMessageContainer-Sect2">
                <p><b>Message</b></p>
                <div>
                    <p>{message}</p>
                </div>
                <p className="UserMessageContainer-FontDarker UserMessageContainer-Sender">
                    <i>Sender: {senderName} ( {senderEmail} )</i>
                </p>
            </div>

            <hr />

            <div className="UserMessageContainer-Sect3">
                <p><b>Answer</b></p>
                {
                    !wasAnswered && (
                        <p className="UserMessageContainer-FontDarker"><i>No answer to display.</i></p>
                    )
                }
                {
                    wasAnswered && (
                        <>
                            <div>
                                <p>{answer}</p>
                            </div>
                            <p className="UserMessageContainer-FontDarker UserMessageContainer-Answerer">
                                <i>Answered by: {answeredBy}</i>
                            </p>
                            <p className="UserMessageContainer-FontDarker UserMessageContainer-Answerer">
                                <i>Date: {answerDate}</i>
                            </p>
                        </>
                    )
                }
            </div>

            <hr />

            <div>
                <p><b>Actions</b></p>
                <br />
                <p>Mark as no answer needed</p>
                <p>Mark as answered</p>
                <p>Flag message</p>
            </div>


        </div>
    );
};
UserMessageContainer.propTypes = {
    theMessage: PropTypes.shape({
        date: PropTypes.string.isRequired,
        senderName: PropTypes.string.isRequired,
        senderEmail: PropTypes.string.isRequired,
        message: PropTypes.string.isRequired,
        flagged: PropTypes.string.isRequired,
        answerNeeded: PropTypes.bool.isRequired,
        wasAnswered: PropTypes.bool.isRequired,
        answeredBy: PropTypes.string.isRequired,
        answerDate: PropTypes.string.isRequired,
        answer: PropTypes.string.isRequired,
    }).isRequired,
};
export default UserMessageContainer;