import React from "react";
import AuthForm from "../../components/AuthForm";
import axios from "axios";
import type { AuthSubmitData } from "../../types/auth";

const Login: React.FC = () => {
  const handleLogin = async (data: AuthSubmitData) => {
    if (data.formType !== "login") return;
    try {
      const response = await axios.post(
        "https://purple-plus-auth-demo.onrender.com/api/v1/accounts/login/",
        { email: data.email, password: data.password }
      );

      const { access, refresh, user } = response.data;

      // Save tokens for future requests
      localStorage.setItem("accessToken", access);
      localStorage.setItem("refreshToken", refresh);
      localStorage.setItem("user", JSON.stringify(user));

      // Redirect based on user role
      if (user.is_superuser) {
        window.location.href = "/create-staff";
      } else if (user.is_staff) {
        window.location.href = "/hr-dashboard";
      } else {
        window.location.href = "/patient-dashboard";
      }
    } catch (error: unknown) {
      // Log the full error object
      console.error("Login error:", error);
      // If it's an Axios error, you can get more details:
      if (axios.isAxiosError(error)) {
        console.error("Response data:", error.response?.data);
        console.error("Status code:", error.response?.status);
      }
      alert("Login failed: check credentials.");
    }
  };
  return (
    <AuthForm
      heading="Welcome Back"
      description="It's been a while but we're always here for your medical needs."
      btnText="Login"
      text="Forgot Password?"
      formType="login"
      onSubmit={handleLogin}
    />
  );
};

export default Login;
