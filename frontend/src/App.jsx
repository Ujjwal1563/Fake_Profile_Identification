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
    <div className="min-h-screen bg-gray-100 p-6 flex flex-col items-center">
      <header className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white text-center py-6 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold">Fake Profile Identification</h1>
        <p className="text-sm opacity-90">Detect fake profiles using AI models</p>
      </header>
      <button onClick={generateData} disabled={loading}
      className="mt-6 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md transition-transform transform hover:scale-105 hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Generating..." : "Generate Data"}
      </button>

      {data && (
        <div>
          <h2 className="text-xl font-bold text-gray-800">Accuracy: {data.accuracy.toFixed(2)}</h2>
          <div className="mt-6 bg-white p-4 shadow-lg rounded-lg">
          <h2 className="text-lg font-semibold text-gray-700 mb-3">Graph Visualization</h2>
          <img src={`data:image/png;base64,${data.graph}`} alt="Graph" className="rounded-lg shadow-md" />
        </div>

          <h3 className="text-xl font-semibold mt-6">Synthetic Data:</h3>
<div className="overflow-x-auto bg-white shadow-lg rounded-lg mt-4">
  <table className="w-full border-collapse">
    <thead>
      <tr className="bg-blue-600 text-white">
        <th className="py-3 px-4 border">Posts</th>
        <th className="py-3 px-4 border">Requests</th>
        <th className="py-3 px-4 border">Followers</th>
        <th className="py-3 px-4 border">Account Age (Days)</th>
        <th className="py-3 px-4 border">Label</th>
      </tr>
    </thead>
    <tbody>
      {data.synthetic_data.map((row, index) => (
        <tr
          key={index}
          className={`border text-gray-700 hover:bg-gray-100 transition ${
            index % 2 === 0 ? "bg-gray-50" : "bg-white"
          }`}
        >
          <td className="py-3 px-4 border">{row.number_of_posts}</td>
          <td className="py-3 px-4 border">{row.number_of_requests}</td>
          <td className="py-3 px-4 border">{row.number_of_followers}</td>
          <td className="py-3 px-4 border">{row.account_age_days}</td>
          <td
            className={`py-3 px-4 border font-semibold ${
              row.label === 1 ? "text-red-500" : "text-green-500"
            }`}
          >
            {row.label === 1 ? "Fake" : "Real"}
          </td>
        </tr>
      ))}
    </tbody>
  </table>
</div>

        </div>
      )}
    </div>
  );
};

export default App;
