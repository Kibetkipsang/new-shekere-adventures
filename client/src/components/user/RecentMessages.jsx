import React from "react";

export default function RecentMessages(){
    return(
        <>
        <div className="bg-white p-4 rounded-2xl shadow border border-yellow-400 mt-6">
            <h3 className="text-lg font-semibold text-black mb-2">Recent Messages</h3>
            {RecentMessages.length === 0 ? (<p className="text-gray-500">No recent messages!</p>) : (
                <ul className="text-gray-700 space-y-2">
                    {messages.map((msg, index) => (
                        <li key={index} >
                            <strong>{msg.groupName}</strong>:"{msg.content}"
                        </li>
                    ))}
                </ul> 
            )}
        </div>
        </>
    )
}