import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AuthForm from "../../components/AuthForm";
import axios from "axios";
import type { AuthSubmitData } from "../../types/auth";

const NewPassword: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user") || "null");
    const token = localStorage.getItem("accessToken");

    // Not logged in? Send to login
    if (!user || !token) {
      navigate("/login");
      return;
    }

    // Already changed password? Redirect based on role
    if (!user.must_change_password) {
      if (user.is_superuser) navigate("/create-staff");
      else if (user.is_staff) navigate("/hr-dashboard");
      else navigate("/patient-dashboard");
    }
  }, [navigate]);

  const handleNewPassword = async (data: AuthSubmitData) => {
    if (data.formType !== "newPassword") return;

    // Passwords match check
    if (data.newPassword !== data.confirmPassword) {
      alert("New password and confirm password do not match.");
      return;
    }

    const token = localStorage.getItem("accessToken");
    if (!token) {
      alert("You must be logged in to change your password.");
      navigate("/login");
      return;
    }

    try {
      const response = await axios.put(
        "https://purple-plus-auth-demo.onrender.com/api/v1/accounts/change/password/",
        {
          old_pw: data.oldPassword, // <-- changed
          new_pw: data.newPassword, // <-- changed
          confirm_new_pw: data.confirmPassword,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      alert("Password changed successfully!");

      // Update user in localStorage to remove must_change_password
      const user = JSON.parse(localStorage.getItem("user") || "{}");
      const updatedUser = { ...user, must_change_password: false };
      localStorage.setItem("user", JSON.stringify(updatedUser));

      // Redirect based on role
      if (updatedUser.is_superuser) navigate("/create-staff");
      else if (updatedUser.is_staff) navigate("/hr-dashboard");
      else navigate("/patient-dashboard");
    } catch (error: unknown) {
      console.error("Password change error:", error);
      if (axios.isAxiosError(error)) {
        console.error("Response data:", error.response?.data);
        console.error("Status code:", error.response?.status);
        if (error.response?.data?.message) {
          alert(`Error: ${error.response.data.message}`);
        }
      } else {
        alert("Password change failed.");
      }
    }
  };

  return (
    <AuthForm
      heading="Protect Your Health Details"
      description="Your new password must contain special characters like @#$& and at least one digit."
      btnText="Enter"
      formType="newPassword"
      onSubmit={handleNewPassword}
    />
  );
};

export default NewPassword;
