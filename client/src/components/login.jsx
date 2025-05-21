import React, { useState, useContext } from "react";
import axios from "../api/axios";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const { login } = useContext(AuthContext); 

    const handleLogin = async () => {
        if (!email || !password) {
            alert("Please fill in both email and password.");
            return;
        }
        setLoading(true);

        try {
            const res = await axios.post('/auth/login', { email, password }, {
                headers: { 'Content-Type': 'application/json' }
            });

            localStorage.setItem('token', res.data.token);
            localStorage.setItem('user', JSON.stringify(res.data.user));
            login(); 
            navigate("/UserDashboard");
        } catch (error) {
            const errorMessage = error.response?.data?.error || error.message;
            alert("Login failed: " + errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center h-screen">
            <div className="bg-slate-100 h-96 w-96 p-6 rounded-lg shadow-lg">
                <h2 className="text-center text-xl font-semibold mb-2">Login</h2>
                <div className="mb-4">
                    <label className="block mb-2 font-medium text-gray-700">Email</label>
                    <input
                        className="w-full border border-gray-300 rounded h-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div>
                    <label className="block mb-2 font-medium text-gray-700">Password</label>
                    <input
                        className="w-full mb-10 border border-gray-300 rounded h-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Password"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <div onClick={handleLogin} disabled={loading}
                className="mt-4 px-16 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-center mb-2">
                    <button>{loading? "Logging In!" : "Log In"}</button>
                </div>
                <p className="text-sm font-normal text-gray-600">
                    Don't have an account?{" "}
                    <Link to="/signUp" className="text-blue-600 hover:underline">Sign Up</Link>
                </p>
            </div>
        </div>
    );
}
