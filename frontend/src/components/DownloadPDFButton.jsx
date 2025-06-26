// src/components/DownloadPDFButton.js
import React from "react";
import api from "../api/http"; 

const DownloadPDFButton = ({ managerId }) => {
  const handleDownload = async () => {
    try {
      const response = await api.get(`/feedback/manager/${managerId}/export/pdf`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data], { type: "application/pdf" }));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "manager_feedback_report.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Failed to download PDF:", error);
    }
  };

  return (
    <button
      onClick={handleDownload}
      className="bg-indigo-600 text-white px-4 py-2 rounded-xl hover:bg-indigo-700 transition"
    >
      Download PDF Report
    </button>
  );
};

export default DownloadPDFButton;
