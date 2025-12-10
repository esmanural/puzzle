"""Unit tests for JigsawLogic class"""

import unittest
import pygame
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece
from jigsaw_puzzle.services.jigsaw_logic import JigsawLogic


class TestJigsawLogic(unittest.TestCase):
    """Unit tests for JigsawLogic class"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize pygame"""
        pygame.init()
    
    @classmethod
    def tearDownClass(cls):
        """Quit pygame"""
        pygame.quit()
    
    def setUp(self):
        """Create a new JigsawLogic for each test"""
        # Create simple pygame Surfaces for testing
        surface1 = pygame.Surface((50, 50))
        surface2 = pygame.Surface((50, 50))
        surface3 = pygame.Surface((50, 50))
        surface4 = pygame.Surface((50, 50))
        
        # Create 4 pieces for a 2x2 grid
        self.pieces = [
            JigsawPiece(surface1, (0, 0), 0),
            JigsawPiece(surface2, (0, 1), 1),
            JigsawPiece(surface3, (1, 0), 2),
            JigsawPiece(surface4, (1, 1), 3)
        ]
        
        self.game_state = GameState(grid_size=(2, 2), pieces=self.pieces)
        self.logic = JigsawLogic(self.game_state)
    
    def test_initialization(self):
        """Test JigsawLogic initialization"""
        self.assertIsNotNone(self.logic.game_state)
        self.assertIsNotNone(self.logic.drag_handler)
    
    def test_scatter_pieces(self):
        """Pieces are scattered into the PiecePool"""
        piece_pool = pygame.Rect(100, 100, 400, 400)
        
        self.logic.scatter_pieces(piece_pool)
        
        # All pieces should have pixel_position set
        for piece in self.pieces:
            self.assertIsNotNone(piece.pixel_position)
            
            # Positions should be within piece_pool
            x, y = piece.pixel_position
            self.assertGreaterEqual(x, piece_pool.x)
            self.assertGreaterEqual(y, piece_pool.y)
            self.assertLessEqual(x, piece_pool.x + piece_pool.width)
            self.assertLessEqual(y, piece_pool.y + piece_pool.height)
    
    def test_get_piece_at_position_found(self):
        """Finds the piece under the mouse position"""
        # Assign positions to pieces
        self.pieces[0].pixel_position = (100, 100)
        self.pieces[1].pixel_position = (200, 200)
        
        # Click on the first piece
        piece = self.logic.get_piece_at_position((110, 110))
        
        self.assertIsNotNone(piece)
        self.assertEqual(piece.piece_id, 0)
    
    def test_get_piece_at_position_not_found(self):
        """Returns None when no piece under mouse position"""
        # Assign positions to pieces
        self.pieces[0].pixel_position = (100, 100)
        
        # Click on an empty area
        piece = self.logic.get_piece_at_position((500, 500))
        
        self.assertIsNone(piece)
    
    def test_get_piece_at_position_z_index_priority(self):
        """Finds the topmost piece by z-index"""
        # Place two pieces overlapping
        self.pieces[0].pixel_position = (100, 100)
        self.pieces[0].z_index = 1
        
        self.pieces[1].pixel_position = (100, 100)
        self.pieces[1].z_index = 2
        
        # Click on the same position
        piece = self.logic.get_piece_at_position((110, 110))
        
        # Piece with higher z-index should be selected
        self.assertEqual(piece.piece_id, 1)
    
    def test_is_puzzle_solved_true(self):
        """Returns True when all pieces are placed"""
        # Place all pieces
        for piece in self.pieces:
            piece.is_placed = True
        
        result = self.logic.is_puzzle_solved()
        self.assertTrue(result)
    
    def test_is_puzzle_solved_false(self):
        """Returns False when pieces are not placed"""
        # Do not place pieces
        for piece in self.pieces:
            piece.is_placed = False
        
        result = self.logic.is_puzzle_solved()
        self.assertFalse(result)
    
    def test_get_completion_percentage_all_placed(self):
        """Returns 100% when all pieces are placed"""
        for piece in self.pieces:
            piece.is_placed = True
        
        percentage = self.logic.get_completion_percentage()
        self.assertEqual(percentage, 100.0)
    
    def test_get_completion_percentage_partial(self):
        """Returns correct percentage for partial placement"""
        # Place 2 pieces
        self.pieces[0].is_placed = True
        self.pieces[1].is_placed = True
        self.pieces[2].is_placed = False
        self.pieces[3].is_placed = False
        
        percentage = self.logic.get_completion_percentage()
        self.assertEqual(percentage, 50.0)
    
    def test_get_completion_percentage_none_placed(self):
        """Returns 0% when no pieces are placed"""
        for piece in self.pieces:
            piece.is_placed = False
        
        percentage = self.logic.get_completion_percentage()
        self.assertEqual(percentage, 0.0)


if __name__ == '__main__':
    unittest.main()
