// src/pages/Login.jsx
import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import LoginForm from "../components/LoginForm";
import { AuthContext } from "../contexts/AuthContext";
import api from "../api/http"; // make sure your renamed file is used
import toast from "react-hot-toast";

const Login = () => {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("employee");
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async () => {
  try {
    if (!email.endsWith("@company.com")) {
      toast.error("Invalid email");
      return;
    }

    const res = await api.post("/login", { email, role });
    console.log("Received user from backend:", res.data);
    if (res.data?.id) {
      // Store full user object from backend
      login(res.data); // ✅ Now includes id, name, email, role
      toast.success("Logged in!");
      navigate("/dashboard");
    } else {
      toast.error("Login failed: incomplete user data");
    }
  } catch (err) {
    toast.error("Login failed.");
    console.error(err);
  }
};



  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0F172A] text-white px-4">
      <LoginForm
        email={email}
        role={role}
        setEmail={setEmail}
        setRole={setRole}
        onLogin={handleLogin}
      />
    </div>
  );
};

export default Login;
