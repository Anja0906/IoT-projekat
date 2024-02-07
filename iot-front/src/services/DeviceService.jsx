import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

export const getDeviceNames = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/device_names`);
    return response.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return [];
  }
};

export const getComponentData = async (componentName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/component_data/${componentName}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching component data:", error);
    return null;
  }
};

export const activateDevice = (time) => {
  const hours = time.getHours().toString().padStart(2, '0'); // Dodaje vodeću nulu ako je potrebno
  const minutes = time.getMinutes().toString().padStart(2, '0'); // Dodaje vodeću nulu ako je potrebno

  const formattedTime = `${hours}:${minutes}`;
  console.log("Activating device at time:", formattedTime);
  // Implementirajte logiku za aktivaciju uređaja
};

export const setClockTimer = async (time) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/set_clock_timer`, { time });
    return response.data;
  } catch (error) {
    console.error("Error setting clock timer:", error);
    return null;
  }
};

export const turnOffAlarm = async (time) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/set_off_alarm`,  {});
    return response.data;
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
};

export const simulateDevice = async (deviceName) => {
  try {
    const endpoint = deviceName === 'DS1' ? 'simulate_ds1' : 'simulate_ds2';
    const response = await axios.get(`${API_BASE_URL}/${endpoint}`);
    return response.data;
  } catch (error) {
    console.error("Error simulating device:", error);
    return null;
  }
};

export const setCode = async (code) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/set_code`, { code });
    return response.data;
  } catch (error) {
    console.error("Error setting code:", error);
    return null;
  }
};

export const sendHexValue = async (hexValue) => {
  try {
    const hexString = hexValue.toString(16);
    const response = await axios.put(`${API_BASE_URL}/ir_remote/${hexString}`);
    return response.data;
  } catch (error) {
    console.error("Error sending hex value:", error);
    return null;
  }
};

export const deleteClockTimer = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/delete_clock_timer`);
    return response.data;
  } catch (error) {
    console.error("Error deleting clock timer:", error);
    return null;
  }
};