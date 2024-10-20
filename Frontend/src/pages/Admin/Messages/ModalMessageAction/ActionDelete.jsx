import { PropTypes } from "prop-types";

/**
 * Component returns fragment of 'delete message' action
 * 
 * @visibleName Message action: delete message
 * @param {object} props 
 * @param {string} props.senderName
 * @param {string} props.senderEmail
 * @param {bool} props.isSpam 
 * @returns {React.ReactFragment}
 *
 */
function ActionDeleteMessage(props) {
    const { senderName, senderEmail, isSpam } = props;

    return (
        <>
            <p>You are about to delete a message from:</p>
            <p><b>{senderName} | {senderEmail}</b></p>
            <br />
            {
                isSpam && (
                    <p>This message has been marked as spam.</p>
                )
            }
            {
                !isSpam && (
                    <>
                        <p>This action cannot be undone.</p>
                        <p>Are you sure you want to proceed?</p>
                    </>
                )
            }
        </>
    );
};
ActionDeleteMessage.propTypes = {
    senderName: PropTypes.string.isRequired,
    senderEmail: PropTypes.string.isRequired,
    isSpam: PropTypes.bool.isRequired,
};

export default ActionDeleteMessage;