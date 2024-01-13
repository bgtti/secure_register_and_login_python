import PropTypes from 'prop-types';

/**
 * Component returns HTML table rows (tr element) representing a log.
 * 
 * @todo click view btn to view that user's logs
 * @todo implement colourful flag according to log type
 * 
 * @visibleName Admin Area: Dashboard: Log Table: Log Row
 * @param {object} props
 * @param {object} props.log 
 * @param {string} props.log.createdAt
 * @param {string} props.log.type
 * @param {string} props.log.activity
 * @param {string} props.log.message
 * @returns {React.ReactElement}
 */
function LogTableRow(props) {
    const { log } = props;
    const { createdAt, type, activity, message, userUuid } = log;

    return (
        <tr role="row">
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="date">Date:</label>
                {createdAt}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="type">Type:</label>
                {type.toLowerCase()}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="activity">Activity:</label>
                {activity}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="message">Message:</label>
                {message}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="action">Action:</label>
                {
                    userUuid === "" ?
                        (
                            <span className="LogTable-spanNoBtn">no uuid</span>
                        ) :
                        (
                            <button className="LogTable-viewBtn" onClick={() => { console.log("get the particular user's logs") }}>view</button>
                        )
                }
            </td>
        </tr>
    );
};
LogTableRow.propTypes = {
    log: PropTypes.shape({
        createdAt: PropTypes.string.isRequired,
        type: PropTypes.string.isRequired,
        activity: PropTypes.string.isRequired,
        message: PropTypes.string.isRequired,
    }).isRequired,
};
export default LogTableRow;