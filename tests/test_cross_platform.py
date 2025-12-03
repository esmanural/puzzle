"""
Cross-platform compatibility tests
Tests for Windows, macOS compatibility and different screen resolutions
"""

import sys
import os
import platform
import pygame
from pathlib import Path
from typing import Tuple, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from jigsaw_puzzle.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_OPTIONS, SUPPORTED_FORMATS
)
from jigsaw_puzzle.services.image_processor import ImageProcessor
from jigsaw_puzzle.ui.game_renderer import GameRenderer
from jigsaw_puzzle.models.game_state import GameState


class CrossPlatformTester:
    """Cross-platform compatibility tester"""
    
    def __init__(self):
        self.test_results = []
        self.platform_info = self._get_platform_info()
    
    def _get_platform_info(self) -> dict:
        """Get detailed platform information"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
        }
    
    def log_result(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = f"{status} - {test_name}"
        if message:
            result += f": {message}"
        self.test_results.append((passed, result))
        print(result)
    
    def test_platform_detection(self):
        """Test platform detection"""
        print("\n" + "="*60)
        print("PLATFORM DETECTION TEST")
        print("="*60)
        
        system = self.platform_info['system']
        print(f"Operating System: {system}")
        print(f"Release: {self.platform_info['release']}")
        print(f"Version: {self.platform_info['version']}")
        print(f"Machine: {self.platform_info['machine']}")
        print(f"Python Version: {self.platform_info['python_version']}")
        
        # Check if running on supported platform
        supported = system in ['Windows', 'Darwin', 'Linux']
        self.log_result(
            "Platform Detection",
            supported,
            f"Running on {system}"
        )
        
        return supported
    
    def test_file_path_handling(self):
        """Test cross-platform file path handling"""
        print("\n" + "="*60)
        print("FILE PATH HANDLING TEST")
        print("="*60)
        
        try:
            # Test pathlib usage
            test_path = Path(__file__).parent.parent / "jigsaw_puzzle" / "utils" / "constants.py"
            exists = test_path.exists()
            
            self.log_result(
                "Pathlib Path Handling",
                exists,
                f"Path exists: {test_path}"
            )
            
            # Test path separator handling
            path_str = str(test_path)
            correct_separator = os.sep in path_str or '/' in path_str
            
            self.log_result(
                "Path Separator Handling",
                correct_separator,
                f"Using correct separator for {self.platform_info['system']}"
            )
            
            return exists and correct_separator
            
        except Exception as e:
            self.log_result("File Path Handling", False, str(e))
            return False
    
    def test_pygame_initialization(self):
        """Test pygame initialization on current platform"""
        print("\n" + "="*60)
        print("PYGAME INITIALIZATION TEST")
        print("="*60)
        
        try:
            pygame.init()
            pygame.font.init()
            
            # Check pygame version
            pygame_version = pygame.version.ver
            print(f"Pygame Version: {pygame_version}")
            
            self.log_result(
                "Pygame Initialization",
                True,
                f"Version {pygame_version}"
            )
            
            pygame.quit()
            return True
            
        except Exception as e:
            self.log_result("Pygame Initialization", False, str(e))
            return False
    
    def test_screen_resolutions(self):
        """Test different screen resolutions"""
        print("\n" + "="*60)
        print("SCREEN RESOLUTION TEST")
        print("="*60)
        
        # Test resolutions to check
        test_resolutions = [
            (1400, 900),   # Default
            (1920, 1080),  # Full HD
            (1366, 768),   # Common laptop
            (1280, 720),   # HD
            (1024, 768),   # Old standard
            (2560, 1440),  # 2K
        ]
        
        try:
            pygame.init()
            
            # Get display info
            display_info = pygame.display.Info()
            current_w = display_info.current_w
            current_h = display_info.current_h
            
            print(f"Current Display: {current_w}x{current_h}")
            
            all_passed = True
            
            for width, height in test_resolutions:
                try:
                    # Only test resolutions that fit in current display
                    if width <= current_w and height <= current_h:
                        screen = pygame.display.set_mode((width, height))
                        
                        # Test layout calculations with this resolution
                        temp_state = GameState((3, 3), [])
                        renderer = GameRenderer((width, height), temp_state)
                        
                        # Verify layout areas are valid
                        valid = (
                            renderer.play_area.width > 0 and
                            renderer.play_area.height > 0 and
                            renderer.piece_pool.width > 0 and
                            renderer.piece_pool.height > 0
                        )
                        
                        self.log_result(
                            f"Resolution {width}x{height}",
                            valid,
                            "Layout calculated successfully"
                        )
                        
                        if not valid:
                            all_passed = False
                    else:
                        print(f"⚠️  SKIP - Resolution {width}x{height}: Larger than display")
                        
                except Exception as e:
                    self.log_result(
                        f"Resolution {width}x{height}",
                        False,
                        str(e)
                    )
                    all_passed = False
            
            pygame.quit()
            return all_passed
            
        except Exception as e:
            self.log_result("Screen Resolution Test", False, str(e))
            pygame.quit()
            return False
    
    def test_image_format_support(self):
        """Test supported image formats"""
        print("\n" + "="*60)
        print("IMAGE FORMAT SUPPORT TEST")
        print("="*60)
        
        print(f"Supported formats: {', '.join(SUPPORTED_FORMATS)}")
        
        # Check if PIL/Pillow is available
        try:
            from PIL import Image
            pil_version = Image.__version__ if hasattr(Image, '__version__') else "Unknown"
            print(f"PIL/Pillow Version: {pil_version}")
            
            self.log_result(
                "PIL/Pillow Available",
                True,
                f"Version {pil_version}"
            )
            
            return True
            
        except ImportError as e:
            self.log_result("PIL/Pillow Available", False, str(e))
            return False
    
    def test_tkinter_availability(self):
        """Test tkinter availability for cross-platform dialogs"""
        print("\n" + "="*60)
        print("TKINTER AVAILABILITY TEST")
        print("="*60)
        
        try:
            import tkinter as tk
            from tkinter import filedialog, messagebox
            
            # Get tkinter version
            root = tk.Tk()
            tk_version = root.tk.call('info', 'patchlevel')
            root.destroy()
            
            print(f"Tkinter Version: {tk_version}")
            
            self.log_result(
                "Tkinter Available",
                True,
                f"Version {tk_version}"
            )
            
            return True
            
        except ImportError as e:
            self.log_result("Tkinter Available", False, str(e))
            return False
    
    def test_constants_configuration(self):
        """Test constants are properly configured"""
        print("\n" + "="*60)
        print("CONSTANTS CONFIGURATION TEST")
        print("="*60)
        
        try:
            # Check screen dimensions
            valid_screen = SCREEN_WIDTH > 0 and SCREEN_HEIGHT > 0
            self.log_result(
                "Screen Dimensions",
                valid_screen,
                f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}"
            )
            
            # Check grid options
            valid_grids = len(GRID_OPTIONS) > 0 and all(
                isinstance(g, tuple) and len(g) == 2 for g in GRID_OPTIONS
            )
            self.log_result(
                "Grid Options",
                valid_grids,
                f"{len(GRID_OPTIONS)} options available"
            )
            
            # Check supported formats
            valid_formats = len(SUPPORTED_FORMATS) > 0
            self.log_result(
                "Supported Formats",
                valid_formats,
                f"{len(SUPPORTED_FORMATS)} formats"
            )
            
            return valid_screen and valid_grids and valid_formats
            
        except Exception as e:
            self.log_result("Constants Configuration", False, str(e))
            return False
    
    def test_aspect_ratio_handling(self):
        """Test aspect ratio preservation across different resolutions"""
        print("\n" + "="*60)
        print("ASPECT RATIO HANDLING TEST")
        print("="*60)
        
        try:
            pygame.init()
            
            # Test with different aspect ratios
            test_cases = [
                ((800, 600), "4:3"),
                ((1920, 1080), "16:9"),
                ((1280, 1024), "5:4"),
                ((2560, 1440), "16:9"),
            ]
            
            all_passed = True
            
            for (width, height), ratio in test_cases:
                try:
                    screen = pygame.display.set_mode((width, height))
                    temp_state = GameState((3, 3), [])
                    renderer = GameRenderer((width, height), temp_state)
                    
                    # Check if play area maintains reasonable proportions
                    play_ratio = renderer.play_area.width / renderer.play_area.height
                    valid = 0.5 < play_ratio < 2.0  # Reasonable range
                    
                    self.log_result(
                        f"Aspect Ratio {ratio} ({width}x{height})",
                        valid,
                        f"Play area ratio: {play_ratio:.2f}"
                    )
                    
                    if not valid:
                        all_passed = False
                        
                except Exception as e:
                    self.log_result(
                        f"Aspect Ratio {ratio}",
                        False,
                        str(e)
                    )
                    all_passed = False
            
            pygame.quit()
            return all_passed
            
        except Exception as e:
            self.log_result("Aspect Ratio Handling", False, str(e))
            pygame.quit()
            return False
    
    def run_all_tests(self):
        """Run all cross-platform tests"""
        print("\n" + "="*70)
        print(" "*15 + "CROSS-PLATFORM COMPATIBILITY TEST SUITE")
        print("="*70)
        
        # Run all tests
        self.test_platform_detection()
        self.test_file_path_handling()
        self.test_pygame_initialization()
        self.test_tkinter_availability()
        self.test_image_format_support()
        self.test_constants_configuration()
        self.test_screen_resolutions()
        self.test_aspect_ratio_handling()
        
        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        
        passed = sum(1 for p, _ in self.test_results if p)
        total = len(self.test_results)
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        
        if passed == total:
            print("\n🎉 All tests passed! Application is cross-platform compatible.")
        else:
            print("\n⚠️  Some tests failed. Review the results above.")
        
        return passed == total


def main():
    """Main test runner"""
    tester = CrossPlatformTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
