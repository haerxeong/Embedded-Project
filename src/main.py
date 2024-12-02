import time
import board
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import random

class Character:
    def __init__(self, image_path, size):
        self.image = Image.open(image_path).convert("RGBA").resize(size)
        self.x = 0
        self.y = 0
        self.size = size
        self.hp = 100
        self.attack_damage = 20
        self.is_attacking = False
        self.shield_duration = 3
        self.is_shielding = False
        self.move_speed = 20
        self.jump_speed = 30
        self.gravity = 10
        self.is_jumping = False
        self.velocity_y = 0
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.experience_to_next_level *= 1.5
        self.hp += 20
        self.attack_damage += 5
        self.move_speed += 2
        self.jump_speed += 5
        print(f"Level Up! New Level: {self.level}")

class Monster:
    def __init__(self, image_path, size):
        self.image = Image.open(image_path).convert("RGBA").resize(size)
        self.x = 0
        self.y = 0
        self.size = size
        self.hp = 100
        # 움직임 변수
        self.move_direction = 1 # 1: 오른쪽, -1: 왼쪽
        self.move_timer = 0
        self.move_interval = random.randint(10, 50)  # 몬스터 방향 변경 간격
        self.move_speed = 5
        # 공격 변수
        self.attack_damage = 10
        self.attack_interval = random.randint(10, 30)
        self.attack_timer = 0
        self.attack_active = False
        self.attack_x = self.x
        self.attack_y = self.y

    def level_up(self):
        self.hp += 50
        self.attack_damage += 5
        self.move_speed += 1
        self.attack_interval = max(50, self.attack_interval - 20)
        print(f"Monster Level Up! New HP: {self.hp}")

