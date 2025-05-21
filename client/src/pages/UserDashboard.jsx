import React, { useEffect, useState } from "react";
import axios from "../api/axios";

export default function UserDashboard() {
  const [user, setUser] = useState(null);
  const [communities, setCommunities] = useState([]);
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch user profile
        const { data: userData } = await axios.get("/auth/profile");
        setUser(userData);

        // Fetch communities (adjust endpoint as per your backend)
        // const { data: communitiesData } = await axios.get("/communities");
        // setCommunities(communitiesData);

        // // Fetch user plans (adjust endpoint accordingly)
        // const { data: plansData } = await axios.get("/plans/my-plans");
        // setPlans(plansData);
      } catch (err) {
        console.error("Error loading dashboard data:", err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) return <div className="p-4">Loading your dashboard...</div>;
  if (error) return <div className="p-4 text-red-600">{error}</div>;

  return (
    <div className="p-6 max-w-4xl mx-auto bg-yellow-50 rounded shadow mt-6 mb-6">
      <h2 className="text-2xl font-bold mb-4">
        Welcome, {user ? user.name : "Traveller"}
      </h2>

      {/* Profile Section */}
      <section className="mb-6 p-4 bg-white rounded shadow-sm">
        <h3 className="text-lg font-semibold mb-2">Your Profile</h3>
        <p><strong>Email:</strong> {user?.email || "N/A"}</p>
        <p><strong>Role:</strong> {user?.role || "N/A"}</p>
      </section>

      {/* Communities Section */}
      <section className="mb-6 p-4 bg-white rounded shadow-sm">
        <h3 className="text-lg font-semibold mb-2">Communities</h3>
        {communities.length === 0 ? (
          <p>No communities found.</p>
        ) : (
          <ul className="list-disc list-inside">
            {communities.map((comm) => (
              <li key={comm.id} className="mb-1">
                {comm.name}{" "}
                <button
                  className="ml-2 px-2 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700"
                  onClick={() => alert(`Join community: ${comm.name}`)}
                  type="button"
                >
                  Join
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      {/* Plans Section */}
      <section className="mb-6 p-4 bg-white rounded shadow-sm">
        <h3 className="text-lg font-semibold mb-2">Your Plans</h3>
        {plans.length === 0 ? (
          <p>You haven't created or joined any plans yet.</p>
        ) : (
          <ul className="list-disc list-inside">
            {plans.map((plan) => (
              <li key={plan.id}>
                {plan.title} {plan.date && <> - {new Date(plan.date).toLocaleDateString()}</>}
              </li>
            ))}
          </ul>
        )}
      </section>

      {/* Logout Button */}
      <button
        type="button"
        onClick={() => {
          localStorage.removeItem("token");
          window.location.reload();
        }}
        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        Logout
      </button>
    </div>
  );
}
