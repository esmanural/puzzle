"""JigsawPiece model representing a single piece of the jigsaw puzzle"""

from typing import Tuple, Optional
from pygame import Surface


class JigsawPiece:
    """Represents a single jigsaw puzzle piece"""
    
    def __init__(self, image: Surface, original_position: Tuple[int, int], 
                 piece_id: int):
        """
        JigsawPiece constructor
        
        Args:
            image: Piece image as pygame Surface
            original_position: Original grid position (row, col)
            piece_id: Unique piece identifier
        """
        self.image = image
        self.original_position = original_position  
        self.pixel_position: Optional[Tuple[int, int]] = None  
        self.piece_id = piece_id
        self.is_dragging = False  
        self.is_placed = False    
        self.z_index = 0          
    
    def is_in_correct_position(self) -> bool:
        """
        Check whether the piece is placed in its correct position
        
        Returns:
            bool: True if the piece has been placed, otherwise False
        """
        return self.is_placed
    
    def distance_to_correct_position(self, target_pixel_pos: Tuple[int, int]) -> float:
        """
        Calculate the pixel distance to the correct target position
        
        Args:
            target_pixel_pos: Target pixel position (x, y)
            
        Returns:
            float: Distance in pixels
        """
        if self.pixel_position is None:
            return float('inf')
        dx = self.pixel_position[0] - target_pixel_pos[0]
        dy = self.pixel_position[1] - target_pixel_pos[1]
        return (dx**2 + dy**2) ** 0.5
