import { BrowserRouter as Router, Routes,Route } from 'react-router-dom'
import './App.css'
import Login from './components/login'
import SignUp from './components/signUp';
import { Navigate } from "react-router-dom";
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import ProtectedRoute from './components/ProtectedRoutes';
import UserDashboard from './pages/UserDashboard';
import CreateAdventure from './pages/CreateAdventure';

function App() {
  return (
    <div className="min-h-screen bg-gray-800 flex flex-col">
      <NavBar />
      <main className='flex-1'> 
      <Routes>
        <Route path="/" element={<Navigate to="/signUp" />} />
        <Route path='/login' element={<Login/>}/>
        <Route path='/signUp' element={<SignUp />}/>
        <Route path="/create-adventure" element={<CreateAdventure />} />
        <Route path='UserDashboard' element={
          <ProtectedRoute>
            <UserDashboard />
          </ProtectedRoute>
        } />
      </Routes>
      </main> 
      <Footer />
    </div>
  )
}

export default App
