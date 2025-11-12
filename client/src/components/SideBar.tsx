import React, { useState, type JSX } from "react";
import { Link } from "react-router-dom";
import { Menu } from "lucide-react";

interface MenuItem {
  icon: JSX.Element;
  label: string;
  to: string;
}
// interface
interface SidebarProps {
  pageTitle?: string;
  content: React.ReactNode; // the dynamic dashboard content
}

const SideBar: React.FC<SidebarProps> = ({ content }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const menuIconsStyle = `  text-purple-powder group-hover:text-purple-3 transition-colors shrink-0 self-center my-auto ${
    isSidebarOpen ? "w-[0.805rem] h-[0.805rem]" : "w-[1rem] h-[1rem]"
  }`;
  const menuItems: MenuItem[] = [
    {
      icon: (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 13 13"
          className={menuIconsStyle}
          fill="currentColor"
        >
          <path d="M9.10667 1.88667L10.9933 3.77333L9.10667 5.66L7.22 3.77333L9.10667 1.88667ZM4 2.20667V4.87333H1.33333V2.20667H4ZM10.6667 8.87333V11.54H8V8.87333H10.6667ZM4 8.87333V11.54H1.33333V8.87333H4ZM9.10667 0L5.33333 3.76667L9.10667 7.54L12.88 3.76667L9.10667 0ZM5.33333 0.873333H0V6.20667H5.33333V0.873333ZM12 7.54H6.66667V12.8733H12V7.54ZM5.33333 7.54H0V12.8733H5.33333V7.54Z" />
        </svg>
      ),
      label: "Dashboard",
      to: "/dashboard",
    },
    {
      icon: (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          className={menuIconsStyle}
          fill="currentColor"
        >
          <path d="M13.3334 2.00033H12.6667V0.666992H11.3334V2.00033H4.66671V0.666992H3.33337V2.00033H2.66671C1.93337 2.00033 1.33337 2.60033 1.33337 3.33366V14.0003C1.33337 14.7337 1.93337 15.3337 2.66671 15.3337H13.3334C14.0667 15.3337 14.6667 14.7337 14.6667 14.0003V3.33366C14.6667 2.60033 14.0667 2.00033 13.3334 2.00033ZM13.3334 14.0003H2.66671V6.66699H13.3334V14.0003ZM13.3334 5.33366H2.66671V3.33366H13.3334V5.33366Z" />
        </svg>
      ),
      label: "Calendar",
      to: "/calendar",
    },
    {
      icon: (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          className={menuIconsStyle}
          fill="currentColor"
        >
          <path d="M4.36 3.33333C4.4 3.92667 4.5 4.50667 4.66 5.06L3.86 5.86C3.58667 5.06 3.41333 4.21333 3.35333 3.33333H4.36ZM10.9333 11.3467C11.5 11.5067 12.08 11.6067 12.6667 11.6467V12.64C11.7867 12.58 10.94 12.4067 10.1333 12.14L10.9333 11.3467ZM5 2H2.66667C2.3 2 2 2.3 2 2.66667C2 8.92667 7.07333 14 13.3333 14C13.7 14 14 13.7 14 13.3333V11.0067C14 10.64 13.7 10.34 13.3333 10.34C12.5067 10.34 11.7 10.2067 10.9533 9.96C10.8867 9.93333 10.8133 9.92667 10.7467 9.92667C10.5733 9.92667 10.4067 9.99333 10.2733 10.12L8.80667 11.5867C6.92 10.62 5.37333 9.08 4.41333 7.19333L5.88 5.72667C6.06667 5.54 6.12 5.28 6.04667 5.04667C5.8 4.3 5.66667 3.5 5.66667 2.66667C5.66667 2.3 5.36667 2 5 2Z" />
        </svg>
      ),
      label: "Tele-medicine",
      to: "/tele-medicine",
    },
    {
      icon: (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 15 10"
          className={menuIconsStyle}
          fill="currentColor"
        >
          <path d="M10.6667 0H1.33333C0.6 0 0 0.593333 0 1.33333V7.33333H1.33333C1.33333 8.44 2.22667 9.33333 3.33333 9.33333C4.44 9.33333 5.33333 8.44 5.33333 7.33333H9.33333C9.33333 8.44 10.2267 9.33333 11.3333 9.33333C12.44 9.33333 13.3333 8.44 13.3333 7.33333H14.6667V4L10.6667 0ZM9.33333 1.33333H10L12 3.33333H9.33333V1.33333ZM5.33333 1.33333H8V3.33333H5.33333V1.33333ZM1.33333 1.33333H4V3.33333H1.33333V1.33333ZM3.33333 8.16667C2.87333 8.16667 2.5 7.79333 2.5 7.33333C2.5 6.87333 2.87333 6.5 3.33333 6.5C3.79333 6.5 4.16667 6.87333 4.16667 7.33333C4.16667 7.79333 3.79333 8.16667 3.33333 8.16667ZM11.3333 8.16667C10.8733 8.16667 10.5 7.79333 10.5 7.33333C10.5 6.87333 10.8733 6.5 11.3333 6.5C11.7933 6.5 12.1667 6.87333 12.1667 7.33333C12.1667 7.79333 11.7933 8.16667 11.3333 8.16667ZM13.3333 6H12.8133C12.4467 5.59333 11.92 5.33333 11.3333 5.33333C10.7467 5.33333 10.22 5.59333 9.85333 6H4.81333C4.44667 5.59333 3.92667 5.33333 3.33333 5.33333C2.74 5.33333 2.22 5.59333 1.85333 6H1.33333V4.66667H13.3333V6Z" />
        </svg>
      ),
      label: "Ambulance",
      to: "/ambulance",
    },
    {
      icon: (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          className={menuIconsStyle}
          fill="currentColor"
        >
          <path d="M8.33333 2.33333C11.2733 2.33333 13.6667 4.72667 13.6667 7.66667C13.6667 10.6067 11.2733 13 8.33333 13C7.54667 13 6.77333 12.8267 6.04667 12.48C5.86667 12.3933 5.67333 12.3533 5.47333 12.3533C5.34667 12.3533 5.22 12.3733 5.1 12.4067L2.96667 13.0333L3.59333 10.9C3.68667 10.5867 3.66 10.2467 3.52 9.95333C3.17333 9.22667 3 8.45333 3 7.66667C3 4.72667 5.39333 2.33333 8.33333 2.33333ZM8.33333 1C4.65333 1 1.66667 3.98667 1.66667 7.66667C1.66667 8.69333 1.90667 9.65333 2.31333 10.5267L1 15L5.47333 13.6867C6.34667 14.0933 7.30667 14.3333 8.33333 14.3333C12.0133 14.3333 15 11.3467 15 7.66667C15 3.98667 12.0133 1 8.33333 1Z" />
          <path
            fill-rule="evenodd"
            clip-rule="evenodd"
            d="M9 5H7.66667V7H5.66667V8.33333H7.66667V10.3333H9V8.33333H11V7H9V5Z"
          />
        </svg>
      ),
      label: "PlusGPT",
      to: "/PlusGPT",
    },
    {
      icon: (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          className={menuIconsStyle}
          fill="currentColor"
        >
          <path d="M2.66671 2.66634H13.3334V10.6663H3.44671L2.66671 11.4463V2.66634ZM2.66671 1.33301C1.93337 1.33301 1.34004 1.93301 1.34004 2.66634L1.33337 14.6663L4.00004 11.9997H13.3334C14.0667 11.9997 14.6667 11.3997 14.6667 10.6663V2.66634C14.6667 1.93301 14.0667 1.33301 13.3334 1.33301H2.66671ZM4.00004 7.99967H12V9.33301H4.00004V7.99967ZM4.00004 5.99967H12V7.33301H4.00004V5.99967ZM4.00004 3.99967H12V5.33301H4.00004V3.99967Z" />
        </svg>
      ),
      label: "Chats",
      to: "/chats",
    },
  ];

  const bottomMenuItems: MenuItem[] = [
    {
      icon: (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          className={menuIconsStyle}
          fill="currentColor"
        >
          <path d="M12.6667 1.13965H3.33333C2.59333 1.13965 2 1.73965 2 2.47298V11.8063C2 12.5396 2.6 13.1396 3.33333 13.1396H6L7.52667 14.6663C7.78667 14.9263 8.20667 14.9263 8.46667 14.6663L10 13.1396H12.6667C13.4 13.1396 14 12.5396 14 11.8063V2.47298C14 1.73965 13.4 1.13965 12.6667 1.13965ZM8 3.33965C8.99333 3.33965 9.8 4.14632 9.8 5.13965C9.8 6.13298 8.99333 6.93965 8 6.93965C7.00667 6.93965 6.2 6.13298 6.2 5.13965C6.2 4.14632 7.00667 3.33965 8 3.33965ZM12 10.473H4V9.87298C4 8.53965 6.66667 7.80632 8 7.80632C9.33333 7.80632 12 8.53965 12 9.87298V10.473Z" />
        </svg>
      ),
      label: "Profile",
      to: "/Profile",
    },
    {
      icon: (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          className={menuIconsStyle}
          fill="currentColor"
        >
          <path d="M12.6667 1H3.33333C2.59333 1 2 1.6 2 2.33333V11.6667C2 12.4 2.59333 13 3.33333 13H6L8 15L10 13H12.6667C13.4 13 14 12.4 14 11.6667V2.33333C14 1.6 13.4 1 12.6667 1ZM12.6667 11.6667H9.44667L8 13.1133L6.55333 11.6667H3.33333V2.33333H12.6667V11.6667ZM8 7C9.1 7 10 6.1 10 5C10 3.9 9.1 3 8 3C6.9 3 6 3.9 6 5C6 6.1 6.9 7 8 7ZM8 4.33333C8.36667 4.33333 8.66667 4.63333 8.66667 5C8.66667 5.36667 8.36667 5.66667 8 5.66667C7.63333 5.66667 7.33333 5.36667 7.33333 5C7.33333 4.63333 7.63333 4.33333 8 4.33333ZM12 10.0533C12 8.38667 9.35333 7.66667 8 7.66667C6.64667 7.66667 4 8.38667 4 10.0533V11H12V10.0533ZM5.65333 9.66667C6.14667 9.32667 7.14 9 8 9C8.86 9 9.85333 9.32667 10.3467 9.66667H5.65333Z" />
        </svg>
      ),
      label: "Notifications",
      to: "/notifications",
    },
    {
      icon: (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          className={menuIconsStyle}
          fill="currentColor"
        >
          <path d="M12.6667 1H3.33333C2.59333 1 2 1.6 2 2.33333V11.6667C2 12.4 2.59333 13 3.33333 13H6L8 15L10 13H12.6667C13.4 13 14 12.4 14 11.6667V2.33333C14 1.6 13.4 1 12.6667 1ZM12.6667 11.6667H9.44667L8 13.1133L6.55333 11.6667H3.33333V2.33333H12.6667V11.6667ZM8 7C9.1 7 10 6.1 10 5C10 3.9 9.1 3 8 3C6.9 3 6 3.9 6 5C6 6.1 6.9 7 8 7ZM8 4.33333C8.36667 4.33333 8.66667 4.63333 8.66667 5C8.66667 5.36667 8.36667 5.66667 8 5.66667C7.63333 5.66667 7.33333 5.36667 7.33333 5C7.33333 4.63333 7.63333 4.33333 8 4.33333ZM12 10.0533C12 8.38667 9.35333 7.66667 8 7.66667C6.64667 7.66667 4 8.38667 4 10.0533V11H12V10.0533ZM5.65333 9.66667C6.14667 9.32667 7.14 9 8 9C8.86 9 9.85333 9.32667 10.3467 9.66667H5.65333Z" />
        </svg>
      ),
      label: "Log Out",
      to: "/log-out",
    },
  ];

  return (
    <div className="flex h-screen bg-gray-100 ">
      {/* padding: 3rem 1rem 2.5rem 1rem; */}
      {/* Sidebar */}
      <aside
        className={`${
          isSidebarOpen ? "w-67" : "w-17"
        } bg-purple-dark text-white transition-all duration-300 ease-in-out shrink-0 flex flex-col `}
      >
        <div className="flex flex-col justify-start ">
          {/* Sidebar header */}
          <div className="flex flex-col justify-start h-full px-4 md:px-6 pt-10">
            {/* Top row: Title + Toggle */}
            <div className="flex items-center justify-between">
              {/* Main title */}
              {isSidebarOpen && (
                <h2 className="font-bold text-md">Purple Plus</h2>
              )}

              {/* Toggle button */}
              <button
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                className=" hover:bg-gray-800 rounded-md transition-colors"
              >
                <Menu size={24} />
              </button>
            </div>

            {/* Subtitle / Add Patient */}
            {isSidebarOpen && (
              <div className="flex items-center gap-2 my-4">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="18"
                  height="18"
                  viewBox="0 0 18 18"
                  fill="none"
                >
                  <path
                    d="M9 1.5C4.86 1.5 1.5 4.86 1.5 9C1.5 13.14 4.86 16.5 9 16.5C13.14 16.5 16.5 13.14 16.5 9C16.5 4.86 13.14 1.5 9 1.5ZM12 9.75H9.75V12C9.75 12.4125 9.4125 12.75 9 12.75C8.5875 12.75 8.25 12.4125 8.25 12V9.75H6C5.5875 9.75 5.25 9.4125 5.25 9C5.25 8.5875 5.5875 8.25 6 8.25H8.25V6C8.25 5.5875 8.5875 5.25 9 5.25C9.4125 5.25 9.75 5.5875 9.75 6V8.25H12C12.4125 8.25 12.75 8.5875 12.75 9C12.75 9.4125 12.4125 9.75 12 9.75Z"
                    fill="#D9BDFA"
                  />
                </svg>
                <span className=" text-xs text-purple-powder">
                  Register Patient
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Sidebar menu */}
        <div className="flex flex-col h-full justify-between">
          {/* Top menu */}
          <nav className="p-4">
            <ul className="space-y-2">
              {menuItems.map(({ icon, label, to }) => (
                <li key={label}>
                  <Link
                    to={to}
                    className="group flex items-center h-8 gap-2 p-3 rounded-[0.625rem] text-purple-powder  transition-colors hover:bg-purple-7 hover:text-purple-3"
                  >
                    <div className="w-6 flex justify-center">{icon}</div>
                    {isSidebarOpen && (
                      <span className="group-hover:text-purple-3 text-sm">{label}</span>
                    )}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          {/* Bottom menu */}
          <nav className="p-4">
            <ul className="space-y-2">
              {bottomMenuItems.map(({ icon, label, to }) => (
                <li key={label}>
                  <Link
                    to={to}
                    className="group flex items-center h-8 gap-1 p-3 rounded-[0.625rem] text-purple-powder  transition-colors hover:bg-purple-7 hover:text-purple-3"
                  >
                    <div className="w-6 flex justify-center">{icon}</div>
                    {isSidebarOpen && (
                      <span className="group-hover:text-purple-3 text-sm">{label}</span>
                    )}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </aside>
      {/* Dynamic content */}
      <main className="flex-1 overflow-auto p-6">{content}</main>
    </div>
  );
};

export default SideBar;
