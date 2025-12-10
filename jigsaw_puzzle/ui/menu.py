"""Menu UI component for user selections"""

from typing import Optional, Tuple, Dict
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from jigsaw_puzzle.utils.constants import (
    GRID_OPTIONS, 
    SUPPORTED_FORMATS, 
    STOCK_IMAGES_DIR,
    GAME_MODE_CREATIVE,
    GAME_MODE_TIMED,
    GAME_MODE_CHALLENGE
)


class Menu:
    """Main menu and user selections"""
    
    @staticmethod
    def show_main_menu() -> bool:
        """
        Shows enhanced main menu
        
        Returns:
            True: Start game
            False: Exit
        """
        try:
            root = tk.Tk()
            root.title("Jigsaw Puzzle Game")
            root.geometry("600x700")
            root.resizable(False, False)
            
            # Modern colors - Gradient effect
            bg_color = "#0f0c29"  # Dark purple-blue
            bg_gradient = "#302b63"  # Medium purple
            fg_color = "#ffffff"
            accent_color = "#24c6dc"  # Light blue
            button_color = "#1e3c72"  # Dark blue
            button_hover = "#2a5298"  # Medium blue
            
            root.configure(bg=bg_color)
            
            # Center window on screen
            root.update_idletasks()
            x = (root.winfo_screenwidth() // 2) - (600 // 2)
            y = (root.winfo_screenheight() // 2) - (700 // 2)
            root.geometry(f"+{x}+{y}")
            
            # Handle window close properly
            def on_closing():
                result[0] = False
                root.destroy()
            
            root.protocol("WM_DELETE_WINDOW", on_closing)
            
            result = [False]
            
            # Main container
            main_frame = tk.Frame(root, bg=bg_color)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
            
            # Title section
            title_frame = tk.Frame(main_frame, bg=bg_color)
            title_frame.pack(pady=(0, 20))
            
            title_label = tk.Label(
                title_frame,
                text="🧩 JIGSAW PUZZLE",
                font=("Segoe UI", 36, "bold"),
                bg=bg_color,
                fg=accent_color
            )
            title_label.pack()
            
            subtitle_label = tk.Label(
                title_frame,
                text="Modern Puzzle Game",
                font=("Segoe UI", 14, "italic"),
                bg=bg_color,
                fg=fg_color
            )
            subtitle_label.pack(pady=(5, 0))
            
            # Version
            version_label = tk.Label(
                title_frame,
                text="v2.3",
                font=("Segoe UI", 9),
                bg=bg_color,
                fg="#888888"
            )
            version_label.pack()
            
            # Separator line
            separator = tk.Frame(main_frame, height=2, bg=accent_color)
            separator.pack(fill=tk.X, pady=15)
            
            # Description
            desc_label = tk.Label(
                main_frame,
                text="Select your image or use stock images\nSplit into pieces and complete the puzzle!",
                font=("Segoe UI", 11),
                bg=bg_color,
                fg="#cccccc",
                justify=tk.CENTER
            )
            desc_label.pack(pady=(0, 25))
            
            # Button frame
            button_frame = tk.Frame(main_frame, bg=bg_color)
            button_frame.pack(pady=10)
            
            def on_start():
                result[0] = True
                root.destroy()
            
            def on_exit():
                result[0] = False
                root.destroy()
            
            def create_button(parent, text, command, bg, hover_bg, emoji=""):
                """Creates enhanced button"""
                btn = tk.Button(
                    parent,
                    text=f"{emoji} {text}",
                    font=("Segoe UI", 13, "bold"),
                    bg=bg,
                    fg=fg_color,
                    activebackground=hover_bg,
                    activeforeground=fg_color,
                    relief=tk.FLAT,
                    bd=0,
                    width=28,
                    height=2,
                    cursor="hand2",
                    command=command
                )
                
                def on_enter(e):
                    btn['background'] = hover_bg
                    btn['font'] = ("Segoe UI", 13, "bold")
                
                def on_leave(e):
                    btn['background'] = bg
                    btn['font'] = ("Segoe UI", 13, "bold")
                
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
                
                return btn
            
            # Start button
            start_btn = create_button(
                button_frame,
                "START GAME",
                on_start,
                button_color,
                button_hover,
                "🎮"
            )
            start_btn.pack(pady=8)
            
            # Exit button
            exit_btn = create_button(
                button_frame,
                "EXIT",
                on_exit,
                "#c0392b",
                "#e74c3c",
                "❌"
            )
            exit_btn.pack(pady=8)
            
            # Features section
            features_frame = tk.Frame(main_frame, bg=bg_color)
            features_frame.pack(pady=(25, 10))
            
            features = [
                "🖱️  Drag-and-drop mechanism",
                "🎨  Stock images and custom image support",
                "🎯  Different difficulty levels",
                "⏱️  Timed and free modes"
            ]
            
            for feature in features:
                feature_label = tk.Label(
                    features_frame,
                    text=feature,
                    font=("Segoe UI", 9),
                    bg=bg_color,
                    fg="#aaaaaa",
                    anchor=tk.W
                )
                feature_label.pack(anchor=tk.W, pady=2)
            
            # Footer info
            info_label = tk.Label(
                main_frame,
                text="© 2024 Jigsaw Puzzle Game | All rights reserved",
                font=("Segoe UI", 8),
                bg=bg_color,
                fg="#666666"
            )
            info_label.pack(side=tk.BOTTOM, pady=(15, 0))
            
            # Keyboard shortcuts
            def on_key(event):
                if event.keysym == 'Return':
                    on_start()
                elif event.keysym == 'Escape':
                    on_exit()
            
            root.bind('<Key>', on_key)
            
            # Show window
            root.mainloop()
            
            return result[0]
            
        except Exception as e:
            print(f"Main menu error: {e}")
            return True  # Continue game on error
    
    @staticmethod
    def select_image() -> Optional[str]:
        """
        Enhanced image selection menu (stock images + custom image)
        
        Returns:
            Selected image file path (str) or None if canceled
        """
        try:
            root = tk.Tk()
            root.title("Image Selection")
            root.geometry("700x600")
            root.resizable(False, False)
            
            # Modern colors
            bg_color = "#2c3e50"
            fg_color = "#ffffff"
            accent_color = "#3498db"
            button_bg = "#34495e"
            button_hover = "#4a5f7f"
            
            root.configure(bg=bg_color)
            
            # Center the window on the screen
            root.update_idletasks()
            x = (root.winfo_screenwidth() // 2) - (700 // 2)
            y = (root.winfo_screenheight() // 2) - (600 // 2)
            root.geometry(f"+{x}+{y}")
            
            selected_image = [None]
            
            # Title
            title_label = tk.Label(
                root,
                text="🖼️ Image Selection",
                font=("Segoe UI", 20, "bold"),
                bg=bg_color,
                fg=fg_color,
                pady=20
            )
            title_label.pack()
            
            # Description
            desc_label = tk.Label(
                root,
                text="Select one of the stock images or upload your own",
                font=("Segoe UI", 11),
                bg=bg_color,
                fg="#bdc3c7"
            )
            desc_label.pack(pady=(0, 20))
            
            # Stock images section
            stock_frame = tk.LabelFrame(
                root,
                text="📁 Stock Images",
                font=("Segoe UI", 12, "bold"),
                bg=bg_color,
                fg=fg_color,
                bd=2,
                relief=tk.GROOVE
            )
            stock_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)
            
            # List stock images
            stock_images = Menu._get_stock_images()
            
            if stock_images:
                # Scrollbar ile liste
                canvas = tk.Canvas(stock_frame, bg=bg_color, highlightthickness=0)
                scrollbar = tk.Scrollbar(stock_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg=bg_color)
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                for img_path in stock_images:
                    img_name = Path(img_path).name
                    
                    def select_stock(path=img_path):
                        selected_image[0] = path
                        root.destroy()
                    
                    btn = tk.Button(
                        scrollable_frame,
                        text=f"📷 {img_name}",
                        font=("Segoe UI", 10),
                        bg=button_bg,
                        fg=fg_color,
                        activebackground=button_hover,
                        activeforeground=fg_color,
                        relief=tk.FLAT,
                        bd=0,
                        width=60,
                        height=2,
                        cursor="hand2",
                        anchor=tk.W,
                        padx=20,
                        command=select_stock
                    )
                    btn.pack(pady=3, padx=10, fill=tk.X)
                    
                    # Hover effect
                    btn.bind("<Enter>", lambda e, b=btn: b.config(bg=button_hover))
                    btn.bind("<Leave>", lambda e, b=btn: b.config(bg=button_bg))
                
                canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
                scrollbar.pack(side="right", fill="y")
            else:
                no_stock_label = tk.Label(
                    stock_frame,
                    text="No stock images yet.\nYou can add images to 'assets/stock_images' folder.",
                    font=("Segoe UI", 10),
                    bg=bg_color,
                    fg="#95a5a6",
                    justify=tk.CENTER
                )
                no_stock_label.pack(pady=30)
            
            # Custom image upload button
            custom_frame = tk.Frame(root, bg=bg_color)
            custom_frame.pack(pady=15)
            
            def browse_custom():
                filetypes = [
                    ("Image files", " ".join(f"*{fmt}" for fmt in SUPPORTED_FORMATS)),
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg *.jpeg"),
                    ("BMP files", "*.bmp"),
                    ("All files", "*.*")
                ]
                
                file_path = filedialog.askopenfilename(
                    title="Select your image",
                    filetypes=filetypes
                )
                
                if file_path:
                    path = Path(file_path)
                    if path.suffix.lower() in SUPPORTED_FORMATS and path.exists():
                        selected_image[0] = str(path)
                        root.destroy()
            
            custom_btn = tk.Button(
                custom_frame,
                text="📂 Upload My Image",
                font=("Segoe UI", 12, "bold"),
                bg="#27ae60",
                fg=fg_color,
                activebackground="#2ecc71",
                activeforeground=fg_color,
                relief=tk.FLAT,
                bd=0,
                width=30,
                height=2,
                cursor="hand2",
                command=browse_custom
            )
            custom_btn.pack(pady=5)
            
            # Hover effect
            custom_btn.bind("<Enter>", lambda e: custom_btn.config(bg="#2ecc71"))
            custom_btn.bind("<Leave>", lambda e: custom_btn.config(bg="#27ae60"))
            
            # Cancel button
            cancel_btn = tk.Button(
                custom_frame,
                text="✖ Cancel",
                font=("Segoe UI", 10),
                bg="#95a5a6",
                fg=fg_color,
                activebackground="#7f8c8d",
                activeforeground=fg_color,
                relief=tk.FLAT,
                bd=0,
                width=30,
                cursor="hand2",
                command=lambda: root.destroy()
            )
            cancel_btn.pack(pady=5)
            
            # Hover effect
            cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(bg="#7f8c8d"))
            cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(bg="#95a5a6"))
            
            root.mainloop()
            
            return selected_image[0]
            
        except Exception as e:
            print(f"Image selector error: {e}")
            return None
    
    @staticmethod
    def _get_stock_images() -> list:
        """
        List images in the stock images folder
        
        Returns:
            List of paths to stock images
        """
        stock_images = []
        
        if os.path.exists(STOCK_IMAGES_DIR):
            for file in os.listdir(STOCK_IMAGES_DIR):
                file_path = os.path.join(STOCK_IMAGES_DIR, file)
                if os.path.isfile(file_path):
                    ext = Path(file).suffix.lower()
                    if ext in SUPPORTED_FORMATS:
                        stock_images.append(file_path)
        
        return sorted(stock_images)
    
    @staticmethod
    def select_game_mode() -> Optional[str]:
        """
        Game mode selection menu
        
        Returns:
            Selected game mode (creative/timed/challenge) or None
        """
        try:
            root = tk.Tk()
            root.title("Game Mode Selection")
            root.geometry("500x550")
            root.resizable(False, False)
            
            # Modern colors
            bg_color = "#2c3e50"
            fg_color = "#ffffff"
            button_bg = "#34495e"
            button_hover = "#4a5f7f"
            
            root.configure(bg=bg_color)
            
            # Center the window on the screen
            root.update_idletasks()
            x = (root.winfo_screenwidth() // 2) - (500 // 2)
            y = (root.winfo_screenheight() // 2) - (550 // 2)
            root.geometry(f"+{x}+{y}")
            
            selected_mode = [None]
            
            # Title
            title_label = tk.Label(
                root,
                text="🎮 Game Mode Selection",
                font=("Segoe UI", 20, "bold"),
                bg=bg_color,
                fg=fg_color,
                pady=25
            )
            title_label.pack()
            
            # Description
            desc_label = tk.Label(
                root,
                text="Select the mode you want to play:",
                font=("Segoe UI", 11),
                bg=bg_color,
                fg="#bdc3c7"
            )
            desc_label.pack(pady=(0, 20))
            
            # Mode buttons frame
            modes_frame = tk.Frame(root, bg=bg_color)
            modes_frame.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)
            
            def create_mode_button(mode, title, desc, emoji, color):
                """Create a mode button"""
                frame = tk.Frame(modes_frame, bg=bg_color)
                frame.pack(pady=8, fill=tk.X)
                
                def select_mode():
                    selected_mode[0] = mode
                    root.destroy()
                
                btn = tk.Button(
                    frame,
                    text=f"{emoji} {title}\n{desc}",
                    font=("Segoe UI", 11, "bold"),
                    bg=color,
                    fg=fg_color,
                    activebackground=button_hover,
                    activeforeground=fg_color,
                    relief=tk.FLAT,
                    bd=0,
                    width=45,
                    height=3,
                    cursor="hand2",
                    justify=tk.LEFT,
                    anchor=tk.W,
                    padx=20,
                    command=select_mode
                )
                btn.pack(fill=tk.X)
                
                # Hover effect
                original_color = color
                btn.bind("<Enter>", lambda e: btn.config(bg=button_hover))
                btn.bind("<Leave>", lambda e: btn.config(bg=original_color))
                
                return btn
            
            # Free Mode
            create_mode_button(
                GAME_MODE_CREATIVE,
                "FREE MODE",
                "No time limit, play comfortably",
                "🎨",
                "#27ae60"
            )
            
            # Time Attack Mode
            create_mode_button(
                GAME_MODE_TIMED,
                "TIME ATTACK",
                "Race against time, be fast!",
                "⏱️",
                "#e67e22"
            )
            
            # Challenge Mode
            create_mode_button(
                GAME_MODE_CHALLENGE,
                "CHALLENGE",
                "Complete with limited moves",
                "🏆",
                "#e74c3c"
            )
            
            # Cancel button
            cancel_btn = tk.Button(
                root,
                text="✖ Cancel",
                font=("Segoe UI", 10),
                bg="#95a5a6",
                fg=fg_color,
                activebackground="#7f8c8d",
                activeforeground=fg_color,
                relief=tk.FLAT,
                bd=0,
                width=30,
                cursor="hand2",
                command=lambda: root.destroy()
            )
            cancel_btn.pack(pady=15)
            
            # Hover effect
            cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(bg="#7f8c8d"))
            cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(bg="#95a5a6"))
            
            root.mainloop()
            
            return selected_mode[0]
            
        except Exception as e:
            print(f"Game mode selector error: {e}")
            return GAME_MODE_CREATIVE  # Default to creative mode
    
    @staticmethod
    def select_grid_size() -> Optional[Tuple[int, int]]:
        """
        Ask user to select grid size (modern tkinter UI)
        
        Returns:
            Selected grid size (rows, cols) or None if canceled
        """
        try:
            # Tkinter penceresi oluştur
            root = tk.Tk()
            root.title("Jigsaw Puzzle - Grid Size")
            root.geometry("380x520")
            root.resizable(False, False)
            
            # Modern colors
            bg_color = "#2d3436"  # Dark gray
            fg_color = "#ffffff"  # White
            accent_color = "#3498db"  # Blue
            button_bg = "#34495e"  # Medium gray
            button_hover = "#4a5f7f"  # Light gray
            
            root.configure(bg=bg_color)
            
            # Center the window on the screen
            root.update_idletasks()
            x = (root.winfo_screenwidth() // 2) - (380 // 2)
            y = (root.winfo_screenheight() // 2) - (520 // 2)
            root.geometry(f"+{x}+{y}")
            
            # Variable to store selected grid size
            selected_grid = [None]
            
            # Title label
            title_label = tk.Label(
                root,
                text="🧩 Puzzle Grid Size",
                font=("Segoe UI", 16, "bold"),
                bg=bg_color,
                fg=fg_color,
                pady=20
            )
            title_label.pack()
            
            # Description label
            info_label = tk.Label(
                root,
                text="Select difficulty level:",
                font=("Segoe UI", 11),
                bg=bg_color,
                fg=fg_color,
                pady=5
            )
            info_label.pack()
            
            # Buttons for grid options
            button_frame = tk.Frame(root, bg=bg_color)
            button_frame.pack(pady=15, padx=25, fill=tk.BOTH, expand=True)
            
            def on_grid_select(grid_size: Tuple[int, int]):
                """Called when a grid size is selected"""
                selected_grid[0] = grid_size
                root.quit()
                root.destroy()
            
            def on_enter(e, btn):
                """Mouse hover effect"""
                btn['background'] = button_hover
            
            def on_leave(e, btn):
                """Mouse leave effect"""
                btn['background'] = button_bg
            
            # Create a button for each grid option
            for i, grid_size in enumerate(GRID_OPTIONS):
                rows, cols = grid_size
                total_pieces = rows * cols
                
                # Determine difficulty level
                if total_pieces <= 9:
                    difficulty = "🟢 Easy"
                    difficulty_color = "#27ae60"
                elif total_pieces <= 16:
                    difficulty = "🟡 Medium"
                    difficulty_color = "#f39c12"
                else:
                    difficulty = "🔴 Hard"
                    difficulty_color = "#e74c3c"
                
                button_text = f"{rows} × {cols}  ({total_pieces} pieces)\n{difficulty}"
                
                btn = tk.Button(
                    button_frame,
                    text=button_text,
                    font=("Segoe UI", 10, "bold"),
                    bg=button_bg,
                    fg=fg_color,
                    activebackground=accent_color,
                    activeforeground=fg_color,
                    relief=tk.FLAT,
                    bd=0,
                    width=30,
                    height=2,
                    cursor="hand2",
                    command=lambda gs=grid_size: on_grid_select(gs)
                )
                btn.pack(pady=4)
                
                # Add hover effects
                btn.bind("<Enter>", lambda e, b=btn: on_enter(e, b))
                btn.bind("<Leave>", lambda e, b=btn: on_leave(e, b))
            
            # Cancel button
            cancel_btn = tk.Button(
                root,
                text="✖ Cancel",
                font=("Segoe UI", 10),
                bg="#95a5a6",
                fg=fg_color,
                activebackground="#7f8c8d",
                activeforeground=fg_color,
                relief=tk.FLAT,
                bd=0,
                width=20,
                cursor="hand2",
                command=lambda: root.destroy()
            )
            cancel_btn.pack(pady=15)
            
            # Hover effect for cancel button
            cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(bg="#7f8c8d"))
            cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(bg="#95a5a6"))
            
            # Show window and wait for user selection
            root.mainloop()
            
            return selected_grid[0]
            
        except Exception as e:
            print(f"Grid size selector error: {e}")
            return None
    
    @staticmethod
    def show_error(title: str, message: str):
        """
        Show an error message
        
        Args:
            title: Error title
            message: Error content
        """
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(title, message)
            root.destroy()
        except Exception as e:
            print(f"Error message could not be displayed: {e}")
            print(f"{title}: {message}")
    
    @staticmethod
    def show_info(title: str, message: str):
        """
        Show an informational message
        
        Args:
            title: Message title
            message: Message content
        """
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(title, message)
            root.destroy()
        except Exception as e:
            print(f"Info message could not be displayed: {e}")
            print(f"{title}: {message}")
