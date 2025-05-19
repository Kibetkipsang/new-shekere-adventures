import { BrowserRouter as Router, Routes,Route } from 'react-router-dom'
import './App.css'
import Login from './components/login'
import SignUp from './components/signUp';
import { Navigate } from "react-router-dom";
import NavBar from './components/NavBar';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-green-200">
      <NavBar />
      <Routes>
        <Route path="/" element={<Navigate to="/signUp" />} />
        <Route path='/login' element={<Login/>}/>
        <Route path='/signUp' element={<SignUp />}/>
      </Routes>
      <Footer />
    </div>
  )
}

export default App
