# Author: Christopher Vote
# GitHub username: cbourjaily
# Date: 6/6/25
# Description: This program implements the core structure of the Animal Game, a grid-based strategy game played on a
#              7x7 board. Players take turns moving animal-themed game pieces—-each with unique movement rules—-across
#              the board. The program includes object-oriented classes to represent game pieces, board squares,
#              directional  linkers, and game state. It supports turn-based play, movement validation, piece tracking,
#              and endgame detection between two players: Tangerine and Amethyst.

RESET = "\033[0m"
TANGERINE_COLOR = "\033[35m"  # Magenta
AMETHYST_COLOR = "\033[36m"   # Cyan

class DirectionalLinkers:
    """
    A modular component that encapsulates 8-directional movement logic.

    DirectionalLinkers are used by multiple classes to manage spatial relationships on the game board. Each
    GameSquare holds a DirectionalLinkers object to track its neighboring squares in all eight directions:
    up, down, left, right, up_left, up_right, down_left, and down_right.

    These linkers are initialized and connected during GameSquare instantiation. GameRow uses them for lateral linking
    during recursive row population. They are also utilized during GameBoard construction, enabling a fully navigable
    grid.

    GamePiece instances also utilize DirectionalLinkers to evaluate legal move paths based on their movement
    rules. This allows pieces to interpret the board spatially without needing global awareness.

    The AnimalGame engine ultimately leverages this structure to validate moves, detect captures, and enforce
    movement constraints in a clean, modular fashion.
    """

    def __init__(self):
        """
        Initializes all directional links to None. These will be assigned to neighboring GameSquare objects.
        """
        self._up = None
        self._down = None
        self._left = None
        self._right = None
        self._upper_left = None
        self._upper_right = None
        self._lower_left = None
        self._lower_right = None

    def get_up(self):
        """
        Returns the square directly above.

        :return: The GameSquare object above this one, or None if unlinked.
        """
        return self._up

    def get_down(self):
        """
        Returns the square directly below.

        :return: The GameSquare object below this one, or None if unlinked.
        """
        return self._down

    def get_left(self):
        """
        Returns the square directly left.

        :return: The GameSquare object to the left, or None if unlinked.
        """
        return self._left

    def get_right(self):
        """
        Returns the square directly right.

        :return: The GameSquare object to the right, or None if unlinked.
        """
        return self._right

    def get_upper_left(self):
        """
        Returns the square to the upper-left.

        :return: The GameSquare object diagonally above and left, or None if unlinked.
        """
        return self._upper_left

    def get_upper_right(self):
        """
        Returns the square to the upper-right.

        :return: The GameSquare object diagonally above and right, or None if unlinked.
        """
        return self._upper_right

    def get_lower_left(self):
        """
        Returns the square to the lower-left.

        :return: The GameSquare object diagonally below and left, or None if unlinked.
        """
        return self._lower_left

    def get_lower_right(self):
        """
        Returns the square to the lower-right.

        :return: The GameSquare object diagonally below and right, or None if unlinked.
        """
        return self._lower_right

    def set_up(self, square):
        """
        Sets the square above.

        :param square: the GameSquare object to link in the uper-right direction.
        """
        self._up = square

    def set_down(self, square):
        """
        Sets the square below.

        :param square: the GameSquare object to link in the uper-right direction.
        """
        self._down = square

    def set_left(self, square):
        """
        Sets the square to the left.

        :param square: the GameSquare object to link in the uper-right direction.
        """
        self._left = square

    def set_right(self, square):
        """
        Sets the square to the right.

        :param square: the GameSquare object to link in the uper-right direction.
        """
        self._right = square

    def set_upper_left(self, square):
        """
        Sets the square to the upper-left.

        :param square: the GameSquare object to link in the uper-right direction.
        """
        self._upper_left = square

    def set_upper_right(self, square):
        """
        Sets the square to the upper-right.

        :param square: the GameSquare object to link in the uper-right direction.
        """
        self._upper_right = square

    def set_lower_left(self, square):
        """
        Sets the square to the lower-left.

        :param square: the GameSquare object to link in the uper-right direction.
        """
        self._lower_left = square

    def set_lower_right(self, square):
        """
        Sets the square to the lower-right.

        :param square: the GameSquare object to link in the uper-right direction.
        """
        self._lower_right = square


