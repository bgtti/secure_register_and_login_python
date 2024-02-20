import PropTypes from 'prop-types';
import TableRow from './TableRow.jsx';
import "./table.css"

/**
 * Component returns HTML table for showing a table with all users
 * 
 * Child component: TableRow
 * 
 * @visibleName Admin Area: Users' Table: Table
 * @param {object} props 
 * @param {object[]} props.users an array of user objects (see example bellow)
 * @param {string} props.users[].name
 * @param {string} props.users[].email
 * @param {string} props.users[].lastSeen
 * @param {string} props.users[].isBlocked
 * @param {number} props.users[].id
 * @param {func} props.toggleModal function passed on to child
 * @param {func} props.setShowUserLogs function passed on to child
 * @param {func} props.selectUserAction function passed on to child
 * @returns {React.ReactElement}
 * 
 * @example
 * The users array to be passed as props should look something like this:
 * const users = [
    {
        name: "John Alfred",
        email: "john@alfred",
        lastSeen: "14 Dec 2023",
        isBlocked: "false",
        id: 1234
    },
    ...
]
 */
function Table(props) {
    const { users, toggleModal, setShowUserLogs, selectUserAction } = props

    return (
        <table className="MAIN-table Table" role="table">
            <thead role="rowgroup">
                <tr role="row">
                    <th role="columnheader">Name</th>
                    <th role="columnheader">Email</th>
                    <th role="columnheader">Last seen</th>
                    <th role="columnheader">Blocked</th>
                    <th role="columnheader">Actions</th>
                </tr>
            </thead>
            <tbody role="rowgroup">
                {users && (
                    users.map((user, index) => (
                        <TableRow
                            user={user}
                            key={index}
                            toggleModal={toggleModal}
                            setShowUserLogs={setShowUserLogs}
                            selectUserAction={selectUserAction} />
                    ))
                )}
            </tbody>
        </table>
    );
}
Table.propTypes = {
    users: PropTypes.arrayOf(PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        lastSeen: PropTypes.string.isRequired,
        isBlocked: PropTypes.string.isRequired,
        id: PropTypes.number.isRequired
    })).isRequired,
    toggleModal: PropTypes.func.isRequired,
    setShowUserLogs: PropTypes.func.isRequired,
    selectUserAction: PropTypes.func.isRequired
}
export default Table;