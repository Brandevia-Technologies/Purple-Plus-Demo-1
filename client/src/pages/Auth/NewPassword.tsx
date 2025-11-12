import React from "react";
import AuthForm from "../../components/AuthForm";
const NewPassword: React.FC = () => {
  return (
    <AuthForm
      heading="Protect Your Health Details"
      description="Protect your medical health records. Your new password is to contain special characters like @#$& and at least one digit."
          btnText="Enter"
          formType="newPassword"
    />
  );
};

export default NewPassword;
