import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { getStatistics, getSummary } from "../../api";
import HistoryGraph from "./HistoryGraph";
import "./GameInfo.css";

const GameInfo = () => {
  const { gameId, playerName } = useSelector((state) => state);

  const [statisticVisible, setStatisticsVisible] = useState(false);
  const [historyVisible, setHistorysVisible] = useState(false);
  const [summaryVisible, setSummaryVisible] = useState(false); // Controls summary visibility
  const [summary, setSummary] = useState(""); // Holds the game summary
  const [selectedLLM, setSelectedLLM] = useState("gpt"); // Default LLM option
  const [loading, setLoading] = useState(false); // Loading state

  const [statistics, setStatistics] = useState({
    totalGames: 0,
    totalScore: 0,
    highestScore: 0,
    lowestScore: 0,
    averageScore: 0,
  });

  const handleStatistics = () => {
    setStatisticsVisible(!statisticVisible);
  };

  const handleHistory = () => {
    setHistorysVisible(!historyVisible);
  };

  const handleSummary = () => {
    setSummaryVisible(!summaryVisible);
  };

  const fetchStatistics = async (playerName) => {
    const data = await getStatistics(playerName);
    setStatistics({
      totalGames: data.total_games,
      totalScore: data.total_score,
      highestScore: data.highest_score,
      lowestScore: data.lowest_score,
      averageScore: data.average_score,
    });
  };

  const fetchSummary = async (gameId) => {
    if (summaryVisible) {
      setLoading(true);
      try {
        const fetchedSummary = await getSummary(gameId, selectedLLM);
        setSummary(fetchedSummary); // Set the fetched summary
      } catch (error) {
        console.error("Error fetching summary:", error);
        setSummary("Failed to fetch summary");
      }
      setLoading(false);
    }
  };

  const handleLLMChange = (event) => {
    setSelectedLLM(event.target.value);
  };

  useEffect(() => {
    if (statisticVisible) {
      fetchStatistics(playerName);
    }
  }, [statisticVisible]);

  useEffect(() => {
    fetchSummary(gameId);
  }, [summaryVisible, selectedLLM]);

  return (
    <div>
      <h2>Player: {playerName}</h2>
      <div className="">
        <div className="game-info-head">
          <h3>Statistics</h3>
          <button onClick={handleStatistics}>
            {statisticVisible ? "Hide" : "Show"}
          </button>
        </div>
        {statisticVisible && (
          <div className="game-info-content">
            <p>total games: {statistics.totalGames}</p>
            <p>total score: {statistics.totalScore}</p>
            <p>highest score: {statistics.highestScore}</p>
            <p>lowest score: {statistics.lowestScore}</p>
            <p>average score: {statistics.averageScore}</p>
          </div>
        )}
        <div className="game-info-head">
          <h3>History</h3>
          <button onClick={handleHistory}>
            {historyVisible ? "Hide" : "Show"}
          </button>
        </div>
        {historyVisible && (
          <div className="game-info-content">
            <HistoryGraph playerName={playerName} />
          </div>
        )}
        <div className="game-info-head">
          <h3>Summary</h3>
          <button onClick={handleSummary}>
            {summaryVisible ? "Hide" : "Show"}
          </button>

          {/* Dropdown for LLM options */}
          <select value={selectedLLM} onChange={handleLLMChange}>
            <option value="gpt">OpenAI GPT</option>
            <option value="bert">Google BERT</option>
            <option value="t5">T5</option>
            <option value="llama">LLaMA</option>
          </select>
        </div>

        {/* Summary content */}
        {summaryVisible && (
          <div className="game-info-content">
            {loading ? <p>Loading summary...</p> : <p>{summary}</p>}
          </div>
        )}
      </div>
    </div>
  );
};

export default GameInfo;
