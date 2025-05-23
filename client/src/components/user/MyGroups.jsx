import React from "react";

export default function MyGroups(){
    return(
        <>
        <div className="bg-white p-4 rounded-xl shadow border border-yellow-400 mt-6">
            <h3 className="text-lg font-semibold text-black mb-2">My Groups</h3>
            {MyGroups.length === 0 ? (<p>You have not joined any groups yet!</p>) : (
                <ul className="text-gray-700 space-y-2">
                    {MyGroups.map((group, index) => (
                        <li key={index}>
                            <span>{group.name}</span>
                            <button className="ml-2 text-yellow-600 hover: underline">View</button>
                            <button className="ml-2 text-yellow-600 hover: underline">Chat</button>
                            </li>
                    ))}
                </ul>
            )}
        </div>
        </>
    )
}