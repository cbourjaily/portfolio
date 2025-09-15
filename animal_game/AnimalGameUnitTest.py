# Author: Christopher Vote
# GitHub username: cbourjaily
# Date: 6/2/25
# Description: This file contains unit tests for testing all of the methods present in the AnamilGame program file.
#              Efforts were taken to have wide test coverage over a high propertion of data attributes, use cases, and
#              the like.



import unittest

from AnimalGame import (DirectionalLinkers, GameSquare, GameRow, GameBoard, GamePiece, Chinchilla, Wombat, Emu,
                        Cuttlefish, AnimalGame)

class TestDirectionalLinkers(unittest.TestCase):

    def test_linker_get_up(self):
        """Tests the get_up method in DirectionalLinkers, which should be initialized to None."""
        linkers = DirectionalLinkers()
        self.assertIs(linkers.get_up(), None)

    def test_linker_get_down(self):
        """Tests the get_down method in DirectionalLinkers, which should be initialized to None."""
        linkers = DirectionalLinkers()
        self.assertIs(linkers.get_down(), None)

    def test_linker_get_left(self):
        """Tests the get_left method in DirectionalLinkers, which should be initialized to None."""
        linkers = DirectionalLinkers()
        self.assertIs(linkers.get_left(), None)

    def test_linker_get_right(self):
        """Tests the get_right method in DirectionalLinkers, which should be initialized to None."""
        linkers = DirectionalLinkers()
        self.assertIs(linkers.get_right(), None)

    def test_linker_get_upper_left(self):
        """Tests the get_upper_left method in DirectionalLinkers, which should be initialized to None."""
        linkers = DirectionalLinkers()
        self.assertIs(linkers.get_upper_left(), None)

    def test_linker_get_upper_right(self):
        """Tests the get_upper_right method in DirectionalLinkers, which should be initialized to None."""
        linkers = DirectionalLinkers()
        self.assertIs(linkers.get_upper_right(), None)

    def test_linker_get_lower_left(self):
        """Tests the get_lower_left method in DirectionalLinkers, which should be initialized to None."""
        linkers = DirectionalLinkers()
        self.assertIs(linkers.get_lower_left(), None)

    def test_linker_get_lower_right(self):
        """Tests the get_lower_right method in DirectionalLinkers, which should be initialized to None."""
        linkers = DirectionalLinkers()
        self.assertIs(linkers.get_lower_right(), None)

    def test_set_up(self):
        """Tests the set_up method to ensure it correctly assigns the 'up' square."""
        linkers = DirectionalLinkers()
        test_square = GameSquare()
        linkers.set_up(test_square)
        self.assertIs(linkers.get_up(), test_square)

    def test_set_down(self):
        """Tests the set_down method to ensure it correctly assigns the 'down' square."""
        linkers = DirectionalLinkers()
        test_square = GameSquare()
        linkers.set_down(test_square)
        self.assertIs(linkers.get_down(), test_square)

    def test_set_left(self):
        """Tests the set_left method to ensure it correctly assigns the 'left' square."""
        linkers = DirectionalLinkers()
        test_square = GameSquare()
        linkers.set_left(test_square)
        self.assertIs(linkers.get_left(), test_square)

    def test_set_right(self):
        """Tests the set_right method to ensure it correctly assigns the 'right' square."""
        linkers = DirectionalLinkers()
        test_square = GameSquare()
        linkers.set_right(test_square)
        self.assertIs(linkers.get_right(), test_square)

    def test_set_upper_left(self):
        """Tests the set_up method to ensure it correctly assigns the 'upper_left' square."""
        linkers = DirectionalLinkers()
        test_square = GameSquare()
        linkers.set_upper_left(test_square)
        self.assertIs(linkers.get_upper_left(), test_square)

    def test_set_upper_right(self):
        """Tests the set_upper_right method to ensure it correctly assigns the 'upper_right' square."""
        linkers = DirectionalLinkers()
        test_square = GameSquare()
        linkers.set_upper_right(test_square)
        self.assertIs(linkers.get_upper_right(), test_square)

    def test_set_lower_left(self):
        """Tests the set_lower_left method to ensure it correctly assigns the 'lower_left' square."""
        linkers = DirectionalLinkers()
        test_square = GameSquare()
        linkers.set_lower_left(test_square)
        self.assertIs(linkers.get_lower_left(), test_square)

    def test_set_lower_right(self):
        """Tests the set_lower_right method to ensure it correctly assigns the 'lower_right' square."""
        linkers = DirectionalLinkers()
        test_square = GameSquare()
        linkers.set_lower_right(test_square)
        self.assertIs(linkers.get_lower_right(), test_square)


