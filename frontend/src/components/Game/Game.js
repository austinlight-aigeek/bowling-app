import React, { useState } from "react";
import { useSelector } from "react-redux";
import Scorecard from "../Scorecard/Scorecard";
import Controls from "../Controls/Controls";
import GameInfo from "../GameInfo/GameInfo";
import "./Game.css";

const Game = () => {
  return (
    <div className="Game">
      <Scorecard />
      <Controls />
      <GameInfo />
    </div>
  );
};

export default Game;
