import React, { useEffect, useState } from "react";
import {
  deleteClockTimer,
  getComponentData,
  getDeviceNames,
  sendHexValue,
  setClockTimer,
  setCode,
  simulateDevice,
  turnOffAlarm,
} from "../../services/DeviceService";
import {
  CenteredContainer,
  StyledOption,
  StyledSelect,
} from "../styled/SelectStyled";
import {
  ButtonNames,
  SimulatedButtons,
  urlGraphs,
} from "../../services/constants";
import ComponentDataTable from "../shared/ComponentDataTable";
import ReactDatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const Device = () => {
  const [deviceNames, setDeviceNames] = useState([]);
  const [selectedDevice, setSelectedDevice] = useState("");
  const [componentData, setComponentData] = useState(null);
  const [selectedTime, setSelectedTime] = useState(new Date());
  const [inputValue, setInputValue] = useState("");
  const [responseMessage, setResponseMessage] = useState('');
  const [error, setError] = useState('');

  const handleSelectChange = async (event) => {
    const newDevice = event.target.value;
    setSelectedDevice(newDevice);
    console.log(newDevice);
    if (newDevice) {
      const componentData = await getComponentData(newDevice);
      setComponentData(componentData);
    }
  };

  const handleActivateDevice = async () => {
    const formattedTime = formatTimeForRequest(selectedTime);
    const response = await setClockTimer(formattedTime);
    if (response && response.status === "uspešno") {
      console.log("Vreme uspešno postavljeno:", response.time);
    }
  };

  const handleAlarm = async () => {
    const response = await turnOffAlarm();
    if (response && response.status === "uspešno") {
      console.log("Vreme uspešno postavljeno:", response.time);
    }
  };

  const handleRemoteButtonClick = async (buttonCode) => {
    console.log("Button pressed:", buttonCode);
    const response = await sendHexValue(buttonCode);
    if (response && response.message) {
      console.log("Response from server:", response.message);
    }
  };
  const formatTimeForRequest = (time) => {
    const hours = time.getHours().toString().padStart(2, "0");
    const minutes = time.getMinutes().toString().padStart(2, "0");
    return `${hours}:${minutes}`;
  };

  const handleSimulateDevice = async () => {
    if (selectedDevice === "DS1" || selectedDevice === "DS2") {
      const response = await simulateDevice(selectedDevice);
      if (response && response.ok) {
        console.log("Device simulation successful:", response.ok);
      }
    }
  };

  const isValidInput = (input) => {
    const validCharacters = /^[1234567890ABCD*#]{4}$/;
    return validCharacters.test(input);
  };

  const handleConfirm = async () => {
    if (isValidInput(inputValue)) {
      console.log("Input Value:", inputValue);
      const response = await setCode(inputValue);
      if (response && response.message) {
        console.log(response.message);
      }
    } else {
      console.log("Neispravan unos!");
    }
  };
  const handleDeleteClockTimer = async () => {
    try {
      const response = await deleteClockTimer();
      setResponseMessage(response.status || "Uspešno ugašeno"); // Obrada odgovora
      setError(""); // Resetovanje greške
    } catch (err) {
      setError("Došlo je do greške"); // Obrada greške
      setResponseMessage(""); // Resetovanje odgovora
    }
  };
  useEffect(() => {
    const fetchData = async () => {
      const data = await getDeviceNames();
      setDeviceNames(data);
    };

    fetchData();
  }, []);

  return (
    <CenteredContainer>
      <StyledSelect value={selectedDevice} onChange={handleSelectChange}>
        <StyledOption value="">Select a Device</StyledOption>
        {deviceNames.map((name, index) => (
          <StyledOption key={index} value={name}>
            {name}
          </StyledOption>
        ))}
      </StyledSelect>
      <button onClick={handleAlarm}>Turn Off Alarm</button>
      {selectedDevice && (
        <>
          <h2>Selected Device: {selectedDevice}</h2>
          <iframe
            src={urlGraphs[selectedDevice]}
            width="900"
            height="400"
            frameBorder="0"
          ></iframe>
          {componentData && (
            <div>
              <h3>Component Data:</h3>
              <ComponentDataTable data={componentData.data} />
            </div>
          )}
        </>
      )}

      {selectedDevice === "B4SD" && (
        <div>
          <ReactDatePicker
            selected={selectedTime}
            onChange={(date) => setSelectedTime(date)}
            showTimeSelect
            dateFormat="Pp"
          />
          <button onClick={handleActivateDevice}>Set Clock Timer</button>
          <button onClick={handleDeleteClockTimer}>Ugasi Tajmer</button>
          {responseMessage && <p>{responseMessage}</p>}
          {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
      )}
      {(selectedDevice === "DS1" || selectedDevice === "DS2") && (
        <button onClick={handleSimulateDevice}>
          Simulate {selectedDevice}
        </button>
      )}
      {selectedDevice === "DMS" && (
        <div>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          <button onClick={handleConfirm}>Potvrdi</button>
        </div>
      )}
      {selectedDevice === "BIR" && (
        <div className="remote-control">
          {ButtonNames.map((name, index) => (
            <button
              key={index}
              onClick={() => handleRemoteButtonClick(SimulatedButtons[index])}
            >
              {name}
            </button>
          ))}
        </div>
      )}
    </CenteredContainer>
  );
};

export default Device;
