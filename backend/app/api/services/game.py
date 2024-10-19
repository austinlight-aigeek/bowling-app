from app.db.models import Roll, Game, Frame


class BowlingGame:
    """
    A class that represents the logic for a bowling game, including adding rolls,
    calculating scores, and handling frame management.

    Attributes:
        game (Game): The Game object representing the current game state.
        frames (List[Frame]): A list of frames (each with rolls) in the game.
        current_frame (int): The current frame index for the game.
    """

    def __init__(self, game):
        """
        Initialize the BowlingGame object with a given Game instance.

        This constructor sets up the current frame and initializes all 10 frames
        for a standard bowling game if they do not already exist.

        Args:
            game (Game): An instance of the Game model representing the current game state.
        """
        self.game = game
        self.current_frame = 0
        if not self.game.frames:
            for _ in range(10):  # Create 10 frames for a standard game
                frame = Frame(game_id=self.game.id)
                self.game.frames.append(frame)

    def add_roll(self, pins_knocked):
        """
        Add a roll to the current frame and manage frame transitions.

        This method adds a roll to the current frame and automatically handles
        the transition to the next frame based on the number of pins knocked down
        and whether it is a strike or a regular frame.

        Args:
            pins_knocked (int): The number of pins knocked down in this roll.

        Raises:
            ValueError: If the number of pins is invalid or if the frame exceeds its limit.
        """
        if pins_knocked > 10 or pins_knocked < 0:
            raise ValueError("Invalid roll: Number of pins knocked down must be between 0 and 10.")

        current_frame = self._get_current_frame()
        current_rolls = current_frame.rolls

        # Debug print to see the current frame and roll count
        print(f"Adding roll to frame {self.current_frame}, current rolls: {len(current_rolls)}")

        # Ensure that no more than two rolls can be added to frames 1-9
        if len(current_rolls) >= 2 and self.current_frame < 9:
            raise ValueError("Cannot add more than two rolls in a regular frame.")

        # Handle 10th frame differently (allowing extra rolls for strike/spare)
        if self.current_frame == 9:
            if len(current_rolls) == 2 and sum(roll.pins_knocked for roll in current_rolls) >= 10:
                pass  # Allow extra roll in the 10th frame if strike or spare
            elif len(current_rolls) >= 2:
                raise ValueError("No more rolls allowed in the 10th frame unless it's a spare or strike.")

        # Add the roll to the current frame
        roll = Roll(pins_knocked=pins_knocked, frame_id=current_frame.id)
        current_frame.rolls.append(roll)

        # Automatically advance to the next frame if needed
        if len(current_rolls) == 1 and current_rolls[0].pins_knocked == 10 and self.current_frame < 9:
            self.current_frame += 1
        elif len(current_rolls) == 2 and self.current_frame < 9:
            self.current_frame += 1

    def calculate_score(self):
        """
        Calculate the total score for the entire game.

        This method goes through each frame, calculates the score for the frame,
        and handles the special cases for strikes and spares by adding appropriate bonuses.

        Returns:
            int: The total score for the game.
        """
        total_score = 0
        for i, frame in enumerate(self.game.frames):
            frame_score = sum(roll.pins_knocked for roll in frame.rolls)

            # Handle strike
            if len(frame.rolls) == 1 and frame.rolls[0].pins_knocked == 10 and i < 9:
                frame_score += self._get_next_two_rolls(i)

            # Handle spare
            if len(frame.rolls) == 2 and sum(roll.pins_knocked for roll in frame.rolls) == 10 and i < 9:
                frame_score += self._get_next_roll(i)

            total_score += frame_score

        return total_score

    def _get_next_two_rolls(self, frame_index):
        """
        Retrieve the next two rolls after a strike for bonus scoring.

        Args:
            frame_index (int): The index of the current frame in which the strike occurred.

        Returns:
            int: The sum of the pins knocked down in the next two rolls.
        """
        next_two_rolls = 0
        if frame_index + 1 < len(self.game.frames):
            next_frame = self.game.frames[frame_index + 1]
            next_two_rolls += next_frame.rolls[0].pins_knocked
            if len(next_frame.rolls) > 1:
                next_two_rolls += next_frame.rolls[1].pins_knocked
            elif frame_index + 2 < len(self.game.frames):
                next_two_rolls += self.game.frames[frame_index + 2].rolls[0].pins_knocked
        return next_two_rolls

    def _get_next_roll(self, frame_index):
        """
        Retrieve the next roll after a spare for bonus scoring.

        Args:
            frame_index (int): The index of the current frame in which the spare occurred.

        Returns:
            int: The number of pins knocked down in the next roll.
        """
        if frame_index + 1 < len(self.game.frames):
            next_frame = self.game.frames[frame_index + 1]
            return next_frame.rolls[0].pins_knocked
        return 0

    def _get_current_frame(self):
        """
        Get the current active frame in the game.

        Raises:
            IndexError: If there are no more frames available.

        Returns:
            Frame: The current frame object.
        """
        if self.current_frame >= len(self.game.frames):
            raise IndexError("No more frames available in the game.")

        return self.game.frames[self.current_frame]

    def _is_strike(self, frame) -> bool:
        """
        Checks if the frame is a strike (all 10 pins knocked down in the first roll).

        Args:
            frame (Frame): The frame to check.

        Returns:
            bool: True if the frame is a strike, False otherwise.
        """
        return len(frame.rolls) == 1 and frame.rolls[0].pins_knocked == 10

    def _is_spare(self, frame) -> bool:
        """
        Checks if the frame is a spare (all 10 pins knocked down using both rolls).

        Args:
            frame (Frame): The frame to check.

        Returns:
            bool: True if the frame is a spare, False otherwise.
        """
        return len(frame.rolls) == 2 and sum(roll.pins_knocked for roll in frame.rolls) == 10

    def _frame_score(self, frame) -> int:
        """
        Calculates the score for a single frame.

        Args:
            frame (Frame): The frame to calculate the score for.

        Returns:
            int: The score for the frame.
        """
        return sum(roll.pins_knocked for roll in frame.rolls)

    def _strike_bonus(self, frame_index: int) -> int:
        """
        Calculates the bonus for a strike (the next two rolls after the strike).

        Args:
            frame_index (int): The index of the frame where the strike occurred.

        Returns:
            int: The strike bonus score.
        """
        next_rolls = self._get_next_two_rolls(frame_index)
        return sum(roll.pins_knocked for roll in next_rolls)

    def _spare_bonus(self, frame_index: int) -> int:
        """
        Calculates the bonus for a spare (the pins knocked down in the next roll).

        Args:
            frame_index (int): The index of the frame where the spare occurred.

        Returns:
            int: The spare bonus score.
        """
        next_rolls = self._get_next_roll(frame_index)
        return next_rolls[0].pins_knocked if next_rolls else 0

    def _handle_tenth_frame(self, pins_knocked: int):
        """
        Handles the special case for the 10th frame where players can get extra rolls in the case
        of a strike or spare.

        Args:
            pins_knocked (int): The number of pins knocked down in the current roll.

        Raises:
            ValueError: If an invalid roll is attempted in the 10th frame.
        """
        frame = self._get_current_frame()

        # Allow extra rolls in the 10th frame if a strike or spare is scored
        if len(frame.rolls) < 2 or (frame.rolls[0].pins_knocked == 10):
            frame.rolls.append(Roll(pins_knocked=pins_knocked))
        else:
            raise ValueError("Invalid roll in the 10th frame")
