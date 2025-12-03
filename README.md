# Jigsaw Puzzle Game

A modern and visually appealing jigsaw puzzle game developed with Python. Select your own image, split it into pieces, and solve the puzzle with drag-and-drop!

## Features

### 🎮 Game Mechanics
- 🏠 **Main Menu**: Modern and user-friendly start screen
- 🖱️ **Drag & Drop**: Real puzzle experience - drag pieces with mouse and drop them in correct places
- 📍 **Smart Snap-to-Grid**: Pieces automatically snap when close to correct position
- 🎯 **Free Movement**: Move pieces anywhere, organize them in the piece pool area
- 🔄 **Z-Index Management**: Dragged piece always appears on top
- 📐 **Smart Image Scaling**: Images fit perfectly to grid size, no empty space
- 🎮 **Three Game Modes**:
  - 🎨 **Free Mode**: No time limit, play comfortably
  - ⏱️ **Time Attack**: Race against time (30 seconds per piece)
  - 🏆 **Challenge**: Complete with limited moves (3 moves per piece)

### 🎨 Modern User Interface
- 🖼️ **Two-Panel Layout**: 
  - **Play Area**: Main area where you complete the puzzle (with grid lines)
  - **Piece Pool**: Side area with mixed pieces
- ✨ **Visual Effects**:
  - Realistic shadow effects
  - Piece scaling while dragging (hover effect)
  - Placement animations
- 🎨 **Modern Color Palette**: Dark theme that's easy on the eyes
- � ***Aspect Ratio Preservation**: Images displayed at optimal size without distortion

### 📊 Information and Statistics
- ⏱️ **Time Tracking**: See how long it takes to solve the puzzle
- 📈 **Completion Percentage**: Track your progress in real-time
- 🏆 **Move Counter**: See how many moves you've made
- 🖼️ **Preview Panel**: Small preview of the original image

### � Othelr Features
- 🖼️ **Image Options**:
  - Stock images from the stock images folder
  - Upload your own image (PNG, JPG, JPEG, BMP)
- 🎮 **Different Difficulty Levels**: 2x3, 3x3, 3x4, 4x4, 4x5, 5x5 grid sizes
- 🔄 Random shuffle algorithm
- 🔁 New game feature (N key)
- ⌨️ **Keyboard Shortcuts**:
  - N: New game (after completion)
  - ESC: Exit
  - Enter: Quick selection in menus
- 💻 Cross-platform support (Windows, macOS, Linux)

## What's New

### v2.4.2 (Latest)
- ✅ **Fixed Statistics Panel**: Proper layout and alignment
- ✅ **Fixed ESC Key**: Now exits game properly
- ✅ **Optimized Layout**: Better space distribution for all UI elements
- ✅ **Compact Design**: Smaller fonts and spacing for better fit

### v2.4 - Fully English
- � **1e00% English**: Removed all Turkish language support
- ❌ **No Multi-language**: Simplified codebase, English only
- ✅ **Clean Code**: Removed translation system for better performance

### v2.3 - English Translation
- 🌐 **English by Default**: All UI elements in English
- 🔄 **Bilingual Support**: English and Turkish available
- 📝 **Translated Code**: All comments and documentation in English

### v2.2 - Game Modes & Enhanced UI/UX
- 🎮 **Game Modes**: Free, Time Attack, and Challenge modes added
- 🖼️ **Stock Images**: Quick start with ready-to-use images
- 🎨 **Enhanced UI/UX**: Modern gradient colors, animated buttons, better visual design
- ⌨️ **Keyboard Shortcuts**: Enter to start, ESC to exit

### v2.1 - Main Menu & Smart Scaling
- 🏠 **Main Menu Added**: Modern and user-friendly start screen
- 📐 **Smart Image Scaling**: Images now fit perfectly to grid size, no empty space
- 🎯 **Improved Aspect Ratio**: Images centered and cropped, full area used

### v2.0 - Modern Drag & Drop System
- 🎮 **Drag & Drop Mechanism**: Real puzzle experience
- 🎨 **Modern UI/UX**: Two-panel layout, shadow effects, hover animations
- � **Advanceİd Info Panel**: Real-time completion percentage, time tracking, move counter
- 🔧 **Technical Improvements**: Modular code, better error handling, performance optimizations

## Requirements

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### 1. Download the Project

```bash
git clone <repository-url>
cd jigsaw_puzzle
```

