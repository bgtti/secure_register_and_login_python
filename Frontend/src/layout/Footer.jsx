import { NavLink } from "react-router-dom"
import GithubIcon from "../assets/icons/github.png";
import "./footer.css"

function Footer() {
    return (
        <footer className="Footer">
            <ul className="Footer-Nav">
                <li>
                    <NavLink to="contact">Contact</NavLink>
                </li>
            </ul>
            <div>
                <p>2022 by </p>
                <a href="https://github.com/bgtti"><img src={GithubIcon} alt="github repo" /></a>
            </div>

        </footer>
    )
}

export default Footer;