class GameSquare:
    """
    The GameSquare class represents the atomic units of the GameBoard. Each GameSquare is technically a graphical node.
    Each GameSquare has an index representing its relative position in a flattened 7×7 board layout. Index 0 maps to A1,
    index 6 to G1, index 7 to A2, and index 48 to G7.

    Each GameSquare also includes a label (A1 through G7) that corresponds directly to its index.

    The data member, self._data, stores the occupant data of a given square on a given turn. If a GamePiece is present
    on the GameSquare, the specific GamePiece object is recorded on self._data. If no GamePiece occupies the GameSquare,
    the self._data value is None.

    GameSquare objects initialize DirectionalLinkers objects by composition. The self._square_history attribute is a
    dictionary that maps turn numbers to the value of self._data at each turn. This records every piece that has
    occupied the square, enabling move history tracking or undo functionality.

    GameRow and GameBoard objects are composed of GameSquare objects. The logic of GameSquare objects is utilized by
    GamePiece objects to traverse the board and by the AnimalGame class to coordinate gameplay, resolve moves, and
    evaluate interactions by the game engine.
    """

    def __init__(self):
        """
        Creates a GameSquare object, which is a Node Abstract Data Type. Includes an index, label, data of square
        occupant, turn history record, and composition of DirectionalLinkers.
        """
        self._index = None
        self._label = None
        self._data = None
        self._square_history = {}
        self._linkers = DirectionalLinkers()

    def record_square_history(self, turn_number):
        """
        Records the piece occupying this square on the given turn.

        :param turn_number: The current turn number in the game.
        """
        self._square_history[turn_number] = self._data

    def linkers(self) -> DirectionalLinkers:
        """
        Returns the DirectionalLinkers object that holds references to adjacent GameSquares in all eight directions.

        :return: The DirectionalLinkers instance for this square.
        """
        return self._linkers

    def get_index(self) -> int:
        """
        Returns the numerical index of this square in the board’s flattened layout (0–48).

        :return: Integer index of the square.
        """
        return self._index

    def get_label(self) -> str:
        """
        Returns the geometric label of this square (e.g., 'A1', 'C5').

        :return: String label of the square.
        """
        return self._label

    def get_data(self):
        """
        Returns the current occupant of the square.

        :return: GamePiece occupying the square or None if unoccupied.
        """
        return self._data

    def get_square_history(self):
        """
        Returns the full move history for this square.

        :return: A dictionary mapping turn numbers to occupying GamePiece objects or None.
        """
        return self._square_history

    def get_history_entry(self, turn_number: int):
        """
        Returns the occupant data for this square at a specific turn.

        :param turn_number: Turn number to query.
        :return: GamePiece or None
        """
        return self._square_history.get(turn_number)

    def set_index(self, num: int):
        """
        Sets the index of this square in the board’s flattened layout.

        :param num: Integer index corresponding to square position.
        """
        self._index = num

    def set_label(self, new_label: str):
        """
        Sets the geometric label of this square.

        :param new_label: String representing board coordinates (e.g., 'D3').
        """
        self._label = new_label

    def set_data(self, new_data):
        """
        Sets the occupant of the square.

        :param new_data: Either a GamePiece object, or None if unoccupied.
        """
        self._data = new_data

class GameRow:
    """
    The GameRow class constructs a linear sequence of GameSquare objects, linked via directional references.
    It serves as an intermediate structure used by the GameBoard class to build rows during board generation.
    Each GameRow begins with a head GameSquare and recursively extends to the right.
    """
    def __init__(self):
        """
        Initializes an empty GameRow with a head initialized to None.
        """
        self._head = None

    def get_head(self) -> GameSquare:
        """
        Returns the head GameSquare of this row.

        :return: The head GameSquare object in this row.
        """
        return self._head

    def generate_row(self, row_length:int):
        """
        Initializes a row of GameSquare objects of specified length.
        This is the public interface for recursive row generation.

        :param row_length: The length of a row, measured by number of GameSquare objects used to create it.
        """
        self.generate_row_recursive(row_length)

    def generate_row_recursive(self, row_length:int, a_square=None):
        """
        Recursively builds a horizontal row of GameSquares, starting from the head.

        :param row_length: Remaining number of squares to create.
        :param current_square: The current GameSquare to extend from (None for head).
        """
        if row_length == 0:         # Base case
            return

        if self._head is None:
            self._head = GameSquare()
            self.generate_row_recursive(row_length - 1, self._head)
        else:
            if a_square.linkers().get_right() is None:
                a_square.linkers().set_right(GameSquare())
                self.generate_row_recursive(row_length - 1, a_square.linkers().get_right())


