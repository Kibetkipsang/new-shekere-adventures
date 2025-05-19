import React from "react";
import { useState } from "react";
import axios from "../api/axios";
import { Navigate, useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

export default function SignUp(){
    const [firstName, setFirstName] = useState('');
    const [middleName, setMiddleName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const navigate = useNavigate();
    
    const handleSignup = async () => {
        if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
        }
        
        try{
            const res = await axios.post("/register", {
                firstName,
                middleName,
                lastName,
                email,
                role: "user", 
                password
            });
            localStorage.setItem("token", res.data.access_token);
            navigate("/users");
        } catch(error){
            alert("Signup Failed:" + (error.response?.data?.msg || error.message))
        }
    };
    console.log("SignUp loaded")

    return(
        <>
        <div className="flex items-center justify-center h-screen mt-10 mb-20">
            <div className="bg-slate-100 min-h-96 min-w-96 p-6 rounded-lg shadow-lg mt-10">
                <div>
                <h2 className="text-center text-xl font-semibold mb-2">Register</h2>
                <div className="mb-2">
                <label className="block mb-2 font-normal text-gray-700">First Name</label>
                <input
                className="w-full border border-gray-300 rounded h-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="First Name"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                />
                </div>
                <div>
                <label className="block mb-2 font-normal text-gray-700">Middle Name</label>
                <input
                className="w-full border border-gray-300 rounded h-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Middle Name (optional)"
                value={middleName}
                onChange={(e) => setMiddleName(e.target.value)}
                />
                </div>
                <div>
                <label className="block mb-2 font-normal text-gray-700">Last Name</label>
                <input
                className="w-full border border-gray-300 rounded h-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Last Name"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                />
                </div>
                <div>
                <label className="block mb-2 font-normal text-gray-700">Email</label>
                <input
                className="w-full border border-gray-300 rounded h-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type="email"
                placeholder="eg: yourmail@gmail.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                />  
                </div>
                <div className="relative mb-4">           
                <label className="block mb-2 font-normal text-gray-700">Password</label>
                <input
                className="w-full border border-gray-300 rounded h-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type={showPassword ? "text" : "password"}
                placeholder="eg: Pass123!"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                />
                <button
                type="button"
                onClick={() => setShowPassword(prev => !prev)}
                className="absolute top-8 right-3 text-gray-600 hover:text-gray-900 mt-2"
                tabIndex={-1}
                 >
                {showPassword ? "Hide" : "Show"}
                 </button>
                </div> 
                <div className="relative ">
                <label className="block mb-2 font-normal text-gray-700">Confirm Password</label>
                <input
                className="w-full border border-gray-300 rounded h-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type={showConfirmPassword ? "text" : "password"}
                placeholder="eg: Pass123!"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                />
                <button
                type="button"
                onClick={() => setShowConfirmPassword(prev => !prev)}
                className="absolute top-8 right-3 text-gray-600 hover:text-gray-900 mt-2"
                tabIndex={-1}
                >
                {showConfirmPassword ? "Hide" : "Show"}
                </button>
                </div>
                <div className="mt-4 px-16 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-center mb-2">
                <button onClick={handleSignup}>Sign Up</button>
                </div>
                <p className="text-sm font-normal text-gray-600">Already have an account? {" "} <Link to="/login" className="text-blue-600 hover:underline">Sign In</Link></p>
                </div>       
            </div>
        </div>
        </>
    )
    

}