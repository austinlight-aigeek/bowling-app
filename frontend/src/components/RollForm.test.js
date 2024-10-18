import { render, screen, fireEvent } from "@testing-library/react";
import RollForm from "./RollForm";

test("submits roll with correct value", () => {
  const mockSubmit = jest.fn();
  render(<RollForm onSubmit={mockSubmit} />);

  // Find the input and the submit button
  const input = screen.getByPlaceholderText(/enter pins/i);
  const button = screen.getByRole("button", { name: /record roll/i });

  // Simulate typing into the input and clicking the button
  fireEvent.change(input, { target: { value: "7" } });
  fireEvent.click(button);

  // Assert that the mock function was called with the correct value
  expect(mockSubmit).toHaveBeenCalledWith("7");
});
