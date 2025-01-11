import { PropTypes } from "prop-types";
import "./tooltip.css";

/**
 * Component returns span with info icon, tooltip, and the word that should preceed the info icon
 * Should be used inside a p tag or a heading tag
 * 
 * @visibleName Tooltip
 * @param {object} props 
 * @param {string} props.text // the word(s) that preceeds the tooltip info icon
 * @param {string} props.message // the message that should be displayed when the info icon is hovered
 * @param {string} [props.cssClass] // optional: add a class for text styling (eg: Tooltip-text-bold will make text bold)
 * @returns {React.ReactElement}
 * 
 * @example 
 * import Tooltip from "./Tooltip";
 * <p>
        Mailing 
        <Tooltip text="list" message="Get news from us" />
   </p>
 *
 */
function Tooltip(props) {
    const { text, message, cssClass = "" } = props;
    return (
        <span className="Tooltip-wrapper">
            <span className={`Tooltip-text ${cssClass}`}>{text}</span>
            <span className="Tooltip-info-icon">i</span>
            <span className="Tooltip-message">{message}</span>
        </span>
    );
}
Tooltip.propTypes = {
    text: PropTypes.string.isRequired,
    message: PropTypes.string.isRequired
};

export default Tooltip;