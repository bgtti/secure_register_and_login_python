import UsersLogRow from "./UsersLogRow"
function UsersLogs(props) {
    const { name, email, uuid } = props.user;
    const logs = [{ date: "02/12/23", type: "info", activity: "whatever", message: "logged in" }, { date: "03/12/23", type: "info", activity: "whatever", message: "logged in" }]

    return (
        <div className="UsersLogs">
            <h3>Activity Logs</h3>
            <div>
                <p>User: {name}</p>
                <p>Email: {email}</p>
            </div>
            <table className="AdminDashboard-UserTable" role="table">
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
};
export default UsersLogs;