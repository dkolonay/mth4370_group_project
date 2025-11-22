import {Link} from "react-router-dom"

import "./Navbar.css"

const Navbar = ()=>{
    return(
        <div className={"nav-container"}>
            <nav>
                <Link className={"title-logo-link"} to="/">MovieApp</Link>
                <div className={"navbar-standard-links"}>
                    <Link className={"navbar-standard-link"} to ={"/"}>Browse</Link>
                    <Link className={"navbar-standard-link"} to ={"/recommendations"}>Recommendations</Link>
                </div>
                 <Link className={"login-link"} to="/login">Login</Link>
            </nav>
        </div>
    )
}

export default Navbar;