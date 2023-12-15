import PropTypes from 'prop-types';
import iconUserBlock from "../../../assets/icon_user_block.svg";
import iconUserDelete from "../../../assets/icon_user_delete.svg";
import iconUserMore from "../../../assets/icon_user_more.svg";
// import "../admindashboard.css"

function UsersTableRow(props) {
    const { selectUserAction, toggleModal, user } = props
    const { name, email, lastSeen, isBlocked, uuid } = user;

    return (
        <tr role="row">
            <td role="cell">
                <label className="UserTable-Label" htmlFor="name">Name:</label>
                {name}
            </td>
            <td role="cell">
                <label className="UserTable-Label" htmlFor="email">Email:</label>
                {email}
            </td>
            <td role="cell">
                <label className="UserTable-Label" htmlFor="last-seen">Last seen:</label>
                {lastSeen}
            </td>
            <td role="cell">
                <label className="UserTable-Label" htmlFor="blocked">Blocked:</label>
                {isBlocked}
            </td>
            <td role="cell">
                <label className="UserTable-Label" htmlFor="actions">Actions:</label>
                <div className="UserTable-IconsContainer">
                    <img
                        alt="More user information"
                        className="UserTable-icon"
                        role="button"
                        title="More information"
                        src={iconUserMore} />
                    <img
                        alt="Block user"
                        className="UserTable-icon"
                        role="button"
                        title="Block user"
                        src={iconUserBlock}
                        onClick={() => { selectUserAction(uuid, "block"); toggleModal() }}
                    />
                    <img
                        alt="Delete user"
                        className="UserTable-icon"
                        role="button"
                        title="Delete user"
                        src={iconUserDelete}
                        onClick={() => { selectUserAction(uuid, "delete"); toggleModal() }}
                    />
                </div>
            </td>
        </tr>
    );
};

UsersTableRow.propTypes = {
    user: PropTypes.shape({
        name: PropTypes.string.isRequired,
        email: PropTypes.string.isRequired,
        lastSeen: PropTypes.string.isRequired,
        isBlocked: PropTypes.string.isRequired,
        uuid: PropTypes.string.isRequired
    }).isRequired,
    toggleModal: PropTypes.func.isRequired,
    selectUserAction: PropTypes.func.isRequired
}


export default UsersTableRow;