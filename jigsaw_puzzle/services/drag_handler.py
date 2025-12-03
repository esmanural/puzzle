"""DragHandler service managing drag-and-drop operations for jigsaw pieces"""

from typing import Optional, Tuple
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece
from jigsaw_puzzle.utils.constants import SNAP_THRESHOLD


class DragHandler:
    """Sürükle-bırak işlemlerini yönetir"""
    
    def __init__(self, game_state: GameState, snap_threshold: int = SNAP_THRESHOLD):
        """
        DragHandler constructor
        
        Args:
            game_state: Oyun durumu referansı
            snap_threshold: Snap için mesafe eşiği (piksel cinsinden)
        """
        self.game_state = game_state
        self.snap_threshold = snap_threshold
        self.dragged_piece: Optional[JigsawPiece] = None
        self.drag_offset: Tuple[int, int] = (0, 0)  # Fare ile parça arasındaki offset
        self._max_z_index = 0  # En yüksek z-index değerini takip et
    
    def start_drag(self, piece: JigsawPiece, mouse_pos: Tuple[int, int]) -> None:
        """
        Sürükleme işlemini başlatır
        
        Args:
            piece: Sürüklenecek parça
            mouse_pos: Fare pozisyonu (x, y)
        """
        if piece is None:
            return
        
        # Parçayı sürükleme moduna al
        self.dragged_piece = piece
        piece.is_dragging = True
        
        # Fare ile parça arasındaki offset'i hesapla
        if piece.pixel_position is not None:
            self.drag_offset = (
                mouse_pos[0] - piece.pixel_position[0],
                mouse_pos[1] - piece.pixel_position[1]
            )
        else:
            self.drag_offset = (0, 0)
        
        # Sürüklenen parçayı en üste getir (z-index)
        self._max_z_index += 1
        piece.z_index = self._max_z_index
    
    def update_drag(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Sürükleme sırasında parçanın pozisyonunu günceller
        
        Args:
            mouse_pos: Güncel fare pozisyonu (x, y)
        """
        if self.dragged_piece is None:
            return
        
        # Parçanın yeni pozisyonunu hesapla (offset'i uygula)
        new_x = mouse_pos[0] - self.drag_offset[0]
        new_y = mouse_pos[1] - self.drag_offset[1]
        
        self.dragged_piece.pixel_position = (new_x, new_y)
    
    def end_drag(self) -> bool:
        """
        Sürükleme işlemini bitirir ve snap kontrolü yapar
        
        Returns:
            bool: Parça doğru konuma yerleştirildiyse True, değilse False
        """
        if self.dragged_piece is None:
            return False
        
        # Snap kontrolü yap
        snapped = self.check_snap_to_grid(self.dragged_piece)
        
        # Sürükleme durumunu kapat
        self.dragged_piece.is_dragging = False
        self.dragged_piece = None
        self.drag_offset = (0, 0)
        
        return snapped
    
    def check_snap_to_grid(self, piece: JigsawPiece) -> bool:
        """
        Parçanın doğru konuma yakın olup olmadığını kontrol eder ve
        yakınsa otomatik olarak doğru konuma yerleştirir (snap-to-grid)
        
        Args:
            piece: Kontrol edilecek parça
            
        Returns:
            bool: Parça yerleştirildiyse True, değilse False
        """
        if piece is None or piece.pixel_position is None:
            return False
        
        # Parçanın doğru konumunu hesapla
        # Bu hesaplama için play_area bilgisine ihtiyacımız var
        # Şimdilik basit bir yaklaşım: eğer parça zaten yerleştirilmişse kontrol etme
        if piece.is_placed:
            return False
        
        # Doğru konumu hesaplamak için grid bilgisini kullan
        # Not: Bu hesaplama GameRenderer'daki layout bilgisine bağlı
        # Şimdilik parçanın target_position'ını piece üzerinde saklayacağız
        # veya GameState üzerinden erişeceğiz
        
        # Eğer parçanın target_pixel_position'ı varsa (GameRenderer tarafından set edilmiş)
        if hasattr(piece, 'target_pixel_position') and piece.target_pixel_position is not None:
            target_pos = piece.target_pixel_position
            distance = piece.distance_to_correct_position(target_pos)
            
            # Eşik değerinden küçükse snap yap
            if distance <= self.snap_threshold:
                piece.pixel_position = target_pos
                piece.is_placed = True
                return True
        
        return False
    
    def cancel_drag(self) -> None:
        """
        Sürükleme işlemini iptal eder (örneğin ESC tuşuna basıldığında)
        """
        if self.dragged_piece is not None:
            self.dragged_piece.is_dragging = False
            self.dragged_piece = None
            self.drag_offset = (0, 0)
