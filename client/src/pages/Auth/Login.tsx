import React from "react";
import AuthForm from "../../components/AuthForm";
import {Link} from 'react-router-dom'
const Login: React.FC = () => {
  return (
    <AuthForm
      heading="Welcome Back"
      description="It's been a while but we're always here for your medical needs."
      btnText="Login"
      text="Forgot Password?"
    />
  );
};

export default Login;
