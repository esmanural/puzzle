"""GameRenderer UI component for rendering the jigsaw puzzle game using pygame"""

import pygame
from typing import Tuple, Optional
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece
from jigsaw_puzzle.ui.effects import Effects
from jigsaw_puzzle.utils.constants import (
    BACKGROUND_COLOR,
    PLAY_AREA_BG,
    PIECE_POOL_BG,
    GRID_LINE_COLOR,
    TEXT_COLOR,
    GRID_LINE_WIDTH,
    MARGIN,
    PLAY_AREA_WIDTH_RATIO,
    PIECE_POOL_WIDTH_RATIO
)


class GameRenderer:
    """Render the game using modern pygame"""
    
    def __init__(self, screen_size: Tuple[int, int], game_state: GameState, 
                 preview_image: Optional[pygame.Surface] = None):
        """
        GameRenderer constructor
        
        Args:
            screen_size: Screen size (width, height)
            game_state: Game state
            preview_image: Original image for preview (optional)
        """
        self.screen_size = screen_size
        self.game_state = game_state
        self.screen = pygame.display.set_mode(screen_size)
        self.effects = Effects()
        self.preview_image = preview_image  
        
        # Set window title
        rows, cols = game_state.grid_size
        pygame.display.set_caption(f"Jigsaw Puzzle Game - {rows}x{cols}")
        
        # Layout calculations
        self.play_area: Optional[pygame.Rect] = None
        self.piece_pool: Optional[pygame.Rect] = None
        self.preview_area: Optional[pygame.Rect] = None
        self.info_area: Optional[pygame.Rect] = None
        
        self._calculate_layout()
    
    def _calculate_layout(self):
        """
        Calculate screen layout (PlayArea, PiecePool, Preview, Info)
        
        Layout structure:
        - Left (65%): PlayArea - puzzle completion area
        - Right (30%): PiecePool (top), Preview (middle), Info (bottom)
        """
        screen_width, screen_height = self.screen_size
        
        # PlayArea (left - puzzle completion area)
        # Takes 65% of screen width, full height
        play_area_width = int(screen_width * PLAY_AREA_WIDTH_RATIO)
        self.play_area = pygame.Rect(
            MARGIN,
            MARGIN,
            play_area_width - MARGIN * 2,
            screen_height - MARGIN * 2
        )
        
        # Start x for right side
        right_side_x = play_area_width + MARGIN
        right_side_width = int(screen_width * PIECE_POOL_WIDTH_RATIO) - MARGIN
        
        # Calculate available height for right side
        available_height = screen_height - MARGIN * 2
        
        # PiecePool (top right - mixed pieces area)
        # Takes 50% of right side
        piece_pool_height = int(available_height * 0.50)
        self.piece_pool = pygame.Rect(
            right_side_x,
            MARGIN,
            right_side_width,
            piece_pool_height
        )
        
        # Preview area (middle right - preview)
        # Square shape, fits right side width
        preview_size = min(right_side_width, 200)
        self.preview_area = pygame.Rect(
            right_side_x,
            self.piece_pool.bottom + MARGIN,
            preview_size,
            preview_size
        )
        
        # Info area (bottom right - info panel)
        # Takes remaining space
        info_height = screen_height - self.preview_area.bottom - MARGIN * 2
        self.info_area = pygame.Rect(
            right_side_x,
            self.preview_area.bottom + MARGIN,
            right_side_width,
            info_height
        )
    
    def render(self):
        """
        Main render method - draws the entire game screen
        
        Draw order:
        1. Background
        2. PlayArea (grid + placed pieces)
        3. PiecePool (unplaced pieces)
        4. Preview
        5. Info Panel
        """
        # Clear background
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw PlayArea (grid + placed pieces)
        self.draw_play_area()
        
        # Draw PiecePool (mixed pieces)
        self.draw_piece_pool()
        
        # Draw preview and info panel
        self.draw_preview()
        self.draw_info_panel()
    
    def draw_play_area(self):
        """
        Draw PlayArea (grid lines + placed pieces)
        
        PlayArea is the area where puzzle pieces are placed.
        Grid lines indicate piece boundaries.
        """
        # PlayArea background
        pygame.draw.rect(self.screen, PLAY_AREA_BG, self.play_area)
        
        # Draw grid lines
        rows, cols = self.game_state.grid_size
        
        # Compute piece dimensions
        piece_width = self.play_area.width // cols
        piece_height = self.play_area.height // rows
        
        # Vertical lines (between columns)
        for col in range(1, cols):
            x = self.play_area.x + col * piece_width
            pygame.draw.line(
                self.screen,
                GRID_LINE_COLOR,
                (x, self.play_area.y),
                (x, self.play_area.bottom),
                GRID_LINE_WIDTH
            )
        
        # Horizontal lines (between rows)
        for row in range(1, rows):
            y = self.play_area.y + row * piece_height
            pygame.draw.line(
                self.screen,
                GRID_LINE_COLOR,
                (self.play_area.x, y),
                (self.play_area.right, y),
                GRID_LINE_WIDTH
            )
        
        # PlayArea frame
        pygame.draw.rect(self.screen, GRID_LINE_COLOR, self.play_area, GRID_LINE_WIDTH)
        
        # Draw placed pieces
        for piece in self.game_state.pieces:
            if piece.is_placed:
                self.draw_piece(piece)
    
    def draw_piece_pool(self):
        """
        Draw the PiecePool (mixed pieces area)
        
        PiecePool contains unplaced pieces.
        Pieces are ordered by z-index (dragged piece on top).
        """
        # PiecePool background
        pygame.draw.rect(self.screen, PIECE_POOL_BG, self.piece_pool)
        
        # PiecePool frame
        pygame.draw.rect(self.screen, GRID_LINE_COLOR, self.piece_pool, GRID_LINE_WIDTH)
        
        # Draw unplaced pieces
        # Sort by z-index (lower first, higher last)
        unplaced_pieces = [p for p in self.game_state.pieces if not p.is_placed]
        sorted_pieces = sorted(unplaced_pieces, key=lambda p: p.z_index)
        
        for piece in sorted_pieces:
            self.draw_piece(piece)
    
    def draw_piece(self, piece: JigsawPiece):
        """
        Draw a single piece with shadow effect
        
        Args:
            piece: Jigsaw piece to draw
            
        For dragged pieces:
        - Shadow effect is applied
        - Slight scaling applied (hover effect)
        
        For normal pieces:
        - Draw directly
        """
        if piece.pixel_position is None:
            return
        
        # Create piece rect
        piece_rect = pygame.Rect(
            piece.pixel_position[0],
            piece.pixel_position[1],
            piece.image.get_width(),
            piece.image.get_height()
        )
        
        # Shadow and hover effects (if dragging)
        if piece.is_dragging:
            # Draw shadow
            self.effects.draw_shadow(self.screen, piece_rect)
            
            # Apply hover effect (slight scaling)
            scaled_image = self.effects.apply_hover_effect(piece.image)
            
            # Center the scaled piece
            scaled_width = scaled_image.get_width()
            scaled_height = scaled_image.get_height()
            offset_x = (scaled_width - piece.image.get_width()) // 2
            offset_y = (scaled_height - piece.image.get_height()) // 2
            
            adjusted_pos = (
                piece.pixel_position[0] - offset_x,
                piece.pixel_position[1] - offset_y
            )
            
            self.screen.blit(scaled_image, adjusted_pos)
        else:
            # Normal draw (no shadow, no scaling)
            self.screen.blit(piece.image, piece.pixel_position)
    
    def draw_preview(self):
        """
        Draw a small preview of the original image
        
        The preview helps the user see the completed image.
        Image is fit into preview_area while preserving aspect ratio.
        """
        # Preview background (white)
        pygame.draw.rect(self.screen, (255, 255, 255), self.preview_area)
        
        # If preview image exists, draw it
        if self.preview_image:
            # Fit the image to preview_area (preserve aspect ratio)
            preview_width = self.preview_area.width - 10  # 5px padding her yandan
            preview_height = self.preview_area.height - 10
            
            # Original image size
            img_width = self.preview_image.get_width()
            img_height = self.preview_image.get_height()
            
            # Calculate aspect ratio
            scale_x = preview_width / img_width
            scale_y = preview_height / img_height
            scale = min(scale_x, scale_y)
            
            # New size
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Scale image
            scaled_preview = pygame.transform.smoothscale(
                self.preview_image, 
                (new_width, new_height)
            )
            
            # Center align
            x = self.preview_area.x + (self.preview_area.width - new_width) // 2
            y = self.preview_area.y + (self.preview_area.height - new_height) // 2
            
            self.screen.blit(scaled_preview, (x, y))
        else:
            # Show "Preview" text if no preview image
            font = pygame.font.Font(None, 24)
            text = font.render("Preview", True, (100, 100, 100))
            text_rect = text.get_rect(
                center=(self.preview_area.centerx, self.preview_area.centery)
            )
            self.screen.blit(text, text_rect)
        
        # Preview frame
        pygame.draw.rect(self.screen, GRID_LINE_COLOR, self.preview_area, 2)
    
    def draw_info_panel(self):
        """
        Draw info panel (time, completion %, move count)
        
        The info panel shows game statistics:
        - Elapsed time (mm:ss)
        - Completion percentage (based on placed pieces)
        - Move count (total drag-and-drop operations)
        """
        # Info panel background (dark gray)
        pygame.draw.rect(self.screen, (60, 70, 75), self.info_area)
        pygame.draw.rect(self.screen, GRID_LINE_COLOR, self.info_area, 2)
        
        # Font settings - smaller for better fit
        title_font = pygame.font.Font(None, 28)
        info_font = pygame.font.Font(None, 24)
        
        # Title
        title = title_font.render("Statistics", True, TEXT_COLOR)
        title_rect = title.get_rect(
            centerx=self.info_area.centerx,
            top=self.info_area.y + 10
        )
        self.screen.blit(title, title_rect)
        
        # Time
        minutes = int(self.game_state.elapsed_time // 60)
        seconds = int(self.game_state.elapsed_time % 60)
        time_text = info_font.render(
            f"Time: {minutes:02d}:{seconds:02d}", 
            True, 
            TEXT_COLOR
        )
        
        # Completion percentage
        percentage = self.game_state.completion_percentage
        percent_text = info_font.render(
            f"Completion: {percentage:.0f}%", 
            True, 
            TEXT_COLOR
        )
        
        # Move count
        moves_text = info_font.render(
            f"Moves: {self.game_state.move_count}", 
            True, 
            TEXT_COLOR
        )
        
        # Total piece count
        total_pieces = len(self.game_state.pieces)
        placed_pieces = sum(1 for p in self.game_state.pieces if p.is_placed)
        pieces_text = info_font.render(
            f"Pieces: {placed_pieces}/{total_pieces}", 
            True, 
            TEXT_COLOR
        )
        
        # Game mode info
        mode_names = {
            "creative": "🎨 Free",
            "timed": "⏱️ Time Attack",
            "challenge": "🏆 Challenge"
        }
        mode_name = mode_names.get(self.game_state.game_mode, "🎮 Game")
        mode_text = info_font.render(
            f"Mode: {mode_name}",
            True,
            TEXT_COLOR
        )
        
        # Align texts vertically with compact spacing
        y_start = title_rect.bottom + 12
        line_spacing = 30
        
        self.screen.blit(mode_text, (self.info_area.x + 15, y_start))
        self.screen.blit(time_text, (self.info_area.x + 15, y_start + line_spacing))
        self.screen.blit(percent_text, (self.info_area.x + 15, y_start + line_spacing * 2))
        self.screen.blit(pieces_text, (self.info_area.x + 15, y_start + line_spacing * 3))
        self.screen.blit(moves_text, (self.info_area.x + 15, y_start + line_spacing * 4))
        
        # Keyboard shortcuts info at bottom
        small_font = pygame.font.Font(None, 16)
        hint_y = self.info_area.bottom - 25
        
        hint_text = small_font.render("ESC: Exit", True, (150, 150, 150))
        self.screen.blit(hint_text, (self.info_area.x + 15, hint_y))
    
    def show_completion_message(self):
        """
        Shows completion or failure message
        
        Displays a box in the center of the screen when puzzle is completed or game fails.
        Contains statistics and new game instructions.
        """
        # Font settings
        title_font = pygame.font.Font(None, 84)
        info_font = pygame.font.Font(None, 38)
        small_font = pygame.font.Font(None, 32)
        
        # Message based on success or failure
        if self.game_state.is_failed:
            title_text = title_font.render("😔 Game Over!", True, (231, 76, 60))
            title_color = (231, 76, 60)
        else:
            title_text = title_font.render("🎉 Congratulations! 🎉", True, (52, 152, 219))
            title_color = (52, 152, 219)
        
        minutes = int(self.game_state.elapsed_time // 60)
        seconds = int(self.game_state.elapsed_time % 60)
        time_text = info_font.render(
            f"Time: {minutes:02d}:{seconds:02d}",
            True,
            (45, 52, 54)
        )
        moves_text = info_font.render(
            f"Moves: {self.game_state.move_count}",
            True,
            (45, 52, 54)
        )
        
        # Separator line
        separator_text = info_font.render("─────────────", True, (150, 150, 150))
        
        restart_text = small_font.render(
            "Press 'N' for new game",
            True,
            (100, 100, 100)
        )
        quit_text = small_font.render(
            "Press 'ESC' to exit",
            True,
            (100, 100, 100)
        )
        
        # Create semi-transparent background
        overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  
        self.screen.blit(overlay, (0, 0))
        
        # Create message box
        box_width = 600
        box_height = 400
        center_x = self.screen_size[0] // 2
        center_y = self.screen_size[1] // 2
        
        box_rect = pygame.Rect(
            center_x - box_width // 2,
            center_y - box_height // 2,
            box_width,
            box_height
        )
        
        # Box background (white)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, border_radius=15)
        pygame.draw.rect(self.screen, title_color, box_rect, 4, border_radius=15)
        
        # Center and draw texts
        y_offset = box_rect.y + 50
        
        title_rect = title_text.get_rect(center=(center_x, y_offset))
        self.screen.blit(title_text, title_rect)
        
        y_offset += 80
        time_rect = time_text.get_rect(center=(center_x, y_offset))
        self.screen.blit(time_text, time_rect)
        
        y_offset += 50
        moves_rect = moves_text.get_rect(center=(center_x, y_offset))
        self.screen.blit(moves_text, moves_rect)
        
        y_offset += 60
        separator_rect = separator_text.get_rect(center=(center_x, y_offset))
        self.screen.blit(separator_text, separator_rect)
        
        y_offset += 50
        restart_rect = restart_text.get_rect(center=(center_x, y_offset))
        self.screen.blit(restart_text, restart_rect)
        
        y_offset += 40
        quit_rect = quit_text.get_rect(center=(center_x, y_offset))
        self.screen.blit(quit_text, quit_rect)
