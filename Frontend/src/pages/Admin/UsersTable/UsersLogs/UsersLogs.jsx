import PropTypes from 'prop-types';
import UsersLogRow from "./UsersLogRow"
import "./usersLogs.css"

/**
 * Component returns HTML div with user logs as a table
 * 
 * Child component: UserLogRow
 * 
 * @visibleName Admin Area: Users' Table: User Logs
 * @param {object} props
 * @param {object} props.user 
 * @param {string} props.user.name
 * @param {string} props.user.email
 * @param {string} props.user.uuid
 * @param {func} props.setShowUserLogs 
 * @param {func} props.selectUserAction 
 * @returns {React.ReactElement}
 */
function UsersLogs(props) {
    const { user, setShowUserLogs, selectUserAction } = props;
    const { name, email, uuid } = user;
    const logs = [{ date: "02/12/23", type: "info", activity: "whatever", message: "logged in" }, { date: "03/12/23", type: "info", activity: "whatever", message: "logged in" }]

    function handleReturn() {
        selectUserAction("", "");
        setShowUserLogs(false);
    }

    return (
        <div className="UsersLogs">
            <button onClick={handleReturn}>Back to Users Table</button>
            <h3>Activity Logs</h3>
            <div>
                <p><b className='UsersLogs-Bold'>User:</b> {name}</p>
                <p><b className='UsersLogs-Bold'>Email:</b> {email}</p>
            </div>
            <table className="MAIN-table UsersLogs-Table" role="table">
                <thead role="rowgroup">
                    <tr role="row">
                        <th role="columnheader">Date</th>
                        <th role="columnheader">Type</th>
                        <th role="columnheader">Activity</th>
                        <th role="columnheader">Log message</th>
                    </tr>
                </thead>
                <tbody role="rowgroup">
                    {logs && (
                        logs.map((log, index) => (
                            <UsersLogRow
                                log={log}
                                key={index}
                            />
                        ))
                    )}
                </tbody>
            </table>

        </div>
    );
};
UsersLogs.propTypes = {
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        uuid: PropTypes.string.isRequired
    }).isRequired,
    setShowUserLogs: PropTypes.func.isRequired,
    selectUserAction: PropTypes.func.isRequired,
};
export default UsersLogs;