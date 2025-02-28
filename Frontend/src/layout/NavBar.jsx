import { useState } from "react"
import { Outlet, NavLink } from "react-router-dom"
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { setLoader } from "../redux/loader/loaderSlice";
import { logoutUser } from "../config/apiHandler/authSession/logout";
import { setNightModeFrontEnd } from "../config/apiHandler/userSettings/setNightMode";
import MenuIcon from "../assets/icon_menu.svg"
import IconDarkMode from "../assets/icon_mode_dark.svg"
import IconLightMode from "../assets/icon_mode_light.svg"
import "./navbar.css"

function NavBar() {
    const [showNavbar, setShowNavbar] = useState(false)
    const user = useSelector((state) => state.user);

    //Night mode settings: getting stored at redux
    const nightModeOn = useSelector((state) => state.preferences.nightMode);

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const logOut = () => {
        dispatch(setLoader(true))
        logoutUser()
            .then(res => {
                if (!res.response) {
                    console.warn("Check logout function.");
                }
            })
            .catch(error => {
                console.error("Error in logout function.", error);
            })
            .finally(() => {
                dispatch(setLoader(false));
            })
    }

    const handleShowNavbar = () => {
        setShowNavbar(!showNavbar)
    }

    const changeDisplayMode = () => {
        setNightModeFrontEnd(!nightModeOn)
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
                        {
                            (!user || !user.loggedIn) && (
                                <>
                                    <li>
                                        <NavLink to="/login" onClick={handleShowNavbar}>Login</NavLink>
                                    </li>
                                    <li>
                                        <NavLink to="/signup" onClick={handleShowNavbar}>Signup</NavLink>
                                    </li>
                                    <li className="Nav-modeIcon">
                                        <img
                                            alt={`${nightModeOn ? "dark mode" : "light mode"}`}
                                            role="button"
                                            title={nightModeOn ? "Switch to light mode" : "Switch to dark mode"}
                                            src={nightModeOn ? IconLightMode : IconDarkMode}
                                            onClick={changeDisplayMode}
                                        />
                                    </li>
                                </>

                            )
                        }
                        {
                            user && user.loggedIn && (
                                <>
                                    <li>
                                        <NavLink to="/login" onClick={() => { logOut(); handleShowNavbar(); }}>Logout</NavLink>
                                    </li>
                                    <li>
                                        <NavLink to="/userAccount" onClick={handleShowNavbar}>Account</NavLink>
                                    </li>
                                </>

                            )
                        }
                        {
                            user && (user.access === "admin" || user.access === "super_admin") && (
                                <li>
                                    <NavLink to="/adminArea" onClick={handleShowNavbar}>Admin</NavLink>
                                </li>
                            )
                        }
                    </ul>
                </div>
            </nav>
            <Outlet />
        </>
    )
}

export default NavBar;