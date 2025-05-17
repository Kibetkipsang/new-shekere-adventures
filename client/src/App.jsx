import { useState } from 'react'
import './App.css'

function App() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [phoneNumber, setPhoneNumber] = useState('')
  
  const handleSubmit = (e) => {
    e.preventDefault()
    console.log({name, email, phoneNumber})
  }
 

  return (
    <div className="min-h-screen flex justify-center items-center bg-green-200">
  <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-full max-w-sm">
    <label className="block mb-4">
      <span className="block text-left font-semibold mb-1">Name:</span>
      <input
        type="text"
        placeholder="Write your name here!"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="w-full border rounded px-3 py-2"
      />
    </label>

    <label className="block mb-4">
      <span className="block text-left font-semibold mb-1">Email:</span>
      <input
        type="email"
        placeholder="Write your email here!"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full border rounded px-3 py-2"
      />
    </label>

    <label className="block mb-4">
      <span className="block text-left font-semibold mb-1">Phone:</span>
      <input
        type="tel"
        placeholder="eg: 0712345678"
        value={phoneNumber}
        onChange={(e) => setPhoneNumber(e.target.value)}
        className="w-full border rounded px-3 py-2"
      />
    </label>

    <button type="submit" className="bg-green-500 text-white px-4 py-2 rounded">
      Submit
    </button>
  </form>
</div>

  )
}

export default App