def game_end(disp, width, height, status):
    image = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill=(255, 255, 255))  # 배경 흰색
    if status == "clear":
        draw.text((width // 2 - 50, height // 2 - 10), "Game Clear!", fill="black", font=font)
    elif status == "over":
        draw.text((width // 2 - 50, height // 2 - 10), "Game Over!", fill="red", font=font)
    draw.text((width // 2 - 50, height // 2 + 20), "Press A to Restart", fill="black", font=font)
    disp.image(image)

    while True:
        if not button_A.value:
            return  # A 버튼이 눌리면 함수 종료
        time.sleep(0.1)

def character_select(disp, width, height):
    # 캐릭터 이미지 로드
    characters = [
        Character("../assets/chiikawa_thumbnail.png", (50, 50)),
        Character("../assets/hachiware_thumbnail.png", (50, 50)),
        Character("../assets/usagi_thumbnail.png", (50, 50)),
        Character("../assets/kurimanju_thumbnail.png", (50, 50)),
        Character("../assets/momonga_thumbnail.png", (50, 50)),
        Character("../assets/rakko_thumbnail.png", (50, 50)),
        Character("../assets/shisa_thumbnail.png", (50, 50))
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
            image.paste(characters[i].image, (x_position, y_position), mask=characters[i].image)

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
            image.paste(characters[i].image, (x_position, y_position), mask=characters[i].image)

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
    character.size = ((character_size, character_size))

    character.image = character.image.resize((character_size, character_size))
    sub_character = Image.open("../assets/pochette.png").convert("RGBA").resize((sub_character_size, sub_character_size))

    character.x = 0  # 초기 위치
    character.y = height - 50 - character_size  # 바닥 이미지 위에 위치하도록 캐릭터 높이만큼 뺌

    sub_character_x = width - sub_character_size
    sub_character_y = height - 50 - sub_character_size + 10

    # 바닥 이미지 설정
    ground = Image.open("../assets/ground.png").resize((width, 50))

    # 폰트 설정
    global font
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)

    # 게임 루프
    while True:
        # 입력 처리
        if not button_L.value:
            character.x -= character.move_speed
            print("왼쪽 이동...")
        if not button_R.value:
            character.x += character.move_speed
            print("오른쪽 이동...")
        if not button_U.value:
            character.is_jumping = True
            character.velocity_y = -character.jump_speed
            print("jump!")

        # 캐릭터가 화면 밖으로 나가지 않도록 x 좌표 제한
        if character.x < 0:
            character.x = 0
        if character.x > width - character.size[0]:
            character.x = width - character.size[0]

        # 점프 처리
        if character.is_jumping:
            character.velocity_y += character.gravity
            character.y += character.velocity_y

            if character.y >= height - 50 - character.size[1]:  # 바닥 이미지 위에 위치하도록 설정
                character.y = height - 50 - character.size[1]
                character.is_jumping = False
                character.velocity_y = 0

        # 화면 그리기
        draw.rectangle((0, 0, width, height), outline=0, fill=(135, 206, 235))  # 하늘색 배경
        image.paste(ground, (0, height - 50))
        image.paste(character.image, (int(character.x), int(character.y)), mask=character.image)
        image.paste(sub_character, (sub_character_x, sub_character_y), mask=sub_character)

        # 충돌 감지 (서브 만남!)
        if (character.x < sub_character_x + sub_character_size and
            character.x + character.size[0] > sub_character_x and
            character.y < sub_character_y + sub_character_size and
            character.y + character.size[1] > sub_character_y):

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
                print("Attack Start!")

        disp.image(image)

        time.sleep(0.01)

def attack(disp, width, height, character, character_size, ground):
    monster_size = 70

    monster = Monster("../assets/kimera.png", (monster_size, monster_size))
    monster.size = ((monster_size, monster_size))
    monster_attack_image = Image.open('../assets/moster_attack_effect.png').convert("RGBA").resize((80, 80))
    
    shield_image = Image.open("../assets/shield.png").convert("RGBA").resize((character_size + 50, character_size + 50))
    attack_image = Image.open("../assets/attack_effect1.jpg").convert("RGBA").resize((80, 80))
    image = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(image)
    
    character.x = 0
    monster.x = width - monster_size    
    character.y = height - 50 - character_size
    monster.y = height - 50 - monster_size

    while True:
        # 입력 처리
        if not button_L.value:
            character.x -= character.move_speed
        if not button_R.value:
            character.x += character.move_speed
        if not button_U.value:
            character.is_jumping = True
            character.velocity_y = -character.jump_speed

        # 캐릭터가 화면 밖으로 나가지 않도록 x 좌표 제한
        if character.x < 0:
            character.x = 0
        if character.x > width - character.size[0]:
            character.x = width - character.size[0]

        # y 좌표 제한
        if character.y < 0:
            character.y = 0

        # 점프 처리
        if character.is_jumping:
            character.velocity_y += character.gravity
            character.y += character.velocity_y

            if character.y >= height - 50 - character.size[1]:  # 바닥 이미지 위에 위치하도록 설정
                character.y = height - 50 - character.size[1]
                character.is_jumping = False
                character.velocity_y = 0

        # 몬스터 움직임 로직
        monster.move_timer += 1
        if monster.move_timer >= monster.move_interval:
            monster.move_direction *= -1  # 방향 변경
            monster.move_timer = 0
            monster.move_interval = random.randint(10, 50)
            print("Monster Direction Changed!")

        # 몬스터 이동
        monster.x += monster.move_direction * 5
        monster.x = max(width - monster_size * 2, min(monster.x, width - monster_size))

        # 몬스터 공격 로직
        monster.attack_timer += 1
        if monster.attack_timer >= monster.attack_interval:
            monster.attack_active = True
            monster.attack_x = monster.x
            monster.attack_y = monster.y
            monster.attack_timer = 0
            monster.attack_interval = random.randint(100, 300)
            print("Monster Attack!")

        # 몬스터 공격 이동
        if monster.attack_active:
            monster.attack_x -= 10  # 공격 이미지 이동 속도
            print(f"Monster Attack: {monster.attack_x}")

            # 공격과 캐릭터 충돌 체크
            if (monster.attack_x < character.x + character.size[0] and 
                monster.attack_x + 80 > character.x and 
                monster.attack_y < character.y + character.size[1] and 
                monster.attack_y + 80 > character.y):
                
                # 방어 상태 체크
                if not character.is_shielding:
                    character.hp -= monster.attack_damage
                    print(f"Player HP: {character.hp}")

                monster.attack_active = False

            # 공격이 화면 왼쪽 끝에 도달하면 비활성화
            if monster.attack_x < 0:
                monster.attack_active = False

        # 공격 및 방패 처리
        if character.is_attacking:
            character.attack_x += 15  # 공격 이미지가 왼쪽으로 이동
            if character.attack_x > monster.x - monster.size[0]:  # `monster` 위치에 도달하면 멈춤
                monster.hp -= character.attack_damage
                character.is_attacking = False
                character.gain_experience(20)  # 경험치 획득
                # attack_x = character_x + character_size  # 공격 이미지 초기화..를 아래로 옮겼더니 여러번 됨

        if character.is_shielding:
            character.shield_duration -= 1
            if character.shield_duration <= 0:
                character.is_shielding = False

        # 화면 그리기
        # 배경색
        draw.rectangle((0, 0, width, height), outline=0, fill=(35, 0, 25)) # 뭔가 어두운 색

        # 바닥 이미지 그리기
        image.paste(ground, (0, height - 50))  

        # 왼쪽에 character 이미지 표시
        image.paste(character.image, (character.x, character.y), mask=character.image)  

        # 오른쪽에 monster 이미지 표시
        image.paste(monster.image, (monster.x, monster.y), mask=monster.image)  

        # 몬스터 공격 이미지 그리기
        if monster.attack_active:
            image.paste(monster_attack_image, (monster.attack_x, monster.attack_y), mask=monster_attack_image)

        if character.is_shielding:
            image.paste(
                shield_image,
                (character.x - 25, character.y - 25),  # 캐릭터를 감싸도록 위치 조정
                mask=shield_image,
            )

        if character.is_attacking:
            image.paste(attack_image, (character.attack_x, character.y), mask=attack_image)

        # B 버튼이 눌렸는지 확인
        if not button_B.value and not character.is_attacking:
            character.is_attacking = True
            character.attack_x = character.x  # 공격 이미지 초기화
            print("Attack!")

        # A 버튼이 눌렸는지 확인
        if not button_A.value and not character.is_shielding:
            character.is_shielding = True
            character.shield_duration = 5  # 방패 지속 시간 (프레임 수)
            print("Shield!")

        # 캐릭터 HP 표시
        hp_text = f"HP: {character.hp}"
        draw.text((10, 10), hp_text, fill=(255, 255, 255), font=font)

        # 몬스터 HP 표시
        hp_text = f"HP: {monster.hp}"
        draw.text((width - 70, 10), hp_text, fill="red", font=font)

        disp.image(image)
        time.sleep(0.01)

        # 게임 클리어 체크
        if monster.hp <= 0:
            print("Game Clear!")
            game_end(disp, width, height, "clear")
            break

        # 게임 오버 체크
        if character.hp <= 0:
            print("Game Over!")
            game_end(disp, width, height, "over")
            break

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
print(f"width, height = {width}, {height}")

image = Image.new("RGBA", (width, height))
draw = ImageDraw.Draw(image)

character = character_select(disp, width, height)
main(disp, width, height, character)