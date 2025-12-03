"""Unit tests for GameState class"""

import unittest
import pygame
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece


class TestGameState(unittest.TestCase):
    """GameState sınıfı için unit testler"""
    
    @classmethod
    def setUpClass(cls):
        """Pygame'i başlat"""
        pygame.init()
    
    @classmethod
    def tearDownClass(cls):
        """Pygame'i kapat"""
        pygame.quit()
    
    def setUp(self):
        """Her test için yeni bir GameState oluştur"""
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
        
        # Parçaları doğru konuma yerleştir (test için)
        for piece in self.pieces:
            piece.is_placed = True
        
        self.game_state = GameState(grid_size=(2, 2), pieces=self.pieces)
    
    def test_initialization(self):
        """GameState'in doğru şekilde başlatıldığını test et"""
        self.assertEqual(self.game_state.grid_size, (2, 2))
        self.assertEqual(len(self.game_state.pieces), 4)
        self.assertIsNone(self.game_state.selected_piece)
        self.assertFalse(self.game_state.is_completed)
        self.assertEqual(self.game_state.move_count, 0)
        self.assertEqual(self.game_state.elapsed_time, 0.0)
    
    def test_get_piece_at_existing(self):
        """Var olan konumdaki parçayı bulmalı"""
        # get_piece_at sadece yerleştirilmiş parçaları bulur
        piece = self.game_state.get_piece_at((0, 0))
        self.assertIsNotNone(piece)
        self.assertEqual(piece.piece_id, 0)
    
    def test_get_piece_at_nonexisting(self):
        """Olmayan konumda None döndürmeli"""
        piece = self.game_state.get_piece_at((5, 5))
        self.assertIsNone(piece)
    
    def test_elapsed_time(self):
        """Elapsed time özelliğinin çalıştığını test et"""
        self.assertEqual(self.game_state.elapsed_time, 0.0)
        self.game_state.elapsed_time = 10.5
        self.assertEqual(self.game_state.elapsed_time, 10.5)
    
    def test_check_completion_all_correct(self):
        """Tüm parçalar doğru konumdayken True döndürmeli"""
        result = self.game_state.check_completion()
        self.assertTrue(result)
        self.assertTrue(self.game_state.is_completed)
    
    def test_check_completion_not_complete(self):
        """Parçalar yanlış konumdayken False döndürmeli"""
        # Bir parçayı yerleştirilmemiş olarak işaretle
        self.pieces[0].is_placed = False
        
        result = self.game_state.check_completion()
        self.assertFalse(result)
        self.assertFalse(self.game_state.is_completed)
    
    def test_completion_percentage_all_placed(self):
        """Tüm parçalar yerleştirildiğinde %100 döndürmeli"""
        percentage = self.game_state.completion_percentage
        self.assertEqual(percentage, 100.0)
    
    def test_completion_percentage_partial(self):
        """Kısmi yerleştirmede doğru yüzdeyi döndürmeli"""
        # 2 parçayı yerleştirilmemiş yap
        self.pieces[0].is_placed = False
        self.pieces[1].is_placed = False
        
        percentage = self.game_state.completion_percentage
        self.assertEqual(percentage, 50.0)  # 2/4 = 50%
    
    def test_completion_percentage_none_placed(self):
        """Hiç parça yerleştirilmediğinde %0 döndürmeli"""
        for piece in self.pieces:
            piece.is_placed = False
        
        percentage = self.game_state.completion_percentage
        self.assertEqual(percentage, 0.0)


if __name__ == '__main__':
    unittest.main()
