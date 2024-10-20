import React, { useState } from "react";
import { recordRoll } from "../api"; // Import the API function

const RollForm = ({ gameId }) => {
  const [pinsKnocked, setPinsKnocked] = useState(""); // Input for pins knocked

  const handleRecordRoll = async (event) => {
    event.preventDefault();
    try {
      await recordRoll(gameId, parseInt(pinsKnocked)); // Send roll data to API
      setPinsKnocked(""); // Clear input after submitting
    } catch (error) {
      console.error("Error recording roll:", error);
    }
  };

  return (
    <form onSubmit={handleRecordRoll}>
      <label>
        Pins knocked:
        <input
          type="number"
          value={pinsKnocked}
          onChange={(e) => setPinsKnocked(e.target.value)}
          min="0"
          max="10"
          required
        />
      </label>
      <button type="submit">Record Roll</button>
    </form>
  );
};

export default RollForm;