class TestGameSquare(unittest.TestCase):

    def test_record_square_history(self):
        """Tests that the GameSquare correctly records the occupying piece at a given turn."""
        test_square = GameSquare()
        test_piece = Chinchilla()
        test_square.set_data(test_piece)
        test_square.record_square_history(1)
        self.assertIs(test_square.get_square_history()[1], test_piece)

    def test_linkers(self):
        """Tests that the linkers are correctly initialized in the GameSquare objects"""
        square_1 = GameSquare()
        square_2 = GameSquare()
        square_1.linkers().set_lower_left(square_2)
        self.assertIs(square_1.linkers().get_lower_left(), square_2)

    def test_get_index(self):
        """Tests that a square's index is returned correctly."""
        a_square = GameSquare()
        a_square.set_index(23)
        self.assertIs(a_square.get_index(), 23)

    def test_get_label(self):
        """Tests that a square's label is returned correctly."""
        a_square = GameSquare()
        a_square.set_label("E5")
        self.assertIs(a_square.get_label(), "E5")

    def test_get_data(self):
        """Tests that the data attribute is successfully implemented and returned."""
        test_square = GameSquare()
        test_piece = Emu()
        test_square.set_data(test_piece)
        self.assertIs(test_square.get_data(), test_piece)

    def test_get_square_history(self):
        """Checks that the get_square_history method properly executes"""
        test_square = GameSquare()
        test_piece = Cuttlefish()
        test_square.set_data(test_piece)
        test_square.record_square_history(4)
        self.assertIs(test_square.get_square_history()[4], test_piece)

    def test_get_history_entry(self):
        """Tests the get_history_entry method, which returns data of square occupant for a specific turn."""
        test_square = GameSquare()
        test_piece = Cuttlefish()
        test_square.set_data(test_piece)
        test_square.record_square_history(4)
        self.assertIs(test_square.get_history_entry(4), test_piece)

    def test_set_index(self):
        """Tests that the set_index method is properly functioning."""
        a_square = GameSquare()
        a_square.set_index(24)
        self.assertEqual(a_square.get_index(), 24)

    def test_set_label(self):
        """Tests that the set_label method executes correctly."""
        a_square = GameSquare()
        a_square.set_label("G2")
        self.assertIs(a_square.get_label(), "G2")

    def test_set_data(self):
        """Tests that the set_data method properly executes."""
        test_square = GameSquare()
        test_piece = Wombat()
        test_square.set_data(test_piece)
        self.assertIs(test_square.get_data(), test_piece)


class TestGameRow(unittest.TestCase):

    def test_get_head(self):
        """Tests that the head of the row is properly returned."""
        a_row = GameRow()
        head = a_row.generate_row(7)
        self.assertIsInstance(a_row.get_head(), GameSquare)

    def test_generate_row(self):
        """Tests that the generate_row method generates rows successfully."""
        test_row = GameRow()
        test_row.generate_row(10)
        self.assertIsInstance(test_row, GameRow)


