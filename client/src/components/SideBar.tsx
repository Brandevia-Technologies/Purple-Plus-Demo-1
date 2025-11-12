import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, Home, Settings, FileText } from "lucide-react";
import { MdPassword, MdOutlineMail } from "react-icons/md";

interface MenuItem {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  to: string;
}

interface SidebarProps {
  pageTitle?: string;
  content: React.ReactNode; // the dynamic dashboard content
}

const SideBar: React.FC<SidebarProps> = ({
  pageTitle = "Dashboard",
  content,
}) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const menuItems: MenuItem[] = [
    { icon: Home, label: "Home", to: "/home" },
    { icon: MdPassword, label: "Change Password", to: "/new-password" },
    { icon: MdOutlineMail, label: "Messages", to: "/messages" },
    { icon: Settings, label: "Settings", to: "/settings" },
    { icon: FileText, label: "Documents", to: "/documents" },
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside
        className={`${
          isSidebarOpen ? "w-64" : "w-17"
        } bg-gray-900 text-white transition-all duration-300 ease-in-out shrink-0 flex flex-col`}
      >
        {/* Toggle button */}
        <div
          className={`flex ${isSidebarOpen ? "justify-end pr-10" : "justify-center"}`}
        >
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-1 hover:bg-gray-800 rounded-md transition-colors"
          >
            <Menu size={24} />
          </button>
        </div>

        {/* Sidebar menu */}
        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {menuItems.map(({ icon: Icon, label, to }) => (
              <li key={label}>
                <Link
                  to={to}
                  className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-800 transition-colors"
                >
                  <Icon className="text-xl flex-shrink-0" />{" "}
                  {/* prevents shrinking */}
                  {isSidebarOpen && <span>{label}</span>}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </aside>

      {/* Dynamic content */}
      <main className="flex-1 overflow-auto p-6">{content}</main>
    </div>
  );
};

export default SideBar;
