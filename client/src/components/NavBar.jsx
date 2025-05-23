import { Link, useNavigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

export default function NavBar() {
  const navigate = useNavigate();
  const { isLoggedIn, logout } = useContext(AuthContext);

  const handleLogout = () => {
    localStorage.removeItem("token")
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-black shadow-md p-4 h-20">
      <div className="container mx-auto flex items-center justify-between">
        <h3 className="text-xl font-medium text-white">Shekere Adventures</h3>

        <div className="flex space-x-4 ml-auto">
          {!isLoggedIn && (
            <div className="text-white space-x-2">
              <Link to="/login" className="hover:underline">Login</Link>
              <Link to="/signUp" className="hover:underline">Sign Up</Link>
            </div>
          )}

          {isLoggedIn && (
            <button 
              onClick={handleLogout} 
              className="text-red-600 hover:underline"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}
