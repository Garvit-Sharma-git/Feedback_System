// src/components/DownloadPDFButton.js
import React, { useState } from "react";
import api from "../api/http";
import toast from "react-hot-toast";

const FeedbackForm = ({ employeeId, managerId, onFeedbackSubmitted }) => {
  const [strengths, setStrengths] = useState("");
  const [improvements, setImprovements] = useState("");
  const [sentiment, setSentiment] = useState("positive");
  const [isAnonymous, setIsAnonymous] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post(`/feedback?manager_id=${managerId}`, {
        employee_id: employeeId,
        strengths,
        improvements,
        sentiment,
        is_anonymous: isAnonymous, // send anonymous flag
      });
      toast.success("Feedback submitted!");

      // Reset form
      setStrengths("");
      setImprovements("");
      setSentiment("positive");
      setIsAnonymous(false);

      if (onFeedbackSubmitted) onFeedbackSubmitted();
    } catch (err) {
      toast.error("Failed to submit feedback");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block font-medium">Strengths</label>
        <textarea
          className="w-full border text-black rounded p-2"
          rows={3}
          value={strengths}
          onChange={(e) => setStrengths(e.target.value)}
          required
        />
      </div>

      <div>
        <label className="block font-medium">Areas to Improve</label>
        <textarea
          className="w-full border text-black rounded p-2"
          rows={3}
          value={improvements}
          onChange={(e) => setImprovements(e.target.value)}
          required
        />
      </div>

      <div>
        <label className="block font-medium">Overall Sentiment</label>
        <select
          className="w-full border text-black rounded p-2"
          value={sentiment}
          onChange={(e) => setSentiment(e.target.value)}
          required
        >
          <option value="positive">Positive</option>
          <option value="neutral">Neutral</option>
          <option value="negative">Negative</option>
        </select>
      </div>

      <div className="flex items-center space-x-2">
        <input
          type="checkbox"
          checked={isAnonymous}
          onChange={(e) => setIsAnonymous(e.target.checked)}
          className="form-checkbox h-4 w-4 text-indigo-600"
        />
        <span className="text-sm text-gray-200">Submit anonymously</span>
      </div>

      <button
        type="submit"
        className={`bg-blue-600 text-white px-4 py-2 rounded ${loading ? "opacity-50" : ""}`}
        disabled={loading}
      >
        {loading ? "Submitting..." : "Submit Feedback"}
      </button>
    </form>
  );
};

export default FeedbackForm;
