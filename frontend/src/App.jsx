import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home/Home";
import MovieDetailsPage from "./pages/MovieDetailsPage/MovieDetailsPage";
import NotFound from "./pages/NotFound";
import Logout from "./components/Logout";
import { AuthProvider, AuthContext } from "./AuthContext";
import { useContext, useEffect } from "react";
import { setupApiInterceptors } from "./api";

function RegisterAndLogout() {
  localStorage.clear(); // remove potential old access tokens before registering new user
  return <Register />;
}

function App() {
  const auth = useContext(AuthContext);
  useEffect(() => {
    setupApiInterceptors(auth);
  }, [auth]);

  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/register" element={<RegisterAndLogout />} />
          <Route path="/movie-details/:id" element={<MovieDetailsPage />} />

          <Route path="*" element={<NotFound />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
