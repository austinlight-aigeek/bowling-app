import { render, screen, fireEvent } from "@testing-library/react";
import App from "./App";
import * as api from "./api"; // Mock API requests

jest.mock("./api"); // Mock the API module

test("starts a new game and records rolls", async () => {
  api.createGame.mockResolvedValue({ game_id: 1 });
  api.recordRoll.mockResolvedValue({});
  api.getScore.mockResolvedValue({ score: 20 });
  api.getSummary.mockResolvedValue({ summary: "Great game!" });

  await render(<App />); // Ensure render is awaited

  // Start a new game
  const startButton = screen.getByText(/start new game/i);
  await fireEvent.click(startButton); // Await click event

  // Assert that the game ID is displayed
  expect(await screen.findByText(/game id: 1/i)).toBeInTheDocument();

  // Enter a roll and record it
  const input = screen.getByPlaceholderText(/enter pins/i);
  await fireEvent.change(input, { target: { value: "5" } }); // Await input change
  await fireEvent.click(screen.getByText(/record roll/i)); // Await click event

  // Check that the score is updated
  expect(await screen.findByText(/current score: 20/i)).toBeInTheDocument();
});
