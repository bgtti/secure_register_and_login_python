import { useState } from "react";
import { PropTypes } from "prop-types";

const SPAM_OPTS = {
    spam: "Message is spam",
    notSpam: "Message is not spam"
}

const ANS_OPTS = {
    needAns: "Answer is needed",
    noNeedAns: "No answer is needed"
}

const ALL_OPTS = [...Object.keys(SPAM_OPTS), ...Object.keys(ANS_OPTS)]

/**
 * Component returns fragment of message status selection
 * 
 * 
 * @visibleName Message action: status change
 * @param {object} props 
 * @param {bool} props.isSpam
 * @param {bool} props.answerNeeded 
 * @param {bool} props.wasAnswered
 * @param {bool} props.senderIsUser
 * @param {bool} props.changesWereMade 
 * @returns {React.ReactFragment}
 *
 */
function ActionMarkAs(props) {
    const { isSpam, answerNeeded, wasAnswered, senderIsUser, changesWereMade } = props;

    const [markedSpam, setMarkedSpam] = useState(isSpam);
    const [currentStatus, setCurrentStatus] = useState(getOriginalStatus());
    const [markSenderAsSpammer, setMarkSenderAsSpammer] = useState(false);

    const originalStatus = getOriginalStatus()
    const selectionOptions = getSelectionOptions()

    const spamMarkChange = (isSpam && currentStatus !== "spam") || (!isSpam && currentStatus === "spam")

    function getOriginalStatus() {
        if (isSpam) { return "spam" }
        if (answerNeeded && !wasAnswered) { return "needAns" }
        return "noNeedAns"
    }

    function getSelectionOptions() {
        if (isSpam || wasAnswered) { return SPAM_OPTS }
        else { return { ...ANS_OPTS, spam: SPAM_OPTS.spam } }
    }

    function checkStatusChange(val = currentStatus) {
        return originalStatus === val
    }

    function handleChange(e) {
        switch (e.target.value) {
            case "needAns":
            case "noNeedAns":
                setCurrentStatus(e.target.value);
                break
            case "spam":
                setMarkedSpam(true);
                setCurrentStatus("spam");
                break
            case "notSpam":
                setMarkedSpam(false);
                if (wasAnswered) { setCurrentStatus("noNeedAns"); }
                else { setCurrentStatus("needAns") }
                break
            default:
                console.error("Input not accepted")
                return
        }
    }

    return (
        <>
            <div className="Modal-displayTable">
                <label htmlFor="changeStatus">Select new status:</label>
                <select
                    className="Modal-Select"
                    name="changeStatus"
                    id="changeStatus"
                    defaultValue={currentStatus}
                    disabled={changesWereMade ? true : false}
                    onChange={handleChange}>
                    {
                        Object.keys(selectionOptions).map((key, index) => (
                            <option value={key} key={index}>{selectionOptions[key]}</option>
                        ))
                    }
                </select>
            </div>

            {/* If message was originally marked as spam, but user unmarks as spam, allow user to decide whether message requires an answer (if message has not yet been answered)*/}
            {isSpam && spamMarkChange && !wasAnswered && (
                <div className="Modal-displayTable">
                    <label htmlFor="ansStatus">Set answer requirement:</label>
                    <select
                        className="Modal-Select"
                        name="ansStatus"
                        id="ansStatus"
                        defaultValue={currentStatus}
                        disabled={changesWereMade ? true : false}
                        onChange={handleChange}>
                        {
                            Object.keys(ANS_OPTS).map((key, index) => (
                                <option value={key} key={index}>{ANS_OPTS[key]}</option>
                            ))
                        }
                    </select>
                </div>
            )}

            {/* If message was originally marked as spam, but user unmarks as spam, allow user to decide whether to remove sender from spammers list*/}
            {spamMarkChange && (
                <>
                    {markedSpam && (
                        <>
                            <br />
                            <p> Would you like to include the sender's email to the spammer's list?</p>
                            <p> Future messages received by the sender will be automatically marked as spam and no longer forwarded to the site's admin email address. </p>
                        </>
                    )}
                    {!markedSpam && (
                        <>
                            <br />
                            <p> If you included the sender's email address in the spammers list, would you like to remove it?</p>
                            <p> Messages received by spammers are automatically marked as spam and are not forwarded to the site's admin email address. </p>
                        </>
                    )}
                    <br />
                    <div className="Modal-displayTable Modal-displayTable-3auto">
                        <label htmlFor="spamList">Spammer list:</label>
                        <select
                            className=""
                            name="spamList"
                            id="spamList"
                            defaultValue={markSenderAsSpammer}
                            disabled={changesWereMade ? true : false}
                            onChange={(e) => { setMarkSenderAsSpammer(e.target.value) }}>
                            <option value={true} key={0}>
                                {isSpam ? "Keep sender in list" : "Mark sender as spammer"}
                            </option>
                            <option value={false} key={1}>
                                {isSpam ? "Remove sender from list" : "Do not mark sender as spammer"}
                            </option>
                        </select>
                    </div>
                    <br />
                    {markSenderAsSpammer && senderIsUser && (
                        <p>Attention: the sender is a subscribed user. If you mark the sender as a spammer, no admin will be notified of new incomming messages from this user.</p>
                    )}
                </>
            )}
        </>
    );
};
ActionMarkAs.propTypes = {
    changesWereMade: PropTypes.bool.isRequired,
};

export default ActionMarkAs;