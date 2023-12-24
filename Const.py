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
