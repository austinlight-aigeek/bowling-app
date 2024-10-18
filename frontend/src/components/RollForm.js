import React, { useState } from "react";

const RollForm = ({ onSubmit }) => {
  const [pins, setPins] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const parsedPins = parseInt(pins, 10);
    if (isNaN(parsedPins) || parsedPins < 0 || parsedPins > 10) {
      alert("Please enter a valid number between 0 and 10.");
      return;
    }
    onSubmit(parsedPins);
    setPins("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="number"
        value={pins}
        onChange={(e) => setPins(e.target.value)}
        placeholder="Enter pins"
      />
      <button type="submit">Record Roll</button>
    </form>
  );
};

export default RollForm;
