import React, { useState } from "react";
import axios from "axios";

interface StaffForm {
  first_name: string;
  middle_name: string;
  last_name: string;
  email: string;
  sex: "Female" | "Male";
  group:
    | "Doctor"
    | "Clinician"
    | "Registrar"
    | "Outreach Coordinator"
    | "Outreach Worker"
    | "Public Health Analyst"
    | "Inventory Manager"
    | "Finance Officer"
    | "Cashier"
    | "Hr"
    | "Receptionist"
    | "Nurse";
  department: string;
  address: string;
  nin: number;
  emergency_contact: string;
}

const CreateStaff: React.FC = () => {
  const [form, setForm] = useState<StaffForm>({
    first_name: "",
    middle_name: "",
    last_name: "",
    email: "",
    sex: "Female",
    group: "Hr",
    department: "",
    address: "1, dotun street",
    nin: 12345678911,
    emergency_contact: "12345678",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();

    const token = localStorage.getItem("accessToken");
    if (!token) {
      alert("You must be logged in as a superuser.");
      return;
    }

    try {
      const response = await axios.post(
        "https://purple-plus-auth-demo.onrender.com/api/v1/accounts/staff/create/",
        form,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("Staff created:", response.data);
      alert("Staff user created successfully!");
    } catch (error: unknown) {
      console.error("Create staff error:", error);
      if (axios.isAxiosError(error)) {
        console.error(error.response?.data);
        alert(error.response?.data?.message || "Failed to create staff");
      } else {
        alert("Failed to create staff");
      }
    }
  };

  return (
    <form onSubmit={handleCreate} className="p-6 max-w-md space-y-3">
      <input
        name="first_name"
        placeholder="First name"
        value={form.first_name}
        onChange={handleChange}
        className="border p-2 w-full rounded"
      />
      <input
        name="middle_name"
        placeholder="Middle name"
        value={form.middle_name}
        onChange={handleChange}
        className="border p-2 w-full rounded"
      />
      <input
        name="last_name"
        placeholder="Last name"
        value={form.last_name}
        onChange={handleChange}
        className="border p-2 w-full rounded"
      />
      <input
        name="email"
        placeholder="Email"
        type="email"
        value={form.email}
        onChange={handleChange}
        className="border p-2 w-full rounded"
      />
  

      <select
        name="sex"
        value={form.sex}
        onChange={handleChange}
        className="border p-2 w-full rounded"
      >
        <option value="Female">Female</option>
        <option value="Male">Male</option>
      </select>

      <select
        name="group"
        value={form.group}
        onChange={handleChange}
        className="border p-2 w-full rounded"
      >
        <option value="Doctor">Doctor</option>
        <option value="Clinician">Clinician</option>
        <option value="Registrar">Registrar</option>
        <option value="Outreach Coordinator">Outreach Coordinator</option>
        <option value="Outreach Worker">Outreach Worker</option>
        <option value="Public Health Analyst">Public Health Analyst</option>
        <option value="Inventory Manager">Inventory Manager</option>
        <option value="Finance Officer">Finance Officer</option>
        <option value="Cashier">Cashier</option>
        <option value="Hr">Hr</option>
        <option value="Receptionist">Receptionist</option>
        <option value="Nurse">Nurse</option>
      </select>

      <input
        name="department"
        placeholder="Department"
        value={form.department}
        onChange={handleChange}
        className="border p-2 w-full rounded"
      />
      <input
        name="Address"
        placeholder="Address"
        value={form.address}
        onChange={handleChange}
        className="border p-2 w-full rounded"
      />
      <input
        name="nin"
        placeholder="NIN"
        type="number"
        value={form.nin}
        onChange={(e) =>
          setForm((prev) => ({ ...prev, nin: Number(e.target.value) }))
        }
        className="border p-2 w-full rounded"
      />

      <input
        name="Emergency contact"
        placeholder="Emergency Contact"
        value={form.emergency_contact}
        onChange={handleChange}
        className="border p-2 w-full rounded"
      />

      <button
        type="submit"
        className="bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700"
      >
        Create Staff
      </button>
    </form>
  );
};

export default CreateStaff;
