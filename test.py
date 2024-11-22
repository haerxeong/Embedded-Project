import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

# 디스플레이 생성
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# 입력 핀 설정
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT

# 백라이트 켜기
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# 그리기 위한 빈 이미지 생성
# 색상을 위해 'RGB' 모드로 이미지 생성
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))

# 이미지에 그리기 위한 객체 가져오기
draw = ImageDraw.Draw(image)

# 디스플레이 초기화
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
disp.image(image)

# 이미지에 그리기 위한 객체 가져오기
draw = ImageDraw.Draw(image)

# 이미지를 초기화하기 위해 검은색 채우기
draw.rectangle((0, 0, width, height), outline=0, fill=0)

udlr_fill = "#00FF00"
udlr_outline = "#00FFFF"
button_fill = "#FF00FF"
button_outline = "#FFFFFF"

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

while True:
    up_fill = 0
    if not button_U.value:  # 위 버튼 눌림
        up_fill = udlr_fill
    draw.polygon(
        [(40, 40), (60, 4), (80, 40)], outline=udlr_outline, fill=up_fill
    )  # 위

    down_fill = 0
    if not button_D.value:  # 아래 버튼 눌림
        down_fill = udlr_fill
    draw.polygon(
        [(60, 120), (80, 84), (40, 84)], outline=udlr_outline, fill=down_fill
    )  # 아래

    left_fill = 0
    if not button_L.value:  # 왼쪽 버튼 눌림
        left_fill = udlr_fill
    draw.polygon(
        [(0, 60), (36, 42), (36, 81)], outline=udlr_outline, fill=left_fill
    )  # 왼쪽

    right_fill = 0
    if not button_R.value:  # 오른쪽 버튼 눌림
        right_fill = udlr_fill
    draw.polygon(
        [(120, 60), (84, 42), (84, 82)], outline=udlr_outline, fill=right_fill
    )  # 오른쪽

    center_fill = 0
    if not button_C.value:  # 중앙 버튼 눌림
        center_fill = button_fill
    draw.rectangle((40, 44, 80, 80), outline=button_outline, fill=center_fill)  # 중앙

    A_fill = 0
    if not button_A.value:  # A 버튼 눌림
        A_fill = button_fill
    draw.ellipse((140, 80, 180, 120), outline=button_outline, fill=A_fill)  # A 버튼

    B_fill = 0
    if not button_B.value:  # B 버튼 눌림
        B_fill = button_fill
    draw.ellipse((190, 40, 230, 80), outline=button_outline, fill=B_fill)  # B 버튼

    # 랜덤 색상 생성 및 텍스트 출력
    rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
    draw.text((20, 150), "Hello World", font=fnt, fill=rcolor)
    rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
    draw.text((20, 180), "Hello World", font=fnt, fill=rcolor)
    rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
    draw.text((20, 210), "Hello World", font=fnt, fill=rcolor)

    # 이미지 디스플레이
    disp.image(image)

    time.sleep(0.01)