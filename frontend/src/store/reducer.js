import { createAction } from "redux-actions";
import mapValues from "lodash.mapvalues";
import {
  updateFrames,
  updateCumulativeScore,
  isGameOver,
  updateCurrentRoll,
} from "../utils";

// Action types
const types = {
  enterScore: "Game/EnterScore",
  setScore: "Game/SetScore",
  restart: "Game/Restart",
  startGame: "Game/StartGame",
  resetGame: "Game/ResetGame",
};

// Action creators
export const actions = mapValues(types, (type) => createAction(type));

// Initial state
const initialState = {
  gameId: null,
  playerName: "",
  frames: [],
  cumulativeScores: [],
  totalScore: "",
  gameOver: false,
  pins: [],
  rolls: 0,
};

// Reducer function
const reducer = (state = initialState, action) => {
  switch (action.type) {
    case types.startGame:
      return {
        ...state,
        gameId: action.payload.gameId,
        playerName: action.payload.playerName,
      };

    case types.setScore:
      return {
        ...state,
        totalScore: action.payload.score,
      };

    case types.resetGame:
      return {
        ...state,
        gameId: null,
        playerName: "",
      };

    case types.enterScore:
      const { frames, cumulativeScores, pins, rolls } = state;

      return {
        ...state,
        frames: updateFrames(rolls, action.payload, frames),
        cumulativeScores: updateCumulativeScore(
          rolls,
          frames,
          cumulativeScores,
          pins,
          action.payload
        ),
        gameOver: isGameOver(rolls, action.payload, pins),
        pins: pins.concat(action.payload),
        rolls: updateCurrentRoll(rolls, action.payload),
      };

    case types.restart:
      return initialState;

    default:
      return state;
  }
};

export default reducer;
