import SideBar from "../../components/SideBar";

const DashboardPage = () => {
  return (
    <SideBar
      content={
        <div className="space-y-6">
          <h2 className="text-2xl font-bold">Welcome Back!</h2>
        </div>
      }
    />
  );
};

export default DashboardPage;
