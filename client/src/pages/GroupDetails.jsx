import React, { useEffect, useState } from "react";
import axios from "../api/axios";
import { useParams } from "react-router-dom";

export default function GroupDetails() {
  const { groupId } = useParams();

  const [group, setGroup] = useState(null);
  const [activeTab, setActiveTab] = useState("Members");
  const [members, setMembers] = useState([]);
  const [chatMessages, setChatMessages] = useState([]);
  const [plans, setPlans] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [newPlan, setNewPlan] = useState({ title: "", time: "", location: "" });
  const [polls, setPolls] = useState([]);
  const [voteData, setVoteData] = useState({});
  const [newPoll, setNewPoll] = useState({ question: "", options: ["", ""] });
  const [editingPollId, setEditingPollId] = useState(null);
  const [editPollData, setEditPollData] = useState({ question: "", options: ["", ""] });
  const [showCreatePoll, setShowCreatePoll] = useState(false);
  const [showCreatePlan, setShowCreatePlan] = useState(false);
  const [editingPlanId, setEditingPlanId] = useState(null);
  const [editPlan, setEditPlan] = useState({ title: "", time: "", location: "" });


  const currentUserId = parseInt(localStorage.getItem("user_id")) || null;
  const myMembership = members.find(m => m.id === currentUserId);
  const userRole = myMembership?.role?.toLowerCase();

  useEffect(() => {
    fetchGroupDetails();
    fetchPolls();
  }, []);

  const fetchGroupDetails = async () => {
    try {
      const res = await axios.get(`/community-trips/${groupId}`);
      setGroup(res.data);
      setMembers(res.data.members || []);
      setChatMessages(res.data.chat || []);
      setPlans(res.data.plans || []);
    } catch (err) {
      console.error("Error fetching community trip:", err);
    }
  };

  const fetchPolls = async () => {
    try {
      const res = await axios.get(`/community-trips/${groupId}/polls`);
      setPolls(res.data);
    } catch (err) {
      console.error("Error fetching polls", err);
    }
  };

  const handleSendMessage = async () => {
    try {
      const res = await axios.post(`/community-trips/${groupId}/chat`, { message: newMessage });
      setChatMessages([...chatMessages, res.data]);
      setNewMessage("");
    } catch (err) {
      console.error("Send message error:", err);
    }
  };

  const handleAddPlan = async () => {
    try {
      const res = await axios.post(`/community-trips/${groupId}/plans`, newPlan);
      setPlans([...plans, res.data]);
      setNewPlan({ title: "", time: "", location: "" });
    } catch (err) {
      console.error("Add plan error:", err);
    }
  };

  const handleRoleChange = async (userId, newRole) => {
    try {
      const res = await axios.patch(`/community-trips/${groupId}/participants/${userId}/role`, { role: newRole });
      const updated = members.map(m => m.id === userId ? { ...m, role: newRole } : m);
      setMembers(updated);
    } catch (err) {
      console.error("Role update failed:", err);
    }
  };

  const handleVote = async (pollId) => {
    const option_id = voteData[pollId];
    if (!option_id) return alert("Please select an option");

    try {
      await axios.post(`/polls/${pollId}/vote`, { option_id });
      fetchPolls();
    } catch (err) {
      console.error("Voting failed", err);
    }
  };

  const updatePollOption = (index, value) => {
    const updated = [...newPoll.options];
    updated[index] = value;
    setNewPoll({ ...newPoll, options: updated });
  };

  const addPollOption = () => {
    setNewPoll({ ...newPoll, options: [...newPoll.options, ""] });
  };
  
  const submitNewPoll = async () => {
    try {
      await axios.post(`/community-trips/${groupId}/polls`, newPoll);
      setNewPoll({ question: "", options: ["", ""] });
      fetchPolls();
    } catch (err) {
      console.error("Poll creation failed", err);
    }
  };

  const deletePoll = async (pollId) => {
    if (!window.confirm("Are you sure you want to delete this poll?")) return;
    try {
      await axios.delete(`/polls/${pollId}`);
      fetchPolls();
    } catch (err) {
      console.error("Poll deletion failed", err);
    }
  };
  // Begin editing a poll
const startEditingPoll = (poll) => {
  setEditingPollId(poll.id);
  setEditPollData({
    question: poll.question,
    options: poll.options.map(opt => opt.name),
  });
};

const addEditPollOption = () => {
  setEditPollData({ ...editPollData, options: [...editPollData.options, ""] });
};

const removeEditPollOption = (indexToRemove) => {
  const updated = editPollData.options.filter((_, idx) => idx !== indexToRemove);
  setEditPollData({ ...editPollData, options: updated });
};
// Update a specific option in the edit form
const handleEditPollOption = (index, value) => {
  const updatedOptions = [...editPollData.options];
  updatedOptions[index] = value;
  setEditPollData({ ...editPollData, options: updatedOptions });
};

// Submit the edited poll to the backend
const submitPollEdit = async () => {
  try {
    await axios.patch(`/polls/${editingPollId}`, editPollData);
    setEditingPollId(null);
    fetchPolls(); 
  } catch (err) {
    console.error("Poll edit failed:", err);
  }
};

// Cancel editing
const cancelEdit = () => {
  setEditingPollId(null);
};

const startEditPlan = (plan) => {
  setEditingPlanId(plan.id);
  setEditPlan({ title: plan.title, time: plan.time, location: plan.location });
};

const submitEditPlan = async (planId) => {
  try {
    await axios.patch(`/community-trips/${groupId}/plans/${planId}`, editPlan);
    setEditingPlanId(null);
    fetchGroupDetails(); // Refresh plan list
  } catch (err) {
    console.error("Update plan failed", err);
  }
};

const handleDeletePlan = async (planId) => {
  if (!window.confirm("Are you sure you want to delete this plan?")) return;
  try {
    await axios.delete(`/community-trips/${groupId}/plans/${planId}`);
    fetchGroupDetails(); // Refresh plan list
  } catch (err) {
    console.error("Delete plan failed", err);
  }
};


  

  if (!group) return <div className="text-center py-10 text-white">Loading trip...</div>;

  return (
    <div className="max-w-4xl mx-auto p-4 text-gray-100">
      <div className="bg-white shadow rounded p-6 text-gray-800">
        <h1 className="text-2xl font-semibold mb-1">{group.title}</h1>
        <p className="text-sm text-gray-600">{group.location} — {group.date} at {group.time}</p>
        <p className="text-sm text-gray-700 mt-1">Created by: {group.creator}</p>
      </div>

      <div className="flex gap-4 mt-6 border-b border-gray-600">
        {["Members", "Chat Room", "Plans", "Polling Station", "Settings"].map(tab => (
          <button
            key={tab}
            className={`pb-2 font-medium ${activeTab === tab ? "border-b-2 border-yellow-400 text-yellow-400" : "text-gray-400 hover:text-white"}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </div>

      {activeTab === "Members" && (
        <div className="mt-4">
          <ul>
            {members.map(m => (
              <li key={m.id} className="border-b border-gray-700 py-2 text-white flex justify-between items-center">
                <div>
                  {m.name} - <span className="italic text-gray-400">{m.role}</span>
                </div>
                {(userRole === "creator" || userRole === "admin") && parseInt(currentUserId) !== m.id && (
                  <select
                    value={m.role}
                    onChange={(e) => handleRoleChange(m.id, e.target.value)}
                    className="bg-gray-800 border border-gray-600 text-white px-2 py-1 rounded"
                  >
                    <option value="member">member</option>
                    <option value="admin">admin</option>
                    {userRole === "creator" && <option value="creator">creator</option>}
                  </select>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {activeTab === "Chat Room" && (
        <div className="mt-4">
          <div className="h-60 overflow-y-auto border border-gray-700 p-3 rounded bg-gray-900">
            {chatMessages.map((msg, idx) => (
              <div key={idx} className="mb-2">
                <span className="font-semibold text-yellow-400">{msg.user_name}</span>:
                <span className="ml-2 text-gray-200">{msg.message}</span>
              </div>
            ))}
          </div>
          <div className="flex mt-2 gap-2">
            <input
              value={newMessage}
              onChange={e => setNewMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 border border-gray-600 bg-gray-800 text-white rounded px-3 py-2"
            />
            <button onClick={handleSendMessage} className="bg-yellow-400 text-black font-semibold px-4 py-2 rounded">Send</button>
          </div>
        </div>
      )}

      {activeTab === "Plans" && (
  <div className="mt-4 text-white">
    {/* Toggle Button to show/hide plan creation form */}
    {(userRole === "creator" || userRole === "admin") && (
      <div className="flex justify-end gap-4 mb-4">
        <button
          onClick={() => setShowCreatePlan(!showCreatePlan)}
          className="bg-yellow-400 text-black px-4 py-2 rounded font-semibold"
        >
          {showCreatePlan ? "Hide Plan Form" : "Create New Plan"}
        </button>
      </div>
    )}

    {/* Display existing plans */}
    <ul className="mb-4">
      {plans.map((p, i) => (
        <li key={i} className="mb-2 border border-gray-700 p-2 rounded bg-gray-900 text-white">
          {editingPlanId === p.id ? (
            <div className="space-y-2">
              <input
                className="w-full border border-gray-600 bg-gray-800 text-white rounded px-3 py-2"
                placeholder="Plan title"
                value={editPlan.title}
                onChange={e => setEditPlan({ ...editPlan, title: e.target.value })}
              />
              <input
                className="w-full border border-gray-600 bg-gray-800 text-white rounded px-3 py-2"
                placeholder="Time"
                value={editPlan.time}
                onChange={e => setEditPlan({ ...editPlan, time: e.target.value })}
              />
              <input
                className="w-full border border-gray-600 bg-gray-800 text-white rounded px-3 py-2"
                placeholder="Location"
                value={editPlan.location}
                onChange={e => setEditPlan({ ...editPlan, location: e.target.value })}
              />
              <div className="flex gap-2">
                <button
                  onClick={() => submitEditPlan(p.id)}
                  className="bg-yellow-400 text-black px-4 py-2 rounded"
                >
                  Save
                </button>
                <button
                  onClick={() => setEditingPlanId(null)}
                  className="bg-gray-500 text-white px-4 py-2 rounded"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              <strong className="text-yellow-300">{p.title}</strong><br />
              {p.time} at {p.location}
              {(userRole === "creator" || userRole === "admin") && (
                <div className="mt-2 flex gap-2">
                  <button
                    onClick={() => startEditPlan(p)}
                    className="text-blue-400 hover:text-blue-600 underline"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeletePlan(p.id)}
                    className="text-red-400 hover:text-red-600 underline"
                  >
                    Delete
                  </button>
                </div>
              )}
            </>
          )}
        </li>
      ))}
    </ul>

    {/* Plan creation form shown when toggled */}
    {showCreatePlan && (userRole === "creator" || userRole === "admin") && (
      <div className="space-y-2">
        <input
          className="w-full border border-gray-600 bg-gray-800 text-white rounded px-3 py-2"
          placeholder="Plan title"
          value={newPlan.title}
          onChange={e => setNewPlan({ ...newPlan, title: e.target.value })}
        />
        <input
          className="w-full border border-gray-600 bg-gray-800 text-white rounded px-3 py-2"
          placeholder="Time"
          value={newPlan.time}
          onChange={e => setNewPlan({ ...newPlan, time: e.target.value })}
        />
        <input
          className="w-full border border-gray-600 bg-gray-800 text-white rounded px-3 py-2"
          placeholder="Location"
          value={newPlan.location}
          onChange={e => setNewPlan({ ...newPlan, location: e.target.value })}
        />
        <button
          onClick={handleAddPlan}
          className="bg-yellow-400 text-black font-semibold px-4 py-2 rounded"
        >
          Add Plan
        </button>
      </div>
    )}
  </div>
)}


   {/* polling station tab */}
     {activeTab === "Polling Station" && (
  <div className="mt-4 space-y-6 text-white">
    <div className="flex justify-end gap-4 mb-4">
      {(userRole === "creator" || userRole === "admin") && (
        <button
          onClick={() => setShowCreatePoll(!showCreatePoll)}
          className="bg-yellow-400 text-black px-4 py-2 rounded font-semibold"
        >
          {showCreatePoll ? "Hide Poll Form" : "Create New Poll"}
        </button>
      )}
    </div>

    {showCreatePoll && (userRole === "creator" || userRole === "admin") && (
      <div className="border border-gray-600 p-4 rounded bg-gray-800">
        <h4 className="text-lg font-semibold text-yellow-400 mb-2">Create a New Poll</h4>
        <input
          className="w-full mb-2 px-3 py-2 bg-gray-800 border border-gray-600 rounded"
          placeholder="Category/Question"
          value={newPoll.question}
          onChange={e => setNewPoll({ ...newPoll, question: e.target.value })}
        />
        {newPoll.options.map((opt, idx) => (
          <div key={idx} className="flex items-center gap-2 mb-2">
            <input
              className="flex-1 px-3 py-2 bg-gray-800 border border-gray-600 rounded"
              placeholder={`Option ${idx + 1}`}
              value={opt}
              onChange={e => updatePollOption(idx, e.target.value)}
            />
            {newPoll.options.length > 2 && (
              <button
                onClick={() => {
                  const updated = newPoll.options.filter((_, i) => i !== idx);
                  setNewPoll({ ...newPoll, options: updated });
                }}
                className="text-red-400 hover:text-red-600 text-sm"
              >
                ✕
              </button>
            )}
          </div>
        ))}
        <button
          onClick={addPollOption}
          className="bg-gray-700 text-white px-3 py-1 rounded mr-2"
        >
          Add Option
        </button>
        <button
          onClick={submitNewPoll}
          className="bg-yellow-400 text-black px-4 py-2 rounded"
        >
          Create Poll
        </button>
      </div>
    )}

    {polls.map(poll => {
      const totalVotes = poll.options.reduce((sum, o) => sum + o.votes, 0);
      return (
        <div key={poll.id} className="border border-gray-600 p-4 rounded bg-gray-900">
          {editingPollId === poll.id ? (
            <div>
              <input
                className="w-full mb-2 px-3 py-2 bg-gray-800 border border-gray-600 rounded"
                value={editPollData.question}
                onChange={(e) => setEditPollData({ ...editPollData, question: e.target.value })}
              />
              {editPollData.options.map((opt, idx) => (
                <div key={idx} className="flex items-center gap-2 mb-2">
                  <input
                    className="flex-1 px-3 py-2 bg-gray-800 border border-gray-600 rounded"
                    value={opt.name || opt}
                    placeholder={`Option ${idx + 1}`}
                    onChange={(e) => handleEditPollOption(idx, e.target.value)}
                  />
                  {editPollData.options.length > 2 && (
                    <button
                      onClick={() => removeEditPollOption(idx)}
                      className="text-red-400 hover:text-red-600 text-sm"
                    >
                      ✕
                    </button>
                  )}
                </div>
              ))}
              <button
                onClick={addEditPollOption}
                className="bg-gray-700 text-white px-3 py-1 rounded mb-3"
              >
                + Add Option
              </button>
              <div className="flex gap-2">
                <button onClick={submitPollEdit} className="bg-yellow-400 text-black px-4 py-2 rounded">Save</button>
                <button onClick={cancelEdit} className="bg-gray-500 text-white px-4 py-2 rounded">Cancel</button>
              </div>
            </div>
          ) : (
            <>
              <h3 className="text-lg font-bold text-yellow-300">{poll.question}</h3>
              {poll.has_voted ? (
                <div className="mt-2 space-y-3">
                  {poll.options.map(opt => {
                    const percentage = totalVotes > 0 ? (opt.votes / totalVotes) * 100 : 0;
                    return (
                      <div key={opt.id}>
                        <div className="flex justify-between mb-1">
                          <span>{opt.name}</span>
                          <span>{opt.votes} votes ({percentage.toFixed(1)}%)</span>
                        </div>
                        <div className="w-full bg-gray-700 rounded h-3">
                          <div className="h-3 bg-yellow-400 rounded" style={{ width: `${percentage}%` }}></div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div className="mt-2">
                  {poll.options.map(opt => (
                    <label key={opt.id} className="block">
                      <input
                        type="radio"
                        name={`poll-${poll.id}`}
                        value={opt.id}
                        onChange={() => setVoteData({ ...voteData, [poll.id]: opt.id })}
                      />
                      <span className="ml-2">{opt.name}</span>
                    </label>
                  ))}
                  <button
                    onClick={() => handleVote(poll.id)}
                    className="mt-2 bg-yellow-400 text-black px-4 py-1 rounded"
                  >
                    Vote
                  </button>
                </div>
              )}
              {userRole === "creator" && (
                <div className="flex gap-4 mt-3">
                  <button onClick={() => startEditingPoll(poll)} className="text-blue-300 hover:text-blue-500 underline">Edit Poll</button>
                  <button onClick={() => deletePoll(poll.id)} className="text-red-400 hover:text-red-600 underline">Delete Poll</button>
                </div>
              )}
            </>
          )}
        </div>
      );
    })}
  </div>
)}

      {activeTab === "Settings" && (
        <div className="mt-4 text-gray-400 italic">
          Settings panel (edit trip, manage participants, delete trip, etc.) — To be implemented
        </div>
      )}
    </div>
  );
}
