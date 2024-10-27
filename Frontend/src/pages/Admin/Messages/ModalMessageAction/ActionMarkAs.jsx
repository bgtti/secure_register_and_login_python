import { useState, useRef } from "react";
import { PropTypes } from "prop-types";

/**
 * Component returns fragment of message status selection.
 * A message can be marked as 'spam', 'no answer needed', or 'answer needed'. The sender could also be marked as a 'spammer'.
 * Fragment used as modal content in ModalMessageAction.
 * 
 * 
 * @visibleName Message action: status change
 * @param {object} props
 * @param {object} props.currentState   
 * @param {bool} props.currentState.isSpam
 * @param {bool} props.currentState.answerNeeded
 * @param {bool} props.currentState.markSenderAsSpammer
 * @param {bool} props.senderIsUser
 * @param {bool} props.wasAnswered
 * @param {func} props.changeState
 * 
 * @returns {React.ReactFragment}
 *
 */
function ActionMarkAs(props) {
    const { currentState, senderIsUser, changeState, wasAnswered } = props;
    const { isSpam, answerNeeded, markSenderAsSpammer } = currentState;

    //The original 'isSpam' state is recorded upon mount, so it can be referred to when needed 
    const originalIsSpam = useRef(isSpam);

    // Selection options for marking the message
    const SPAM_OPTS = {
        spam: "Message is spam",
        notSpam: "Message is not spam"
    }
    const ANS_OPTS = {
        needAns: "Answer is needed",
        noNeedAns: "No answer is needed"
    }

    // Selection options for marking the sender
    const SENDER_OPTS = {
        senderSpam: "Sender is spammer",
        noSenderSpam: "Sender is not spammer"
    }

    // Determine the available message selection options based on the original state
    function getSelectionOptions() {
        if (originalIsSpam.current || wasAnswered) { return SPAM_OPTS } //case 1 
        else { return { ...ANS_OPTS, spam: SPAM_OPTS.spam } } //case 2 
    }
    const selectionOptions = getSelectionOptions();


    //Determining how message is marked:
    //1st:"Message is spam" (isSpam) or "Message is not spam" (!isSpam)
    //     => if spam, user can also choose "Sender is spammer" or "sender is not spammer"
    //2nd: "Answer needed" (answerNeeded), "Answer not needed" (!answerNeeded).
    //    => Answer is not needed if: A) isSpam, B) wasAnswered, C) !answerNeeded

    const [msgMark, setMsgMark] = useState(() => {
        if (isSpam) { return "spam" } // isSpam && !answerNeeded
        if (answerNeeded && !wasAnswered) { return "needAns" } // !isSpam && answerNeeded
        return "noNeedAns" // !isSpam && !answerNeeded
    });

    //Keep track of whether changes were made to isSpam
    const spamMarkChange = (originalIsSpam.current && msgMark !== "spam") || (!originalIsSpam.current && msgMark === "spam")

    //Function to update parent state with new values
    function changeParentState(update) {
        const obj = {
            ...currentState,
            ...update
        };
        changeState(obj);
    }

    //Handle changes to the message mark or 'sender as spammer' status
    //Accepted arguments: "spam", "notSpam", "needAns", "noNeedAns", senderSpam, "noSenderSpam"
    function handleChange(e) {
        switch (e.target.value) {
            case "spam":
                setMsgMark("spam");
                changeParentState({ isSpam: true, answerNeeded: false });
                break
            case "notSpam":
                if (wasAnswered) { setMsgMark("noNeedAns"); changeParentState({ isSpam: false }); }
                else { setMsgMark("needAns"); changeParentState({ isSpam: false, answerNeeded: true }) };
                break
            case "needAns":
                setMsgMark(e.target.value);
                changeParentState({ answerNeeded: true });
                break
            case "noNeedAns":
                setMsgMark(e.target.value);
                changeParentState({ answerNeeded: false });
                break
            case "senderSpam":
                changeParentState({ markSenderAsSpammer: true });
                break
            case "noSenderSpam":
                changeParentState({ markSenderAsSpammer: false });
                break
            default:
                console.error("Input not accepted");
                return
        }
    }

    return (
        <>
            <div className="Modal-displayTable">
                {/* Main selection options: depend on current mark, which defines selectionOptions*/}
                <label htmlFor="changeStatus">Select new status:</label>
                <select
                    className="Modal-Select"
                    name="changeStatus"
                    id="changeStatus"
                    defaultValue={msgMark}
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
                        defaultValue={ANS_OPTS.needAns}
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
                    {(msgMark === "spam") && (
                        <>
                            <br />
                            <p> Would you like to include the sender's email to the spammer's list?</p>
                            <p> Future messages received by the sender will be automatically marked as spam. </p>
                        </>
                    )}
                    {(msgMark !== "spam") && (
                        <>
                            <br />
                            <p> If you included the sender's email address in the spammers list, would you like to remove it?</p>
                            <p> Messages received by spammers are automatically marked as spam. </p>
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
                            onChange={handleChange}>
                            {
                                Object.keys(SENDER_OPTS).map((key, index) => (
                                    <option value={key} key={index}>{SENDER_OPTS[key]}</option>
                                ))
                            }
                        </select>
                    </div>
                    <br />
                    {markSenderAsSpammer && senderIsUser && (
                        <>
                            <p>Attention: the sender is a subscribed user.</p>
                            <p>The user will be blocked.</p>
                            <p>Messages received by spammers are automatically marked as spam.</p>
                        </>
                    )}
                </>
            )}
        </>
    );
};
ActionMarkAs.propTypes = {
    senderIsUser: PropTypes.bool.isRequired,
    wasAnswered: PropTypes.bool.isRequired,
    currentState: PropTypes.shape({
        isSpam: PropTypes.bool.isRequired,
        answerNeeded: PropTypes.bool.isRequired,
        markSenderAsSpammer: PropTypes.bool.isRequired,
    }).isRequired,
    changeState: PropTypes.func.isRequired,
};

export default ActionMarkAs;

//Display logic: selection options

//1.case MESSAGE IS SPAM (isSpam is true) OR MESSAGE HAS BEEN ANSWERED (wasAnswered is true):
// Show options to user: ["Message is spam","Message is not spam"] and if
// A) => "Message is spam" selected: isSpam is true and show second selection options:
//    opts =>[ "Sender is spammer", "Sender is not spammer"], where (markSenderAsSpammer) or (!markSenderAsSpammer) is set respectively
// B) => "Message is not spam" selected: isSpam is false and
//    B.1) if no answer recorded (wasAnswered is false), show second selection options:
//         opts => [ "Answer is needed", "No answer is needed"] where (answerNeeded) or (!answerNeeded) is set respectively.
//    B.2) is answer is recorded, no other selection tag is shown.
//2.case MESSAGE IS NOT SPAM (isSpam is false) AND NO ANSWER RECORDED (wasAnswered is false):
// Show options to user: [ "Answer is needed", "No answer is needed", "Message is spam"] and if
// A) => "Answer is needed" is selected, answerNeeded is set to true
// B) => "No answer is needed" is selected, answerNeeded is set to false
// C) => "Message is spam" is selected, isSpam is set to true and show second selection options:
//    opts =>[ "Sender is spammer", "Sender is not spammer"], where (markSenderAsSpammer) or (!markSenderAsSpammer) is set respectively