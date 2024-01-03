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
