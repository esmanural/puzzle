"""Unit tests for DragHandler class"""

import unittest
import pygame
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece
from jigsaw_puzzle.services.drag_handler import DragHandler


class TestDragHandler(unittest.TestCase):
    """DragHandler sınıfı için unit testler"""
    
    @classmethod
    def setUpClass(cls):
        """Pygame'i başlat"""
        pygame.init()
    
    @classmethod
    def tearDownClass(cls):
        """Pygame'i kapat"""
        pygame.quit()
    
    def setUp(self):
        """Her test için yeni bir DragHandler oluştur"""
        # Test için basit pygame Surface'ler oluştur
        surface1 = pygame.Surface((50, 50))
        surface2 = pygame.Surface((50, 50))
        
        # 2 parça oluştur
        self.pieces = [
            JigsawPiece(surface1, (0, 0), 0),
            JigsawPiece(surface2, (0, 1), 1)
        ]
        
        # Parçalara başlangıç pozisyonları ver
        self.pieces[0].pixel_position = (100, 100)
        self.pieces[1].pixel_position = (200, 200)
        
        self.game_state = GameState(grid_size=(1, 2), pieces=self.pieces)
        self.drag_handler = DragHandler(self.game_state, snap_threshold=30)
    
    def test_initialization(self):
        """DragHandler'ın doğru şekilde başlatıldığını test et"""
        self.assertEqual(self.drag_handler.snap_threshold, 30)
        self.assertIsNone(self.drag_handler.dragged_piece)
        self.assertEqual(self.drag_handler.drag_offset, (0, 0))
    
    def test_start_drag(self):
        """Sürükleme başlatma işlemini test et"""
        piece = self.pieces[0]
        mouse_pos = (110, 110)
        
        self.drag_handler.start_drag(piece, mouse_pos)
        
        self.assertEqual(self.drag_handler.dragged_piece, piece)
        self.assertTrue(piece.is_dragging)
        self.assertEqual(self.drag_handler.drag_offset, (10, 10))
        self.assertGreater(piece.z_index, 0)
    
    def test_start_drag_none_piece(self):
        """None parça ile sürükleme başlatma test et"""
        self.drag_handler.start_drag(None, (100, 100))
        self.assertIsNone(self.drag_handler.dragged_piece)
    
    def test_update_drag(self):
        """Sürükleme güncelleme işlemini test et"""
        piece = self.pieces[0]
        self.drag_handler.start_drag(piece, (110, 110))
        
        # Fareyi hareket ettir
        self.drag_handler.update_drag((150, 150))
        
        # Parçanın pozisyonu güncellenmiş olmalı (offset uygulanmış)
        self.assertEqual(piece.pixel_position, (140, 140))
    
    def test_update_drag_no_dragged_piece(self):
        """Sürüklenen parça yokken güncelleme test et"""
        # Hiçbir şey olmamalı
        self.drag_handler.update_drag((150, 150))
        self.assertIsNone(self.drag_handler.dragged_piece)
    
    def test_end_drag(self):
        """Sürükleme bitirme işlemini test et"""
        piece = self.pieces[0]
        self.drag_handler.start_drag(piece, (110, 110))
        
        result = self.drag_handler.end_drag()
        
        self.assertFalse(piece.is_dragging)
        self.assertIsNone(self.drag_handler.dragged_piece)
        self.assertEqual(self.drag_handler.drag_offset, (0, 0))
        self.assertIsInstance(result, bool)
    
    def test_end_drag_no_dragged_piece(self):
        """Sürüklenen parça yokken bitirme test et"""
        result = self.drag_handler.end_drag()
        self.assertFalse(result)
    
    def test_check_snap_to_grid_within_threshold(self):
        """Snap eşiği içinde olan parça için snap test et"""
        piece = self.pieces[0]
        piece.pixel_position = (100, 100)
        piece.target_pixel_position = (110, 110)  # 14.14 piksel uzakta
        
        result = self.drag_handler.check_snap_to_grid(piece)
        
        self.assertTrue(result)
        self.assertTrue(piece.is_placed)
        self.assertEqual(piece.pixel_position, (110, 110))
    
    def test_check_snap_to_grid_outside_threshold(self):
        """Snap eşiği dışında olan parça için snap test et"""
        piece = self.pieces[0]
        piece.pixel_position = (100, 100)
        piece.target_pixel_position = (200, 200)  # 141.42 piksel uzakta
        
        result = self.drag_handler.check_snap_to_grid(piece)
        
        self.assertFalse(result)
        self.assertFalse(piece.is_placed)
    
    def test_check_snap_to_grid_already_placed(self):
        """Zaten yerleştirilmiş parça için snap test et"""
        piece = self.pieces[0]
        piece.is_placed = True
        
        result = self.drag_handler.check_snap_to_grid(piece)
        
        self.assertFalse(result)
    
    def test_cancel_drag(self):
        """Sürükleme iptal etme işlemini test et"""
        piece = self.pieces[0]
        self.drag_handler.start_drag(piece, (110, 110))
        
        self.drag_handler.cancel_drag()
        
        self.assertFalse(piece.is_dragging)
        self.assertIsNone(self.drag_handler.dragged_piece)
        self.assertEqual(self.drag_handler.drag_offset, (0, 0))
    
    def test_z_index_increment(self):
        """Z-index'in her sürüklemede arttığını test et"""
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