or download and extract the ZIP file.

### 2. Create Virtual Environment (Recommended)

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install the following packages:
- `pygame>=2.5.0` - Game engine and visualization
- `Pillow>=10.0.0` - Image processing

## Usage

### Starting the Game

```bash
python main.py
```

### Game Flow

1. **Main Menu**: When the game starts, a modern welcome screen appears. Click "START GAME" or press Enter.

2. **Game Mode Selection**: Select the mode you want to play:
   - 🎨 **Free Mode**: No time limit, play comfortably
   - ⏱️ **Time Attack**: Race against time
   - 🏆 **Challenge**: Complete with limited moves

3. **Image Selection**: Two options:
   - **Stock Images**: Select from ready-to-use images in `assets/stock_images` folder
   - **Upload Your Image**: Click "Upload My Image" to select from your computer

4. **Grid Size Selection**: Select how many pieces the puzzle will be split into:
   - 2x3 (6 pieces) - Very Easy
   - 3x3 (9 pieces) - Easy
   - 3x4 (12 pieces) - Easy-Medium
   - 4x4 (16 pieces) - Medium
   - 4x5 (20 pieces) - Medium-Hard
   - 5x5 (25 pieces) - Hard

5. **Game Screen**: 
   - **Left Side (Play Area)**: Puzzle completion area marked with grid lines
   - **Right Side (Piece Pool)**: Area with mixed pieces
   - **Top Section**: Preview panel and info panel (time, completion %, move count)

6. **Solving the Puzzle (Drag & Drop)**:
   - **Click and hold** on a piece in the Piece Pool
   - **Drag** the piece by moving the mouse
   - **Drop** the piece where you want
   - If the piece is close to the correct position, it will **automatically snap** (snap-to-grid)
   - If the piece is far from the correct position, it stays free, you can drag it again
   - Place all pieces in their correct positions

7. **Completion**: 
   - When the puzzle is completed, a success message appears on screen
   - Your total time and move count are displayed
   - Press `N` to start a new game

### Controls

#### Mouse Controls
- **Left Click + Drag**: Drag and place pieces
- **Mouse Release**: Drop piece (snap check performed)

#### Keyboard Shortcuts
- **N**: Start new game (after completion)
- **ESC**: Exit game or cancel drag
- **Enter**: Quick selection in menus

### Tips

#### General Strategies
- 🎯 **Corner and Edge Pieces**: Start with corner and edge pieces
- 🖼️ **Use Preview**: Look at the small image preview in the top right to find pieces
- 📍 **Snap Distance**: Pieces automatically snap when you bring them close to the correct position
- 🎨 **Color Groups**: Group similar colored pieces together
- 🔄 **Organize**: Organize pieces in the Piece Pool for easier finding

#### Mode-Specific Tips
- 🎨 **Free Mode**: Don't rush, think strategically
- ⏱️ **Time Attack**: Move fast, place easy pieces first
- 🏆 **Challenge**: Plan each move carefully, avoid trial and error

#### Technical Tips
- 🖱️ **Precise Dragging**: Drag pieces slowly for more precise placement

## Cross-Platform Compatibility

This game is designed to work on **Windows**, **macOS**, and **Linux** platforms.

### ✅ Tested
- **Windows 10/11**: Fully compatible, all features working
- **Different Screen Resolutions**: Tested from 1024x768 to 2560x1440

### 🔧 Platform Independent Features
- **File Paths**: Automatic platform compatibility using `pathlib.Path`
- **File Dialogs**: Native platform dialogs with Tkinter
- **Graphics Rendering**: Cross-platform visualization with Pygame
- **Image Processing**: Platform-independent image processing with PIL/Pillow

### 📊 Test Results

Automated tests successfully completed on Windows:
- ✅ 61/61 tests passed
- ✅ 100% success rate
- ✅ All screen resolutions supported
- ✅ Aspect ratio preservation working

Detailed test report: `tests/CROSS_PLATFORM_TEST_REPORT.md`

## Platform Specific Notes

### Windows ✅

**Status**: Fully compatible, tested

- Make sure Python is added to PATH
- tkinter usually comes with Python
- If you get pygame sound errors, update your sound drivers
- Your antivirus might block pygame, allow it if necessary

**Installation Issues:**
```cmd
# If pip is not found:
python -m ensurepip --upgrade

# If pygame cannot be installed:
python -m pip install --upgrade pip
pip install pygame --user
```

