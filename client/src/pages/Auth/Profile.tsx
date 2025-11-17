// import React, { useState, useEffect } from "react";
// import axios from "axios";

// const Profile: React.FC = () => {
//   const [user, setUser] = useState<any>(null);
//   const [oldPassword, setOldPassword] = useState("");
//   const [newPassword, setNewPassword] = useState("");
//   const [confirmPassword, setConfirmPassword] = useState("");

//   useEffect(() => {
//     const storedUser = localStorage.getItem("user");
//     if (storedUser) setUser(JSON.parse(storedUser));
//   }, []);

//   const handleChangePassword = async () => {
//     const token = localStorage.getItem("accessToken");
//     if (!token) return alert("Not logged in");

//     try {
//       const response = await axios.post(
//         "https://purple-plus-auth-demo.onrender.com/api/v1/accounts/change-password/",
//         { oldPassword, newPassword, confirmPassword },
//         { headers: { Authorization: `Bearer ${token}` } }
//       );

//       alert("Password changed successfully!");
//     } catch (error: any) {
//       console.error("Password change error:", error);
//       if (axios.isAxiosError(error)) {
//         console.error("Response data:", error.response?.data);
//         alert(
//           `Error: ${error.response?.data?.message || "Password change failed"}`
//         );
//       } else {
//         alert("Password change failed.");
//       }
//     }
//   };

//   return (
//     <div className="p-8">
//       <h1>Profile</h1>
//       <p>Email: {user?.email}</p>
//       <div>
//         <input
//           type="password"
//           placeholder="Old Password"
//           value={oldPassword}
//           onChange={(e) => setOldPassword(e.target.value)}
//         />
//         <input
//           type="password"
//           placeholder="New Password"
//           value={newPassword}
//           onChange={(e) => setNewPassword(e.target.value)}
//         />
//         <input
//           type="password"
//           placeholder="Confirm New Password"
//           value={confirmPassword}
//           onChange={(e) => setConfirmPassword(e.target.value)}
//         />
//         <button onClick={handleChangePassword}>Change Password</button>
//       </div>
//     </div>
//   );
// };

// export default Profile;
