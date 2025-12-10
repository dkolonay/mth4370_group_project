import { useContext, useEffect } from "react"
import { AuthContext } from "../AuthContext"
import { useNavigate } from "react-router-dom"

function Logout() {
    const navigate = useNavigate()
    const {logout} = useContext(AuthContext)
    useEffect(()=>{

        logout()
        navigate('/login')
    }, [])
    return null
}

export default Logout;