class GameBoard:
    """
    The GameBoard class represents a square grid of GameSquare objects, constructed to support 8-directional movement
    logic.

    Each square is connected to its neighbors using DirectionalLinkers, forming a navigable graph structure.

    The board is generated recursively using GameRow objects, and finalized by linking all GameSquares in all eight
    directions (up, down, left, right, and diagonals). GameBoard maintains lookup dictionaries for indexing
    and label access.
    """
    def __init__(self, board_size:int=7):
        """
        Initializes a GameBoard composed of GameRow objects forming a square grid.

        :param board_size: The number of squares per side (e.g., 7 for a 7×7 board).
        """
        self._anchor = None
        self._board_size = board_size
        self._index_to_label = {}
        self._label_to_index = {}
        self._index_to_square = {}
        self._label_to_square = {}
        self.board_constructor()    # Builds the board

    def get_anchor(self) -> GameSquare:
        """
        Returns the anchor GameSquare (bottom-left square, index 0, labeled 'A1').

        :return: The anchor GameSquare object of the board.
        """
        return self._anchor

    def get_index_to_label(self):
        """
        Returns the dictionary mapping indices to square labels (e.g., 0 -> 'A1').

        :return: Dictionary with index keys and label string values.
        """
        return self._index_to_label

    def get_label_to_index(self):
        """
        Returns the dictionary mapping square labels to indices (e.g., 'A1' -> 0).

        :return: Dictionary with label string keys and index integer values.
        """
        return self._label_to_index

    def get_index_to_square(self):
        """
        Returns the dictionary mapping indices to GameSquare objects.

        :return: Dictionary with index keys and GameSquare values.
        """
        return self._index_to_square

    def get_label_to_square(self):
        """
        Returns the dictionary mapping square labels to GameSquare objects.

        :return: Dictionary with label string keys and GameSquare values.
        """
        return self._label_to_square

    def board_constructor(self, previous_row_head = None, row_count: int = 0) -> None:
        """
        Recursively builds a square GameBoard row by row, linking each row vertically.

        Called during GameBoard initialization. Starts from the anchor square at A1 and builds upward.

        :param previous_row_head: The head GameSquare of the previously constructed row (used for vertical linking).
        :param row_count: The current row index being built; recursion ends when row_count == self._board_size.
        :return: None
        """
        if row_count == self._board_size:           # Base case.
            self.finalize_linkers()                 # Calls a helper function to set all directional linkers
            self.indexing_utility()                 # Calls a helper function to set indices and labels
            return

        row = GameRow()
        row.generate_row(self._board_size)
        current_row_head = row.get_head()

        if self._anchor is None:
            self._anchor = current_row_head

        if previous_row_head:
            lower = previous_row_head
            upper = current_row_head

            while lower is not None and upper is not None:
                lower.linkers().set_up(upper)
                upper.linkers().set_down(lower)
                lower = lower.linkers().get_right()
                upper = upper.linkers().get_right()

        self.board_constructor(current_row_head, row_count + 1)

    def finalize_linkers(self) -> None:
        """
        Finalizes directional connections between GameSquares after initial board construction.

        This method backfills any remaining directional linkers (left, down, diagonals) across the grid, ensuring each
        square has full 8-way linkage. Called by board_constructor once row generation is complete.
        """
        row_head = self._anchor
        while row_head is not None:
            current = row_head
            while current is not None:
                right = current.linkers().get_right()
                up = current.linkers().get_up()
                down = current.linkers().get_down()
                left = current.linkers().get_left()

                if right:
                    right.linkers().set_left(current)
                if up:
                    up.linkers().set_down(current)

                if up and up.linkers().get_left():
                    current.linkers().set_upper_left(up.linkers().get_left())
                if up and up.linkers().get_right():
                    current.linkers().set_upper_right(up.linkers().get_right())
                if down and down.linkers().get_left():
                    current.linkers().set_lower_left(down.linkers().get_left())
                if down and down.linkers().get_right():
                    current.linkers().set_lower_right(down.linkers().get_right())

                current = right
            row_head = row_head.linkers().get_up()


    def indexing_utility(self) -> None:
        """
        Assigns index and label metadata to all GameSquares on the board.

        This method is called during board construction. It assigns a unique index (e.g., 0–48) and a geometric label
        (e.g., A1–G7) to each GameSquare and stores these mappings in lookup dictionaries for fast access.
        """
        index = 0
        row_head = self._anchor
        row_number = 1

        while row_head is not None:
            current = row_head
            column_num = 0

            while current is not None:
                alpha_label = chr(0x41 + (column_num % 26))     # ASCII: 0x41 = 'A'
                label = f"{alpha_label}{row_number}"

                current.set_index(index)
                current.set_label(label)

                self._index_to_label[index] = label
                self._label_to_index[label] = index
                self._index_to_square[index] = current
                self._label_to_square[label] = current

                current = current.linkers().get_right()
                index += 1
                column_num += 1

            row_head = row_head.linkers().get_up()
            row_number += 1


