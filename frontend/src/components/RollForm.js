import React, { useState } from "react";

const RollForm = ({ onSubmit }) => {
  const [pins, setPins] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(pins);
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
