import axios from "axios";
const API_URL = "http://localhost:8000/api";

class DeviceService {
  getDevices() {
    return axios.get(`${API_URL}/device_info`);
  }

  getDeviceValues() {
    return axios.get(`${API_URL}/device_values`);
  }

  async activateSystem() {
    try {
      const response = await axios.get(`${API_URL}/active`);
      return response.data;
    } catch (error) {
      console.error("Error activating system:", error);
      throw error;
    }
  }

  async deactivateSystem() {
    try {
      const response = await axios.get(`${API_URL}/deactive`);
      return response.data;
    } catch (error) {
      console.error("Error deactivating system:", error);
      throw error;
    }
  }

  async updateRGBLight(color) {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/updateRGB/${color}`
      );
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  }

  async getAlarmClock() {
    try {
      const response = await axios.get(
        "http://localhost:8000/api/getAlarmClock"
      );
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  }

  async updateAlarmClock(time) {
    try {
      const response = await axios.put(
        "http://localhost:8000/api/setAlarmClock",
        { time }
      );
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  }

  async inputPin(pin) {
    try {
      const response = await axios.put("http://localhost:8000/api/inputPin", {
        pin,
      });
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  }

  async turnOffAlarmClock() {
    try {
      const response = await axios.get(
        "http://localhost:8000/api/turnOffAlarmClock"
      );
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  }
}

export default new DeviceService();
