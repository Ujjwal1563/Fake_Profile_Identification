import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateData = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:8000/generate");
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data", error);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Fake Profile Detection</h1>
      <button onClick={generateData} disabled={loading}>
        {loading ? "Generating..." : "Generate Data"}
      </button>

      {data && (
        <div>
          <h2>Accuracy: {data.accuracy.toFixed(2)}</h2>
          <h3>Graph Visualization:</h3>
          <img src={`data:image/png;base64,${data.graph}`} alt="Graph" />

          <h3>Synthetic Data:</h3>
          <table border="1">
            <thead>
              <tr>
                <th>Posts</th>
                <th>Requests</th>
                <th>Followers</th>
                <th>Account Age (Days)</th>
                <th>Label</th>
              </tr>
            </thead>
            <tbody>
              {data.synthetic_data.map((row, index) => (
                <tr key={index}>
                  <td>{row.number_of_posts}</td>
                  <td>{row.number_of_requests}</td>
                  <td>{row.number_of_followers}</td>
                  <td>{row.account_age_days}</td>
                  <td>{row.label === 1 ? "Fake" : "Real"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default App;
