import { useState } from "react"
import { Outlet, NavLink } from "react-router-dom"
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { setUserLogout } from "../redux/user/userSlice";
import MenuIcon from "../assets/icon_menu.svg"
import api from "../config/axios"
import APIURL from "../config/apiUrls";
import "./navbar.css"

function NavBar() {
    const [showNavbar, setShowNavbar] = useState(false)

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const logoutUser = async () => {
        const response = await api.post(APIURL.LOGOUT);
        dispatch(setUserLogout());
        navigate("/login");
    }

    const handleShowNavbar = () => {
        setShowNavbar(!showNavbar)
    }
    return (
        <>
            <nav className="NavBar" role="navigation" aria-labelledby="firstLabel" aria-label="Primary">
                <div className="NavBar-logo">
                    <span>/</span>SafeDev <span>_</span>
                </div>
                <div className="NavBar-menu-icon" onClick={handleShowNavbar}>
                    <img src={MenuIcon} alt="Menu Icon" className={`NavBar-menu-icon-sgv  ${showNavbar && 'active'}`} />
                </div>
                <div className={`NavBar-nav-elements  ${showNavbar && 'active'}`} role="navigation" aria-label="Main">
                    <ul>
                        <li>
                            <NavLink to="/" onClick={handleShowNavbar}>Home</NavLink>
                        </li>
                        <li>
                            <NavLink to="/login" onClick={handleShowNavbar}>Login</NavLink>
                        </li>
                        <li>
                            <NavLink to="/signup" onClick={handleShowNavbar}>Signup</NavLink>
                        </li>
                        <li>
                            <a href="#!" onClick={() => { logoutUser(); handleShowNavbar(); }}>Logout</a>
                        </li>
                        <li>
                            <NavLink to="/admin_login" onClick={handleShowNavbar}>ADMIN login</NavLink>
                        </li>
                        <li>
                            <NavLink to="/admin_dashboard" onClick={handleShowNavbar}>ADMIN dashboard</NavLink>
                        </li>
                    </ul>
                </div>
            </nav>
            <Outlet />
        </>
    )
}

export default NavBar;