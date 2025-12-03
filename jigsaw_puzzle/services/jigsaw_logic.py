"""JigsawLogic service managing jigsaw puzzle game logic"""

import random
from typing import Optional, Tuple
import pygame
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece
from jigsaw_puzzle.services.drag_handler import DragHandler


class JigsawLogic:
    """Yapboz oyun mantığını yönetir"""
    
    def __init__(self, game_state: GameState):
        """
        JigsawLogic constructor
        
        Args:
            game_state: Yönetilecek oyun durumu
        """
        self.game_state = game_state
        self.drag_handler = DragHandler(game_state)
    
    def scatter_pieces(self, piece_pool_area: pygame.Rect):
        """
        Parçaları PiecePool alanına rastgele dağıtır
        
        Args:
            piece_pool_area: Parçaların dağıtılacağı alan
        """
        for piece in self.game_state.pieces:
            # Rastgele pozisyon hesapla
            x = random.randint(
                piece_pool_area.x,
                piece_pool_area.x + piece_pool_area.width - piece.image.get_width()
            )
            y = random.randint(
                piece_pool_area.y,
                piece_pool_area.y + piece_pool_area.height - piece.image.get_height()
            )
            piece.pixel_position = (x, y)
    
    def get_piece_at_position(self, mouse_pos: Tuple[int, int]) -> Optional[JigsawPiece]:
        """
        Fare pozisyonundaki parçayı bulur (z-index'e göre en üstteki)
        
        Args:
            mouse_pos: Fare pozisyonu (x, y)
            
        Returns:
            Optional[JigsawPiece]: Bulunan parça veya None
        """
        # Z-index'e göre sırala (en üstteki önce)
        sorted_pieces = sorted(
            self.game_state.pieces,
            key=lambda p: p.z_index,
            reverse=True
        )
        
        for piece in sorted_pieces:
            if piece.pixel_position is None:
                continue
            
            # Parçanın rect'ini oluştur
            piece_rect = pygame.Rect(
                piece.pixel_position[0],
                piece.pixel_position[1],
                piece.image.get_width(),
                piece.image.get_height()
            )
            
            # Fare pozisyonu parçanın içinde mi?
            if piece_rect.collidepoint(mouse_pos):
                return piece
        
        return None
    
    def is_puzzle_solved(self) -> bool:
        """
        Yapboz'un çözülüp çözülmediğini kontrol eder
        
        Returns:
            bool: Yapboz tamamlandıysa True, değilse False
        """
        return self.game_state.check_completion()
    
    def get_completion_percentage(self) -> float:
        """
        Tamamlanma yüzdesini hesaplar
        
        Returns:
            float: Tamamlanma yüzdesi (0-100)
        """
        return self.game_state.completion_percentage
