import PropTypes from "prop-types";
import { useNavigate } from "react-router-dom";
import { USER_ACCESS_TYPES, FLAG_TYPES, IS_BLOCKED_TYPES } from "../../../../../utils/constants.js";
import Flag from "../../../../../components/Flag/Flag.jsx"
import iconUserIsBlocked from "../../../../../assets/icon_user_status_blocked.svg";
import iconUserIsNotBlocked from "../../../../../assets/icon_user_status_unblocked.svg";
import iconUserTypeAdmin from "../../../../../assets/icon_user_type_admin.svg";
import iconUserTypeUser from "../../../../../assets/icon_user_type_user.svg";
import iconUserBlock from "../../../../../assets/icon_user_block.svg";
import iconUserDelete from "../../../../../assets/icon_user_delete.svg";
import iconUserMore from "../../../../../assets/icon_user_more.svg";

/**
 * Component returns HTML table row (tr element) with user information and action buttons
 * 
 * @visibleName Users' Table: Table Row
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
 * @param {func} props.selectUserAction from grandparent (UsersTable)
 * @returns {React.ReactElement}
 */
function TableRow(props) {
    const { user, toggleModal, selectUserAction } = props;
    const { id, name, email, lastSeen, access, flagged, isBlocked } = user;

    const navigate = useNavigate();

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
            <td role="cell" className="TableRow-iconCell">
                <label className="MAIN-table-label" htmlFor="access_level">Type:</label>
                <div className="MAIN-iconContainerCircle">
                    <img
                        alt={`User is ${access === "user" ? "regular user" : "admin"}`}
                        className="MAIN-iconUserType"
                        role="img"
                        title={access === "user" ? "Regular user" : "Admin user"}
                        src={access === "user" ? iconUserTypeUser : iconUserTypeAdmin}
                    />
                </div>
            </td>
            <td role="cell" className="TableRow-iconCell">
                <label className="MAIN-table-label" htmlFor="flag">Flag:</label>
                <div className="MAIN-iconContainerCircle">
                    <Flag flag={flagged} />
                </div>
            </td>
            <td role="cell" className="TableRow-iconCell">
                <label className="MAIN-table-label" htmlFor="blocked">Blocked:</label>
                <div className="MAIN-iconContainerCircle">
                    <img
                        alt={`User is ${isBlocked === "false" ? "un" : ""}blocked`}
                        role="img"
                        className={`${isBlocked === "false" ? "" : "MAIN-iconUserBlocked"}`}
                        title={`User is ${isBlocked === "false" ? "un" : ""}blocked`}
                        src={isBlocked === "false" ? iconUserIsNotBlocked : iconUserIsBlocked}
                    />
                </div>
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
                        onClick={() => { navigate("userInfo", { state: id }) }}
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
    selectUserAction: PropTypes.func.isRequired
}


export default TableRow;