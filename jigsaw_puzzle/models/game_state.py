"""GameState model managing the current state of the jigsaw puzzle game"""

from typing import List, Optional, Tuple
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece


class GameState:
    """Manages current game state"""
    
    def __init__(self, grid_size: Tuple[int, int], pieces: List[JigsawPiece]):
        """
        GameState constructor
        
        Args:
            grid_size: Grid size (rows, cols)
            pieces: List of all jigsaw pieces
        """
        self.grid_size = grid_size
        self.pieces = pieces
        self.selected_piece: Optional[JigsawPiece] = None
        self.is_completed = False
        self.is_failed = False  
        self.move_count = 0
        self.elapsed_time = 0.0  
        self.game_mode = "creative"  
    
    def get_piece_at(self, position: Tuple[int, int]) -> Optional[JigsawPiece]:
        """
        Return the piece located at the specified grid position
        
        Args:
            position: Position to search (row, col)
            
        Returns:
            Optional[JigsawPiece]: Piece at position or None
        """
        for piece in self.pieces:
            if piece.original_position == position and piece.is_placed:
                return piece
        return None
    
    def check_completion(self) -> bool:
        """
        Check whether the puzzle is completed
        
        Returns:
            bool: True if all pieces are in correct positions
        """
        # Check if all pieces are in correct position
        for piece in self.pieces:
            if not piece.is_in_correct_position():
                self.is_completed = False
                return False
        
        self.is_completed = True
        return True
    
    @property
    def completion_percentage(self) -> float:
        """
        Calculate completion percentage
        
        Returns:
            float: Completion percentage (0-100)
        """
        if not self.pieces:
            return 0.0
        placed_count = sum(1 for piece in self.pieces if piece.is_placed)
        return (placed_count / len(self.pieces)) * 100
