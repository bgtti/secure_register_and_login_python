import PropTypes from 'prop-types';
import iconUserBlock from "../../../../assets/icon_user_block.svg";
import iconUserDelete from "../../../../assets/icon_user_delete.svg";
import iconUserMore from "../../../../assets/icon_user_more.svg";

/**
 * Component returns HTML table row (tr element) with user information and action buttons
 * 
 * @visibleName Admin Area: Users' Table: Table: TableRow
 * @param {object} props
 * @param {object} props.user 
 * @param {string} props.user.name
 * @param {string} props.user.email
 * @param {string} props.user.lastSeen
 * @param {string} props.user.isBlocked
 * @param {number} props.user.id
 * @param {func} props.toggleModal from grandparent (UsersTable)
 * @param {func} props.setShowUserLogs from grandparent (UsersTable)
 * @param {func} props.selectUserAction from grandparent (UsersTable)
 * @returns {React.ReactElement}
 */
function TableRow(props) {
    const { user, toggleModal, setShowUserLogs, selectUserAction } = props
    const { name, email, lastSeen, isBlocked, id } = user;

    return (
        <tr role="row">
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="name">Name:</label>
                {name}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="email">Email:</label>
                {email}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="last-seen">Last seen:</label>
                {lastSeen}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="blocked">Blocked:</label>
                {isBlocked}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="actions">Actions:</label>
                <div className="Table-IconsContainer">
                    <img
                        alt="More user information"
                        className="Table-icon"
                        role="button"
                        title="More information"
                        src={iconUserMore}
                        onClick={() => { selectUserAction(id, "logs"); setShowUserLogs(true) }}
                    />
                    <img
                        alt="Block user"
                        className="Table-icon"
                        role="button"
                        title="Block user"
                        src={iconUserBlock}
                        onClick={() => { selectUserAction(id, (isBlocked === "false" ? "block" : "unblock")); toggleModal() }}
                    />
                    <img
                        alt="Delete user"
                        className="Table-icon"
                        role="button"
                        title="Delete user"
                        src={iconUserDelete}
                        onClick={() => { selectUserAction(id, "delete"); toggleModal() }}
                    />
                </div>
            </td>
        </tr>
    );
};

TableRow.propTypes = {
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        lastSeen: PropTypes.string.isRequired,
        isBlocked: PropTypes.string.isRequired,
        id: PropTypes.number.isRequired
    }).isRequired,
    toggleModal: PropTypes.func.isRequired,
    setShowUserLogs: PropTypes.func.isRequired,
    selectUserAction: PropTypes.func.isRequired
}


export default TableRow;