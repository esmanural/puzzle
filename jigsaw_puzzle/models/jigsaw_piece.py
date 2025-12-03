"""JigsawPiece model representing a single piece of the jigsaw puzzle"""

from typing import Tuple, Optional
from pygame import Surface


class JigsawPiece:
    """Bir yapboz parçasını temsil eder"""
    
    def __init__(self, image: Surface, original_position: Tuple[int, int], 
                 piece_id: int):
        """
        JigsawPiece constructor
        
        Args:
            image: Parçanın pygame Surface görüntüsü
            original_position: Orijinal konum (row, col) - grid'deki doğru konum
            piece_id: Benzersiz parça kimliği
        """
        self.image = image
        self.original_position = original_position  # (row, col) - grid'deki doğru konum
        self.pixel_position: Optional[Tuple[int, int]] = None  # (x, y) - ekrandaki piksel konumu
        self.piece_id = piece_id
        self.is_dragging = False  # Sürükleniyor mu?
        self.is_placed = False    # Doğru konuma yerleştirildi mi?
        self.z_index = 0          # Çizim sırası (sürüklenirken en üstte)
    
    def is_in_correct_position(self) -> bool:
        """
        Parçanın doğru konumda olup olmadığını kontrol eder
        
        Returns:
            bool: Parça doğru konuma yerleştirilmişse True, değilse False
        """
        return self.is_placed
    
    def distance_to_correct_position(self, target_pixel_pos: Tuple[int, int]) -> float:
        """
        Parçanın doğru konuma olan piksel mesafesini hesaplar
        
        Args:
            target_pixel_pos: Hedef piksel pozisyonu (x, y)
            
        Returns:
            float: Mesafe (piksel cinsinden)
        """
        if self.pixel_position is None:
            return float('inf')
        dx = self.pixel_position[0] - target_pixel_pos[0]
        dy = self.pixel_position[1] - target_pixel_pos[1]
        return (dx**2 + dy**2) ** 0.5
