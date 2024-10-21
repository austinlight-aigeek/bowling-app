import React, { useState } from "react";
import { useSelector } from "react-redux";
import { getScore, getSummary } from "../../api"; // Import score and summary API functions
import Scorecard from "../Scorecard/Scorecard";
import Controls from "../Controls/Controls";
import "./Game.css";

const Game = () => {
  const { gameId, playerName } = useSelector((state) => state);

  return (
    <div className="Game">
      <h2>Player: {playerName}</h2>
      <Scorecard />
      <Controls />
    </div>
  );
};

export default Game;