class GamePiece:
    """
    Parent class for all animal game pieces. Encapsulates movement logic and tracking info.
    """
    def __init__(self, direction: str, distance: int, locomotion: str):
        """
        Initializes a GamePiece with movement capabilities, internal move tracking and index of pieces.

        :param direction: The allowed direction of movement ('orthogonal' or 'diagonal').
        :param distance: The maximum number of squares this piece can move.
        :param locomotion: The movement type ('sliding' or 'jumping').
        """
        self._piece_index = 0
        self._board_data = None
        self._current_square = None
        self._color = None
        self._move_history: dict[int, str] = {}
        self._direction = direction
        self._distance = distance
        self._locomotion = locomotion
        self._linkers = DirectionalLinkers()

    def validate_move(self, from_label, to_label):
        """
        Placeholder movement validator for GamePiece.
        :param from_label: The starting square label (e.g., 'A3').
        :param to_label: The destination square label (e.g., 'B4').
        :return: False (from base class).
        """
        return False

    def get_piece_index(self) -> int:
        """
        Returns the assigned index of this piece (1–14), or 0 if unassigned.
        :return: The integer index of the piece.
        """
        return self._piece_index

    def set_piece_index(self, index: int) -> None:
        """
        Assigns a piece index (1–14). Used to track player affiliation and identity.
        :param index: The index to assign.
        """
        self._piece_index = index

    def get_board_data(self):
        """
        returns the current data for the GameBoard.
        ret: The current board
        """
        return self._board_data

    def set_board_data(self, board):
        """
        Updates the gameboard data
        :param board: Current GameBoard
        """
        self._board_data = board

    def get_color(self):
        """
        Returns the color of a GamePiece object.
        """
        return self._color

    def set_color(self, color):
        """
        Sets the color of a GamePiece object.
        :param color: The color being assigned to the piece.
        """
        self._color = color

    def get_current_square(self) -> GameSquare:
        """
        Returns the current GameSquare this piece occupies.

        :return: The GameSquare object where the piece is currently located.
        """
        return self._current_square

    def set_current_square(self, square: GameSquare) -> None:
        """
        Sets the current GameSquare this piece occupies.

        :param square: A GameSquare object representing the piece’s current location.
        """
        self._current_square = square

    def record_move_history(self, turn: int, square_label: str) -> None:
        """
        Records the square label this piece moved to on the given turn.

        :param turn: Current turn number.
        :param square_label: Label of the square (e.g., 'A3').
        """
        self._move_history[turn] = square_label

    def get_move_history(self):
        """
        Returns the move history of the piece.

        :return: A dictionary mapping turn numbers to square labels (e.g., {3: 'C4'}).
        """
        return self._move_history

    def get_direction(self) -> str:
        """
        Returns the direction of movement for this piece.

        :return: A string indicating the direction (e.g., 'orthogonal', 'diagonal').
        """
        return self._direction

    def get_distance(self) -> int:
        """
        Returns the maximum distance this piece can move.

        :return: An integer representing the number of squares the piece may travel in one move.
        """
        return self._distance

    def get_locomotion(self) -> str:
        """
        Returns the locomotion type of the piece.

        :return: A string indicating how the piece moves (e.g., 'sliding', 'jumping').
        """
        return self._locomotion

    def get_class_name(self) -> str:
        """
        Returns the class name of the piece as a string.

        :return: The name of the class (e.g., 'Chinchilla', 'Wombat').
        """
        return self.__class__.__name__


class Chinchilla(GamePiece):
    """
    Subclass of GamePiece.
    Move Direction: diagnal; Distance: 1; Movement: sliding; Starting Positions: A & G
    """
    def __init__(self):
        super().__init__(direction="diagonal", distance=1, locomotion="sliding")

    def validate_move(self, from_label, to_label):
        """
        Validates movements based on the Chinchilla GamePiece object's logic.
        :param from_label: The starting square label (e.g., 'A7').
        :param to_label: The destination square label (e.g., 'B6').
        :return: False if invalid, otherwise None
        """
        valid_moves_set = set()
        board = self._board_data
        from_square = board.get_label_to_square()[from_label]
        to_square = board.get_label_to_square()[to_label]

        if from_square.linkers().get_left() is not None:
            left = from_square.linkers().get_left()
            valid_moves_set.add(left)
        if from_square.linkers().get_right() is not None:
            right = from_square.linkers().get_right()
            valid_moves_set.add(right)
        if from_square.linkers().get_up() is not None:
            up = from_square.linkers().get_up()
            valid_moves_set.add(up)
        if from_square.linkers().get_down() is not None:
            down = from_square.linkers().get_down()
            valid_moves_set.add(down)
        if from_square.linkers().get_upper_left() is not None:
            upper_left = from_square.linkers().get_upper_left()
            valid_moves_set.add(upper_left)
        if from_square.linkers().get_upper_right() is not None:
            upper_right = from_square.linkers().get_upper_right()
            valid_moves_set.add(upper_right)
        if from_square.linkers().get_lower_left() is not None:
            lower_left = from_square.linkers().get_lower_left()
            valid_moves_set.add(lower_left)
        if from_square.linkers().get_lower_right() is not None:
            lower_right = from_square.linkers().get_lower_right()
            valid_moves_set.add(lower_right)
        if to_square not in valid_moves_set:
            return False
        return True

