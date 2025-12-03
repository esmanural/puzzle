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
    """Modern pygame kullanarak oyunu render eder"""
    
    def __init__(self, screen_size: Tuple[int, int], game_state: GameState, 
                 preview_image: Optional[pygame.Surface] = None):
        """
        GameRenderer constructor
        
        Args:
            screen_size: Ekran boyutu (width, height)
            game_state: Oyun durumu
            preview_image: Önizleme için orijinal resim (opsiyonel)
        """
        self.screen_size = screen_size
        self.game_state = game_state
        self.screen = pygame.display.set_mode(screen_size)
        self.effects = Effects()
        self.preview_image = preview_image  # Önizleme için orijinal resim
        
        # Pencere başlığını ayarla
        rows, cols = game_state.grid_size
        pygame.display.set_caption(f"Jigsaw Puzzle Game - {rows}x{cols}")
        
        # Layout hesaplamaları
        self.play_area: Optional[pygame.Rect] = None
        self.piece_pool: Optional[pygame.Rect] = None
        self.preview_area: Optional[pygame.Rect] = None
        self.info_area: Optional[pygame.Rect] = None
        
        self._calculate_layout()
    
    def _calculate_layout(self):
        """
        Ekran layout'unu hesapla (PlayArea, PiecePool, Preview, Info)
        
        Layout yapısı:
        - Sol taraf (%65): PlayArea - yapboz tamamlama alanı
        - Sağ taraf (%30): PiecePool (üst), Preview (orta), Info (alt)
        """
        screen_width, screen_height = self.screen_size
        
        # PlayArea (sol taraf - yapboz tamamlama alanı)
        # Ekranın %65'ini kaplar, tüm yüksekliği kullanır
        play_area_width = int(screen_width * PLAY_AREA_WIDTH_RATIO)
        self.play_area = pygame.Rect(
            MARGIN,
            MARGIN,
            play_area_width - MARGIN * 2,
            screen_height - MARGIN * 2
        )
        
        # Sağ taraf için başlangıç x koordinatı
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
        Ana render metodu - tüm oyun ekranını çizer
        
        Çizim sırası:
        1. Arka plan
        2. PlayArea (grid + yerleştirilmiş parçalar)
        3. PiecePool (karışık parçalar)
        4. Preview (önizleme)
        5. Info Panel (bilgiler)
        """
        # Arka planı temizle
        self.screen.fill(BACKGROUND_COLOR)
        
        # PlayArea'yı çiz (grid + yerleştirilmiş parçalar)
        self.draw_play_area()
        
        # PiecePool'u çiz (karışık parçalar)
        self.draw_piece_pool()
        
        # Önizleme ve bilgi panelini çiz
        self.draw_preview()
        self.draw_info_panel()
    
    def draw_play_area(self):
        """
        PlayArea'yı çizer (grid çizgileri + yerleştirilmiş parçalar)
        
        PlayArea, yapboz parçalarının doğru konumlarına yerleştirileceği alandır.
        Grid çizgileri parça sınırlarını gösterir.
        """
        # PlayArea arka planı
        pygame.draw.rect(self.screen, PLAY_AREA_BG, self.play_area)
        
        # Grid çizgilerini çiz
        rows, cols = self.game_state.grid_size
        
        # Parça boyutlarını hesapla
        piece_width = self.play_area.width // cols
        piece_height = self.play_area.height // rows
        
        # Dikey çizgiler (sütunlar arası)
        for col in range(1, cols):
            x = self.play_area.x + col * piece_width
            pygame.draw.line(
                self.screen,
                GRID_LINE_COLOR,
                (x, self.play_area.y),
                (x, self.play_area.bottom),
                GRID_LINE_WIDTH
            )
        
        # Yatay çizgiler (satırlar arası)
        for row in range(1, rows):
            y = self.play_area.y + row * piece_height
            pygame.draw.line(
                self.screen,
                GRID_LINE_COLOR,
                (self.play_area.x, y),
                (self.play_area.right, y),
                GRID_LINE_WIDTH
            )
        
        # PlayArea çerçevesi
        pygame.draw.rect(self.screen, GRID_LINE_COLOR, self.play_area, GRID_LINE_WIDTH)
        
        # Yerleştirilmiş parçaları çiz
        for piece in self.game_state.pieces:
            if piece.is_placed:
                self.draw_piece(piece)
    
    def draw_piece_pool(self):
        """
        PiecePool'u çizer (karışık parçalar alanı)
        
        PiecePool, henüz yerleştirilmemiş parçaların bulunduğu alandır.
        Parçalar z-index'e göre sıralanır (sürüklenen parça en üstte).
        """
        # PiecePool arka planı
        pygame.draw.rect(self.screen, PIECE_POOL_BG, self.piece_pool)
        
        # PiecePool çerçevesi
        pygame.draw.rect(self.screen, GRID_LINE_COLOR, self.piece_pool, GRID_LINE_WIDTH)
        
        # Henüz yerleştirilmemiş parçaları çiz
        # Z-index'e göre sırala (alttakiler önce çizilsin, üsttekiler en son)
        unplaced_pieces = [p for p in self.game_state.pieces if not p.is_placed]
        sorted_pieces = sorted(unplaced_pieces, key=lambda p: p.z_index)
        
        for piece in sorted_pieces:
            self.draw_piece(piece)
    
    def draw_piece(self, piece: JigsawPiece):
        """
        Tek bir parçayı gölge efektiyle çizer
        
        Args:
            piece: Çizilecek yapboz parçası
            
        Sürüklenen parçalar için:
        - Gölge efekti eklenir
        - Hafif büyütme efekti uygulanır (hover effect)
        
        Normal parçalar için:
        - Doğrudan çizilir
        """
        if piece.pixel_position is None:
            return
        
        # Parça rect'i oluştur
        piece_rect = pygame.Rect(
            piece.pixel_position[0],
            piece.pixel_position[1],
            piece.image.get_width(),
            piece.image.get_height()
        )
        
        # Gölge efekti ve hover efekti (sürükleniyorsa)
        if piece.is_dragging:
            # Gölge çiz
            self.effects.draw_shadow(self.screen, piece_rect)
            
            # Hover efekti uygula (hafif büyütme)
            scaled_image = self.effects.apply_hover_effect(piece.image)
            
            # Büyütülmüş parçayı merkeze hizala
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
            # Normal çizim (gölge yok, büyütme yok)
            self.screen.blit(piece.image, piece.pixel_position)
    
    def draw_preview(self):
        """
        Orijinal resmin küçük önizlemesini çizer
        
        Önizleme, kullanıcının tamamlanmış resmi görmesini sağlar.
        Resim aspect ratio korunarak preview_area'ya sığdırılır.
        """
        # Önizleme arka planı (beyaz)
        pygame.draw.rect(self.screen, (255, 255, 255), self.preview_area)
        
        # Eğer önizleme resmi varsa, onu çiz
        if self.preview_image:
            # Resmi preview_area'ya sığdır (aspect ratio koruyarak)
            preview_width = self.preview_area.width - 10  # 5px padding her yandan
            preview_height = self.preview_area.height - 10
            
            # Orijinal resim boyutları
            img_width = self.preview_image.get_width()
            img_height = self.preview_image.get_height()
            
            # Aspect ratio hesapla
            scale_x = preview_width / img_width
            scale_y = preview_height / img_height
            scale = min(scale_x, scale_y)
            
            # Yeni boyutlar
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resmi ölçeklendir
            scaled_preview = pygame.transform.smoothscale(
                self.preview_image, 
                (new_width, new_height)
            )
            
            # Merkeze hizala
            x = self.preview_area.x + (self.preview_area.width - new_width) // 2
            y = self.preview_area.y + (self.preview_area.height - new_height) // 2
            
            self.screen.blit(scaled_preview, (x, y))
        else:
            # Önizleme resmi yoksa "Preview" yazısı göster
            font = pygame.font.Font(None, 24)
            text = font.render("Preview", True, (100, 100, 100))
            text_rect = text.get_rect(
                center=(self.preview_area.centerx, self.preview_area.centery)
            )
            self.screen.blit(text, text_rect)
        
        # Önizleme çerçevesi
        pygame.draw.rect(self.screen, GRID_LINE_COLOR, self.preview_area, 2)
    
    def draw_info_panel(self):
        """
        Bilgi panelini çizer (süre, tamamlanma %, hamle sayısı)
        
        Bilgi paneli oyun istatistiklerini gösterir:
        - Geçen süre (dakika:saniye formatında)
        - Tamamlanma yüzdesi (yerleştirilmiş parça sayısına göre)
        - Hamle sayısı (toplam sürükleme-bırakma işlemi)
        """
        # Bilgi paneli arka planı (koyu gri)
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
        
        # Yarı saydam arka plan oluştur
        overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Koyu yarı saydam
        self.screen.blit(overlay, (0, 0))
        
        # Mesaj kutusu oluştur
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
        
        # Kutu arka planı (beyaz)
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, border_radius=15)
        pygame.draw.rect(self.screen, title_color, box_rect, 4, border_radius=15)
        
        # Metinleri ortala ve çiz
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
