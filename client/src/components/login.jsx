import React, { useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

export default function Login(){

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async () => {
        if (!email || !password) {
        alert("Please fill in both email and password.");
        return;

        }
        try{
            const res = await axios.post('/login', {email, password});
            localStorage.setItem('token', res.data.access_token);
            navigate("/users");
        }catch (error){
            alert("Login failed: " + error.response?.data?.msg || error.message);
        }
    }

    return(
        <>
        <div className="flex items-center justify-center h-screen">
        <div className="bg-slate-100 h-96 w-96 p-6 rounded-lg shadow-lg ">
            <div>
            <h2 className="text-center text-xl font-semibold mb-2">Login</h2>
            <div className="mb-4">
            <label className="block mb-2 font-medium text-gray-700">Email</label>
            <input className="w-full border border-gray-300 rounded h-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            />
            </div>
            </div>
            <br/>
            <div>
            <label className="block mb-2 font-medium text-gray-700">Password</label>
            <input className="w-full mb-10 border border-gray-300 rounded h-10 focus:outline-none focus:ring-2 focus:ring-blue-500" 
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            />
            </div>
            <div className="mt-4 px-16 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-center mb-2">
            <button  onClick={handleLogin}>Sign In</button>
            </div >
            <p className="text-sm font-normal text-gray-600">Don't have an account?  {" "}  <Link to="/signUp" className="text-blue-600 hover:underline">Sign Up</Link></p>
        </div>
        </div>
        </>
    )
}