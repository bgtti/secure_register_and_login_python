import { useState, useEffect } from "react";
import { PropTypes } from "prop-types";
import { useSelector } from "react-redux";
import { getTodaysDate, dateToYYYYMMDD } from "../../../../utils/helpers"
import { INPUT_LENGTH } from "../../../../utils/constants"

/**
 * Component returns fragment of message answer recording or edditing
 * 
 * @visibleName Message action: record/edit answer
 * @param {object} props 
 * @param {object} props.currentState  
 * @param {string} props.currentState.answeredBy
 * @param {string} props.currentState.answerDate
 * @param {string} props.currentState.answer
 * @param {boolean} props.currentState.answerSend
 * @param {string} props.currentState.answerSubject
 * @param {func} props.changeState
 * @param {func} props.changeBtnText
 * @param {bool} props.wasAnswered
 * @returns {React.ReactFragment}
 *
 */
function ActionAnswer(props) {
    const { currentState, changeState, changeBtnText, wasAnswered } = props;
    const { answeredBy, answerDate, answer, answerSend, answerSubject } = currentState;

    //Function to update parent state with new values
    function changeParentState(update) {
        const obj = {
            ...currentState,
            ...update
        };
        changeState(obj);
    }

    //Handle changes to the answer
    const handleChange = (e) => {
        const { name, value } = e.target;
        changeParentState({ [name]: value })
    };

    useEffect(() => {
        // Update the button text
        let text;
        if (answerSend) { text = "Send answer" }
        else { wasAnswered ? text = "Edit answer" : text = "Record answer" }
        changeBtnText(text)
    }, [answerSend]);

    //Defines latest answer date allowed
    const today = new Date()
    let tomorrow = today.setDate(today.getDate() + 1)
    tomorrow = dateToYYYYMMDD(tomorrow)

    return (
        <>
            <div className="Modal-displayTable">
                <label htmlFor="answerSend">Action:<span className="MAIN-form-star"> *</span></label>
                <select
                    className="Modal-Select"
                    name="answerSend"
                    id="answerSend"
                    defaultValue={answerSend}
                    disabled={wasAnswered}
                    onChange={(e) => { handleChange({ target: { name: e.target.name, value: e.target.value === "true" } }) }}>
                    <option value={true}>Email answer</option>
                    <option value={false}>Record answer </option>
                </select>
            </div>
            <br />
            {
                answerSend && (
                    <div className="Modal-displayTable">
                        <label htmlFor="answerSubject">Subject:<span className="MAIN-form-star"> *</span></label>
                        <input
                            id="answerSubject"
                            defaultValue={answerSubject}
                            name="answerSubject"
                            type="text"
                            onChange={handleChange}
                            minLength={INPUT_LENGTH.contactMessageAnswerSubject.minValue}
                            maxLength={INPUT_LENGTH.contactMessageAnswerSubject.maxValue}
                            required
                        />
                    </div>
                )
            }
            {
                !answerSend && (
                    <>
                        <div className="Modal-displayTable">
                            <label htmlFor="answeredBy">Answered by:<span className="MAIN-form-star"> *</span></label>
                            <input
                                id="answeredBy"
                                defaultValue={answeredBy}
                                name="answeredBy"
                                type="text"
                                onChange={handleChange}
                                minLength={INPUT_LENGTH.email.minValue}
                                maxLength={INPUT_LENGTH.email.maxValue}
                                required
                            />
                        </div>

                        <br />
                        <div className="Modal-displayTable">
                            <label htmlFor="answerDate">Answer date:<span className="MAIN-form-star"> *</span></label>
                            <input
                                id="answerDate"
                                defaultValue={answerDate}
                                name="answerDate"
                                type="date"
                                min="2024-01-01"
                                max={tomorrow}
                                onChange={handleChange}
                                required
                            />
                        </div>
                    </>
                )
            }

            <br />

            <div className="Modal-displayTable">
                <label htmlFor="answer">Answer text:<span className="MAIN-form-star"> *</span></label>
                <textarea
                    id="answer"
                    defaultValue={answer}
                    name="answer"
                    type="text"
                    onChange={handleChange}
                    rows="4"
                    minLength={INPUT_LENGTH.contactMessage.minValue}
                    maxLength={INPUT_LENGTH.contactMessage.maxValue}
                    required
                >
                </textarea>
            </div>
        </>
    );
};
ActionAnswer.propTypes = {
    currentState: PropTypes.shape({
        answeredBy: PropTypes.string.isRequired,
        answerDate: PropTypes.string.isRequired,
        answer: PropTypes.string.isRequired,
        answerSend: PropTypes.bool.isRequired,
        answerSubject: PropTypes.string.isRequired,
    }).isRequired,
    changeState: PropTypes.func.isRequired,
    changeBtnText: PropTypes.func.isRequired,
    wasAnswered: PropTypes.bool.isRequired,
};

export default ActionAnswer;