class TestGameBoard(unittest.TestCase):

    def test_get_anchor(self):
        """Tests that the get_anchor function successfully creates a GameSquare object at index 0"""
        board = GameBoard(7)
        anchor = board.get_anchor()
        index = anchor.get_index()
        self.assertEqual(index, 0)

    def test_get_index_to_label(self):
        """Tests that the get_index_to_label properly returns a dictionary mapping the labels to the indices."""
        board = GameBoard(7)
        index_to_label = board.get_index_to_label()
        self.assertEqual(index_to_label[48], "G7")

    def test_label_to_index(self):
        """Tests that the get_label_to_index function successfully returns a dictionary mapping the indices to the
        labels."""
        board = GameBoard(7)
        label_to_index = board.get_label_to_index()
        self.assertEqual(label_to_index["A1"], 0)

    def test_get_index_to_square(self):
        """Tests that the get_index_to_square function properly returns a dictionary of the GameSquare objects in the
        mapped to the indices. It does so by checking Index 0 against the anchor of the GameBoard (the anchor occurs at
        index 0)."""
        board = GameBoard(7)
        anchor = board.get_anchor()
        index_to_square = board.get_index_to_square()
        self.assertIs(index_to_square[0], anchor)

    def test_get_label_to_square(self):
        """Tests that the get_index_to_square function properly returns a dictionary of GameSquare objects mapped to
        the labels. It uses the anchor and linkers to get the square right of the anchor, and tests this against the
        expected label for that square."""
        board = GameBoard(7)
        right_of_anchor = board.get_anchor().linkers().get_right()
        label_right_of_anchor = right_of_anchor.get_label()

        label_to_square = board.get_label_to_square()
        self.assertEqual(label_right_of_anchor, "B1")

    def test_board_constructor(self):
        """Tests the function which recursively builds the gameboard."""
        game_board = GameBoard(20)
        anchor = game_board.get_anchor()
        anchor_right = anchor.linkers().get_right()
        self.assertIs(anchor_right.get_index(), 1)


    def test_finalize_linkers(self):
        """Tests the function that finalizes the linkers for the integrated GameSquare objects during GameBoard
        construction. It does so by mapping to the square at index 48, and retrieving the square to its left."""
        game_board = GameBoard(7)
        top_corner_square = game_board._index_to_square[48]
        left_of_corner_square = top_corner_square.linkers().get_left()
        self.assertEqual(left_of_corner_square.get_label(), 'F7')

    def test_indexing_utlity(self):
        """Tests the function that finalizes the indexing of the GameSquare objects on the GameBoard. It does so by
        checking some transactions for the dictionaries created by the function."""
        board = GameBoard(7)
        self.assertEqual(board.get_label_to_index()["B1"], 1)
        self.assertEqual(board.get_index_to_label()[8], "B2")
        self.assertIsInstance(board.get_label_to_square()["G3"], GameSquare)
        self.assertIs(board.get_index_to_square()[0], board.get_anchor())

class TestGamePiece(unittest.TestCase):

    def test_get_current_square(self):
        """Tests the function for returning the current square occupied by a GamePiece object."""
        board = GameBoard(7)
        piece = Chinchilla()
        anchor = board.get_anchor()
        piece.set_current_square(anchor)
        piece_occupied_square_index = piece.get_current_square().get_index()
        anchor_index = anchor.get_index()
        self.assertEqual(piece_occupied_square_index, anchor_index)

    def test_set_current_square(self):
        """Tests that the set_current_square successfully sets the piece for a square."""
        board = GameBoard(7)
        piece = Wombat()
        anchor_upper_right = board.get_anchor().linkers().get_upper_right()
        piece.set_current_square(anchor_upper_right)
        piece_occupied_square_label = piece.get_current_square().get_label()
        square_label = anchor_upper_right.get_label()
        self.assertEqual(piece_occupied_square_label, square_label)

    def test_get_piece_index(self):
        """Tests the get_index function for GamePiece objects."""
        piece = Chinchilla()
        piece.set_piece_index(14)
        self.assertEqual(piece.get_piece_index(), 14)

    def test_set_piece_index(self):
        """Tests that the set_piece_index function is properly working, over the course of multiple calls."""
        piece = Cuttlefish()
        piece.set_piece_index(1)
        piece.set_piece_index(5)
        self.assertEqual(piece.get_piece_index(), 5)

    def test_record_move_history(self):
        """Tests that the function for recording the move history of a piece is operational."""
        piece = Emu()
        piece.record_move_history(1, "A1")
        self.assertEqual(piece.get_move_history()[1], "A1")

    def test_get_move_history(self):
        """Tests the functionality of the get_move_history function, with multiple dictionary entries by
        record_move_history."""
        piece = Emu()
        piece.record_move_history(1, "A1")
        piece.record_move_history(2, "B1")
        self.assertEqual(piece.get_move_history()[2], "B1")

    def test_get_direction(self):
        """Tests that the function successfully returns the movement type for a given piece
        (orthogonal or diagonal)."""
        chinchilla = Chinchilla()
        self.assertEqual(chinchilla.get_direction(), "diagonal")

    def test_get_locomotion(self):
        """Tests that the function successfully returns the locomotion type for a given piece (sliding or jumping)."""
        wombat = Wombat()
        self.assertEqual(wombat.get_locomotion(), "jumping")

    def test_get_class_name(self):
        """Tests that the function for return the class name successfully executes."""
        emu = Emu()
        self.assertEqual(emu.get_class_name(), "Emu")

