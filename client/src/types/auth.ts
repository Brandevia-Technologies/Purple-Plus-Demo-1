// src/types/auth.ts
export type LoginData = {
  formType: "login";
  email: string;
  password: string;
};

export type OtpData = {
  formType: "otp";
  otp: string;
};

export type NewPasswordData = {
  formType: "newPassword";
  oldPassword: string;
  newPassword: string;
  confirmPassword: string;
};

export type AuthSubmitData = LoginData | OtpData | NewPasswordData;
