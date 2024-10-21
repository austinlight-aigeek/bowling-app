import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { getPlayerHistory } from "../../api"; // Import the API call

const HistoryGraph = ({ playerName }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const history = await getPlayerHistory(playerName);

        // Transform the data for the chart
        const chartData = history.map((game) => ({
          date: new Date(game.start_time).toLocaleDateString(), // Format date for x-axis
          score: game.score, // Total score of the game
          strikes: game.strikes, // Number of strikes
          spares: game.spares, // Number of spares
        }));

        setData(chartData); // Set the data for the chart
      } catch (error) {
        console.error("Error loading player history:", error);
      }
    };

    fetchData();
  }, [playerName]);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart
        data={data}
        margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="date"
          label={{ value: "Date", position: "insideBottomRight", offset: -5 }}
        />
        <YAxis
          label={{ value: "Values", angle: -90, position: "insideLeft" }}
        />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="score"
          stroke="#8884d8"
          activeDot={{ r: 8 }}
        />
        <Line type="monotone" dataKey="strikes" stroke="#82ca9d" />
        <Line type="monotone" dataKey="spares" stroke="#ff7300" />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default HistoryGraph;
