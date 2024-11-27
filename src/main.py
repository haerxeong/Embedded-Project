import time
import board
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

def character_select(disp, width, height):
    # 캐릭터 이미지 로드
    characters = [
        Image.open("../assets/chiikawa_thumbnail.png").convert("RGBA").resize((50, 50)),
        Image.open("../assets/hachiware_thumbnail.png").convert("RGBA").resize((50, 50)),
        Image.open("../assets/usagi_thumbnail.png").convert("RGBA").resize((50, 50)),
        Image.open("../assets/kurimanju_thumbnail.png").convert("RGBA").resize((50, 50)),
        Image.open("../assets/momonga_thumbnail.png").convert("RGBA").resize((50, 50)),
        Image.open("../assets/rakko_thumbnail.png").convert("RGBA").resize((50, 50)),
        Image.open("../assets/shisa_thumbnail.png").convert("RGBA").resize((50, 50))
    ]
    
    selected_index = 0  # 초기 선택된 캐릭터
    num_characters = len(characters)
    image = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(image)

    # 1행 3개, 2행 4개의 캐릭터 배치
    row1 = 3  # 1행에 표시할 캐릭터 수
    row2 = 4  # 2행에 표시할 캐릭터 수
    margin = 10  # 캐릭터 간 간격
    char_width = 50  # 캐릭터 이미지 너비
    char_height = 50  # 캐릭터 이미지 높이
    
    while True:
        # 화면 초기화
        draw.rectangle((0, 0, width, height), fill=(255, 255, 255))  # 배경 흰색
        draw.text((width // 2 - 50, 20), "Select Your Character", fill="black")
        draw.text((width // 2 - 50, 40), "Press U to Confirm", fill="black")

        # 1행 캐릭터 배치
        for i in range(row1):
            x_position = (width // 2 - ((row1 * (char_width + margin)) - margin)) // 2 + i * (char_width + margin) + 50 # 50은 여백
            y_position = height // 3 - char_height // 2 + 20 # 20은 여백
            if i == selected_index:  # 선택된 캐릭터 강조
                draw.rectangle(
                    (x_position - 5, y_position - 5, x_position + char_width + 5, y_position + char_height + 5),
                    outline="red",
                    width=3
                )
            image.paste(characters[i], (x_position, y_position), mask=characters[i])

        # 2행 캐릭터 배치
        for i in range(row1, row1 + row2):
            x_position = (width // 2 - ((row2 * (char_width + margin)) - margin)) // 2 + (i - row1) * (char_width + margin) + 60 # 60은 여백
            y_position = height // 2 + height // 6 - char_height // 2 + 20 # 20은 여백
            if i == selected_index:  # 선택된 캐릭터 강조
                draw.rectangle(
                    (x_position - 5, y_position - 5, x_position + char_width + 5, y_position + char_height + 5),
                    outline="red",
                    width=3
                )
            image.paste(characters[i], (x_position, y_position), mask=characters[i])

        # L 버튼: 왼쪽 이동, R 버튼: 오른쪽 이동, U 버튼: 선택
        if not button_L.value:
            selected_index = (selected_index - 1) % num_characters
            time.sleep(0.2)  # 버튼 반복 방지
        if not button_R.value:
            selected_index = (selected_index + 1) % num_characters
            time.sleep(0.2)  # 버튼 반복 방지
        if not button_U.value:  # 선택 버튼
            print(f"Character {selected_index + 1} selected!")
            return characters[selected_index]

        # 화면 업데이트
        disp.image(image)
        time.sleep(0.01)

def main(disp, width, height, character):
    # 캐릭터 설정
    character_size = 60
    sub_character_size = 100

    character = character.resize((character_size, character_size))
    sub_character = Image.open("../assets/pochette.png").convert("RGBA").resize((sub_character_size, sub_character_size))

    character_x = 0  # 초기 위치
    character_y = height - 50 - character_size  # 바닥 이미지 위에 위치하도록 캐릭터 높이만큼 뺌
    move_speed = 20  # 이동 속도 증가
    jump_speed = 10  # Reduced from 15
    gravity = 0.5    # Reduced from 1 for smoother descent
    max_jump_height = 100  # Add a maximum jump height limit
    is_jumping = False
    jump_velocity = 0

    sub_character_x = width - sub_character_size
    sub_character_y = height - 50 - sub_character_size + 10

    # 바닥 이미지 설정
    ground = Image.open("../assets/ground.png").resize((width, 50))

    # 폰트 설정
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)

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
            if character_y >= height - 50 - character_size:  # 바닥 이미지 위에 위치하도록 설정
                character_y = height - 50 - character_size
                is_jumping = False
            elif character_y < 0:  # 캐릭터가 화면을 벗어나지 않도록 y 좌표 제한
                character_y = 0
                jump_velocity = 0

        # 화면 그리기
        draw.rectangle((0, 0, width, height), outline=0, fill=(135, 206, 235))  # 하늘색 배경
        image.paste(ground, (0, height - 50))
        image.paste(character, (int(character_x), int(character_y)), mask=character)
        image.paste(sub_character, (sub_character_x, sub_character_y), mask=sub_character)

        # 충돌 감지 (서브 만남!)
        if (character_x < sub_character_x + sub_character_size and
            character_x + character_size > sub_character_x and
            character_y < sub_character_y + sub_character_size and
            character_y + character_size > sub_character_y):

            # 미션
            text = "Mission: Defeat the monsters!"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            draw.text(((width - text_width) // 2, 10), text, font=font, fill="black")
            
            confirm_text = "Confirm: press (A)"
            confirm_text_bbox = draw.textbbox((0, 0), confirm_text, font=font)
            confirm_text_width = confirm_text_bbox[2] - confirm_text_bbox[0]
            confirm_text_height = confirm_text_bbox[3] - confirm_text_bbox[1]
            draw.text(((width - confirm_text_width) // 2, 40), confirm_text, font=font, fill="black")

            # A 버튼이 눌렸는지 확인
            if not button_A.value:
                attack(disp, width, height, character, character_size, ground)

        disp.image(image)

        time.sleep(0.01)

def attack(disp, width, height, character, character_size, ground):
    monster_size = 70

    monster = Image.open("../assets/kimera.png").convert("RGBA").resize((monster_size, monster_size))
    shield_image = Image.open("../assets/shield.png").convert("RGBA").resize((character_size + 50, character_size + 50))
    attack_image = Image.open("../assets/attack_effect1.png").convert("RGBA").resize((80, 80))
    image = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(image)
    
    character_x = 0
    monster_x = width - monster_size    
    character_y = height - 50 - character_size
    monster_y = height - 50 - monster_size

    move_speed = 20
    jump_speed = 30
    gravity = 2
    is_jumping = False
    jump_velocity = 0
    is_shielding = False
    is_attacking = False
    shield_duration = 0
    attack_x = character_x #+ character_size  # 공격 이미지의 초기 x 위치

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
            if character_y >= height - 50 - character_size:  # 바닥 이미지 위에 위치하도록 설정
                character_y = height - 50 - character_size
                is_jumping = False
            elif character_y < 0:  # 캐릭터가 화면을 벗어나지 않도록 y 좌표 제한
                character_y = 0
                jump_velocity = 0

        # 공격 및 방패 처리
        if is_attacking:
            attack_x += 15  # 공격 이미지가 왼쪽으로 이동
            if attack_x > monster_x - monster_size:  # `monster` 위치에 도달하면 멈춤
                is_attacking = False
                # attack_x = character_x + character_size  # 공격 이미지 초기화..를 아래로 옮겼더니 여러번 됨

        if is_shielding:
            shield_duration -= 1
            if shield_duration <= 0:
                is_shielding = False

        # 화면 그리기
        # 배경색
        draw.rectangle((0, 0, width, height), outline=0, fill=(35, 0, 25)) # 뭔가 어두운 색

        # 바닥 이미지 그리기
        image.paste(ground, (0, height - 50))  

        # 왼쪽에 character 이미지 표시
        image.paste(character, (character_x, character_y), mask=character)  

        # 오른쪽에 monster 이미지 표시
        image.paste(monster, (monster_x, monster_y), mask=monster)  

        if is_shielding:
            image.paste(
                shield_image,
                (character_x - 25, character_y - 25),  # 캐릭터를 감싸도록 위치 조정
                mask=shield_image,
            )

        if is_attacking:
            image.paste(attack_image, (attack_x, character_y), mask=attack_image)

        # B 버튼이 눌렸는지 확인
        if not button_B.value and not is_attacking:
            is_attacking = True
            attack_x = character_x  # 공격 이미지 초기화
            print("Attack!")

        # A 버튼이 눌렸는지 확인
        if not button_A.value and not is_shielding:
            is_shielding = True
            shield_duration = 5  # 방패 지속 시간 (프레임 수)
            print("Shield!")

        disp.image(image)
        time.sleep(0.01)

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
button_A.pull = Pull.UP

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_B.pull = Pull.UP

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
button_L.pull = Pull.UP

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
button_R.pull = Pull.UP

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_U.pull = Pull.UP

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
button_D.pull = Pull.UP

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
button_C.pull = Pull.UP

# 백라이트 켜기
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# 그리기 위한 빈 이미지 생성
width = disp.width
height = disp.height
image = Image.new("RGBA", (width, height))
draw = ImageDraw.Draw(image)

character = character_select(disp, width, height)
main(disp, width, height, character)