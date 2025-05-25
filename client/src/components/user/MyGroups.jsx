import React from "react";
import { useNavigate } from "react-router-dom";

export default function MyGroups({ groups }) {
  const navigate = useNavigate();

  if (!groups || groups.length === 0) {
    return <p className="text-gray-300">You haven’t joined or created any groups yet.</p>;
  }

  return (
    <div className="bg-gray-900 p-4 rounded shadow text-white">
      <h2 className="text-lg font-semibold text-yellow-400 mb-4">Groups You've Joined</h2>
      <ul className="space-y-4">
        {groups.map((group) => (
          <li key={group.id} className="border border-white rounded p-4 flex justify-between items-center">
            <div>
              <p className="font-bold text-lg text-yellow-300">{group.title}</p>
              <p className="text-gray-400 text-sm">
                {group.location} • {group.date} at {group.time}
              </p>
            </div>
            <button
              onClick={() => navigate(`/community-trips/${group.id}`)}
              className="bg-yellow-400 text-black px-4 py-2 rounded hover:bg-yellow-500 transition"
            >
              View
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
