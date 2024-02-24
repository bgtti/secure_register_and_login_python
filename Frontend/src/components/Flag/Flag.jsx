import { PropTypes } from "prop-types";
import { FLAG_TYPES } from "../../utils/constants"
import "./flag.css";

/**
 * Component returns div with flag
 * 
 * 
 * @visibleName Flag
 * @param {object} props 
 * @param {string} props.flag //one of FLAG_TYPES
 * @returns {React.ReactElement}
 *
 */
function Flag(props) {
    const { flag } = props;
    let colour;

    switch (flag) {
        case "red":
            colour = "#aa0000"
            break
        case "yellow":
            colour = "#DB9A02"
            break
        case "purple":
            colour = "#A020F0"
            break
        case "blue":
            colour = "#376073"
            break
        default:
            colour = "#384d4f"
    }

    return (
        <div className="Flag" role="img" aria-label="Depiction of flag color" title={`${flag} flag`}>
            <div className="Flag-pole">
            </div>
            <div className="Flag-container">
                <div className="Flag-flag" style={{ backgroundColor: `${colour}` }}>
                </div>
                <div className="Flag-empty">
                </div>
            </div>
        </div>
    );
};
Flag.propTypes = {
    flag: PropTypes.PropTypes.oneOf(FLAG_TYPES)
};

export default Flag;