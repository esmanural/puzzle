"""Unit tests for JigsawPiece class"""

import unittest
import pygame
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece


class TestJigsawPiece(unittest.TestCase):
    """JigsawPiece sınıfı için unit testler"""
    
    @classmethod
    def setUpClass(cls):
        """Pygame'i başlat"""
        pygame.init()
    
    @classmethod
    def tearDownClass(cls):
        """Pygame'i kapat"""
        pygame.quit()
    
    def setUp(self):
        """Her test için yeni bir JigsawPiece oluştur"""
        # Basit bir pygame Surface oluştur
        self.test_surface = pygame.Surface((100, 100))
        self.test_surface.fill((255, 0, 0))
        
        self.piece = JigsawPiece(
            image=self.test_surface,
            original_position=(0, 0),
            piece_id=1
        )
    
    def test_initialization(self):
        """JigsawPiece'in doğru şekilde başlatıldığını test et"""
        self.assertEqual(self.piece.original_position, (0, 0))
        self.assertEqual(self.piece.piece_id, 1)
        self.assertIsNone(self.piece.pixel_position)
        self.assertFalse(self.piece.is_dragging)
        self.assertFalse(self.piece.is_placed)
        self.assertEqual(self.piece.z_index, 0)
        self.assertIsNotNone(self.piece.image)
    
    def test_is_in_correct_position_true(self):
        """Parça yerleştirildiğinde True döndürmeli"""
        self.piece.is_placed = True
        self.assertTrue(self.piece.is_in_correct_position())
    
    def test_is_in_correct_position_false(self):
        """Parça yerleştirilmediğinde False döndürmeli"""
        self.piece.is_placed = False
        self.assertFalse(self.piece.is_in_correct_position())
    
    def test_distance_to_correct_position_no_pixel_position(self):
        """pixel_position None ise sonsuz mesafe döndürmeli"""
        distance = self.piece.distance_to_correct_position((100, 100))
        self.assertEqual(distance, float('inf'))
    
    def test_distance_to_correct_position_with_position(self):
        """pixel_position varsa doğru mesafeyi hesaplamalı"""
        self.piece.pixel_position = (0, 0)
        distance = self.piece.distance_to_correct_position((3, 4))
        self.assertEqual(distance, 5.0)  # 3-4-5 üçgeni
    
    def test_dragging_state(self):
        """Sürükleme durumunun değiştirilebildiğini test et"""
        self.assertFalse(self.piece.is_dragging)
        self.piece.is_dragging = True
        self.assertTrue(self.piece.is_dragging)
    
    def test_z_index_update(self):
        """Z-index'in güncellenebilir olduğunu test et"""
        self.assertEqual(self.piece.z_index, 0)
        self.piece.z_index = 5
        self.assertEqual(self.piece.z_index, 5)


if __name__ == '__main__':
    unittest.main()
