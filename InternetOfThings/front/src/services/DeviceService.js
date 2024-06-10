import axios from "axios";

class DeviceService {
  async getDevices() {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/device_names`
      );
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      return [];
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
