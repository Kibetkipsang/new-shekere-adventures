import React from "react";

export default function UpcomingTrips({ trips = [] }){
    return(
        <>
        <div className="bg-white p-4 shadow rounded-xl border border-yellow-400">
            <h4 className="text-lg font-semibold text-black mb-2">Upcoming Trips</h4>
            {trips.length === 0 ? (<p className="text-gray-500">You have no upcoming trips!</p>) : (
                <ul>
                    {trips.map((trip, index) => (
                        <li key={index} className="text-gray-700 space-y-2">
                           {trip.title} - {new Date(trip.date).toLocaleDateString()}
                        </li>
                    ))}
                </ul>
            )}
        </div>
        </>
    )
}