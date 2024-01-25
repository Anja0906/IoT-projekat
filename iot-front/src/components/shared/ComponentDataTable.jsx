const ComponentDataTable = ({ data }) => {
    if (!data || data.length === 0) {
      return <p>No data available for this component.</p>;
    }
  
    return (
      <table>
        <thead>
          <tr>
            <th>Field</th>
            <th>Measurement</th>
            <th>Time</th>
            <th>Value</th>
            <th>Name</th>
            <th>Runs On</th>
            <th>Simulated</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item._field}</td>
              <td>{item._measurement}</td>
              <td>{new Date(item._time).toLocaleString()}</td>
              <td>{item._value.toString()}</td>
              <td>{item.name}</td>
              <td>{item.runs_on}</td>
              <td>{item.simulated}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  export default ComponentDataTable;