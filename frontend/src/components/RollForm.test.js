import { render, screen, fireEvent } from "@testing-library/react";
import RollForm from "./RollForm";

test("displays alert for invalid pin count", () => {
  const mockSubmit = jest.fn();
  global.alert = jest.fn(); // Mock alert
  render(<RollForm onSubmit={mockSubmit} />);

  const input = screen.getByPlaceholderText(/enter pins/i);
  const button = screen.getByRole("button", { name: /record roll/i });

  fireEvent.change(input, { target: { value: "11" } }); // Invalid pin count
  fireEvent.click(button);

  // Assert that the alert is shown
  expect(global.alert).toHaveBeenCalledWith(
    "Please enter a valid number between 0 and 10."
  );
  expect(mockSubmit).not.toHaveBeenCalled();
});
