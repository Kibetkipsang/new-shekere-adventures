import React, { useEffect, useState } from "react";
import axios from "../api/axios";
import WelcomeBanner from "../components/user/WelcomeBanner";
import UpcomingTrips from "../components/user/UpcomingTrips";
import MyGroups from "../components/user/MyGroups";
import RecentMessages from "../components/user/RecentMessages";
import { useNavigate } from "react-router-dom";

export default function UserDashboard() {
  const [user, setUser] = useState(null);
  const [groups, setGroups] = useState([]);
  const [plans, setPlans] = useState([]);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);

        const { data: userData } = await axios.get("/auth/profile");
        setUser(userData);

        const { data: groupsData } = await axios.get("/groups/my-groups");
        setGroups(groupsData);

        const { data: messagesData } = await axios.get("/groups/recent-messages");
        setMessages(messagesData);

        const { data: plansData } = await axios.get("/plans/my-plans");
        setPlans(plansData);

      } catch (err) {
        console.error("Error loading dashboard data:", err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) return <div className="p-4 text-yellow-600">Loading your dashboard...</div>;
  if (error) return <div className="p-4 text-red-600">{error}</div>;

  return (
    <div className="flex font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-800 min-h-screen p-6 space-y-6 text-white">
        <h2 className="text-xl font-bold text-yellow-400">SHEKERE ADVENTURES</h2>
        <nav className="space-y-4 text-white">
          <div><button
              onClick={() => navigate("/create-adventure")}
              className="bg-yellow-400 text-black font-semibold px-4 py-2 rounded hover:bg-yellow-500 transition">
             + Create Adventure
               </button>
          </div>
          <div className="flex items-center gap-2 font-medium text-yellow-400">
            <span className="material-icons">person</span> Profile
          </div>
          <div className="flex items-center gap-2">
            <span className="material-icons">calendar_today</span> Trips
          </div>
          <div className="flex items-center gap-2">
            <span className="material-icons">groups</span> Groups
          </div>
          <div className="flex items-center gap-2">
            <span className="material-icons">settings</span> Settings
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-6 bg-gray-800">
        <WelcomeBanner name={user?.name} />

        {/* Stats Row */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-4 mb-6">
          <div className="bg-yellow-100 text-black rounded-lg p-4 text-center shadow">
            <p className="text-3xl font-bold">{plans.length}</p>
            <p className="text-sm">Trips Booked</p>
          </div>
          <div className="bg-yellow-100 text-black rounded-lg p-4 text-center shadow">
            <p className="text-3xl font-bold">{groups.length}</p>
            <p className="text-sm">Groups Joined</p>
          </div>
          <div className="bg-yellow-100 text-black rounded-lg p-4 text-center shadow">
            <p className="text-3xl font-bold">{messages.length}</p>
            <p className="text-sm">Messages</p>
          </div>
          <div className="bg-yellow-100 text-black rounded-lg p-4 text-center shadow">
            <p className="text-3xl font-bold">1</p>
            <p className="text-sm">Reviews Given</p>
          </div>
        </div>

        <section className="mb-6 ">
          <UpcomingTrips trips={plans} />
        </section>

        <section className="mb-6">
          <MyGroups groups={groups} />
        </section>

        <section>
          <RecentMessages messages={messages} />
        </section>
      </main>
    </div>
  );
}
