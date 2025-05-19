# Configurações de exibição
DEFAULT_IMAGE_SIZE = (300, 300)
FPS = 120
HEIGHT = 1000
WIDTH = 1600
START_X, START_Y = 0, -300
X_OFFSET, Y_OFFSET = 20, 0

# Imagens
BG_IMAGE_PATH = 'graphics/0/bg.png'
GRID_IMAGE_PATH = 'graphics/0/gridline.png'
GAME_INDICES = [1, 2, 3]  # 0 e 4 estão fora da área de jogo
SYM_PATH = 'graphics/0/symbols'

# Texto
TEXT_COLOR = 'White'
# Você precisa fornecer sua própria fonte no diretório abaixo
# Baixei a fonte Kidspace em https://www.dafont.com/kidspace.font
UI_FONT = 'graphics/font/kidspace.ttf'
UI_FONT_SIZE = 30
WIN_FONT_SIZE = 110

# 4 símbolos para mais vitórias
symbols = {
    'diamond':   f"{SYM_PATH}/0_diamond.png",
    'floppy':    f"{SYM_PATH}/0_floppy.png",
    'hourglass': f"{SYM_PATH}/0_hourglass.png",
    'hourglass2':f"{SYM_PATH}/0_hourglass.png",
    'telephone': f"{SYM_PATH}/0_telephone.png"
}