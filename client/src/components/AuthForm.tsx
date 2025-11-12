import React, { useState } from "react";
import { MdPassword, MdOutlineMail } from "react-icons/md";
import { Link } from "react-router-dom";
import assets from "../assets/assets";

interface AuthFormProps {
  heading: string;
  description: string;
  btnText: string;
  showOTP?: boolean;
  text?: string;
  formType?: "login" | "otp" | "newPassword";
}

const AuthForm: React.FC<AuthFormProps> = ({
  heading,
  description,
  btnText,
  showOTP = false,
  text,
  formType,
}) => {
  const [btnClicked, setBtnClicked] = useState(false);
  const [isDisabled, setIsDisabled] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setBtnClicked(true);
    if (showOTP) setIsDisabled(true); // disable only on OTP page
    // Add OTP logic here
  };

  const inputClass =
    "pl-12 text-gray-700 text-sm p-[0.5rem_1rem] border border-light-border rounded-md focus:outline-none placeholder:text-gray-900 w-full h-auto px-4";

  return (
    <div className="flex flex-col md:flex-row items-center justify-between gap-10 px-4 md:px-10 min-h-screen">
      <section className="flex-1 flex flex-col items-center justify-center">
        <form onSubmit={handleSubmit} className="w-full max-w-sm">
          <h1 className="text-[1.625rem] mb-2 font-bold text-gray-900 text-center">
            {heading}
          </h1>
          <p className="text-xs text-gray-500 text-center">{description}</p>
          <div className="mt-6 space-y-6">
            <div className="relative">
              <input
                type={formType === "newPassword" ? "password" : "email"}
                placeholder={
                  formType === "newPassword" ? "Old Password" : "Email"
                }
                className={inputClass}
              />
              {formType === "newPassword" ? (
                <MdPassword className="absolute left-4 top-1/2 -translate-y-1/2 text-xl" />
              ) : (
                <MdOutlineMail className="absolute left-4 top-1/2 -translate-y-1/2 text-xl" />
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
                    />
                    <MdPassword className="absolute left-4 top-1/2 -translate-y-1/2 text-xl" />
                  </div>
                  {/* Add Error Message heere */}
                </div>
                <div className="relative">
                  <div className="relative">
                    <input
                      type="password"
                      placeholder="Re-enter New Password"
                      className={inputClass}
                    />
                    <MdPassword className="absolute left-4 top-1/2 -translate-y-1/2 text-xl" />
                  </div>
                </div>
              </>
            ) : (
              <div className="relative">
                <div className="relative">
                  {" "}
                  <input
                    type={showOTP ? "text" : "password"}
                    inputMode={showOTP ? "numeric" : undefined}
                    pattern={showOTP ? "[0-9]*" : undefined}
                    placeholder={showOTP ? "Input OTP code here" : "Password"}
                    className={inputClass}
                  />
                  <MdPassword className="absolute left-4 top-1/2 -translate-y-1/2 text-xl" />
                </div>

                {!showOTP && text && !btnClicked && (
                  <Link
                    to="/forgot-password"
                    className="block text-right text-sm text-warning-red mt-3"
                  >
                    {text}
                  </Link>
                )}

                {showOTP && btnClicked && (
                  <p className="text-right text-xs text-grey-400 mt-3 cursor-pointer">
                    Didn’t receive an OTP?{" "}
                    <span className="font-semibold text-purple-primary">
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
            className={`py-[11px] px-6 rounded-full w-full text-white font-semibold text-md mt-10 cursor-pointer transition-colors ${
              isDisabled
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-purple-primary"
            }`}
          >
            {btnText}
          </button>
        </form>
      </section>

      <div className="flex-1 hidden md:flex justify-center">
        <img
          src={assets.doodle}
          alt="Doodle"
          className="max-w-full min-h-screen object-contain"
        />
      </div>
    </div>
  );
};

export default AuthForm;
