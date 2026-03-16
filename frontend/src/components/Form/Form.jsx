import { useState } from "react";
import api from "../../api";
import { useNavigate, Link } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../constants";
import "./Form.css"
import LoadingIndicator from "../LoadingIndicator/LoadingIndicator";
import { useContext } from "react";
import { AuthContext } from "../../AuthContext";

const Form = ({ method }) => {
  const {login, register} = useContext(AuthContext)
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const isLogin = method === "login";

  const handleSubmit = (e)=>{
    e.preventDefault()
    if (isLogin){
      login(username, password)
    } else {
      register(username, password)
    }
  }

  return (
    <form onSubmit={handleSubmit} className={"form-container"}>
      <h1>{isLogin? "Login": "Register"}</h1>
      <input
        type="text"
        className={"form-input"}
        value={username}
        onChange={(e) => {
          setUsername(e.target.value);
        }}
        placeholder="Username"
      />
      <input
        type="password"
        className={"form-input"}
        value={password}
        onChange={(e) => {
          setPassword(e.target.value);
        }}
        placeholder="Password"
      />
      {loading && <LoadingIndicator/>}
      <button className={"form-button"} type={"submit"}>
        {isLogin? "Login": "Register"}
      </button>
      <span>{isLogin ? "Don't have an account? " : "Already have an account? "}<Link to={isLogin ? "/register" : "/login"}> {isLogin ? "Register" : "Login"} here</Link></span>
    </form>
  );
};

export default Form;
