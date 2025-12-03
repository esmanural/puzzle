"""
Görsel efektler modülü
"""
import pygame
from typing import Tuple
from ..utils.constants import SHADOW_COLOR, SHADOW_OFFSET, HOVER_SCALE


class Effects:
    """Görsel efektler (gölge, animasyon, vb.)"""
    
    @staticmethod
    def draw_shadow(surface: pygame.Surface, rect: pygame.Rect, offset: int = SHADOW_OFFSET):
        """
        Parça için gölge efekti çizer
        
        Args:
            surface: Çizim yapılacak yüzey
            rect: Gölge çizilecek dikdörtgen alan
            offset: Gölge offset miktarı (piksel)
        """
        # Gölge için dikdörtgen oluştur (offset kadar kaydırılmış)
        shadow_rect = rect.copy()
        shadow_rect.x += offset
        shadow_rect.y += offset
        
        # Yarı saydam gölge yüzeyi oluştur
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_surface.fill(SHADOW_COLOR)
        
        # Gölgeyi çiz
        surface.blit(shadow_surface, shadow_rect)
    
    @staticmethod
    def apply_hover_effect(piece_surface: pygame.Surface, scale: float = HOVER_SCALE) -> pygame.Surface:
        """
        Sürüklenen parça için büyütme efekti
        
        Args:
            piece_surface: Parçanın orijinal yüzeyi
            scale: Büyütme oranı (örn: 1.05 = %5 büyütme)
            
        Returns:
            Büyütülmüş yüzey
        """
        # Orijinal boyutları al
        original_width = piece_surface.get_width()
        original_height = piece_surface.get_height()
        
        # Yeni boyutları hesapla
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        
        # Yüzeyi ölçeklendir
        scaled_surface = pygame.transform.smoothscale(piece_surface, (new_width, new_height))
        
        return scaled_surface
    
    @staticmethod
    def draw_snap_animation(screen: pygame.Surface, piece_image: pygame.Surface, 
                          start_pos: Tuple[int, int], target_pos: Tuple[int, int], 
                          progress: float):
        """
        Parça yerleştirildiğinde animasyon
        
        Args:
            screen: Çizim yapılacak ekran yüzeyi
            piece_image: Parçanın görüntüsü
            start_pos: Başlangıç pozisyonu (x, y)
            target_pos: Hedef pozisyon (x, y)
            progress: Animasyon ilerleme durumu (0.0 - 1.0)
        """
        # Linear interpolation ile mevcut pozisyonu hesapla
        current_x = start_pos[0] + (target_pos[0] - start_pos[0]) * progress
        current_y = start_pos[1] + (target_pos[1] - start_pos[1]) * progress
        
        # Animasyon sırasında hafif bir fade-in efekti için alpha değeri
        alpha = int(255 * (0.5 + 0.5 * progress))  # 127'den 255'e
        
        # Geçici yüzey oluştur ve alpha uygula
        temp_surface = piece_image.copy()
        temp_surface.set_alpha(alpha)
        
        # Parçayı mevcut pozisyonda çiz
        screen.blit(temp_surface, (int(current_x), int(current_y)))
