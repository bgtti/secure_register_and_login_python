import PropTypes from "prop-types";
import TableRow from "./TableRow.jsx";
import { USER_ACCESS_TYPES, FLAG_TYPES, IS_BLOCKED_TYPES } from "../../../../../utils/constants.js";
import "./table.css";

/**
 * Component returns HTML table for showing a table with all users
 * 
 * Child component: TableRow
 * 
 * @visibleName Users Table
 * @param {object} props 
 * @param {object[]} props.users an array of user objects (see example bellow)
 * @param {number} props.users[].id // should be an int
 * @param {string} props.users[].name
 * @param {string} props.users[].email
 * @param {string} props.users[].lastSeen
 * @param {string} props.users[].access //one of USER_ACCESS_TYPES
 * @param {string} props.users[].flagged //one of FLAG_TYPES
 * @param {string} props.users[].isBlocked //one of IS_BLOCKED_TYPES
 * @param {func} props.toggleModal function passed on to child
 * @param {func} props.selectUserAction function passed on to child
 * @returns {React.ReactElement}
 * 
 * @example
 * The users array to be passed as props should look something like this:
 * const users = [
    {   
        id: 1234
        name: "John Alfred",
        email: "john@alfred",
        lastSeen: "14 Dec 2023",
        access: "user",
        flagged: "blue",
        isBlocked: "false"
    },
    ...
]
 */
function Table(props) {
    const { users, toggleModal, setShowUserInfo, selectUserAction } = props

    return (
        <table className="MAIN-table Table" role="table">
            <thead role="rowgroup">
                <tr role="row">
                    <th role="columnheader">Name</th>
                    <th role="columnheader">Email</th>
                    <th role="columnheader">Last seen</th>
                    <th role="columnheader" className="Table-th">Type</th>
                    <th role="columnheader" className="Table-th">Flag</th>
                    <th role="columnheader" className="Table-th">Blocked</th>
                    <th role="columnheader" className="Table-th">Actions</th>
                </tr>
            </thead>
            <tbody role="rowgroup">
                {users && (
                    users.map((user, index) => (
                        <TableRow
                            user={user}
                            key={index}
                            toggleModal={toggleModal}
                            setShowUserInfo={setShowUserInfo}
                            selectUserAction={selectUserAction} />
                    ))
                )}
            </tbody>
        </table>
    );
}
Table.propTypes = {
    users: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        lastSeen: PropTypes.string.isRequired,
        access: PropTypes.PropTypes.oneOf(USER_ACCESS_TYPES),
        flagged: PropTypes.PropTypes.oneOf(FLAG_TYPES),
        isBlocked: PropTypes.PropTypes.oneOf(IS_BLOCKED_TYPES),
    })).isRequired,
    toggleModal: PropTypes.func.isRequired,
    selectUserAction: PropTypes.func.isRequired
}
export default Table;