import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../contexts/AuthContext";
import FeedbackForm from "../components/FeedbackForm";
import FeedbackList from "../components/FeedbackList";
import api from "../api/http";
import toast from "react-hot-toast";
import DownloadPDFButton from "../components/DownloadPDFButton";

const Dashboard = () => {
  const { user, logout } = useContext(AuthContext);
  const [teamMembers, setTeamMembers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user?.role === "manager") {
      api
        .get(`/team?manager_id=${user.id}`)
        .then((res) => setTeamMembers(res.data))
        .catch(() => toast.error("Failed to fetch team members"))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [user]);

  if (!user) return <div className="text-center py-10">Loading...</div>;

  return (
    <div className="max-w-4xl  mx-auto p-6">
      {/* <DownloadPDFButton managerId={user.id} /> */}
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-white mb-1">
            Welcome, {user.name}
          </h2>
          <p className="text-sm text-purple-300 uppercase tracking-wide">
            {user.role}
          </p>
        </div>
        <button
          onClick={() => {
            logout();
            toast.success("Logged out");
          }}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition"
        >
          Logout
        </button>
      </div>

      {/* Main Content */}
      {loading ? (
        <p className="text-purple-300">Loading team...</p>
      ) : (
        <>
          {user.role === "manager" && (
            <div className="space-y-6">
              <DownloadPDFButton managerId={user.id} />
              <div>
                <h3 className="text-xl font-semibold text-white mb-4">
                  Team Members
                </h3>
                {teamMembers.length === 0 ? (
                  <p className="text-purple-300 italic">
                    No team members assigned.
                  </p>
                ) : (
                  teamMembers.map((member) => (
                    <div
                      key={member.id}
                      className="bg-white/5 backdrop-blur rounded-xl p-5 border border-white/10"
                    >
                      <p className="text-lg font-medium text-white mb-2">
                        {member.name}
                      </p>
                      <FeedbackForm
                        employeeId={member.id}
                        managerId={user.id}
                        onFeedbackSubmitted={() =>
                          toast.success("Feedback submitted!")
                        }
                      />
                    </div>
                  ))
                )}
              </div>

              <div>
                <h3 className="text-xl  font-semibold text-white mt-8 mb-4">
                  Feedbacks Given
                </h3>
                <FeedbackList userId={user.id} userRole="manager" />
              </div>
            </div>
          )}

          {user.role === "employee" && (
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">
                Your Feedback Timeline
              </h3>
              <FeedbackList userId={user.id} userRole="employee" />
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Dashboard;
