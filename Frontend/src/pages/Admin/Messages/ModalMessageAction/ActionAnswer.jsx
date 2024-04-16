import { useState } from "react";
import { PropTypes } from "prop-types";
import { useDispatch, useSelector } from "react-redux";
import { FLAG_TYPES } from "../../../../utils/constants.js";

/**
 * Component returns fragment of flag selection
 * 
 * @visibleName Message action: flag change
 * @param {object} props 
 * @param {string} props.messageFlag //one of FLAG_TYPES
 * @param {bool} props.changesWereMade 
 * @param {func} props.setMessageFlag 
 * @returns {React.ReactElement}
 *
 */
function ActionAnswer(props) {
    const { wasAnswered, answeredBy, answerDate, answer, changesWereMade } = props;

    const userEmail = useSelector((state) => state.user.email);

    const today = new Date()

    const [answerData, setAnswerData] = useState({
        answeredBy: wasAnswered ? answeredBy : userEmail,
        answerDate: wasAnswered ? answerDate : today.toJSON().slice(0, 10),
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
            <br />
            <div className="MAIN-form-display-table ModalMessageAction-displayTable">
                <label htmlFor="answeredBy">Answered by:</label>
                <input
                    id="answeredBy"
                    defaultValue={answerData.answeredBy}
                    disabled={changesWereMade ? true : false}
                    name="answeredBy"
                    type="text"
                    onChange={handleChange} />
            </div>

            <br />
            <div className="MAIN-form-display-table ModalMessageAction-displayTable">
                <label htmlFor="answerDate">Select new flag colour:</label>
                <input
                    id="answerDate"
                    defaultValue={answerData.answerDate}
                    disabled={changesWereMade ? true : false}
                    name="answerDate"
                    type="date"
                    min="2017-04-01"
                    max={(today.getDate() + 1).toJSON().slice(0, 10)}
                    onChange={handleChange} />
            </div>

            <br />

            <div className="MAIN-form-display-table ModalMessageAction-displayTable">
                <label htmlFor="answerText">Select new flag colour:</label>
                <input
                    id="answerText"
                    defaultValue={messageAnsweredText}
                    disabled={changesWereMade ? true : false}
                    name="answerText"
                    type="text"
                    onChange={(e) => { setMessageAnsweredText(e.target.value) }} />
            </div>
        </>
    );
};
ActionAnswer.propTypes = {
    messageFlag: PropTypes.PropTypes.oneOf(FLAG_TYPES).isRequired,
    changesWereMade: PropTypes.bool.isRequired,
    setMessageFlag: PropTypes.func.isRequired
};

export default ActionAnswer;