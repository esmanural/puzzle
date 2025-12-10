"""Image processing service for loading and splitting images"""

from typing import List, Tuple
from PIL import Image, UnidentifiedImageError
import pygame


class ImageProcessor:
    """Handles image loading and splitting into pieces"""
    
    @staticmethod
    def load_image(file_path: str, target_area: pygame.Rect, grid_size: Tuple[int, int]) -> Image.Image:
        """
        Load image and scale it to perfectly fill target_area based on grid_size.
        Aspect ratio is preserved and scaled to avoid empty spaces.
        
        Args:
            file_path: Path to the image file
            target_area: Target area (pygame.Rect)
            grid_size: Grid size (rows, cols) used to derive piece sizes
            
        Returns:
            PIL Image scaled to fit the grid exactly
            
        Raises:
            FileNotFoundError: When the file cannot be found
            UnidentifiedImageError: When the image format is invalid
        """
        try:
            image = Image.open(file_path)
            
            rows, cols = grid_size
            
            # Get target dimensions
            target_width = target_area.width
            target_height = target_area.height
            
            # Compute each piece size
            piece_width = target_width // cols
            piece_height = target_height // rows
            
            # Compute final image size based on piece count
            # Ensures no empty space remains
            final_width = piece_width * cols
            final_height = piece_height * rows
            
            # Scale while preserving aspect ratio
            img_ratio = image.width / image.height
            target_ratio = final_width / final_height
            
            if img_ratio > target_ratio:
                # Image is wider: scale by height and crop
                scale = final_height / image.height
                new_width = int(image.width * scale)
                new_height = final_height
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Center crop
                left = (new_width - final_width) // 2
                image = image.crop((left, 0, left + final_width, final_height))
            else:
                # Image is taller: scale by width and crop
                scale = final_width / image.width
                new_width = final_width
                new_height = int(image.height * scale)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Center crop
                top = (new_height - final_height) // 2
                image = image.crop((0, top, final_width, top + final_height))
            
            return image
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Image file not found: {file_path}")
        except UnidentifiedImageError:
            raise UnidentifiedImageError(f"Invalid image format: {file_path}")
    
    @staticmethod
    def split_image(image: Image.Image, grid_size: Tuple[int, int]) -> List[Image.Image]:
        """
        Split the image into equal pieces based on grid_size
        
        Args:
            image: PIL Image to be split
            grid_size: Grid size (rows, cols)
            
        Returns:
            List of PIL Image pieces (left-to-right, top-to-bottom)
        """
        rows, cols = grid_size
        width, height = image.size
        
        piece_width = width // cols
        piece_height = height // rows
        
        pieces = []
        
        for row in range(rows):
            for col in range(cols):
                # Top-left coordinates of each piece
                left = col * piece_width
                top = row * piece_height
                right = left + piece_width
                bottom = top + piece_height
                
                # Crop the piece
                piece = image.crop((left, top, right, bottom))
                pieces.append(piece)
        
        return pieces
    
    @staticmethod
    def pil_to_pygame(pil_image: Image.Image) -> pygame.Surface:
        """
        Convert PIL Image to pygame Surface
        
        Args:
            pil_image: PIL Image
            
        Returns:
            pygame Surface
        """
        # Convert PIL Image to RGB mode
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Convert PIL Image to string buffer
        image_string = pil_image.tobytes()
        size = pil_image.size
        
        # Create pygame Surface
        surface = pygame.image.fromstring(image_string, size, 'RGB')
        
        return surface
    
    @staticmethod
    def create_thumbnail(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """
        Create a small thumbnail for preview
        
        Args:
            image: PIL Image
            size: Thumbnail size (width, height)
            
        Returns:
            Thumbnail PIL Image
        """
        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        return thumbnail
