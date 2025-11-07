import React from "react";
import { MdPassword, MdOutlineMail } from "react-icons/md";

import assets from "../assets/assets";

// Define props type
interface AuthFormProps {
  heading: string;
  description: string;
  btnText: string;
  showOTP?: boolean;
  text?: string;
}

const AuthForm: React.FC<AuthFormProps> = ({
  heading,
  description,
  btnText,
  showOTP = false,
  text,
}) => {
  const inputClass =
    "pl-12 text-gray-700 text-sm pr-4 py-2.5 border border-gray-300 rounded-md focus:outline-none placeholder:text-gray-900 w-full h-auto px-4";

  return (
    <div className="flex gap-10 relative">
      <section className="min-h-screen flex items-center justify-between px-20">
        <form>
          <h1 className="text-3xl mb-2 font-bold text-gray-900 text-center">
            {heading}
          </h1>
          <p className="text-sm text-gray-500 text-center">{description}</p>
          <div className="mt-6">
            <div className="flex flex-col gap-6">
              <div className="relative w-full">
                <input
                  type="email"
                  placeholder="Email"
                  className={inputClass}
                />
                <MdOutlineMail className="absolute left-4 top-1/2 -translate-y-1/2 text-xl" />
              </div>

              <div className="relative w-full">
                <div className="relative">
                  <input
                    type={showOTP ? "number" : "password"}
                    placeholder={showOTP ? "Input OTP code here" : "Password"}
                    className={inputClass}
                  />
                  <MdPassword className="absolute left-4 top-1/2 -translate-y-1/2 text-xl" />
                </div>
                {!showOTP && text && (
                  <p className="text-right text-sm text-warning-red mt-2">
                    {text}
                  </p>
                )}
              </div>
            </div>
            <button
              type="submit"
              className="py-[11px] cursor-pointer px-6 rounded-full w-full  text-white font-semibold text-md mt-10 bg-purple-primary"
            >
              {btnText}
            </button>
          </div>
        </form>
      </section>
      {/* doodle */}
      <div className="absolute right-0">
        <img src={assets.doodle} alt="Doodle" />
      </div>{" "}
    </div>
  );
};

export default AuthForm;
