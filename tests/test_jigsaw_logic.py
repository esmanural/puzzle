"""Unit tests for JigsawLogic class"""

import unittest
import pygame
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece
from jigsaw_puzzle.services.jigsaw_logic import JigsawLogic


class TestJigsawLogic(unittest.TestCase):
    """JigsawLogic için unit testler"""
    
    @classmethod
    def setUpClass(cls):
        """Pygame'i başlat"""
        pygame.init()
    
    @classmethod
    def tearDownClass(cls):
        """Pygame'i kapat"""
        pygame.quit()
    
    def setUp(self):
        """Her test için yeni bir JigsawLogic oluştur"""
        # Test için basit pygame Surface'ler oluştur
        surface1 = pygame.Surface((50, 50))
        surface2 = pygame.Surface((50, 50))
        surface3 = pygame.Surface((50, 50))
        surface4 = pygame.Surface((50, 50))
        
        # 2x2 grid için 4 parça oluştur
        self.pieces = [
            JigsawPiece(surface1, (0, 0), 0),
            JigsawPiece(surface2, (0, 1), 1),
            JigsawPiece(surface3, (1, 0), 2),
            JigsawPiece(surface4, (1, 1), 3)
        ]
        
        self.game_state = GameState(grid_size=(2, 2), pieces=self.pieces)
        self.logic = JigsawLogic(self.game_state)
    
    def test_initialization(self):
        """JigsawLogic'in doğru şekilde başlatıldığını test et"""
        self.assertIsNotNone(self.logic.game_state)
        self.assertIsNotNone(self.logic.drag_handler)
    
    def test_scatter_pieces(self):
        """Parçaların PiecePool'a dağıtıldığını test et"""
        piece_pool = pygame.Rect(100, 100, 400, 400)
        
        self.logic.scatter_pieces(piece_pool)
        
        # Tüm parçaların pixel_position'ı set edilmiş olmalı
        for piece in self.pieces:
            self.assertIsNotNone(piece.pixel_position)
            
            # Pozisyonlar piece_pool içinde olmalı
            x, y = piece.pixel_position
            self.assertGreaterEqual(x, piece_pool.x)
            self.assertGreaterEqual(y, piece_pool.y)
            self.assertLessEqual(x, piece_pool.x + piece_pool.width)
            self.assertLessEqual(y, piece_pool.y + piece_pool.height)
    
    def test_get_piece_at_position_found(self):
        """Fare pozisyonundaki parçayı bulmalı"""
        # Parçalara pozisyon ver
        self.pieces[0].pixel_position = (100, 100)
        self.pieces[1].pixel_position = (200, 200)
        
        # İlk parçanın üzerine tıkla
        piece = self.logic.get_piece_at_position((110, 110))
        
        self.assertIsNotNone(piece)
        self.assertEqual(piece.piece_id, 0)
    
    def test_get_piece_at_position_not_found(self):
        """Fare pozisyonunda parça yoksa None döndürmeli"""
        # Parçalara pozisyon ver
        self.pieces[0].pixel_position = (100, 100)
        
        # Boş bir alana tıkla
        piece = self.logic.get_piece_at_position((500, 500))
        
        self.assertIsNone(piece)
    
    def test_get_piece_at_position_z_index_priority(self):
        """Z-index'e göre en üstteki parçayı bulmalı"""
        # İki parçayı üst üste koy
        self.pieces[0].pixel_position = (100, 100)
        self.pieces[0].z_index = 1
        
        self.pieces[1].pixel_position = (100, 100)
        self.pieces[1].z_index = 2
        
        # Aynı pozisyona tıkla
        piece = self.logic.get_piece_at_position((110, 110))
        
        # Z-index'i daha yüksek olan parça bulunmalı
        self.assertEqual(piece.piece_id, 1)
    
    def test_is_puzzle_solved_true(self):
        """Tüm parçalar yerleştirildiğinde True döndürmeli"""
        # Tüm parçaları yerleştir
        for piece in self.pieces:
            piece.is_placed = True
        
        result = self.logic.is_puzzle_solved()
        self.assertTrue(result)
    
    def test_is_puzzle_solved_false(self):
        """Parçalar yerleştirilmediğinde False döndürmeli"""
        # Parçaları yerleştirme
        for piece in self.pieces:
            piece.is_placed = False
        
        result = self.logic.is_puzzle_solved()
        self.assertFalse(result)
    
    def test_get_completion_percentage_all_placed(self):
        """Tüm parçalar yerleştirildiğinde %100 döndürmeli"""
        for piece in self.pieces:
            piece.is_placed = True
        
        percentage = self.logic.get_completion_percentage()
        self.assertEqual(percentage, 100.0)
    
    def test_get_completion_percentage_partial(self):
        """Kısmi yerleştirmede doğru yüzdeyi döndürmeli"""
        # 2 parçayı yerleştir
        self.pieces[0].is_placed = True
        self.pieces[1].is_placed = True
        self.pieces[2].is_placed = False
        self.pieces[3].is_placed = False
        
        percentage = self.logic.get_completion_percentage()
        self.assertEqual(percentage, 50.0)
    
    def test_get_completion_percentage_none_placed(self):
        """Hiç parça yerleştirilmediğinde %0 döndürmeli"""
        for piece in self.pieces:
            piece.is_placed = False
        
        percentage = self.logic.get_completion_percentage()
        self.assertEqual(percentage, 0.0)


if __name__ == '__main__':
    unittest.main()
