import PropTypes from 'prop-types';

/**
 * Component returns HTML table rows (tr element) representing a log.
 * 
 * @visibleName Admin Area: Users' Table: User Logs: Log Row
 * @param {object} props
 * @param {object} props.log 
 * @param {string} props.log.date
 * @param {string} props.log.info
 * @param {string} props.log.activity
 * @param {string} props.log.message
 * @returns {React.ReactElement}
 */
function UsersLogRow(props) {
    const { date, type, activity, message } = props.log;

    return (
        <tr role="row">
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="date">Date:</label>
                {date}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="type">Type:</label>
                {type}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="activity">Activity:</label>
                {activity}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="message">Message:</label>
                {message}
            </td>
        </tr>
    );
};
UsersLogRow.propTypes = {
    log: PropTypes.shape({
        date: PropTypes.string.isRequired,
        type: PropTypes.string.isRequired,
        activity: PropTypes.string.isRequired,
        message: PropTypes.string.isRequired,
    }).isRequired,
};
export default UsersLogRow;