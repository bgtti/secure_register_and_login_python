import PropTypes from "prop-types";
import { USER_ACCESS_TYPES, FLAG_TYPES, IS_BLOCKED_TYPES } from "../../../../utils/constants.js";
import Flag from "../../../../components/Flag/Flag.jsx"
import iconUserIsBlocked from "../../../../assets/icon_user_status_blocked.svg";
import iconUserIsNotBlocked from "../../../../assets/icon_user_status_unblocked.svg";
import iconUserTypeAdmin from "../../../../assets/icon_user_type_admin.svg";
import iconUserTypeUser from "../../../../assets/icon_user_type_user.svg";
import iconUserBlock from "../../../../assets/icon_user_block.svg";
import iconUserDelete from "../../../../assets/icon_user_delete.svg";
import iconUserMore from "../../../../assets/icon_user_more.svg";

/**
 * Component returns HTML table row (tr element) with user information and action buttons
 * 
 * @visibleName Admin Area: Users' Table: Table: TableRow
 * @param {object} props
 * @param {object} props.user 
 * @param {number} props.user.id // should be an int
 * @param {string} props.user.name
 * @param {string} props.user.email
 * @param {string} props.user.lastSeen
 * @param {string} props.user.access //one of USER_ACCESS_TYPES
 * @param {string} props.user.flagged //one of FLAG_TYPES
 * @param {string} props.user.isBlocked //one of IS_BLOCKED_TYPES
 * @param {func} props.toggleModal from grandparent (UsersTable)
 * @param {func} props.setShowUserInfo from grandparent (UsersTable)
 * @param {func} props.selectUserAction from grandparent (UsersTable)
 * @returns {React.ReactElement}
 */
function TableRow(props) {
    const { user, toggleModal, setShowUserInfo, selectUserAction } = props
    const { id, name, email, lastSeen, access, flagged, isBlocked } = user;

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
                <label className="MAIN-table-label" htmlFor="access_level">Type:</label>
                {access === "user" && (
                    <div className="Table-iconType">
                        <img
                            alt="User is regular user"
                            className="Table-icon"
                            role="img"
                            title="Regular user"
                            src={iconUserTypeUser}
                        />
                    </div>
                )}
                {access === "admin" && (
                    <div className="Table-iconType">
                        <img
                            alt="User is admin user"
                            className="Table-icon"
                            role="img"
                            title="Admin user"
                            src={iconUserTypeAdmin}
                        />
                    </div>
                )}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="flag">Flag:</label>
                <div className="Table-iconFlag">
                    <Flag flag={flagged} />
                </div>
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="blocked">Blocked:</label>
                {isBlocked === "true" && (
                    <div className="Table-iconStatus Table-iconStatus-Blocked">
                        <img
                            alt="User is blocked"
                            className="Table-icon"
                            role="img"
                            title="User is blocked"
                            src={iconUserIsBlocked}
                        />
                    </div>
                )}
                {isBlocked === "false" && (
                    <div className="Table-iconStatus">
                        <img
                            alt="User is unblocked"
                            className="Table-icon"
                            role="img"
                            title="User is unblocked"
                            src={iconUserIsNotBlocked}
                        />
                    </div>
                )}
            </td>
            <td role="cell">
                <label className="MAIN-table-label" htmlFor="actions">Actions:</label>
                <div className="Table-IconsContainer">
                    <img
                        alt="More user information"
                        className="Table-icon"
                        role="button"
                        title="User information"
                        src={iconUserMore}
                        onClick={() => { selectUserAction(id, "userInfo"); setShowUserInfo(true) }}
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
        id: PropTypes.number.isRequired,
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        lastSeen: PropTypes.string.isRequired,
        access: PropTypes.PropTypes.oneOf(USER_ACCESS_TYPES),
        flagged: PropTypes.PropTypes.oneOf(FLAG_TYPES),
        isBlocked: PropTypes.PropTypes.oneOf(IS_BLOCKED_TYPES),
    }).isRequired,
    toggleModal: PropTypes.func.isRequired,
    setShowUserInfo: PropTypes.func.isRequired,
    selectUserAction: PropTypes.func.isRequired
}


export default TableRow;