class Wombat(GamePiece):
    """
    Subclass of GamePiece.
    Move Direction: orthogonal; Distance: 4; Movement: jumping; Starting Positions: B & F
    """
    def __init__(self):
        super().__init__(direction="orthogonal", distance=4, locomotion="jumping")

    def validate_move(self, from_label, to_label):
        """
        Validates movements based on the Wombat GamePiece object's logic.
        :param from_label: The starting square label (e.g., 'A5').
        :param to_label: The destination square label (e.g., 'D5').
        :return: False if invalid, otherwise None
        """
        board = self._board_data
        from_square = board.get_label_to_square()[from_label]
        to_square = board.get_label_to_square()[to_label]
        valid_moves_set = set()

        if from_square.linkers().get_upper_left() is not None:
            upper_left = from_square.linkers().get_upper_left()
            valid_moves_set.add(upper_left)
        if from_square.linkers().get_upper_right() is not None:
            upper_right = from_square.linkers().get_upper_right()
            valid_moves_set.add(upper_right)
        if from_square.linkers().get_lower_left() is not None:
            lower_left = from_square.linkers().get_lower_left()
            valid_moves_set.add(lower_left)
        if from_square.linkers().get_lower_right() is not None:
            lower_right = from_square.linkers().get_lower_right()
            valid_moves_set.add(lower_right)

        left1 = from_square.linkers().get_left()
        if left1:
            left2 = left1.linkers().get_left()
            if left2:
                left3 = left2.linkers().get_left()
                if left3:
                    left4 = left3.linkers().get_left()
                    if left4:
                        valid_moves_set.add(left4)

        right1 = from_square.linkers().get_right()
        if right1:
            right2 = right1.linkers().get_right()
            if right2:
                right3 = right2.linkers().get_right()
                if right3:
                    right4 = right3.linkers().get_right()
                    if right4:
                        valid_moves_set.add(right4)

        up1 = from_square.linkers().get_up()
        if up1:
            up2 = up1.linkers().get_up()
            if up2:
                up3 = up2.linkers().get_up()
                if up3:
                    up4 = up3.linkers().get_up()
                    if up4:
                        valid_moves_set.add(up4)

        down1 = from_square.linkers().get_down()
        if down1:
            down2 = down1.linkers().get_down()
            if down2:
                down3 = down2.linkers().get_down()
                if down3:
                    down4 = down3.linkers().get_down()
                    if down4:
                        valid_moves_set.add(down4)

        return to_square in valid_moves_set

