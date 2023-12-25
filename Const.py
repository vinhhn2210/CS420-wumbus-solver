import pygame

# Color
WHITE = (255, 255, 255)
BROWN = (128,0,0)
BLACK = (0, 0, 0)
RED = (255,0,0)

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

COLOR_AGENT = (228, 185, 36)

AGENT_FRAME_LIST = [
	[pygame.image.load(f'Assets/Images/InGame/Agent/agent-left-{j}.png') for j in range(3)],
	[pygame.image.load(f'Assets/Images/InGame/Agent/agent-right-{j}.png') for j in range(3)],
	[pygame.image.load(f'Assets/Images/InGame/Agent/agent-down-{j}.png') for j in range(3)],
	[pygame.image.load(f'Assets/Images/InGame/Agent/agent-up-{j}.png') for j in range(3)],
]



