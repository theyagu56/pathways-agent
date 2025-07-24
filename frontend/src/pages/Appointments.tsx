import React from 'react';

const Appointments: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Appointments</h1>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
          + New Appointment
        </button>
      </div>

      {/* Upcoming Appointments */}
      <div className="bg-white rounded-lg shadow-md">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Upcoming Appointments</h2>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            <div className="border border-gray-200 rounded-lg p-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-gray-900">Physical Therapy Session</h3>
                  <p className="text-gray-600">Dr. Michael Chen - Physical Therapist</p>
                  <p className="text-sm text-gray-500">Tomorrow, 2:00 PM - 3:00 PM</p>
                </div>
                <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                  Confirmed
                </span>
              </div>
            </div>

            <div className="border border-gray-200 rounded-lg p-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-gray-900">Follow-up Consultation</h3>
                  <p className="text-gray-600">Dr. Sarah Johnson - Orthopedics</p>
                  <p className="text-sm text-gray-500">Dec 15, 2024, 10:00 AM - 10:30 AM</p>
                </div>
                <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">
                  Pending
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Past Appointments */}
      <div className="bg-white rounded-lg shadow-md">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Past Appointments</h2>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            <div className="border border-gray-200 rounded-lg p-4 opacity-75">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-gray-900">Initial Consultation</h3>
                  <p className="text-gray-600">Dr. Sarah Johnson - Orthopedics</p>
                  <p className="text-sm text-gray-500">Dec 1, 2024, 9:00 AM - 9:30 AM</p>
                </div>
                <span className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded-full">
                  Completed
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Appointments; 