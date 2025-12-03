"""Image processing service for loading and splitting images"""

from typing import List, Tuple
from PIL import Image, UnidentifiedImageError
import pygame


class ImageProcessor:
    """Resim yükleme ve parçalara bölme işlemlerini yapar"""
    
    @staticmethod
    def load_image(file_path: str, target_area: pygame.Rect, grid_size: Tuple[int, int]) -> Image.Image:
        """
        Resmi yükler ve grid_size'a göre tam olarak target_area'yı dolduracak şekilde ölçeklendirir.
        Aspect ratio korunur ve boşluk kalmayacak şekilde maksimum boyutta ölçeklenir.
        
        Args:
            file_path: Resim dosyasının yolu
            target_area: Hedef alan (pygame.Rect)
            grid_size: Grid boyutu (rows, cols) - parça boyutlarını hesaplamak için
            
        Returns:
            PIL Image objesi (grid'e tam oturacak şekilde ölçeklenmiş)
            
        Raises:
            FileNotFoundError: Dosya bulunamazsa
            UnidentifiedImageError: Geçersiz resim formatıysa
        """
        try:
            image = Image.open(file_path)
            
            rows, cols = grid_size
            
            # Hedef boyutları al
            target_width = target_area.width
            target_height = target_area.height
            
            # Her parçanın boyutunu hesapla
            piece_width = target_width // cols
            piece_height = target_height // rows
            
            # Toplam resim boyutunu parça sayısına göre hesapla
            # Bu sayede boşluk kalmaz
            final_width = piece_width * cols
            final_height = piece_height * rows
            
            # Aspect ratio'yu koruyarak ölçeklendir
            img_ratio = image.width / image.height
            target_ratio = final_width / final_height
            
            if img_ratio > target_ratio:
                # Resim daha geniş, yüksekliğe göre ölçeklendir ve kırp
                scale = final_height / image.height
                new_width = int(image.width * scale)
                new_height = final_height
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Ortadan kırp
                left = (new_width - final_width) // 2
                image = image.crop((left, 0, left + final_width, final_height))
            else:
                # Resim daha uzun, genişliğe göre ölçeklendir ve kırp
                scale = final_width / image.width
                new_width = final_width
                new_height = int(image.height * scale)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Ortadan kırp
                top = (new_height - final_height) // 2
                image = image.crop((0, top, final_width, top + final_height))
            
            return image
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Resim dosyası bulunamadı: {file_path}")
        except UnidentifiedImageError:
            raise UnidentifiedImageError(f"Geçersiz resim formatı: {file_path}")
    
    @staticmethod
    def split_image(image: Image.Image, grid_size: Tuple[int, int]) -> List[Image.Image]:
        """
        Resmi grid_size'a göre eşit parçalara böler
        
        Args:
            image: Bölünecek PIL Image objesi
            grid_size: Grid boyutu (rows, cols)
            
        Returns:
            PIL Image parçalarının listesi (soldan sağa, yukarıdan aşağıya)
        """
        rows, cols = grid_size
        width, height = image.size
        
        piece_width = width // cols
        piece_height = height // rows
        
        pieces = []
        
        for row in range(rows):
            for col in range(cols):
                # Her parçanın sol üst köşe koordinatları
                left = col * piece_width
                top = row * piece_height
                right = left + piece_width
                bottom = top + piece_height
                
                # Parçayı kes
                piece = image.crop((left, top, right, bottom))
                pieces.append(piece)
        
        return pieces
    
    @staticmethod
    def pil_to_pygame(pil_image: Image.Image) -> pygame.Surface:
        """
        PIL Image'ı pygame Surface'e dönüştürür
        
        Args:
            pil_image: PIL Image objesi
            
        Returns:
            pygame Surface objesi
        """
        # PIL Image'ı RGB moduna çevir
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # PIL Image'ı string buffer'a çevir
        image_string = pil_image.tobytes()
        size = pil_image.size
        
        # pygame Surface oluştur
        surface = pygame.image.fromstring(image_string, size, 'RGB')
        
        return surface
    
    @staticmethod
    def create_thumbnail(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """
        Önizleme için küçük thumbnail oluşturur
        
        Args:
            image: PIL Image objesi
            size: Thumbnail boyutu (width, height)
            
        Returns:
            Thumbnail PIL Image objesi
        """
        thumbnail = image.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        return thumbnail
