import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom"

import ProtectedRoute from "./components/ProtectedRoute"

import Login from "./pages/Login"
import Register from "./pages/Register"
import Home from "./pages/Home/Home"
import NotFound from "./pages/NotFound"

function Logout(){
  localStorage.clear()
  return <Navigate to="/login"/>
}

function RegisterAndLogout(){
  localStorage.clear() // remove potential old access tokens before registering new user
  return <Register />
}

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route 
        path="/" 
        element={
          <ProtectedRoute>
            <Home/>
          </ProtectedRoute>
        }
          />
        <Route path="/login" element={<Login/>}/>
        <Route path="/logout" element={<Logout/>}/>
        <Route path="/register" element={<RegisterAndLogout/>}/>
        <Route path="*" element={<NotFound/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
