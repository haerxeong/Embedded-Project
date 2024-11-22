import time
import board
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

# 디스플레이 설정
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
width = disp.width
height = disp.height
image = Image.new("RGBA", (width, height))
draw = ImageDraw.Draw(image)

# 캐릭터 설정
character = Image.open("chiikawa.png").convert("RGBA").resize((70, 70))

# 픽셀 데이터 확인
# print(character.mode)  # RGBA여야 함
# print(character.getpixel((0, 0)))  # 예: (255, 255, 255, 0) → 알파 값이 0은 투명

character_x = 0 # 초기 위치
character_y = height - 50 - 70 + 10  # 바닥 이미지 위에 위치하도록 캐릭터 높이만큼 뺌 
move_speed = 20  # 이동 속도 증가
jump_speed = 15  # 점프 속도 감소
gravity = 2
is_jumping = False
jump_velocity = 0

# 바닥 이미지 설정
ground = Image.open("ground.png").resize((width, 50))

# 게임 루프
while True:
    # 입력 처리
    if not button_L.value:
        character_x -= move_speed
    if not button_R.value:
        character_x += move_speed
    if not button_U.value and not is_jumping:
        is_jumping = True
        jump_velocity = -jump_speed

    # 캐릭터가 화면 밖으로 나가지 않도록 x 좌표 제한
    if character_x < 0:
        character_x = 0
    if character_x > width - character.width:
        character_x = width - character.width

    # 점프 처리
    if is_jumping:
        character_y += jump_velocity
        jump_velocity += gravity
        if character_y >= height - 50 - 70 + 10:  # 바닥 이미지 위에 위치하도록 설정
            character_y = height - 50 - 70 + 10
            is_jumping = False
        elif character_y < 0:  # 캐릭터가 화면을 벗어나지 않도록 y 좌표 제한
            character_y = 0
            jump_velocity = 0

    # 화면 그리기
    draw.rectangle((0, 0, width, height), outline=0, fill=(135, 206, 235))  # 하늘색 배경
    image.paste(ground, (0, height - 50))
    image.paste(character, (character_x, character_y), mask=character)
    disp.image(image)

    time.sleep(0.01)