import React, { useEffect, useState } from "react";
import api from "../api/http";
import toast from "react-hot-toast";

const FeedbackList = ({ userId, userRole }) => {
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [commentInputs, setCommentInputs] = useState({});

  const fetchFeedbacks = async () => {
    try {
      let res;
      if (userRole === "employee") {
        res = await api.get(`/feedback/${userId}`);
      } else if (userRole === "manager") {
        res = await api.get(`/feedback/manager/${userId}`);
      }
      setFeedbacks(res.data);
    } catch (err) {
      console.error("Failed to load feedbacks:", err);
      toast.error("Failed to load feedbacks.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeedbacks();
  }, [userId, userRole]);

  const handleAcknowledge = async (id) => {
    try {
      await api.post(`/feedback/${id}/acknowledge`);
      toast.success("Feedback acknowledged");
      fetchFeedbacks(); // refresh list
    } catch {
      toast.error("Failed to acknowledge feedback");
    }
  };

  const handleCommentSubmit = async (id) => {
    const comment = commentInputs[id];
    if (!comment.trim()) return;
    try {
      await api.post(`/feedback/${id}/comment`, { comment });
      toast.success("Comment added");
      fetchFeedbacks(); // refresh list
    } catch {
      toast.error("Failed to submit comment");
    }
  };

  const sentimentColor = {
    positive: "text-green-600",
    neutral: "text-yellow-600",
    negative: "text-red-600",
  };

  return (
    <div className="space-y-4">
      {loading ? (
        <p>Loading feedback...</p>
      ) : feedbacks.length === 0 ? (
        <p className="text-gray-500 italic">No feedback yet.</p>
      ) : (
        feedbacks.map((f) => (
          <div
            key={f.id}
            className="border p-4 rounded shadow-sm bg-white transition hover:shadow-md"
          >
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-black">
  {userRole === "employee"
    ? `From: ${f.manager_name || f.manager_email || "Anonymous"}`
    : `To: ${f.employee_name || f.employee_email || "Anonymous"}`}
</span>
              <span className={`font-bold ${sentimentColor[f.sentiment]}`}>
                {f.sentiment.toUpperCase()}
              </span>
            </div>

            <div className="mb-2 text-black">
              <p className="font-semibold">Strengths:</p>
              <p>{f.strengths}</p>
            </div>

            <div className="mb-2 text-black">
              <p className="font-semibold">Areas to Improve:</p>
              <p>{f.improvements}</p>
            </div>

            {userRole === "employee" && (
              <>
                <div className="mt-2">
                  {f.acknowledged ? (
                    <span className="text-green-600 font-semibold">✅ Acknowledged</span>
                  ) : (
                    <button
                      className="text-sm text-blue-600 underline"
                      onClick={() => handleAcknowledge(f.id)}
                    >
                      Acknowledge
                    </button>
                  )}
                </div>

                <div className="mt-4 text-black">
                  <p className="font-semibold mb-1">Your Comment:</p>
                  {f.employee_comment ? (
                    <div className="p-2 bg-gray-100 rounded">{f.employee_comment}</div>
                  ) : (
                    <div className="flex gap-2">
                      <input
                        type="text"
                        className="border p-1 flex-1 rounded text-black"
                        placeholder="Write your comment"
                        value={commentInputs[f.id] || ""}
                        onChange={(e) =>
                          setCommentInputs({ ...commentInputs, [f.id]: e.target.value })
                        }
                      />
                      <button
                        onClick={() => handleCommentSubmit(f.id)}
                        className="bg-blue-600 text-white px-3 py-1 rounded"
                      >
                        Submit
                      </button>
                    </div>
                  )}
                </div>
              </>
            )}
            {userRole === "manager" && (
  <div className="mb-2 text-black">
    <p className="font-semibold">Employee Comment:</p>
    {f.employee_comment ? (
      <div className="p-2 bg-gray-100 rounded">{f.employee_comment}</div>
    ) : (
      <span className="italic text-gray-500">No comment yet</span>
    )}
  </div>
)}
          </div>
          
        ))
      )}
    </div>
  );
};

export default FeedbackList;
