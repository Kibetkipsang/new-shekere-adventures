import React, { useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";


export default function CreateAdventure(){

    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        title: "",
        description: "",
        location: "",
        date: "",
        time: "",
        max_participants: "",
        image_url: ""
    });
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError(null);
        setSuccess(false);
        try {
            const response = await axios.post("/community-trips", formData);
            const newTripId = response.data.id;
            navigate(`/community-trips/${newTripId}`);
        }
        catch(error){
            console.error(error);
            setError("Something went wrong while creating the adventure.");
        }
    };

    return(
        <>
        <div className="flex items-center justify-center h-screen">
        <div className="max-w-3xl mx-auto mt-24 mb-24 p-6 bg-white rounded-lg shadow">
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Create Adventure</h3>
            {error && <p className="text-red-600 mb-4">{error}</p>}
            {success && <p className="text-green-600 mb-4">Adventure created successfully!</p>}
            <form onSubmit={handleSubmit}>
                <input 
                type="text"
                name="title"
                placeholder="Adventure Title"
                value={formData.title}
                required
                onChange={handleChange}
                className="w-full mb-2 p-3 border rounded focus:outline-none focus:ring-2 focus:ring-yellow-400 "
                />
                <textarea 
                name="description"
                placeholder="Description"
                value={formData.description}
                onChange={handleChange}
                required
                rows="4"
                className="w-full mb-2 p-3 border rounded focus:outline-none focus:ring-2 focus:ring-yellow-400"
                ></textarea>
                <input 
                type="text"
                name="location"
                placeholder="Location"
                value={formData.location}
                onChange={handleChange}
                required
                className="w-full mb-2 p-3 border rounded focus:outline-none focus:ring-2 focus:ring-yellow-400"
                />
                <input 
                type="date"
                name="date"
                placeholder="Date"
                value={formData.date}
                onChange={handleChange}
                required
                className="w-full mb-2 p-3 border rounded focus:outline-none focus:ring-2 focus:ring-yellow-400"
                />
                <input 
                type="time"
                name="time"
                placeholder="Time"
                value={formData.time}
                onChange={handleChange}
                className="w-full mb-2 p-3 border rounded focus:outline-none focus:ring-2 focus:ring-yellow-400"
                />
                <input 
                type="number"
                name="max_participants"
                placeholder="Max Participants"
                value={formData.max_participants}
                onChange={handleChange}
                required
                className="w-full mb-2 p-3 border rounded focus:outline-none focus:ring-2 focus:ring-yellow-400"
                />
                <input 
                type="text"
                name="image_url"
                placeholder="Image Url (optional)"
                value={formData.image_url}
                onChange={handleChange}
                required
                className="w-full mb-2 p-3 border rounded focus:outline-none focus:ring-2 focus:ring-yellow-400"
                />
                <button 
                type="submit" 
                className="w-full bg-yellow-400 text-black font-semibold py-3 rounded hover:bg-yellow-500 transition"
                 >Create Adventure</button>
            </form>
        </div>
        </div>
        </>
    )
}