class Emu(GamePiece):
    """
    Subclass of GamePiece.

    As an orthogonal sliding piece with distance 3, the Emu must deal with situations in which another GamePiece,
    either friend or foe, is in the path of their attempted movement. In the former case, the move is False, while
    in the case of a foe, the Emu captures the piece and remains in the square. This case is handled recursively by
    calling make_move() with an updated GameSquare() label for the to_label parameter.

    Move Direction: orthogonal; Distance: 3; Movement: sliding; Starting Positions: C & E
    """
    def __init__(self):
        super().__init__(direction="orthogonal", distance=3, locomotion="sliding")

    def validate_move(self, from_label, to_label):
        """
        Validates movements based on the Emu GamePiece object's logic.
        :param from_label: The starting square label (e.g., 'A5').
        :param to_label: The destination square label (e.g., 'D5').
        :return: False if invalid, otherwise None
        """

        valid_moves_set = set()
        board = self._board_data
        from_square = board.get_label_to_square()[from_label]
        to_square = board.get_label_to_square()[to_label]

        if from_square.linkers().get_upper_left() is not None:
            upper_left = from_square.linkers().get_upper_left()
            valid_moves_set.add(upper_left)
        if from_square.linkers().get_upper_right() is not None:
            upper_right = from_square.linkers().get_upper_right()
            valid_moves_set.add(upper_right)
        if from_square.linkers().get_lower_left() is not None:
            lower_left = from_square.linkers().get_lower_left()
            valid_moves_set.add(lower_left)
        if from_square.linkers().get_lower_right() is not None:
            lower_right = from_square.linkers().get_lower_right()
            valid_moves_set.add(lower_right)

        left1 = from_square.linkers().get_left()
        if left1:
            valid_moves_set.add(left1)
            left2 = left1.linkers().get_left()
            if left2:
                valid_moves_set.add(left2)
                left3 = left2.linkers().get_left()
                if left3:
                    valid_moves_set.add(left3)

        right1 = from_square.linkers().get_right()
        if right1:
            valid_moves_set.add(right1)
            right2 = right1.linkers().get_right()
            if right2:
                valid_moves_set.add(right2)
                right3 = right2.linkers().get_right()
                if right3:
                    valid_moves_set.add(right3)

        up1 = from_square.linkers().get_up()
        if up1:
            valid_moves_set.add(up1)
            up2 = up1.linkers().get_up()
            if up2:
                valid_moves_set.add(up2)
                up3 = up2.linkers().get_up()
                if up3:
                    valid_moves_set.add(up3)

        down1 = from_square.linkers().get_down()
        if down1:
            valid_moves_set.add(down1)
            down2 = down1.linkers().get_down()
            if down2:
                valid_moves_set.add(down2)
                down3 = down2.linkers().get_down()
                if down3:
                    valid_moves_set.add(down3)

        if to_square not in valid_moves_set:
            return False
        result = self.emu_slide_check(from_label, to_label)
        if result is True:
            return True
        return result

    def emu_slide_check(self, from_label, to_label):
        """
        This function is specific to the sliding movement of the Emu piece, to detect situations in which another
        piece is in the path of a moving Emu piece. If the piece in the path is friendly, it is an invalid move. If
        the piece is a foe, the moving Emu piece captures the enemy piece and ends its turn on the spot.
        :param from_label: The starting square label (e.g., 'A5').
        :param to_label: The destination square label (e.g., 'D5').
        """

        piece_index = self._piece_index
        from_index = self._board_data.get_label_to_index()[from_label]
        to_index = self._board_data.get_label_to_index()[to_label]
        if abs(to_index - from_index) not in (1, 2, 3, 6, 7, 8, 14, 21):
            return False
        if to_index - from_index in (3, 2):                 # i.e., 27 - 24 or 26 - 24      (right)
            right_square = self._board_data.get_index_to_square()[from_index+1]
            if right_square.get_data() is not None:
                if self.is_enemy(right_square):
                    return 'CHAIN_TO_' + right_square.get_label()
                return False

        if to_index - from_index in (-3, -2):                 # i.e., 21 - 24 or 21 - 23    (left)
            left_square = self._board_data.get_index_to_square()[from_index-1]
            if left_square.get_data() is not None:
                if self.is_enemy(left_square):
                    return 'CHAIN_TO_' + left_square.get_label()
                return False

        if to_index - from_index in (21, 14):               # i.e., 45 - 24 or 38 - 24      (above)
            above_square = self._board_data.get_index_to_square()[from_index+7]
            if above_square.get_data() is not None:
                if self.is_enemy(above_square):
                    return 'CHAIN_TO_' + above_square.get_label()
                return False

        if to_index - from_index in (-21, -14):             # i.e., 3 - 24 or 10 - 24       (below)
            below_square = self._board_data.get_index_to_square()[from_index-7]
            if below_square.get_data() is not None:
                if self.is_enemy(below_square):
                    return 'CHAIN_TO_' + below_square.get_label()
                return False

        if to_index - from_index == 3:                      # i.e., 27 - 24                 (two_right)
            two_right_square = self._board_data.get_index_to_square()[from_index + 2]
            if two_right_square.get_data() is not None:
                if self.is_enemy(two_right_square):
                    return 'CHAIN_TO_' + two_right_square.get_label()
                return False

        if to_index - from_index == -3:                      # i.e., 21 - 24                 (two_left)
            two_left_square = self._board_data.get_index_to_square()[from_index - 2]
            if two_left_square.get_data() is not None:
                if self.is_enemy(two_left_square):
                    return 'CHAIN_TO_' + two_left_square.get_label()
                return False

        if to_index - from_index == 21:                      # i.e., 45 - 24                 (two_above)
            two_above_sqaure = self._board_data.get_index_to_square()[from_index + 14]
            if two_above_sqaure.get_data() is not None:
                if self.is_enemy(two_above_sqaure):
                    return 'CHAIN_TO_' + two_above_sqaure.get_label()
                return False

        if to_index - from_index == -21:                      # i.e., 3 - 24                 (two_below)
            two_below_square = self._board_data.get_index_to_square()[from_index - 14]
            if two_below_square.get_data() is not None:
                if self.is_enemy(two_below_square):
                    return 'CHAIN_TO_' + two_below_square.get_label()
                return False
        return True

    def is_enemy(self, to_square):
        """
        Helper function for validate_move to check logic for enemy pieces from indices
        :param to_square:
        :return: True if the piece in question is an enemy, otherwise False.
        """
        if to_square is None:
            return False
        if self._piece_index in (3, 5) and to_square.get_data().get_piece_index() in range(8, 15):
            return True
        elif self._piece_index in (10, 12) and to_square.get_data().get_piece_index() in range(1, 8):
            return True
        return False

