"""
Visual effects module
"""
import pygame
from typing import Tuple
from ..utils.constants import SHADOW_COLOR, SHADOW_OFFSET, HOVER_SCALE


class Effects:
    """Visual effects (shadow, animation, etc.)"""
    
    @staticmethod
    def draw_shadow(surface: pygame.Surface, rect: pygame.Rect, offset: int = SHADOW_OFFSET):
        """
        Draw shadow effect for a piece
        
        Args:
            surface: Target drawing surface
            rect: Rectangle area to draw shadow
            offset: Shadow offset amount (pixels)
        """
        # Create shadow rectangle (shifted by offset)
        shadow_rect = rect.copy()
        shadow_rect.x += offset
        shadow_rect.y += offset
        
        # Create semi-transparent shadow surface
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        shadow_surface.fill(SHADOW_COLOR)
        
        # Draw shadow
        surface.blit(shadow_surface, shadow_rect)
    
    @staticmethod
    def apply_hover_effect(piece_surface: pygame.Surface, scale: float = HOVER_SCALE) -> pygame.Surface:
        """
        Scaling effect for dragged piece
        
        Args:
            piece_surface: Original piece surface
            scale: Scale factor (e.g., 1.05 = 5% larger)
            
        Returns:
            Scaled surface
        """
        # Get original dimensions
        original_width = piece_surface.get_width()
        original_height = piece_surface.get_height()
        
        # Compute new dimensions
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        
        # Scale surface
        scaled_surface = pygame.transform.smoothscale(piece_surface, (new_width, new_height))
        
        return scaled_surface
    
    @staticmethod
    def draw_snap_animation(screen: pygame.Surface, piece_image: pygame.Surface, 
                          start_pos: Tuple[int, int], target_pos: Tuple[int, int], 
                          progress: float):
        """
        Animation when a piece is placed
        
        Args:
            screen: Target drawing screen surface
            piece_image: Piece image
            start_pos: Start position (x, y)
            target_pos: Target position (x, y)
            progress: Animation progress (0.0 - 1.0)
        """
        # Compute current position via linear interpolation
        current_x = start_pos[0] + (target_pos[0] - start_pos[0]) * progress
        current_y = start_pos[1] + (target_pos[1] - start_pos[1]) * progress
        
        # Alpha value for slight fade-in during animation
        alpha = int(255 * (0.5 + 0.5 * progress))  
        
        # Create temporary surface and apply alpha
        temp_surface = piece_image.copy()
        temp_surface.set_alpha(alpha)
        
        # Draw piece at current position
        screen.blit(temp_surface, (int(current_x), int(current_y)))