**Tested:**
- Windows 10 (Build 19045)
- Python 3.12.0
- Pygame 2.6.1
- Screen resolutions: 1024x768, 1280x720, 1366x768, 1920x1080

### macOS ⚠️

**Status**: Compatible (code structure is platform independent), manual testing needed

- Python 3 is usually pre-installed, but you can use Homebrew for the latest version:
  ```bash
  brew install python3
  ```
- tkinter comes with Python
- Pygame 2.0+ required for Retina display support (specified in requirements.txt)
- macOS may request security permission on first run

**M1/M2 Mac Notes:**
```bash
# If pygame cannot be installed:
arch -arm64 brew install python3
arch -arm64 pip3 install pygame Pillow
```

**Expected Compatibility:**
- ✅ File path handling (pathlib usage)
- ✅ Native macOS file dialogs (tkinter)
- ✅ Pygame rendering
- ⚠️ Manual testing recommended

### Linux (Ubuntu/Debian) ⚠️

**Status**: Compatible (using cross-platform libraries), manual testing needed

Install system dependencies:

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-tk
sudo apt-get install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

Then install Python packages:
```bash
pip3 install -r requirements.txt
```

**Note**: On Linux, tkinter must be installed as a separate package (`python3-tk`)

**Expected Compatibility:**
- ✅ File path handling (pathlib usage)
- ✅ GTK file dialogs (tkinter)
- ✅ Pygame rendering
- ⚠️ Manual testing recommended

## Project Structure

```
jigsaw_puzzle/
├── main.py                      # Main game file and game loop
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── assets/                      # Game assets
│   └── stock_images/            # Stock images folder
├── jigsaw_puzzle/               # Main package
│   ├── __init__.py
│   ├── models/                  # Data models
│   │   ├── jigsaw_piece.py      # Puzzle piece model (position, drag state)
│   │   └── game_state.py        # Game state model (time, completion %)
│   ├── services/                # Business logic services
│   │   ├── image_processor.py   # Image processing (aspect ratio preserved)
│   │   ├── jigsaw_logic.py      # Game logic (piece distribution, completion check)
│   │   └── drag_handler.py      # Drag-and-drop mechanism (snap-to-grid)
│   ├── ui/                      # User interface
│   │   ├── game_renderer.py     # Modern game visualization (two-panel layout)
│   │   ├── effects.py           # Visual effects (shadow, animation)
│   │   └── menu.py              # Menu and user selections
│   └── utils/                   # Utility tools
│       └── constants.py         # Constants and configuration (colors, sizes)
└── tests/                       # Test files
    ├── test_jigsaw_piece.py
    ├── test_game_state.py
    ├── test_image_processor.py
    ├── test_jigsaw_logic.py
    └── test_drag_handler.py
```

## Technical Details

### Drag-and-Drop Mechanism

The game uses an advanced drag-and-drop system for a realistic puzzle experience:

1. **Piece Selection**: When user clicks on a piece, z-index system selects the topmost piece
2. **Dragging**: Piece follows mouse cursor, shadow effect and scaling effect applied
3. **Snap-to-Grid**: When piece is close to correct position (default 40 pixels), it automatically snaps
4. **Free Drop**: If piece is far from correct position, it stays where dropped

### Layout System

Screen is divided into three main sections:

- **Play Area (Left, 65%)**: Grid area where puzzle is completed
- **Piece Pool (Right, 30%)**: Area with mixed pieces
- **Info Panel (Top)**: Preview, time, completion %, move count

### Visual Effects

- **Shadow Effect**: Realistic shadow for each piece (5 pixel offset)
- **Hover Effect**: Dragged piece scaled by 5%
- **Snap Animation**: Smooth transition when piece is placed
- **Modern Colors**: Dark theme that's easy on the eyes

## Running Tests

### Automated Tests

Use pytest to run tests:

```bash
# Install pytest (if not installed)
pip install pytest

# Run all tests
pytest

# Run specific test file
pytest tests/test_jigsaw_logic.py
pytest tests/test_drag_handler.py

# Run with detailed output
pytest -v

# See test coverage
pip install pytest-cov
pytest --cov=jigsaw_puzzle
```

### Cross-Platform Compatibility Tests

To verify the game works properly on your platform:

```bash
# Run automated cross-platform tests
python tests/test_cross_platform.py
```

This test checks:
- ✅ Platform detection (Windows/macOS/Linux)
- ✅ File path handling (pathlib usage)
- ✅ Pygame initialization
- ✅ Tkinter availability (for file dialogs)
- ✅ PIL/Pillow availability (for image processing)
- ✅ Different screen resolutions (from 1024x768 to 2560x1440)
- ✅ Aspect ratio preservation
- ✅ Layout calculations

**Test Results**: See `tests/CROSS_PLATFORM_TEST_REPORT.md` for detailed test report.

### Manual Tests

Follow the steps in `tests/MANUAL_TEST_GUIDE.md` to manually test the game.

## Troubleshooting

### "ModuleNotFoundError: No module named 'pygame'"

Pygame is not installed. Solution:
```bash
pip install pygame
```

### "ModuleNotFoundError: No module named 'PIL'"

Pillow is not installed. Solution:
```bash
pip install Pillow
```

### Image Selector Not Opening

tkinter might not be installed. See platform-specific installation instructions.

### Pygame Window Not Opening

- Update your graphics drivers
- Reinstall pygame: `pip uninstall pygame && pip install pygame`
- Make sure you're running in a virtual environment

### Image Not Loading

- Make sure the image format is supported (PNG, JPG, JPEG, BMP)
- Check that the image file is not corrupted
- If the file path contains non-ASCII characters, move it to a path with ASCII characters only

### Pieces Not Dragging

- Make sure pygame is installed correctly
- Check your mouse drivers
- Restart the game

### Performance Issues

- Select a smaller image (maximum 2000x2000 pixels recommended)
- Select a grid size with fewer pieces
- Close other running programs
- Update your graphics drivers

## Development

### Adding New Features

1. Select the appropriate module (models, services, ui, utils)
2. Implement the new feature
3. Write tests
4. Integrate in main.py

### Code Style

- Follow PEP 8 standards
- Add docstrings
- Use type hints
- Write modular and testable code

### Customization

You can change the following settings in `jigsaw_puzzle/utils/constants.py`:

- **Screen Size**: `SCREEN_WIDTH`, `SCREEN_HEIGHT`
- **Layout Ratios**: `PLAY_AREA_WIDTH_RATIO`, `PIECE_POOL_WIDTH_RATIO`
- **Colors**: `BACKGROUND_COLOR`, `PLAY_AREA_BG`, `PIECE_POOL_BG`
- **Snap Distance**: `SNAP_THRESHOLD` (default 40 pixels)
- **Visual Effects**: `SHADOW_OFFSET`, `HOVER_SCALE`
- **Grid Options**: Add new sizes to `GRID_OPTIONS` list
- **Stock Images**: Add images to `STOCK_IMAGES_DIR` folder

## License

This project is developed for educational purposes.

## Screenshots

<!-- Uncomment the following lines and add image files to include screenshots -->
<!-- 
### Main Game Screen
![Game Screen](screenshots/gameplay.png)

### Menu Screen
![Menu](screenshots/menu.png)

### Completion Screen
![Completion](screenshots/completion.png)
-->

## Frequently Asked Questions (FAQ)

**Q: Which image formats are supported?**  
A: PNG, JPG, JPEG, and BMP formats are supported.

**Q: What's the maximum number of pieces I can have?**  
A: By default, 5x5 (25 pieces) is the maximum size. You can add larger sizes in `constants.py`.

**Q: The game is running slow, what should I do?**  
A: Select a smaller image or use a grid size with fewer pieces. Also update your graphics drivers.

**Q: I placed a piece in the wrong place, how do I undo?**  
A: You can drag the piece again to move it anywhere. Incorrectly placed pieces won't snap to the correct position.

**Q: How do I add stock images?**  
A: Add PNG, JPG, JPEG, or BMP images to the `assets/stock_images` folder. They will automatically appear when you start the game.

## Contributing

We welcome your contributions! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push your branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Ideas
- New visual effects and animations
- Sound effects support
- Save/load feature
- Leaderboard
- Different piece shapes (classic jigsaw pieces)
- Multi-language support

## Contact

You can open an issue for questions or suggestions.

## Acknowledgments

- [Pygame](https://www.pygame.org/) - Game engine
- [Pillow](https://python-pillow.org/) - Image processing library

---

**Have fun! 🎮🧩**