class Cuttlefish(GamePiece):
    """
    Subclass of GamePiece.
    Move Direction: diagonal; Distance: 2; Movement: jumping; Starting Positions: D
    """
    def __init__(self):
        super().__init__(direction="diagonal", distance=2, locomotion="jumping")

    def validate_move(self, from_label, to_label):
        """
        Validates movements based on the Cuttlefish GamePiece object's logic.
        :param from_label: The starting square label (e.g., 'A3').
        :param to_label: The destination square label (e.g., 'B4').
        :return: False if invalid, otherwise None
        """
        valid_moves_set = set()
        board = self._board_data
        from_square = board.get_label_to_square()[from_label]
        to_square = board.get_label_to_square()[to_label]

        if from_square.linkers().get_left() is not None:
            left = from_square.linkers().get_left()
            valid_moves_set.add(left)
        if from_square.linkers().get_right() is not None:
            right = from_square.linkers().get_right()
            valid_moves_set.add(right)
        if from_square.linkers().get_up() is not None:
            up = from_square.linkers().get_up()
            valid_moves_set.add(up)
        if from_square.linkers().get_down() is not None:
            down = from_square.linkers().get_down()
            valid_moves_set.add(down)

        upper_left1 = from_square.linkers().get_upper_left()
        if upper_left1:
            upper_left2 = upper_left1.linkers().get_upper_left()
            if upper_left2:
                valid_moves_set.add(upper_left2)

        upper_right1 = from_square.linkers().get_upper_right()
        if upper_right1:
            upper_right2 = upper_right1.linkers().get_upper_right()
            if upper_right2:
                valid_moves_set.add(upper_right2)

        lower_left1 = from_square.linkers().get_lower_left()
        if lower_left1:
            lower_left2 = lower_left1.linkers().get_lower_left()
            if lower_left2:
                valid_moves_set.add(lower_left2)

        lower_right1 = from_square.linkers().get_lower_right()
        if lower_right1:
            lower_right2 = lower_right1.linkers().get_lower_right()
            if lower_right2:
                valid_moves_set.add(lower_right2)

        return to_square in valid_moves_set



