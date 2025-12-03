"""GameState model managing the current state of the jigsaw puzzle game"""

from typing import List, Optional, Tuple
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece


class GameState:
    """Oyun durumunu yönetir"""
    
    def __init__(self, grid_size: Tuple[int, int], pieces: List[JigsawPiece]):
        """
        GameState constructor
        
        Args:
            grid_size: Grid boyutu (rows, cols)
            pieces: Tüm yapboz parçalarının listesi
        """
        self.grid_size = grid_size
        self.pieces = pieces
        self.selected_piece: Optional[JigsawPiece] = None
        self.is_completed = False
        self.is_failed = False  # Oyun başarısız oldu mu (süre/hamle sınırı)
        self.move_count = 0
        self.elapsed_time = 0.0  # Geçen süre (saniye)
        self.game_mode = "creative"  # Oyun modu (creative/timed/challenge)
    
    def get_piece_at(self, position: Tuple[int, int]) -> Optional[JigsawPiece]:
        """
        Belirtilen grid konumundaki parçayı döndürür
        
        Args:
            position: Aranacak konum (row, col)
            
        Returns:
            Optional[JigsawPiece]: Konumdaki parça veya None
        """
        for piece in self.pieces:
            if piece.original_position == position and piece.is_placed:
                return piece
        return None
    
    def check_completion(self) -> bool:
        """
        Yapboz'un tamamlanıp tamamlanmadığını kontrol eder
        
        Returns:
            bool: Tüm parçalar doğru konumdaysa True, değilse False
        """
        # Tüm parçaların doğru konumda olup olmadığını kontrol et
        for piece in self.pieces:
            if not piece.is_in_correct_position():
                self.is_completed = False
                return False
        
        self.is_completed = True
        return True
    
    @property
    def completion_percentage(self) -> float:
        """
        Tamamlanma yüzdesini hesaplar
        
        Returns:
            float: Tamamlanma yüzdesi (0-100)
        """
        if not self.pieces:
            return 0.0
        placed_count = sum(1 for piece in self.pieces if piece.is_placed)
        return (placed_count / len(self.pieces)) * 100
