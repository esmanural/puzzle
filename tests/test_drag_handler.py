"""Unit tests for DragHandler class"""

import unittest
import pygame
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece
from jigsaw_puzzle.services.drag_handler import DragHandler


class TestDragHandler(unittest.TestCase):
    """Unit tests for DragHandler class"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize pygame"""
        pygame.init()
    
    @classmethod
    def tearDownClass(cls):
        """Quit pygame"""
        pygame.quit()
    
    def setUp(self):
        """Create a new DragHandler for each test"""
        # Create simple pygame Surfaces for testing
        surface1 = pygame.Surface((50, 50))
        surface2 = pygame.Surface((50, 50))
        
        # Create 2 pieces
        self.pieces = [
            JigsawPiece(surface1, (0, 0), 0),
            JigsawPiece(surface2, (0, 1), 1)
        ]
        
        # Assign initial positions to pieces
        self.pieces[0].pixel_position = (100, 100)
        self.pieces[1].pixel_position = (200, 200)
        
        self.game_state = GameState(grid_size=(1, 2), pieces=self.pieces)
        self.drag_handler = DragHandler(self.game_state, snap_threshold=30)
    
    def test_initialization(self):
        """Test DragHandler initialization"""
        self.assertEqual(self.drag_handler.snap_threshold, 30)
        self.assertIsNone(self.drag_handler.dragged_piece)
        self.assertEqual(self.drag_handler.drag_offset, (0, 0))
    
    def test_start_drag(self):
        """Test starting a drag operation"""
        piece = self.pieces[0]
        mouse_pos = (110, 110)
        
        self.drag_handler.start_drag(piece, mouse_pos)
        
        self.assertEqual(self.drag_handler.dragged_piece, piece)
        self.assertTrue(piece.is_dragging)
        self.assertEqual(self.drag_handler.drag_offset, (10, 10))
        self.assertGreater(piece.z_index, 0)
    
    def test_start_drag_none_piece(self):
        """Test starting drag with None piece"""
        self.drag_handler.start_drag(None, (100, 100))
        self.assertIsNone(self.drag_handler.dragged_piece)
    
    def test_update_drag(self):
        """Test updating position during drag"""
        piece = self.pieces[0]
        self.drag_handler.start_drag(piece, (110, 110))
        
        # Move mouse
        self.drag_handler.update_drag((150, 150))
        
        # Piece position should be updated (offset applied)
        self.assertEqual(piece.pixel_position, (140, 140))
    
    def test_update_drag_no_dragged_piece(self):
        """Test update when no piece is dragged"""
        # Nothing should happen
        self.drag_handler.update_drag((150, 150))
        self.assertIsNone(self.drag_handler.dragged_piece)
    
    def test_end_drag(self):
        """Test ending a drag operation"""
        piece = self.pieces[0]
        self.drag_handler.start_drag(piece, (110, 110))
        
        result = self.drag_handler.end_drag()
        
        self.assertFalse(piece.is_dragging)
        self.assertIsNone(self.drag_handler.dragged_piece)
        self.assertEqual(self.drag_handler.drag_offset, (0, 0))
        self.assertIsInstance(result, bool)
    
    def test_end_drag_no_dragged_piece(self):
        """Test end drag when no piece is dragged"""
        result = self.drag_handler.end_drag()
        self.assertFalse(result)
    
    def test_check_snap_to_grid_within_threshold(self):
        """Test snap when distance is within threshold"""
        piece = self.pieces[0]
        piece.pixel_position = (100, 100)
        piece.target_pixel_position = (110, 110)  # ~14.14 pixels away
        
        result = self.drag_handler.check_snap_to_grid(piece)
        
        self.assertTrue(result)
        self.assertTrue(piece.is_placed)
        self.assertEqual(piece.pixel_position, (110, 110))
    
    def test_check_snap_to_grid_outside_threshold(self):
        """Test snap when distance is outside threshold"""
        piece = self.pieces[0]
        piece.pixel_position = (100, 100)
        piece.target_pixel_position = (200, 200)  # ~141.42 pixels away
        
        result = self.drag_handler.check_snap_to_grid(piece)
        
        self.assertFalse(result)
        self.assertFalse(piece.is_placed)
    
    def test_check_snap_to_grid_already_placed(self):
        """Test snap for already placed piece"""
        piece = self.pieces[0]
        piece.is_placed = True
        
        result = self.drag_handler.check_snap_to_grid(piece)
        
        self.assertFalse(result)
    
    def test_cancel_drag(self):
        """Test canceling a drag operation"""
        piece = self.pieces[0]
        self.drag_handler.start_drag(piece, (110, 110))
        
        self.drag_handler.cancel_drag()
        
        self.assertFalse(piece.is_dragging)
        self.assertIsNone(self.drag_handler.dragged_piece)
        self.assertEqual(self.drag_handler.drag_offset, (0, 0))
    
    def test_z_index_increment(self):
        """Test z-index increases on each drag"""
        piece1 = self.pieces[0]
        piece2 = self.pieces[1]
        
        self.drag_handler.start_drag(piece1, (100, 100))
        z1 = piece1.z_index
        self.drag_handler.end_drag()
        
        self.drag_handler.start_drag(piece2, (200, 200))
        z2 = piece2.z_index
        
        self.assertGreater(z2, z1)


if __name__ == '__main__':
    unittest.main()