class AnimalGame:
    """
    This class is the game engine, where the logic built in to the other classes comes to interact.
    """

    def __init__(self):
        """Launches the game when called."""
        TANGERINE = 'tangerine'
        AMETHYST = 'amethyst'
        self._board_size = 7
        self._board = GameBoard(self._board_size)
        self._turn = 1
        self._active_player = TANGERINE
        self._initialize_pieces()
        self._game_state = 'UNFINISHED'

    def get_game_state(self) -> str:
        """
        Returns the current game state.

        :return: One of 'UNFINISHED', 'TANGERINE_WON', or 'AMETHYST_WON'.
        """
        return self._game_state

    def get_game_board(self):
        """Returns the gameboard in it's present state."""
        return self._board

    def _initialize_pieces(self):
        """
        This class creates all the gamepiece objects

        :return: A dictionary of 14 GamePiece instances (7 per player).
        """
        piece_dic = {}
        for index in range(1, 15):
            piece_dic[index] = None

        for chin_index in [1, 7, 8, 14]:
            piece_dic[chin_index] = Chinchilla()
            piece_dic[chin_index].set_piece_index(chin_index)
        self.place_piece(piece_dic[1], 0)      # A1
        self.place_piece(piece_dic[7], 6)      # G1
        self.place_piece(piece_dic[8], 42)      # A7
        self.place_piece(piece_dic[14], 48)       # G7

        for wom_index in [2, 6, 9, 13]:
            piece_dic[wom_index] = Wombat()
            piece_dic[wom_index].set_piece_index(wom_index)
        self.place_piece(piece_dic[2], 1)      # B1
        self.place_piece(piece_dic[6], 5)       # F1
        self.place_piece(piece_dic[9], 43)      # B7
        self.place_piece(piece_dic[13], 47)     # F7

        for emu_index in [3, 5, 10, 12]:
            piece_dic[emu_index] = Emu()
            piece_dic[emu_index].set_piece_index(emu_index)
        self.place_piece(piece_dic[3], 2)      # C1
        self.place_piece(piece_dic[5], 4)      # E1
        self.place_piece(piece_dic[10], 44)     # C7
        self.place_piece(piece_dic[12], 46)     # E7

        for cuttle_index in [4, 11]:
            piece_dic[cuttle_index] = Cuttlefish()
            piece_dic[cuttle_index].set_piece_index(cuttle_index)
        self.place_piece(piece_dic[4], 3)      # D1
        self.place_piece(piece_dic[11], 45)     # D7

    def place_piece(self, piece: GamePiece, index: int) -> None:
        """
        Helper function alled by initialize_pieces.
        Places a piece on the board: sets the piece's square and updates the square's data.
        Links pieces to square, square to pieces, and board to pieces.
        :param piece: A GamePiece object
        :param index: The index of the GameSquare object where the piece will be placed
        """
        square = self._board.get_index_to_square()[index]
        piece.set_current_square(square)
        square.set_data(piece)
        piece.set_board_data(self._board)

        idx = piece.get_piece_index()
        if 1 <= idx <= 7:
            piece.set_color(TANGERINE_COLOR)
        elif 8 <= idx <= 14:
            piece.set_color(AMETHYST_COLOR)
        else:
            piece.set_color(RESET)


    def make_move(self, from_label:str, to_label:str):
        """
        Returns False if the move is not legal:
        1. the square moved from does not contain a piece
        2. The piece cannot legally move to the indicated taget square
        3. If a friendly piece is in the path (or sliding pieces)
        4. The game has already been won.
        Otherwise, makes the move, updates whose turn it is, and returns True.

        Updates current_turn, updates the state of the board, updates game_state, updates catalogues.

        :param from_label: The label of the square from which the piece is moving (e.g., 'A3').
        :param to_label: The label of the destination square.
        :return: True if the move is valid and executed; False otherwise.
        """
        from_label = from_label.upper()
        to_label = to_label.upper()

        legal_labels = tuple(self._board.get_label_to_square().keys())      # Check squares for legality.
        if from_label not in legal_labels or to_label not in legal_labels:
            return False
        from_square = self._board.get_label_to_square()[from_label]
        to_square = self._board.get_label_to_square()[to_label]
        if from_square.get_data() is None:
            return False

        moving_piece = from_square.get_data()
        if moving_piece.get_piece_index() not in range(1, 8) and self._turn % 2 == 1:
            return False
        if moving_piece.get_piece_index() not in range(8, 15) and self._turn % 2 == 0:
            return False

        move_validation = moving_piece.validate_move(from_label, to_label)      # validate_move
        if move_validation is False:
            return False

        if isinstance(move_validation, str) and move_validation.startswith('CHAIN_TO_'):
            next_label = move_validation.replace('CHAIN_TO_', '')
            to_square.set_data(moving_piece)
            from_square.set_data(None)
            return self.make_move(to_label, next_label)

        if to_square.get_data() is None:
            to_square.set_data(moving_piece)
            from_square.set_data(None)
            self._increment_turn()
            self.print_board()
            return True

        if from_square.get_data().get_piece_index() in range(1, 8):
            if self._turn % 2 == 0:
                return False
            if to_square.get_data().get_piece_index() not in range(1, 8):
                if to_square.get_data().get_piece_index() == 11:
                    to_square.set_data(from_square.get_data())
                    from_square.set_data(None)
                    self._game_state = 'TANGERINE_WON'
                    self.print_board()
                    return True
                else:
                    to_square.set_data(from_square.get_data())
                    from_square.set_data(None)
                    self._increment_turn()
                    self.print_board()
                    return True

        if from_square.get_data().get_piece_index() in range(8, 15):
            if self._turn % 2 == 1:
                return False
            if to_square.get_data().get_piece_index() not in range(8, 15):
                if to_square.get_data().get_piece_index() == 4:
                    to_square.set_data(from_square.get_data())
                    from_square.set_data(None)
                    self._game_state = 'AMETHYST_WON'
                    self.print_board()
                    return True
                else:
                    to_square.set_data(from_square.get_data())
                    from_square.set_data(None)
                    self._increment_turn()
                    self.print_board()
                    return True
        return False

    def _increment_turn(self):
        """
        This function is called during the make_move function in order to toggle between turns.
        """
        self._turn += 1
        if self._turn % 2 == 1:
            self._active_player = 'tangerine'
        else:
            self._active_player = 'amethyst'

    def print_board(self) -> None:
        """
        Prints the GameBoard in a formatted grid.

        Each GameSquare is shown with its label, index, and the name of its occupying GamePiece (or None).
        """
        rows = []
        row_head = self._board.get_anchor()
        while row_head is not None:
            rows.append(row_head)
            row_head = row_head.linkers().get_up()
        print("\n")
        print(f"It is {self._active_player.upper()}'s turn.                    Turn number {self._turn}")
        print("Current game state: " + self._game_state + "\n")
        print("Turn number " + str(self._turn) + "\n")

        print("\n" + "=" * (self._board_size * 24))

        for row in reversed(rows):
            current = row
            row_str = ""
            while current is not None:
                label = current.get_label()
                index = current.get_index()
                data = current.get_data()
                piece = data.get_class_name() if data else "None"
                row_str += f"| {label}:{index:2d} | {piece:<10} "
                current = current.linkers().get_right()

            print(row_str)
            row = row.linkers().get_up()
        print("=" * (self._board_size * 24) + "\n")

