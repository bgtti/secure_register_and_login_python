import PropTypes from 'prop-types';

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
    const { date, senderName, senderEmail, message, flagged, answerNeeded, wasAnswered, answeredBy, answerDate, answer } = message;

    return (
        <div>
            <div>
                <div>
                    <p>Date: {date} </p>
                    <p>Answer needed: {answerNeeded ? "yes" : "no"} </p>
                    <p>Message answered: {wasAnswered ? "yes" : "no"} </p>
                </div>
                <div>
                    <p>{flagged}</p>
                </div>
            </div>

            <div>
                <p>Message</p>
                <p>{message}</p>
            </div>

            <div>
                <p>Sender details:</p>
                <p>Name: {senderName}</p>
                <p>Email: {senderEmail}</p>
            </div>

            <div>
                <p>Answer</p>
                <p>Answered by: {answeredBy}</p>
                <p>Answer date: {answerDate}</p>
                <div>
                    <p>Answer message:</p>
                    <p>{answer}</p>
                </div>
            </div>

            <div>
                <p>Actions</p>
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