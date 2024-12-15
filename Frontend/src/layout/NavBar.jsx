import { useState } from "react"
import { Outlet, NavLink } from "react-router-dom"
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { setLoader } from "../redux/loader/loaderSlice";
import { logoutUser } from "../config/apiHandler/authMain/logout";
import MenuIcon from "../assets/icon_menu.svg"
import "./navbar.css"

function NavBar() {
    const [showNavbar, setShowNavbar] = useState(false)
    const user = useSelector((state) => state.user);

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
                            (!user || user.email === "") && (
                                <>
                                    <li>
                                        <NavLink to="/login" onClick={handleShowNavbar}>Login</NavLink>
                                    </li>
                                    <li>
                                        <NavLink to="/signup" onClick={handleShowNavbar}>Signup</NavLink>
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