class TestChinchilla(unittest.TestCase):

    def test_get_class_name(self):
        """Tests that the get_class_name function successfully returns the name of the class for the GamePiece
        object."""
        chinchilla = Chinchilla()
        self.assertEqual(chinchilla.get_class_name(), "Chinchilla")

    def test_chinchilla_direction(self):
        """Tests the initialized attribute of direction for the GamePiece subclass Chinchilla"""
        chinchilla = Chinchilla()
        self.assertEqual(chinchilla.get_direction(), 'diagonal')

    def test_chinchilla_distance(self):
        """Tests the initialized attribute of distance for the GamePiece sublass Chinchilla"""
        chinchilla = Chinchilla()
        self.assertEqual(chinchilla.get_distance(), 1)

    def test_chinchilla_locomotion(self):
        """Tests the initialized attribute of locomotion for the GamePiece subclass Chinchilla"""
        chinchilla = Chinchilla()
        self.assertEqual(chinchilla.get_locomotion(), 'sliding')


class TestWombat(unittest.TestCase):

    def test_wombat_direction(self):
        """Tests the initialized attribute of direction for the GamePiece subclass Wombat"""
        wombat = Wombat()
        self.assertIs(wombat.get_direction(), 'orthogonal')

    def test_wombat_distance(self):
        """Tests the initialized attribute of distance for the GamePiece sublass Wombat"""
        wombat = Wombat()
        self.assertIs(wombat.get_distance(), 4)

    def test_wombat_locomotion(self):
        """Tests the initialized attribute of locomotion for the GamePiece subclass Wombat"""
        wombat = Wombat()
        self.assertIs(wombat.get_locomotion(), 'jumping')


class TestEmu(unittest.TestCase):

    def test_Emu_direction(self):
        """Tests the initialized attribute of direction for the GamePiece subclass Emu"""
        emu = Emu()
        self.assertIs(emu.get_direction(), 'orthogonal')

    def test_emu_distance(self):
        """Tests the initialized attribute of distance for the GamePiece sublass Emu"""
        emu = Emu()
        self.assertIs(emu.get_distance(), 3)

    def test_emu_locomotion(self):
        """Tests the initialized attribute of locomotion for the GamePiece subclass Emu"""
        emu = Emu()
        self.assertIs(emu.get_locomotion(), 'sliding')


class TestCuttlefish(unittest.TestCase):

    def test_cuttlefish_direction(self):
        """Tests the initialized attribute of direction for the GamePiece subclass Cuttlefish"""
        cuttlefish = Cuttlefish()
        self.assertIs(cuttlefish.get_direction(), 'diagonal')

    def test_cuttlefish_distance(self):
        """Tests the initialized attribute of distance for the GamePiece sublass Cuttlefish"""
        cuttlefish = Cuttlefish()
        self.assertIs(cuttlefish.get_distance(), 2)

    def test_cuttlefish_locomotion(self):
        """Tests the initialized attribute of locomotion for the GamePiece subclass Cuttlefish"""
        cuttlefish = Cuttlefish()
        self.assertIs(cuttlefish.get_locomotion(), 'jumping')


class TestAnimalGame(unittest.TestCase):

    def test_initialize_pieces(self):
        """Tests the function which creates the GamePiece objects and indexes them."""
        game = AnimalGame()
        board = game._board
        anchor = board.get_anchor()
        piece = anchor.get_data()
        self.assertEqual(piece.get_class_name(), "Chinchilla")

    # def test_get_game_state(self):
    #     """Tests the function for checking the state of the game."""
    #     game = AnimalGame()
    #     self.assertIs(game.get_game_state(), 'UNFINISHED')
    #
    # def test_make_move(self):
    #     """Tests that the make_move function operates as expected."""
    #     game = AnimalGame()
    #     game.make_move("A1", "B2")
    #     moved_piece = game._board.get_label_to_square()["B2"].get_data()
    #     self.assertIsInstance(moved_piece, Chinchilla)



if __name__ == '__main__':
    unittest.main()