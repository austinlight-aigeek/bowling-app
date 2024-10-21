import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { actions } from "../../store/reducer";
import "./Controls.css";
import { recordFrames, getScore } from "../../api";

const Controls = () => {
  const { gameId, gameOver, pins, rolls, frames } = useSelector(
    (state) => state
  );
  const lastRoll = pins.slice(-1)[0];

  const dispatch = useDispatch();

  // This effect will trigger whenever `frames` is updated
  useEffect(() => {
    const updateFramesAndScore = async () => {
      if (gameId && frames.length > 0) {
        try {
          await recordFrames(gameId, frames); // Wait for recordFrames to finish
          const scoreData = await getScore(gameId); // Fetch the updated score after frames are recorded

          dispatch(actions.setScore({ score: scoreData.score }));
        } catch (error) {
          console.error("Error updating frames or fetching score:", error);
        }
      }
    };

    updateFramesAndScore();
  }, [frames, gameId]); // Listen to changes in `frames` and `gameId`

  const handleClick = async (pins) => {
    dispatch(actions.enterScore(pins)); // This will update the Redux state (including `frames`)
  };

  const handleRestart = () => {
    dispatch(actions.restart());
  };

  const disableButton = (number) => {
    if (gameOver) return true;
    if (rolls % 2 === 0 || rolls === 0) return false;
    if (rolls === 19 && lastRoll === 10) return false;
    return lastRoll + number > 10;
  };

  return (
    <div className="Container">
      <div>
        {[...Array(11).keys()].map((pin) => (
          <button
            key={pin}
            id={`pin${pin}`}
            disabled={disableButton(pin)}
            onClick={() => handleClick(pin)}
          >
            {pin}
          </button>
        ))}
      </div>
      {rolls > 0 && (
        <button className="Restart" onClick={handleRestart}>
          Restart
        </button>
      )}
    </div>
  );
};

export default Controls;
