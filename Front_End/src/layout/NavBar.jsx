import { useState } from "react"
import { Outlet, NavLink } from "react-router-dom"
import MenuIcon from "../assets/icon_menu.svg"
import "./navbar.css"

function NavBar() {
    const [showNavbar, setShowNavbar] = useState(false)

    const handleShowNavbar = () => {
        setShowNavbar(!showNavbar)
    }
    return (
        <>
            <nav className="NavBar">
                <div className="NavBar-logo">
                    Safe Dev
                </div>
                <div className="NavBar-menu-icon" onClick={handleShowNavbar}>
                    <img src={MenuIcon} alt="Menu Icon" className={`NavBar-menu-icon-sgv  ${showNavbar && 'active'}`} />
                </div>
                <div className={`NavBar-nav-elements  ${showNavbar && 'active'}`}>
                    <ul>
                        <li>
                            <NavLink to="/">Home</NavLink>
                        </li>
                        <li>
                            <NavLink to="/login">Login</NavLink>
                        </li>
                        <li>
                            <NavLink to="/signup">Signup</NavLink>
                        </li>
                    </ul>
                </div>

            </nav>
            <Outlet />
        </>
    )
}

export default NavBar;