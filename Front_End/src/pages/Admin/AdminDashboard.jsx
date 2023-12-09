import iconUserBlock from "../../assets/icon_user_block.svg";
import iconUserDelete from "../../assets/icon_user_delete.svg";
import iconUserMore from "../../assets/icon_user_more.svg";
import "./admindashboard.css"
function AdminDashboard() {

    return (
        <div className="AdminDashboard">
            <h2>Admin Dashboard</h2>
            <h3>Users Table</h3>
            <table className="AdminDashboard-UserTable" role="table">
                <thead role="rowgroup">
                    <tr role="row">
                        <th role="columnheader">Name</th>
                        <th role="columnheader">Email</th>
                        <th role="columnheader">Last seen</th>
                        <th role="columnheader">Actions</th>
                    </tr>
                </thead>
                <tbody role="rowgroup">
                    <tr role="row">
                        <td role="cell">
                            <label className="AdminDashboard-UserTable-Label" htmlFor="name">Name:</label>
                            Alfreds Futterkiste
                        </td>
                        <td role="cell">
                            <label className="AdminDashboard-UserTable-Label" htmlFor="email">Email:</label>
                            Maria@Anders
                        </td>
                        <td role="cell">
                            <label className="AdminDashboard-UserTable-Label" htmlFor="last-seen">Last seen:</label>
                            Germany
                        </td>
                        <td role="cell">
                            <label className="AdminDashboard-UserTable-Label" htmlFor="last-seen">Actions:</label>
                            <div className="AdminDashboard-UserTable-IconsContainer">
                                <img
                                    alt="More user information"
                                    className="AdminDashboard-UserTable-icon"
                                    role="button"
                                    title="More information"
                                    src={iconUserMore} />
                                <img
                                    alt="Block user"
                                    className="AdminDashboard-UserTable-icon"
                                    role="button"
                                    title="Block user"
                                    src={iconUserBlock} />
                                <img
                                    alt="Delete user"
                                    className="AdminDashboard-UserTable-icon"
                                    role="button"
                                    title="Delete user"
                                    src={iconUserDelete} />
                            </div>
                        </td>
                    </tr>
                    <tr role="row">
                        <td role="cell">
                            <label className="AdminDashboard-UserTable-Label" htmlFor="name">Name:</label>
                            Alfreds Futterkiste
                        </td>
                        <td role="cell">
                            <label className="AdminDashboard-UserTable-Label" htmlFor="email">Email:</label>
                            Maria@Anders
                        </td>
                        <td role="cell">
                            <label className="AdminDashboard-UserTable-Label" htmlFor="last-seen">Last seen:</label>
                            Germany
                        </td>
                        <td role="cell" className="AdminDashboard-UserTable-MobileTd">
                            <label className="AdminDashboard-UserTable-Label" htmlFor="last-seen">Actions:</label>
                            <div>
                                <img
                                    alt="More user information"
                                    className="AdminDashboard-UserTable-icon"
                                    role="button"
                                    title="More information"
                                    src={iconUserMore} />
                                <img
                                    alt="Block user"
                                    className="AdminDashboard-UserTable-icon"
                                    role="button"
                                    title="Block user"
                                    src={iconUserBlock} />
                                <img
                                    alt="Delete user"
                                    className="AdminDashboard-UserTable-icon"
                                    role="button"
                                    title="Delete user"
                                    src={iconUserDelete} />
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
}

export default AdminDashboard;