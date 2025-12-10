"""JigsawLogic service managing jigsaw puzzle game logic"""

import random
from typing import Optional, Tuple
import pygame
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece
from jigsaw_puzzle.services.drag_handler import DragHandler


class JigsawLogic:
    """Manages jigsaw puzzle game logic"""
    
    def __init__(self, game_state: GameState):
        """
        JigsawLogic constructor
        
        Args:
            game_state: Game state to manage
        """
        self.game_state = game_state
        self.drag_handler = DragHandler(game_state)
    
    def scatter_pieces(self, piece_pool_area: pygame.Rect):
        """
        Randomly distribute pieces into the PiecePool area
        
        Args:
            piece_pool_area: Area to scatter the pieces into
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
        Find the piece under the mouse position (by highest z-index)
        
        Args:
            mouse_pos: Mouse position (x, y)
            
        Returns:
            Optional[JigsawPiece]: Found piece or None
        """
        # Sort by z-index (topmost first)
        sorted_pieces = sorted(
            self.game_state.pieces,
            key=lambda p: p.z_index,
            reverse=True
        )
        
        for piece in sorted_pieces:
            if piece.pixel_position is None:
                continue
            
            # Create piece rect
            piece_rect = pygame.Rect(
                piece.pixel_position[0],
                piece.pixel_position[1],
                piece.image.get_width(),
                piece.image.get_height()
            )
            
            # Check if mouse position is within the piece
            if piece_rect.collidepoint(mouse_pos):
                return piece
        
        return None
    
    def is_puzzle_solved(self) -> bool:
        """
        Check whether the puzzle has been solved
        
        Returns:
            bool: True if completed, otherwise False
        """
        return self.game_state.check_completion()
    
    def get_completion_percentage(self) -> float:
        """
        Calculate completion percentage
        
        Returns:
            float: Completion percentage (0-100)
        """
        return self.game_state.completion_percentage
