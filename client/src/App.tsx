import React, { useEffect } from "react";
import { Routes, Route, useLocation, useNavigate } from "react-router-dom";
import Login from "./pages/Auth/Login";
import ForgotPassword from "./pages/Auth/ForgotPassword";
import NewPassword from "./pages/Auth/NewPassword";
import Dashboard from "./pages/Dashboard/Dashboard";
import CreateStaff from "./pages/Auth/CreateStaff";

const App: React.FC = () => {
  // const location = useLocation();
  // const navigate = useNavigate();

  // useEffect(() => {
  //   const userInfo = JSON.parse(localStorage.getItem("user") || "null");
  //   if (!userInfo) return;

  //   if (
  //     userInfo.must_change_password &&
  //     location.pathname !== "/new-password"
  //   ) {
  //     navigate("/new-password", { replace: true }); // <-- use navigate instead of window.location.href
  //   }
  // }, [location.pathname, navigate]);

  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/new-password" element={<NewPassword />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/create-staff" element={<CreateStaff />} />
    </Routes>
  );
};

export default App;
