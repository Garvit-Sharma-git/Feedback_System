// src/components/DownloadPDFButton.js
import React from "react";

const LoginForm = ({ email, role, setEmail, setRole, onLogin }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (onLogin) {
      onLogin();
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-6 w-96 bg-white/5 backdrop-blur-md p-8 rounded-2xl shadow-xl border border-white/10"
    >
      <h2 className="text-3xl font-bold text-center text-purple-400">Login</h2>

      <div>
        <label className="block text-sm font-medium text-white/80 mb-1">Email</label>
        <input
          className="w-full bg-white/10 text-white placeholder-white/50 border border-white/20 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
          type="email"
          placeholder="you@company.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-white/80 mb-1">Role</label>
        <select
          className="w-full bg-white/10 text-white border border-white/20 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          required
        >
          <option value="manager">Manager</option>
          <option value="employee">Employee</option>
        </select>
      </div>

      <button
        type="submit"
        className="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded transition duration-200"
      >
        Login
      </button>
    </form>
  );
};

export default LoginForm;
