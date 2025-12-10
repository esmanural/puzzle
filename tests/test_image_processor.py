"""Unit tests for ImageProcessor class"""

import unittest
import os
import pygame
from PIL import Image
from jigsaw_puzzle.services.image_processor import ImageProcessor


class TestImageProcessor(unittest.TestCase):
    """Unit tests for ImageProcessor class"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize pygame and create test images"""
        pygame.init()
        
        # Create a simple test image
        cls.test_image_path = 'test_image.png'
        test_img = Image.new('RGB', (400, 400), color='red')
        test_img.save(cls.test_image_path)
        
        # Create images of different sizes for aspect ratio tests
        cls.wide_image_path = 'test_wide_image.png'
        wide_img = Image.new('RGB', (800, 400), color='blue')
        wide_img.save(cls.wide_image_path)
        
        cls.tall_image_path = 'test_tall_image.png'
        tall_img = Image.new('RGB', (400, 800), color='green')
        tall_img.save(cls.tall_image_path)
    
    @classmethod
    def tearDownClass(cls):
        """Quit pygame and delete test images"""
        pygame.quit()
        for path in [cls.test_image_path, cls.wide_image_path, cls.tall_image_path]:
            if os.path.exists(path):
                os.remove(path)
    
    def test_load_image_success(self):
        """Image should load successfully"""
        target_area = pygame.Rect(0, 0, 200, 200)
        grid_size = (2, 2)
        image = ImageProcessor.load_image(self.test_image_path, target_area, grid_size)
        self.assertIsNotNone(image)
        self.assertEqual(image.size, (200, 200))
    
    def test_load_image_file_not_found(self):
        """Raise FileNotFoundError for missing file"""
        target_area = pygame.Rect(0, 0, 200, 200)
        grid_size = (2, 2)
        with self.assertRaises(FileNotFoundError):
            ImageProcessor.load_image('nonexistent.png', target_area, grid_size)
    
    def test_load_image_aspect_ratio_wide(self):
        """For wide image, should fit the grid exactly"""
        target_area = pygame.Rect(0, 0, 400, 400)
        grid_size = (2, 2)
        image = ImageProcessor.load_image(self.wide_image_path, target_area, grid_size)
        
        # Should fit the grid exactly (no empty space)
        # 400x400 area, 2x2 grid -> each piece 200x200 -> total 400x400
        self.assertEqual(image.width, 400)
        self.assertEqual(image.height, 400)
    
    def test_load_image_aspect_ratio_tall(self):
        """For tall image, should fit the grid exactly"""
        target_area = pygame.Rect(0, 0, 400, 400)
        grid_size = (2, 2)
        image = ImageProcessor.load_image(self.tall_image_path, target_area, grid_size)
        
        # Should fit the grid exactly (no empty space)
        # 400x400 area, 2x2 grid -> each piece 200x200 -> total 400x400
        self.assertEqual(image.width, 400)
        self.assertEqual(image.height, 400)
    
    def test_load_image_aspect_ratio_square(self):
        """For square image, should fit the grid exactly"""
        target_area = pygame.Rect(0, 0, 300, 300)
        grid_size = (3, 3)
        image = ImageProcessor.load_image(self.test_image_path, target_area, grid_size)
        
        # Should fit the grid exactly
        # 300x300 area, 3x3 grid -> each piece 100x100 -> total 300x300
        self.assertEqual(image.width, 300)
        self.assertEqual(image.height, 300)
    
    def test_load_image_max_size_fit(self):
        """Image should fit grid size exactly"""
        target_area = pygame.Rect(0, 0, 600, 400)
        grid_size = (2, 3)
        image = ImageProcessor.load_image(self.wide_image_path, target_area, grid_size)
        
        # Should fit the grid exactly
        # 600x400 area, 2x3 grid -> each piece 200x200 -> total 600x400
        self.assertEqual(image.width, 600)
        self.assertEqual(image.height, 400)
        
        # Should not exceed target area
        self.assertLessEqual(image.width, target_area.width)
        self.assertLessEqual(image.height, target_area.height)
    
    def test_split_image_correct_count(self):
        """Image should split into correct number of pieces"""
        image = Image.new('RGB', (400, 400), color='blue')
        pieces = ImageProcessor.split_image(image, (2, 2))
        
        self.assertEqual(len(pieces), 4)
        
        # Each piece should have correct size
        for piece in pieces:
            self.assertEqual(piece.size, (200, 200))
    
    def test_split_image_different_grid(self):
        """Should work correctly for different grid sizes"""
        image = Image.new('RGB', (600, 400), color='green')
        pieces = ImageProcessor.split_image(image, (2, 3))
        
        self.assertEqual(len(pieces), 6)
        
        # Each piece should have correct size (600/3=200, 400/2=200)
        for piece in pieces:
            self.assertEqual(piece.size, (200, 200))
    
    def test_pil_to_pygame_conversion(self):
        """PIL Image should convert to pygame Surface"""
        pil_image = Image.new('RGB', (100, 100), color='yellow')
        surface = ImageProcessor.pil_to_pygame(pil_image)
        
        self.assertIsInstance(surface, pygame.Surface)
        self.assertEqual(surface.get_size(), (100, 100))
    
    def test_pil_to_pygame_rgba_conversion(self):
        """RGBA PIL Image should convert to RGB and pygame Surface"""
        pil_image = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        surface = ImageProcessor.pil_to_pygame(pil_image)
        
        self.assertIsInstance(surface, pygame.Surface)
        self.assertEqual(surface.get_size(), (100, 100))
    
    def test_create_thumbnail(self):
        """Should create thumbnail"""
        image = Image.new('RGB', (400, 400), color='purple')
        thumbnail = ImageProcessor.create_thumbnail(image, (100, 100))
        
        self.assertIsNotNone(thumbnail)
        # Thumbnail size should be less than or equal to requested size
        self.assertLessEqual(thumbnail.width, 100)
        self.assertLessEqual(thumbnail.height, 100)
    
    def test_create_thumbnail_aspect_ratio(self):
        """Thumbnail should preserve aspect ratio"""
        image = Image.new('RGB', (800, 400), color='orange')
        thumbnail = ImageProcessor.create_thumbnail(image, (200, 200))
        
        # Orijinal aspect ratio: 2.0
        original_ratio = 800 / 400
        thumbnail_ratio = thumbnail.width / thumbnail.height
        self.assertAlmostEqual(original_ratio, thumbnail_ratio, places=1)


if __name__ == '__main__':
    unittest.main()
