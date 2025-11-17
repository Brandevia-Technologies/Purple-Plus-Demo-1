import React, { useState } from "react";
import { MdPassword, MdOutlineMail } from "react-icons/md";
import { Link } from "react-router-dom";
import type { AuthSubmitData } from "../types/auth";

interface AuthFormProps {
  heading: string;
  description: string;
  btnText: string;
  showOTP?: boolean;
  text?: string;
  formType?: "login" | "otp" | "newPassword";
  onSubmit?: (data: AuthSubmitData) => void;
}

const AuthForm: React.FC<AuthFormProps> = ({
  heading,
  description,
  btnText,
  showOTP = false,
  text,
  formType,
  onSubmit,
}) => {
  const [btnClicked, setBtnClicked] = useState(false);
  const [isDisabled, setIsDisabled] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [otp, setOtp] = useState("");

  const [oldPassword, setOldPassword] = useState("");
  const [newPasswordValue, setNewPasswordValue] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [fieldErrors, setFieldErrors] = useState<{
    email?: string;
    password?: string;
  }>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setBtnClicked(true);

    // Reset field errors
    setFieldErrors({});

    let errors: typeof fieldErrors = {};

    // Validate required fields
    if (formType === "login") {
      if (!email.trim()) errors.email = "Email is required";
      if (!password.trim()) errors.password = "Password is required";
    }

    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return; // stop submission
    }

    let payload: AuthSubmitData;

    if (formType === "login") {
      payload = { formType: "login", email, password };
    } else if (formType === "otp") {
      payload = { formType: "otp", otp };
    } else if (formType === "newPassword") {
      payload = {
        formType: "newPassword",
        oldPassword,
        newPassword: newPasswordValue,
        confirmPassword,
      };
    } else {
      return;
    }

    if (onSubmit) {
      onSubmit(payload, setFieldErrors); // pass setFieldErrors to parent
    }
  };

  const inputClass =
    "pl-12 text-gray-700 text-sm p-[0.5rem_1rem] border border-gray-200 rounded-md focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-100 placeholder:text-gray-400 w-full h-auto px-4 transition-all";

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-purple-50 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-xl shadow-lg p-8 md:p-10">
          <form onSubmit={handleSubmit} className="w-full">
            <h1 className="text-3xl mb-2 font-bold text-gray-900 text-center">
              {heading}
            </h1>
            <p className="text-sm text-gray-500 text-center mb-8">
              {description}
            </p>

            <div className="space-y-5">
              <div className="relative">
                <input
                  type={formType === "newPassword" ? "password" : "email"}
                  placeholder={
                    formType === "newPassword" ? "Old Password" : "Email"
                  }
                  className={inputClass}
                  value={formType === "newPassword" ? oldPassword : email}
                  onChange={(e) =>
                    formType === "newPassword"
                      ? setOldPassword(e.target.value)
                      : setEmail(e.target.value)
                  }
                />
                {formType === "newPassword" ? (
                  <MdPassword className="absolute left-4 top-1/2 -translate-y-1/2 text-xl text-gray-400" />
                ) : (
                  <MdOutlineMail className="absolute left-4 top-1/2 -translate-y-1/2 text-xl text-gray-400" />
                )}
              </div>

              {formType === "newPassword" ? (
                <>
                  <div>
                    <div className="relative">
                      <input
                        type="password"
                        placeholder="New Password"
                        className={inputClass}
                        value={newPasswordValue}
                        onChange={(e) => setNewPasswordValue(e.target.value)}
                      />

                      <MdPassword className="absolute left-4 top-1/2 -translate-y-1/2 text-xl text-gray-400" />
                    </div>
                  </div>
                  <div className="relative">
                    <div className="relative">
                      <input
                        type="password"
                        placeholder="Re-enter New Password"
                        className={inputClass}
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                      />

                      <MdPassword className="absolute left-4 top-1/2 -translate-y-1/2 text-xl text-gray-400" />
                    </div>
                  </div>
                </>
              ) : (
                <div className="relative">
                  <div className="relative">
                    <input
                      type={showOTP ? "text" : "password"}
                      inputMode={showOTP ? "numeric" : undefined}
                      pattern={showOTP ? "[0-9]*" : undefined}
                      placeholder={showOTP ? "Input OTP code here" : "Password"}
                      className={inputClass}
                      value={showOTP ? otp : password}
                      onChange={(e) =>
                        showOTP
                          ? setOtp(e.target.value)
                          : setPassword(e.target.value)
                      }
                    />
                    <MdPassword className="absolute left-4 top-1/2 -translate-y-1/2 text-xl text-gray-400" />
                  </div>

                  {!showOTP && text && btnClicked && (
                    <Link
                      to="/forgot-password"
                      className="block text-right text-sm text-red-500 mt-3 hover:text-red-600 transition-colors"
                    >
                      {text}
                    </Link>
                  )}
                  {showOTP && btnClicked && (
                    <p className="text-right text-xs text-gray-500 mt-3 cursor-pointer">
                      Didn't receive an OTP?{" "}
                      <span className="font-semibold text-purple-600 hover:text-purple-700 transition-colors">
                        Resend
                      </span>
                    </p>
                  )}
                </div>
              )}
            </div>

            <button
              type="submit"
              disabled={isDisabled}
              className={`py-2 cursor-pointer px-6 rounded-md w-full text-white font-semibold text-base mt-8 transition-all duration-300 ${
                isDisabled
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-purple-600 hover:bg-purple-700 active:scale-[0.98] shadow-md hover:shadow-lg"
              }`}
            >
              {btnText}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AuthForm;
