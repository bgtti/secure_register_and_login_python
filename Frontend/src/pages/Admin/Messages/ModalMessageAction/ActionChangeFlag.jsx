import { PropTypes } from "prop-types";
import { FLAG_TYPES } from "../../../../utils/constants.js";

/**
 * Component returns fragment of flag selection
 * 
 * @visibleName Message action: flag change
 * @param {object} props 
 * @param {string} props.messageFlag //one of FLAG_TYPES
 * @param {bool} props.changesWereMade 
 * @param {func} props.setMessageFlag 
 * @returns {React.ReactFragment}
 *
 */
function ActionChangeFlag(props) {
    const { messageFlag, changesWereMade, setMessageFlag } = props;

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
                    disabled={changesWereMade ? true : false}
                    onChange={(e) => { setMessageFlag(e.target.value) }}>
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
    changesWereMade: PropTypes.bool.isRequired,
    setMessageFlag: PropTypes.func.isRequired
};

export default ActionChangeFlag;