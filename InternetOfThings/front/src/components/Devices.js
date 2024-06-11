import React, { Component } from "react";
import "./Devices.css";
import { Navigation } from "./Navigation";
import DeviceService from "../services/DeviceService";
import io from "socket.io-client";
import RGBDialog from "./RGBDialog";
import DMSDialog from "./DMSDialog";
import BBDialog from "./BBDialog";

export class Devices extends Component {
  connected = false;

  constructor(props) {
    super(props);
    this.state = {
      data: [],
      deviceValues: {},
      isColorDialogOpen: false,
      isDMSDialogOpen: false,
      isBBDialogOpen: false,
      selectedDevice: null,
      showAlarm: localStorage.getItem("alarm") === "true",
    };
    this.socket = null;
  }

  async fetchData() {
    try {
      const result = await DeviceService.getDevices();
      const valuesResult = await DeviceService.getDeviceValues();
      this.setState({
        data: Object.values(result.data), // Convert object to array
        deviceValues: valuesResult.data.data,
      });
      console.log("Fetched devices:", result);
      console.log("Fetched device values:", valuesResult.data.data);
    } catch (error) {
      console.log("Error fetching data from the server");
      console.log(error);
    }
  }

  async componentDidMount() {
    this.fetchData();

    this.socket = io("http://localhost:8000");

    this.socket.on("connect", () => {
      console.log("Connected to server");
    });

    this.socket.on("disconnect", () => {
      console.log("Disconnected from server");
    });

    this.socket.on("data", (msg) => {
      const message = msg.message;
      console.log(message);
      let updated = this.updateDHT(message);
      if (updated) return;
      updated = this.updateGyro(message);
      if (updated) return;
      this.setState((prevState) => {
        const { data } = prevState;
        const deviceName = message.name;
        const value = message.value;

        const updatedData = data.map((device) =>
          device.name === deviceName
            ? {
                ...device,
                value: value,
                measurement: message.measurement,
              }
            : device
        );
        return {
          data: updatedData,
        };
      });
    });

    this.socket.on("alarm", (msg) => {
      const message = msg.message;
      console.log(message);
      this.setState({ showAlarm: message });
      localStorage.setItem("alarm", message);
    });

    this.socket.on("color_change", (msg) => {
      const { color } = msg;
      console.log("Color change:", color);
      this.setState((prevState) => {
        const updatedData = prevState.data.map((device) =>
          device.name === "BRGB"
            ? {
                ...device,
                value: color,
              }
            : device
        );
        return { data: updatedData };
      });
    });
  }

  updateDHT(message) {
    let updated = false;
    this.setState((prevState) => {
      const { data } = prevState;
      const deviceName = message.name;
      const value = message.value;

      if (message.measurement === "Temperature") {
        updated = true;
        const updatedData = data.map((device) =>
          device.name === deviceName ||
          (device.name === "GLCD" && deviceName === "GDHT")
            ? {
                ...device,
                valueT: value,
              }
            : device
        );
        return {
          data: updatedData,
        };
      } else if (message.measurement === "Humidity") {
        updated = true;
        const updatedData = data.map((device) =>
          device.name === deviceName ||
          (device.name === "GLCD" && deviceName === "GDHT")
            ? {
                ...device,
                valueH: value,
              }
            : device
        );
        return {
          data: updatedData,
        };
      }
    });
    return updated;
  }

  updateGyro(message) {
    let updated = false;
    this.setState((prevState) => {
      const { data } = prevState;
      const deviceName = message.name;
      const value = message.value;
      if (message.measurement === "Acceleration" && message.axis === "x") {
        updated = true;
        const updatedData = data.map((device) =>
          device.name === deviceName
            ? {
                ...device,
                valueAX: value,
              }
            : device
        );
        return {
          data: updatedData,
        };
      } else if (
        message.measurement === "Acceleration" &&
        message.axis === "y"
      ) {
        updated = true;
        const updatedData = data.map((device) =>
          device.name === deviceName
            ? {
                ...device,
                valueAY: value,
              }
            : device
        );
        return {
          data: updatedData,
        };
      } else if (
        message.measurement === "Acceleration" &&
        message.axis === "z"
      ) {
        updated = true;
        const updatedData = data.map((device) =>
          device.name === deviceName
            ? {
                ...device,
                valueAZ: value,
              }
            : device
        );
        return {
          data: updatedData,
        };
      } else if (message.measurement === "Gyroscope" && message.axis === "x") {
        updated = true;
        const updatedData = data.map((device) =>
          device.name === deviceName
            ? {
                ...device,
                valueGX: value,
              }
            : device
        );
        return {
          data: updatedData,
        };
      } else if (message.measurement === "Gyroscope" && message.axis === "y") {
        updated = true;
        const updatedData = data.map((device) =>
          device.name === deviceName
            ? {
                ...device,
                valueGY: value,
              }
            : device
        );
        return {
          data: updatedData,
        };
      } else if (message.measurement === "Gyroscope" && message.axis === "z") {
        updated = true;
        const updatedData = data.map((device) =>
          device.name === deviceName
            ? {
                ...device,
                valueGZ: value,
              }
            : device
        );
        return {
          data: updatedData,
        };
      }
    });
    return updated;
  }

  componentWillUnmount() {
    this.socket.disconnect();
  }

