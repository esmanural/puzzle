"""Unit tests for GameState class"""

import unittest
import pygame
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece


class TestGameState(unittest.TestCase):
    """Unit tests for GameState class"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize pygame"""
        pygame.init()
    
    @classmethod
    def tearDownClass(cls):
        """Quit pygame"""
        pygame.quit()
    
    def setUp(self):
        """Create a new GameState for each test"""
        # Create simple pygame Surfaces for testing
        surface1 = pygame.Surface((50, 50))
        surface2 = pygame.Surface((50, 50))
        surface3 = pygame.Surface((50, 50))
        surface4 = pygame.Surface((50, 50))
        
        # Create 4 pieces for 2x2 grid
        self.pieces = [
            JigsawPiece(surface1, (0, 0), 0),
            JigsawPiece(surface2, (0, 1), 1),
            JigsawPiece(surface3, (1, 0), 2),
            JigsawPiece(surface4, (1, 1), 3)
        ]
        
        # Place all pieces correctly (for testing)
        for piece in self.pieces:
            piece.is_placed = True
        
        self.game_state = GameState(grid_size=(2, 2), pieces=self.pieces)
    
    def test_initialization(self):
        """Test GameState initialization"""
        self.assertEqual(self.game_state.grid_size, (2, 2))
        self.assertEqual(len(self.game_state.pieces), 4)
        self.assertIsNone(self.game_state.selected_piece)
        self.assertFalse(self.game_state.is_completed)
        self.assertEqual(self.game_state.move_count, 0)
        self.assertEqual(self.game_state.elapsed_time, 0.0)
    
    def test_get_piece_at_existing(self):
        """Finds piece at existing position"""
        # get_piece_at only finds placed pieces
        piece = self.game_state.get_piece_at((0, 0))
        self.assertIsNotNone(piece)
        self.assertEqual(piece.piece_id, 0)
    
    def test_get_piece_at_nonexisting(self):
        """Returns None for non-existing position"""
        piece = self.game_state.get_piece_at((5, 5))
        self.assertIsNone(piece)
    
    def test_elapsed_time(self):
        """Test elapsed time property"""
        self.assertEqual(self.game_state.elapsed_time, 0.0)
        self.game_state.elapsed_time = 10.5
        self.assertEqual(self.game_state.elapsed_time, 10.5)
    
    def test_check_completion_all_correct(self):
        """Returns True when all pieces are correct"""
        result = self.game_state.check_completion()
        self.assertTrue(result)
        self.assertTrue(self.game_state.is_completed)
    
    def test_check_completion_not_complete(self):
        """Returns False when pieces are incorrect"""
        # Mark one piece as not placed
        self.pieces[0].is_placed = False
        
        result = self.game_state.check_completion()
        self.assertFalse(result)
        self.assertFalse(self.game_state.is_completed)
    
    def test_completion_percentage_all_placed(self):
        """Returns 100% when all pieces are placed"""
        percentage = self.game_state.completion_percentage
        self.assertEqual(percentage, 100.0)
    
    def test_completion_percentage_partial(self):
        """Returns correct percentage for partial placement"""
        # Mark 2 pieces as not placed
        self.pieces[0].is_placed = False
        self.pieces[1].is_placed = False
        
        percentage = self.game_state.completion_percentage
        self.assertEqual(percentage, 50.0)  # 2/4 = 50%
    
    def test_completion_percentage_none_placed(self):
        """Returns 0% when no pieces are placed"""
        for piece in self.pieces:
            piece.is_placed = False
        
        percentage = self.game_state.completion_percentage
        self.assertEqual(percentage, 0.0)


if __name__ == '__main__':
    unittest.main()
