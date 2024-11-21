import { Outlet, NavLink } from "react-router-dom"
import { Helmet } from "react-helmet-async";
import "./accountMain.css"

function AccountMain() {

    return (
        <div className="AccountMain">
            <Helmet>
                <title>Account</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>
            <h2>Account</h2>
            <nav role="navigation" aria-labelledby="secondLabel" aria-label="Secondary">
                <ul>
                    <li>
                        <NavLink to="userdashboard" >Dashboard</NavLink>
                    </li>
                    <li>
                        <NavLink to="acctSettings">Settings</NavLink>
                    </li>
                </ul>
            </nav>
            <Outlet />
        </div>
    );
}

export default AccountMain;