  openColorDialog = (device) => {
    this.setState({ isColorDialogOpen: true, selectedDevice: device }, () => {
      console.log("Selected Device:", this.state.selectedDevice);
    });
  };

  closeColorDialog = () => {
    this.setState({ isColorDialogOpen: false, selectedDevice: null });
  };

  openDMSDialog = (device) => {
    this.setState({ isDMSDialogOpen: true, selectedDevice: device }, () => {
      console.log("Selected Device:", this.state.selectedDevice);
    });
  };

  closeDMSDialog = () => {
    this.setState({ isDMSDialogOpen: false, selectedDevice: null });
  };

  openBBDialog = (device) => {
    this.setState({ isBBDialogOpen: true, selectedDevice: device }, () => {
      console.log("Selected Device:", this.state.selectedDevice);
    });
  };

  closeBBDialog = () => {
    this.setState({ isBBDialogOpen: false, selectedDevice: null });
  };

  handleActivateSystem = async () => {
    try {
      const response = await DeviceService.activateSystem();
      console.log(response.message);
    } catch (error) {
      console.log("Error activating system:", error);
    }
  };

  handleDeactivateSystem = async () => {
    try {
      const response = await DeviceService.deactivateSystem();
      console.log(response.message);
    } catch (error) {
      console.log("Error deactivating system:", error);
    }
  };

  render() {
    const { data, deviceValues } = this.state;
    const showAlarm = this.state.showAlarm;

    return (
      <div>
        <Navigation showAlarm={showAlarm} />
        <div id="tools"></div>
        <RGBDialog
          open={this.state.isColorDialogOpen}
          onClose={this.closeColorDialog}
          device={this.state.selectedDevice}
          fetchDeviceValues={this.fetchData} // Pass the fetch function to the dialog
        />
        <DMSDialog
          open={this.state.isDMSDialogOpen}
          onClose={this.closeDMSDialog}
          device={this.state.selectedDevice}
        />
        <BBDialog
          open={this.state.isBBDialogOpen}
          onClose={this.closeBBDialog}
          device={this.state.selectedDevice}
        />
        <DevicesList
          devices={data}
          deviceValues={deviceValues}
          openColorDialog={this.openColorDialog}
          openDMSDialog={this.openDMSDialog}
          openBBDialog={this.openBBDialog}
          handleActivateSystem={this.handleActivateSystem}
          handleDeactivateSystem={this.handleDeactivateSystem}
        />
        <iframe
          width="100%"
          height="900vh"
          src="http://localhost:3000/d/b32b85bf-e022-4505-8d2a-e0fd0c9e4f32/rpir4?orgId=1&from=1718038977575&to=1718060577575"
          frameBorder="0"
        ></iframe>
      </div>
    );
  }
}

const DevicesList = ({
  devices = [],
  deviceValues = {},
  openColorDialog,
  openDMSDialog,
  openBBDialog,
  handleActivateSystem,
  handleDeactivateSystem,
}) => {
  return (
    <div id="devices-container">
      {devices.map((device, index) => {
        const deviceValue = deviceValues[device.name] || {};
        return (
          <div key={index} className="device-card">
            <div className="device-info">
              <p className="device-title">{device.name}</p>
              <p className="device-text">
                Simulated: {device.simulated ? "Yes" : "No"}
              </p>
              <p className="device-text">Runs on: {device.runs_on}</p>
              <p className="device-text">Pin: {device.pin}</p>
              {device.measurement && (
                <p className="device-text">Measurement: {device.measurement}</p>
              )}
              <p className="device-text">Value: {device.value}</p>
              {device.valueT && (
                <p className="device-text">Temperature: {device.valueT}</p>
              )}
              {device.valueH && (
                <p className="device-text">Humidity: {device.valueH}</p>
              )}
              {device.valueAX && (
                <p className="device-text">Acceleration X: {device.valueAX}</p>
              )}
              {device.valueAY && (
                <p className="device-text">Acceleration Y: {device.valueAY}</p>
              )}
              {device.valueAZ && (
                <p className="device-text">Acceleration Z: {device.valueAZ}</p>
              )}
              {device.valueGX && (
                <p className="device-text">Gyroscope X: {device.valueGX}</p>
              )}
              {device.valueGY && (
                <p className="device-text">Gyroscope Y: {device.valueGY}</p>
              )}
              {device.valueGZ && (
                <p className="device-text">Gyroscope Z: {device.valueGZ}</p>
              )}
              {device.name.includes("RGB") && (
                <button
                  className="card-button"
                  onClick={() => openColorDialog(device)}
                >
                  Change Light
                </button>
              )}
              {device.name.includes("DMS") && (
                <button
                  className="card-button"
                  onClick={() => openDMSDialog(device)}
                >
                  Enter pin
                </button>
              )}
              {device.name.includes("BB") && (
                <button
                  className="card-button"
                  onClick={() => openBBDialog(device)}
                >
                  Edit alarm clock
                </button>
              )}
              {device.name.includes("DMS") && (
                <div>
                  <button
                    className="card-button"
                    onClick={handleActivateSystem}
                  >
                    Activate System
                  </button>
                  <button
                    className="card-button"
                    onClick={handleDeactivateSystem}
                  >
                    Deactivate System
                  </button>
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
