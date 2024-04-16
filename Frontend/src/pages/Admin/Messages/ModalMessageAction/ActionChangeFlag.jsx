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
 * @returns {React.ReactElement}
 *
 */
function ActionChangeFlag(props) {
    const { messageFlag, changesWereMade, setMessageFlag } = props;

    return (
        <>
            <p>Select the flag colour of the message:</p>
            <br />
            <p><b className="ModalMessageAction-Bold" >Flag: </b> {flag}</p>
            <br />
            <div className="MAIN-form-display-table ModalMessageAction-displayTable">
                <label htmlFor="changeFlag">Select new flag colour:</label>
                <select
                    className="ModalMessageAction-Select"
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