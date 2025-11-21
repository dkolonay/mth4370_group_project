import {Link} from "react-router-dom"

import "./Navbar.css"

const Navbar = ()=>{
    return(
        <div className={"nav-container"}>
            <nav>
                <Link className={"title-logo-link"} to="/">MovieApp</Link>
                 <Link className={"login-link"} to="/login">Login</Link>
            </nav>
        </div>
    )
}

export default Navbar;