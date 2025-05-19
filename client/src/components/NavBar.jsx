import { Link } from "react-router-dom";

export default function NavBar(){
    return(
        <nav className="bg-white  shadow-md p-4 h-20">
            <div className="container mx-auto flex items-center justify-between">
            <h3 className="text-xl font-medium text-gray-800">Shekere Adventures</h3>
            <div className="flex space-x-4 ml-auto">
                <Link to="/login" className="hover:underline">Login</Link>
                <Link to="/signUp" className="hover:underline">Sign Up</Link>       
            </div>
            </div>
        </nav>
    )
}