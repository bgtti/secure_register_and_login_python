import UsersTable from "./UsersTable/UsersTable";

import "./admindashboard.css"
function AdminDashboard() {

    return (
        <div className="AdminDashboard">
            <h2>Admin Dashboard</h2>
            <UsersTable></UsersTable>
        </div>
    );
}

export default AdminDashboard;