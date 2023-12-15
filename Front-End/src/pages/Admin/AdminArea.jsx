import { Outlet, NavLink } from "react-router-dom"
import "./adminArea.css"

function AdminArea() {

    return (
        <div className="AdminArea">
            <h2>Admin Area</h2>
            <nav role="navigation" aria-labelledby="secondLabel" aria-label="Secondary">
                <ul>
                    <li>
                        <NavLink to="dashboard" >Dashboard</NavLink>
                    </li>
                    <li>
                        <NavLink to="usersTable" >Users</NavLink>
                    </li>
                    <li>
                        <NavLink to="adminSettings" >Settings</NavLink>
                    </li>
                </ul>
            </nav>
            <Outlet />
        </div>
    );
}

export default AdminArea;