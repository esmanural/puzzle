"""
Jigsaw Puzzle Game - Main game file
Modern puzzle game with drag-and-drop mechanism
"""

import sys
import time
import pygame
from typing import List, Tuple
from PIL import UnidentifiedImageError

from jigsaw_puzzle.models.jigsaw_piece import JigsawPiece
from jigsaw_puzzle.models.game_state import GameState
from jigsaw_puzzle.services.image_processor import ImageProcessor
from jigsaw_puzzle.services.jigsaw_logic import JigsawLogic
from jigsaw_puzzle.ui.game_renderer import GameRenderer
from jigsaw_puzzle.ui.menu import Menu
from jigsaw_puzzle.utils.constants import (
    SCREEN_WIDTH, 
    SCREEN_HEIGHT, 
    FPS,
    GAME_MODE_CREATIVE,
    GAME_MODE_TIMED,
    GAME_MODE_CHALLENGE
)


def create_jigsaw_pieces(piece_images: List[pygame.Surface], 
                        grid_size: Tuple[int, int]) -> List[JigsawPiece]:
    """
    Creates JigsawPiece list from pygame Surface pieces
    
    Args:
        piece_images: List of pygame Surface pieces
        grid_size: Grid size (rows, cols)
        
    Returns:
        List of JigsawPiece objects
    """
    pieces = []
    rows, cols = grid_size
    piece_id = 0
    
    for row in range(rows):
        for col in range(cols):
            position = (row, col)
            piece = JigsawPiece(
                image=piece_images[piece_id],
                original_position=position,
                piece_id=piece_id
            )
            pieces.append(piece)
            piece_id += 1
    
    return pieces


