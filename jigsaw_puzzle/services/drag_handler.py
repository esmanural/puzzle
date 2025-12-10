"""DragHandler service managing drag-and-drop operations for jigsaw pieces"""

from typing import Optional, Tuple
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece
from jigsaw_puzzle.utils.constants import SNAP_THRESHOLD


class DragHandler:
    """Manages drag-and-drop operations"""
    
    def __init__(self, game_state: GameState, snap_threshold: int = SNAP_THRESHOLD):
        """
        DragHandler constructor
        
        Args:
            game_state: Game state reference
            snap_threshold: Snap distance threshold (in pixels)
        """
        self.game_state = game_state
        self.snap_threshold = snap_threshold
        self.dragged_piece: Optional[JigsawPiece] = None
        self.drag_offset: Tuple[int, int] = (0, 0)  
        self._max_z_index = 0  
    
    def start_drag(self, piece: JigsawPiece, mouse_pos: Tuple[int, int]) -> None:
        """
        Start drag operation
        
        Args:
            piece: Piece to drag
            mouse_pos: Mouse position (x, y)
        """
        if piece is None:
            return
        
        # Activate drag mode for the piece
        self.dragged_piece = piece
        piece.is_dragging = True
        
        # Calculate mouse-to-piece offset
        if piece.pixel_position is not None:
            self.drag_offset = (
                mouse_pos[0] - piece.pixel_position[0],
                mouse_pos[1] - piece.pixel_position[1]
            )
        else:
            self.drag_offset = (0, 0)
        
        # Bring dragged piece to front (z-index)
        self._max_z_index += 1
        piece.z_index = self._max_z_index
    
    def update_drag(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update piece position during drag
        
        Args:
            mouse_pos: Current mouse position (x, y)
        """
        if self.dragged_piece is None:
            return
        
        # Compute new position (apply offset)
        new_x = mouse_pos[0] - self.drag_offset[0]
        new_y = mouse_pos[1] - self.drag_offset[1]
        
        self.dragged_piece.pixel_position = (new_x, new_y)
    
    def end_drag(self) -> bool:
        """
        Finish drag and perform snap-to-grid check
        
        Returns:
            bool: True if piece placed to correct position
        """
        if self.dragged_piece is None:
            return False
        
        # Perform snap check
        snapped = self.check_snap_to_grid(self.dragged_piece)
        
        # Turn off dragging state
        self.dragged_piece.is_dragging = False
        self.dragged_piece = None
        self.drag_offset = (0, 0)
        
        return snapped
    
    def check_snap_to_grid(self, piece: JigsawPiece) -> bool:
        """
        Check proximity to the correct position and snap automatically
        
        Args:
            piece: Piece to check
            
        Returns:
            bool: True if the piece gets placed
        """
        if piece is None or piece.pixel_position is None:
            return False
        
        # Compute target position
        # Requires play area info
        # Early return if already placed
        if piece.is_placed:
            return False
        
        # Use grid/layout info to compute correct position
        # Currently relies on GameRenderer to set target position
        
        # If the piece has target_pixel_position (set by GameRenderer)
        if hasattr(piece, 'target_pixel_position') and piece.target_pixel_position is not None:
            target_pos = piece.target_pixel_position
            distance = piece.distance_to_correct_position(target_pos)
            
            # Snap when within threshold
            if distance <= self.snap_threshold:
                piece.pixel_position = target_pos
                piece.is_placed = True
                return True
        
        return False
    
    def cancel_drag(self) -> None:
        """
        Cancel drag operation (e.g., on ESC key)
        """
        if self.dragged_piece is not None:
            self.dragged_piece.is_dragging = False
            self.dragged_piece = None
            self.drag_offset = (0, 0)
