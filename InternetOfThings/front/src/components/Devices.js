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
      this.setState({ data: result });
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

  render() {
    const { data } = this.state;
    const showAlarm = this.state.showAlarm;

    return (
      <div>
        <Navigation showAlarm={showAlarm} />
        <div id="tools"></div>
        <RGBDialog
          open={this.state.isColorDialogOpen}
          onClose={this.closeColorDialog}
          device={this.state.selectedDevice}
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
          openColorDialog={this.openColorDialog}
          openDMSDialog={this.openDMSDialog}
          openBBDialog={this.openBBDialog}
        />
        <iframe
          width="100%"
          height="900vh"
          src="http://localhost:3000/public-dashboards/b7417158c7d5433e91984caeb220d594"
          frameBorder="0"
        ></iframe>
      </div>
    );
  }
}

const DevicesList = ({
  devices,
  openColorDialog,
  openDMSDialog,
  openBBDialog,
}) => {
  const chunkSize = 5;
  const chunkArray = (arr, size) => {
    return Array.from({ length: Math.ceil(arr.length / size) }, (v, i) =>
      arr.slice(i * size, i * size + size)
    );
  };

  const rows = chunkArray(devices, chunkSize);

  return (
    <div id="devices-container">
      {rows.map((row, rowIndex) => (
        <div key={rowIndex} className="device-row">
          {row.map((device, index) => (
            <div key={index} className="device-card">
              <div className="device-info">
                <p className="device-title">{device.name}</p>
                <p className="device-text">{device.type}</p>
                {device.simulated && (
                  <p className="device-text">
                    <b>Simulation:</b> True
                  </p>
                )}
                {!device.simulated && (
                  <p className="device-text">
                    <b>Simulation:</b> False
                  </p>
                )}
                {device.type.slice(-3) === "DHT" && (
                  <p className="device-text">
                    <b>Temperature: </b>
                    {device.valueT}°C
                  </p>
                )}
                {device.type.slice(-3) === "DHT" && (
                  <p className="device-text">
                    <b>Humidity: </b>
                    {device.valueH}%
                  </p>
                )}
                {device.name === "GLCD" && (
                  <p className="device-text">
                    <b>Temperature: </b>
                    {device.valueT}°C
                  </p>
                )}
                {device.name === "GLCD" && (
                  <p className="device-text">
                    <b>Humidity: </b>
                    {device.valueH}%
                  </p>
                )}
                {device.name === "GSG" && (
                  <p className="device-text">
                    <b>Acceleration: </b>
                    {device.valueAX}, {device.valueAY}, {device.valueAZ}
                  </p>
                )}
                {device.name === "GSG" && (
                  <p className="device-text">
                    <b>Gyroscope: </b>
                    {device.valueGX}, {device.valueGY}, {device.valueGZ}
                  </p>
                )}
                {device.type.slice(-3) !== "DHT" &&
                  device.name !== "GSG" &&
                  device.name !== "GLCD" && (
                    <p className="device-text">
                      <b>{device.measurement}: </b>
                      {device.value}
                    </p>
                  )}
                {device.name === "BRGB" && (
                  <p className="device-text">
                    <button
                      className="card-button"
                      onClick={() => openColorDialog(device)}
                    >
                      Change Light
                    </button>
                  </p>
                )}
                {device.name === "DMS" && (
                  <p className="device-text">
                    <button
                      className="card-button"
                      onClick={() => openDMSDialog(device)}
                    >
                      Enter pin
                    </button>
                  </p>
                )}
                {device.name === "BB" && (
                  <p className="device-text">
                    <button
                      className="card-button"
                      onClick={() => openBBDialog(device)}
                    >
                      Edit alarm clock
                    </button>
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};
