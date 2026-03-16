import { createContext, useState, useEffect } from "react";
import api from "./api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./constants";
import { useNavigate } from "react-router-dom";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(true)
  const navigate = useNavigate()

  // Load user on app start
  useEffect(() => {
    if (localStorage.getItem(ACCESS_TOKEN)){
      setToken(localStorage.getItem(ACCESS_TOKEN))
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    setLoading(true);
    try {
        const res = await api.post("/api/token/", {username, password})
        localStorage.setItem(ACCESS_TOKEN, res.data.access)
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh)
       

    } catch (error) {
      alert(error);
    } finally {
      if (localStorage.getItem(ACCESS_TOKEN)){

        setToken(localStorage.getItem(ACCESS_TOKEN))
      }
      setLoading(false);
     
      navigate("/")
    }
  };

  const logout = () => {
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.removeItem(REFRESH_TOKEN);
    setToken(null)
  };

  const register = async (username, password) => {
    try{

      const res = await api.post("/api/user/register/", { username, password })
      setLoading(false)
      navigate("/login")
    } catch(error){
      alert(error);
      setLoading(false)
    }
  };

  const refreshAccessToken = async () => {
    const refresh = localStorage.getItem(REFRESH_TOKEN);
    if (!refresh) {
      logout();
      throw new Error("No refresh token available");
    }

    try {
      const res = await api.post("/api/token/refresh/", { refresh });
      localStorage.setItem(ACCESS_TOKEN, res.data.access);
      return res.data.access;
    } catch (error) {
      logout();
      throw new Error("Refresh token expired. Please log in again.");
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, register, refreshAccessToken, token }}>
      {children}
    </AuthContext.Provider>
  );
};