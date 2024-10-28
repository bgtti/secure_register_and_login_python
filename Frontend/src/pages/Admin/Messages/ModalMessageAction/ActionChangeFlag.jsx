import { PropTypes } from "prop-types";
import { FLAG_TYPES } from "../../../../utils/constants.js";


/**
 * Component returns fragment of flag selection
 * 
 * @visibleName Message action: flag change
 * @param {object} props 
 * @param {string} props.messageFlag //one of FLAG_TYPES
 * @param {func} props.changeState
 * @returns {React.ReactFragment}
 *
 */
function ActionChangeFlag(props) {
    const { messageFlag, changeState } = props;


    function handleChange(value) {
        // ps:value being of type Flag is being checked by parent
        if (value) {
            return changeState(value);
        } else {
            return console.warn("No value handled in ActionChangeFlag.")
        }
    }

    return (
        <>
            <p><b>Current flag: </b> {messageFlag}</p>
            <br />
            <div className="Modal-displayTable Modal-displayTable-32">
                <label htmlFor="changeFlag">Select new flag colour:</label>
                <select
                    className="Modal-Select"
                    name="changeFlag"
                    id="changeFlag"
                    defaultValue={messageFlag}
                    onChange={(e) => { handleChange(e.target.value) }}>
                    {
                        FLAG_TYPES.map((item, index) => (
                            <option value={item} key={index}>{item}</option>
                        ))
                    }
                </select>
            </div>
        </>
    );
};
ActionChangeFlag.propTypes = {
    messageFlag: PropTypes.PropTypes.oneOf(FLAG_TYPES).isRequired,
    changeState: PropTypes.func.isRequired
};

export default ActionChangeFlag;