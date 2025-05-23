import React, { useEffect, useState } from "react";


export default function WelcomeBanner({ name }) {
  return (
    <div className="bg-white text-black rounded-2xl p-4 shadow border-l-4 border-b-2 border-yellow-400 mt-2 text-center">
      <h3 className="text-xl font-semibold">Welcome {name || "Traveller"}</h3>
      <h3 className="text-gray-800">Ready for your next adventure?</h3>
    </div>
  );
}