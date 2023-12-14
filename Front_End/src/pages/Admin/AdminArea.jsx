import { Outlet, NavLink } from "react-router-dom"
function AdminArea() {

    return (
        <div >
            <h2>Admin Area</h2>
            <nav role="navigation" aria-labelledby="secondLabel" aria-label="Secondary">
                <ul>
                    <li>
                        Dashboard
                        {/* <NavLink to="/">Dashboard</NavLink> */}
                    </li>
                    <li>
                        Users
                        {/* <NavLink to="/">Users</NavLink> */}
                    </li>
                    <li>
                        Settings
                        {/* <NavLink to="/">Settings</NavLink> */}
                    </li>
                </ul>
            </nav>
            <Outlet />
        </div>
    );
}

export default AdminArea;