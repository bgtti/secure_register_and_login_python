import { Outlet, NavLink } from "react-router-dom"
import { Helmet } from "react-helmet-async";

function AccountMain() {

    return (
        <div>
            <Helmet>
                <title>Account</title>
                <meta name="robots" content="noindex, nofollow" />
            </Helmet>
            <h2>Account</h2>
            <nav aria-label="Secondary" aria-labelledby="secondLabel" className="MAIN-subNavigation" role="navigation">
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