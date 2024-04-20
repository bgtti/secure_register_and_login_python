import { useState } from "react";
import { PropTypes } from "prop-types";
import { useSelector } from "react-redux";
import { getTodaysDate, dateToYYYYMMDD } from "../../../../utils/helpers"
import { INPUT_LENGTH } from "../../../../utils/constants"

/**
 * Component returns fragment of message answer recording or edditing
 * 
 * @visibleName Message action: record/edit answer
 * @param {object} props 
 * @param {bool} props.wasAnswered
 * @param {string} [props.answeredBy=""]
 * @param {string} [props.answerDate=""]
 * @param {string} [props.answer=""]
 * @param {bool} props.changesWereMade 
 * @returns {React.ReactFragment}
 *
 */
function ActionAnswer(props) {
    const { wasAnswered, answeredBy = "", answerDate = "", answer = "", changesWereMade = "" } = props;

    const userEmail = useSelector((state) => state.user.email);

    const today = new Date()
    let tomorrow = today.setDate(today.getDate() + 1)
    tomorrow = dateToYYYYMMDD(tomorrow)

    const [answerData, setAnswerData] = useState({
        answeredBy: wasAnswered ? answeredBy : userEmail,
        answerDate: wasAnswered ? answerDate : getTodaysDate(),
        answer: wasAnswered ? answer : ""
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setAnswerData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    return (
        <>
            <div className="Modal-displayTable">
                <label htmlFor="answeredBy">Answered by:<span className="MAIN-form-star"> *</span></label>
                <input
                    id="answeredBy"
                    defaultValue={answerData.answeredBy}
                    disabled={changesWereMade ? true : false}
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
                    defaultValue={answerData.answerDate}
                    disabled={changesWereMade ? true : false}
                    name="answerDate"
                    type="date"
                    min="2024-01-01"
                    max={tomorrow}
                    onChange={handleChange}
                    required
                />
            </div>

            <br />

            <div className="Modal-displayTable">
                <label htmlFor="answer">Answer text:<span className="MAIN-form-star"> *</span></label>
                <textarea
                    id="answer"
                    defaultValue={answerData.answer}
                    disabled={changesWereMade ? true : false}
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
    wasAnswered: PropTypes.bool.isRequired,
    answeredBy: PropTypes.string,
    answerDate: PropTypes.string,
    answer: PropTypes.string,
    changesWereMade: PropTypes.bool.isRequired
};

export default ActionAnswer;