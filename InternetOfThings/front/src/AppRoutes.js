import React from "react";
import { Devices } from "./components/Devices";
import { Routes, Route, Navigate } from "react-router-dom";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/home" />} />
      <Route path="/devices" element={<Devices />} />
      <Route path="/home" element={<Devices />} />
    </Routes>
  );
};

export default AppRoutes;
