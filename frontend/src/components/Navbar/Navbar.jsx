import {Link, useLocation} from "react-router-dom"

import FilmStrip from "../FilmStrip/FilmStrip"
import "./Navbar.css"
import userIcon from "../../assets/img/user.png"

const Navbar = ()=>{
    const location = useLocation()
    const currentPath = location.pathname;
    return(
        <div className={"nav-container"}>
            <FilmStrip />
            <nav>
                <Link className={"title-logo-link"} to="/">FLIX</Link>
                <div className={"navbar-standard-links"}>
                    <Link className={`navbar-standard-link ${currentPath == "/" ? "active-nav-link": ""}`} to ={"/"}>Browse</Link>
                    <Link className={`navbar-standard-link ${currentPath == "/recommendations" ? "active-nav-link": ""}`} to ={"/recommendations"}>Recommendations</Link>
                <div className={"login-wrapper"}>
                    <Link className={"login-link"} to="/login">Sign in</Link>
                    <img className={"user-icon"} src={userIcon} alt="login" />
                </div>
                </div>
            </nav>
            <FilmStrip isBottom={true}/>
        </div>
    )
}

export default Navbar;