import React, { useEffect, useState } from "react";
import { getDeviceNames } from "../../services/DeviceService";
import { CenteredContainer, StyledOption, StyledSelect } from "../styled/SelectStyled";
import { urlGraphs } from "../../services/constants";

const Device = () => {
  const [deviceNames, setDeviceNames] = useState([]);
  const [selectedDevice, setSelectedDevice] = useState("");

  const handleSelectChange = (event) => {
    setSelectedDevice(event.target.value);
    console.log(event.target.value);
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
          <StyledOption key={index} value={name}>{name}</StyledOption>
        ))}
      </StyledSelect>

      {selectedDevice && (
        <>
          <h2>Selected Device: {selectedDevice}</h2>
          <iframe 
            src={urlGraphs[selectedDevice]} 
            width="900" 
            height="500" 
            frameBorder="0">
          </iframe>
        </>
      )}
    </CenteredContainer>
  );
};

export default Device;
