import pygame

# Color
WHITE = (255, 255, 255)
BROWN = (128,0,0)
BLACK = (0, 0, 0)
RED = (255,0,0)
S_COLOR = (255, 117, 117)
B_COLOR = (139, 236, 242)

# Text Font
AMATICSC_FONT = 'Assets/Fonts/AmaticSC-Bold.ttf'
VCR_OSD_MONO_FONT = 'Assets/Fonts/VCR_OSD_MONO.ttf'

# Menu
MENU_BACKGROUND = pygame.image.load('Assets/Images/Menu/Background.png')
IMPORT_MAP_BACKGROUND = pygame.image.load('Assets/Images/Menu/ImportMapBackground.png')
START_BUTTON_IMAGE = pygame.image.load('Assets/Images/Menu/start.png')
IMPORT_BUTTON_IMAGE = pygame.image.load('Assets/Images/Menu/Adjust_button.png')
DROPBOX_IMAGE = pygame.image.load('Assets/Images/Menu/Adjust_button.png')
UP_BUTTON_IMAGE = pygame.image.load('Assets/Images/Menu/up.png')
DOWN_BUTTON_IMAGE = pygame.image.load('Assets/Images/Menu/down.png')
TICK_IMAGE = [
	pygame.image.load('Assets/Images/Menu/checkbox-unchecked.png'),
	pygame.image.load('Assets/Images/Menu/checkbox-checked.png')
]
CLOSE_BUTTON = pygame.image.load('Assets/Images/Menu/CloseButton.png')

# In Game
INGAME_BACKGROUND = pygame.image.load('Assets/Images/InGame/Background.png')
CELL_IMAGE_LIST = [pygame.image.load(f'Assets/Images/InGame/Cell/tile-{i}.png') for i in range(1, 6)]
CELL_IMAGE_CHEST = pygame.image.load(f'Assets/Images/InGame/Cell/chest.png')
CELL_IMAGE_UNEXPLORED = pygame.image.load(f'Assets/Images/InGame/Cell/unexplored-tile.png')
CELL_IMAGE_PIT = pygame.image.load(f'Assets/Images/InGame/Cell/pit.png')
CELL_IMAGE_WUMPUS = pygame.image.load(f'Assets/Images/InGame/Cell/wumpus.png')
CELL_IMAGE_EXIT = pygame.image.load(f'Assets/Images/InGame/Cell/exit.png')

COLOR_AGENT = (228, 185, 36)

# {'UP': 0, 'RIGHT': 1, 'DOWN': 2, 'LEFT': 3}
AGENT_FRAME_LIST = [
	[pygame.image.load(f'Assets/Images/InGame/Agent/agent-up-{j}.png') for j in range(3)],
	[pygame.image.load(f'Assets/Images/InGame/Agent/agent-right-{j}.png') for j in range(3)],
	[pygame.image.load(f'Assets/Images/InGame/Agent/agent-down-{j}.png') for j in range(3)],
	[pygame.image.load(f'Assets/Images/InGame/Agent/agent-left-{j}.png') for j in range(3)],
]

PAUSE_BUTTON = [
	pygame.image.load('Assets/Images/InGame/Pause_button.png'),
	pygame.image.load('Assets/Images/InGame/Continue_button.png')
]
MENU_BUTTON = pygame.image.load('Assets/Images/InGame/Menu_button.png')
LEFT_BUTTON = pygame.image.load('Assets/Images/InGame/left_preview.png')
RIGHT_BUTTON = pygame.image.load('Assets/Images/InGame/right_preview.png')