def main():
    """Main game function - Modern drag-and-drop mechanism"""
    
    # 1. Show main menu (use Tkinter before initializing Pygame to avoid macOS SDL/Tk conflicts)
    print("Opening main menu...")
    if not Menu.show_main_menu():
        print("Exiting game...")
        sys.exit(0)
    
    # 2. Game mode selection
    print("Waiting for game mode selection...")
    game_mode = Menu.select_game_mode()
    
    if game_mode is None:
        print("No game mode selected. Exiting game.")
        sys.exit(0)
    
    print(f"Selected game mode: {game_mode}")
    
    # 3. Get image selection from user
    print("Waiting for image selection...")
    image_path = Menu.select_image()
    
    if image_path is None:
        print("No image selected. Exiting game.")
        sys.exit(0)
    
    print(f"Selected image: {image_path}")
    
    # 4. Get grid size selection from user
    print("Waiting for grid size selection...")
    grid_size = Menu.select_grid_size()
    
    if grid_size is None:
        print("No grid size selected. Exiting game.")
        sys.exit(0)
    
    rows, cols = grid_size
    print(f"Selected grid size: {rows}x{cols}")
    
    # 5. Initialize Pygame (after closing Tkinter windows)
    try:
        pygame.init()
        pygame.font.init()
    except pygame.error as e:
        print(f"Pygame initialization error: {e}")
        sys.exit(1)

    # 6. Create screen
    temp_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
    print(f"🪟 Window size: {screen_width}x{screen_height}")
    
    # 7. Create temporary renderer (for layout calculations)
    temp_state = GameState(grid_size, [])
    temp_renderer = GameRenderer((screen_width, screen_height), temp_state)
    
    # 8. Load image and split into pieces
    try:
        print("Loading image...")
        processor = ImageProcessor()
        
        # Load image to fit play_area and grid_size exactly
        pil_image = processor.load_image(image_path, temp_renderer.play_area, grid_size)
        
        # Create thumbnail for preview
        preview_pil = processor.create_thumbnail(pil_image, (180, 180))
        preview_surface = processor.pil_to_pygame(preview_pil)
        
        print("Splitting image into pieces...")
        pil_pieces = processor.split_image(pil_image, grid_size)
        
        # Convert PIL pieces to pygame Surfaces
        pygame_pieces = [processor.pil_to_pygame(piece) for piece in pil_pieces]
        
    except FileNotFoundError as e:
        print(f"File Error: {e}")
        pygame.quit()
        sys.exit(1)
    except UnidentifiedImageError as e:
        print(f"Image Error: {e}")
        pygame.quit()
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error while processing image: {e}")
        pygame.quit()
        sys.exit(1)
    
    # 9. Create JigsawPiece list
    print("Creating puzzle pieces...")
    pieces = create_jigsaw_pieces(pygame_pieces, grid_size)
    
    # 10. Initialize GameState, JigsawLogic and GameRenderer
    print("Starting game...")
    game_state = GameState(grid_size, pieces)
    game_state.game_mode = game_mode  # Save game mode
    logic = JigsawLogic(game_state)
    renderer = GameRenderer((screen_width, screen_height), game_state, preview_surface)
    
    # 11. Calculate correct positions for pieces and save as target_pixel_position
    piece_width = renderer.play_area.width // cols
    piece_height = renderer.play_area.height // rows
    
    for piece in pieces:
        row, col = piece.original_position
        target_x = renderer.play_area.x + col * piece_width
        target_y = renderer.play_area.y + row * piece_height
        piece.target_pixel_position = (target_x, target_y)
    
    # 12. Scatter pieces to PiecePool
    print("Shuffling pieces...")
    logic.scatter_pieces(renderer.piece_pool)
    
    # 13. Start time for time tracking
    start_time = time.time()
    
    # 14. Special settings based on game mode
    time_limit = None
    move_limit = None
    
    if game_mode == GAME_MODE_TIMED:
        # Timed mode: Set time limit based on grid size
        total_pieces = rows * cols
        time_limit = total_pieces * 30  # 30 seconds per piece
        print(f"⏱️  Time limit: {time_limit} seconds")
    
    elif game_mode == GAME_MODE_CHALLENGE:
        # Challenge mode: Set move limit based on grid size
        total_pieces = rows * cols
        move_limit = total_pieces * 3  # 3 moves per piece
        print(f"🏆 Move limit: {move_limit} moves")
    
    # 15. Main game loop
    clock = pygame.time.Clock()
    running = True
    
    print("Game started! Have fun!")
    print("Hint: Drag and drop pieces to correct positions.")
    
    while running:
        # Event handling
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                running = False
            
            # Mouse click event - Start dragging
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_state.is_completed:
                    # Find piece at clicked position
                    piece = logic.get_piece_at_position(event.pos)
                    if piece and not piece.is_placed:
                        # Start dragging
                        logic.drag_handler.start_drag(piece, event.pos)
            
            # Mouse motion - Continue dragging
            elif event.type == pygame.MOUSEMOTION:
                if logic.drag_handler.dragged_piece:
                    # Update dragged piece
                    logic.drag_handler.update_drag(event.pos)
            
            # Mouse release event - End dragging
            elif event.type == pygame.MOUSEBUTTONUP:
                if logic.drag_handler.dragged_piece:
                    # End dragging and check snap
                    placed = logic.drag_handler.end_drag()
                    if placed:
                        game_state.move_count += 1
                        completion = logic.get_completion_percentage()
                        print(f"Piece placed! Move: {game_state.move_count} | Completion: {completion:.0f}%")
                        
                        # Check completion
                        if logic.is_puzzle_solved():
                            game_state.is_completed = True
                            print(f"\n🎉 Congratulations! You completed the puzzle in {game_state.move_count} moves!")
                            print(f"⏱️  Time: {int(game_state.elapsed_time // 60):02d}:{int(game_state.elapsed_time % 60):02d}")
                            print(f"📊 Completion: 100%")
            
            # Keyboard event
            elif event.type == pygame.KEYDOWN:
                # 'N' key for new game
                if event.key == pygame.K_n and game_state.is_completed:
                    print("\n🔄 Starting new game...")
                    
                    # Reset game state
                    game_state.move_count = 0
                    game_state.is_completed = False
                    
                    # Reset all pieces
                    for piece in pieces:
                        piece.is_placed = False
                        piece.is_dragging = False
                        piece.z_index = 0
                    
                    # Redistribute pieces
                    logic.scatter_pieces(renderer.piece_pool)
                    
                    # Reset time
                    start_time = time.time()
                    
                    print("✅ New game started!")
                
                # ESC key to exit
                elif event.key == pygame.K_ESCAPE:
                    # Always exit on ESC, but cancel drag first if dragging
                    if logic.drag_handler.dragged_piece:
                        logic.drag_handler.cancel_drag()
                    else:
                        running = False
        
        # Time tracking
        game_state.elapsed_time = time.time() - start_time
        
        # Game mode check
        if not game_state.is_completed:
            # Timed mode check
            if game_mode == GAME_MODE_TIMED and time_limit:
                if game_state.elapsed_time >= time_limit:
                    game_state.is_completed = True
                    game_state.is_failed = True
                    print(f"\n⏱️  Time's up! Game over.")
                    print(f"📊 Completion: {logic.get_completion_percentage():.0f}%")
            
            # Challenge mode check
            if game_mode == GAME_MODE_CHALLENGE and move_limit:
                if game_state.move_count >= move_limit:
                    if not logic.is_puzzle_solved():
                        game_state.is_completed = True
                        game_state.is_failed = True
                        print(f"\n🏆 Move limit reached! Game over.")
                        print(f"📊 Completion: {logic.get_completion_percentage():.0f}%")
        
        # Rendering (completion percentage automatically shown in info panel)
        renderer.render()
        
        # Show completion message if game is completed
        if game_state.is_completed:
            renderer.show_completion_message()
        
        # Update screen
        pygame.display.flip()
        
        # Limit FPS
        clock.tick(FPS)
    
    # Cleanup
    print("\n👋 Exiting game...")
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
