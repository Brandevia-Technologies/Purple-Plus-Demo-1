import React from "react";
import AuthForm from "../../components/AuthForm";
const ForgotPassword: React.FC = () => {
  return (
    <AuthForm
      heading="Forgot Your Password?"
      description="That's fine, Fill in your account email to recieve an OTP to reset your password."
      btnText="Request OTP"
      showOTP={true}
    />
  );
};

export default ForgotPassword;
