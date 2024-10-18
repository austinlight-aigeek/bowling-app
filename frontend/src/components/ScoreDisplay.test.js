import { render, screen } from "@testing-library/react";
import ScoreDisplay from "./ScoreDisplay";

test("displays the correct score", () => {
  render(<ScoreDisplay score={150} />);

  // Check if the score is correctly displayed
  expect(screen.getByText(/current score: 150/i)).toBeInTheDocument();
});
