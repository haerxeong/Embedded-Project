import time
import board
import os
import datetime
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import random

class Character:
    def __init__(self, image_path, size):
        self.image = Image.open(image_path).convert("RGBA").resize(size)
        self.name = image_path.split('/')[-1].split('_')[0]  # 캐릭터 이름 추출
        self.x = 0
        self.y = 0
        self.size = size
        self.hp = 300
        self.attack_damage = 20
        self.is_attacking = False
        self.shield_duration = 3
        self.is_shielding = False
        self.move_speed = 10
        self.jump_speed = 20
        self.gravity = 10
        self.is_jumping = False
        self.velocity_y = 0
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        # 기록 관련 변수 추가
        self.start_time = None
        self.clear_time = None

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            # self.level_up()
            pass

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.experience_to_next_level *= 1.5
        self.hp += 5
        self.attack_damage += 5
        self.move_speed += 2
        self.jump_speed += 5
        self.shield_duration += 1

        level_up_image = Image.open("../assets/level_up.png").convert("RGBA").resize((240, 240))
        image.paste(level_up_image, (0, 0), mask=level_up_image)

        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size=20)
        draw = ImageDraw.Draw(image)
        text = f"{self.level}"
        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
        draw.text(((width - text_width) // 2, (height - text_height) - 70), text, font=font, fill="black")

        disp.image(image)
        print(f"Level Up! New Level: {self.level}")

        while True:
            if not button_A.value:
                return  # A 버튼이 눌리면 함수 종료
            time.sleep(0.1)

class Monster:
    def __init__(self, image_path, size):
        self.image = Image.open(image_path).convert("RGBA").resize(size)
        self.x = 0
        self.y = 0
        self.size = size
        self.hp = 300  # 체력 증가
        # 움직임 변수
        self.move_direction = 1 # 1: 오른쪽, -1: 왼쪽
        self.move_timer = 0
        self.move_interval = random.randint(0, 10)  # 몬스터 방향 변경 간격
        self.move_speed = 5
        # 공격 변수
        self.attack_damage = 20
        self.attack_interval = random.randint(10, 30)  # 공격 간격 감소
        self.attack_timer = 0
        self.attack_active = False
        self.attack_x = self.x
        self.attack_y = self.y
        self.attack_speed = 15  # 공격 속도 증가 (10 -> 15)
        self.multi_attack = False  # 다중 공격 가능 여부
        self.attack_count = 0  # 연속 공격 횟수

    def level_up(self):
        self.hp += 50
        self.attack_damage += 5
        self.move_speed += 1
        self.attack_interval = max(10, self.attack_interval - 5)  # 공격 간격 감소
        print(f"Monster Level Up! New HP: {self.hp}")

def save_record(level):
    with open('game_records.txt', 'a') as f:
        f.write(f"{level}\n")

def load_records():
    if not os.path.exists('game_records.txt'):
        return []
    with open('game_records.txt', 'r') as f:
        records = f.readlines()
    records = [int(record.strip()) for record in records if record.strip()]
    top_three_records = sorted(records, reverse=True)[:3]
    return top_three_records

def draw_start_screen(disp, width, height):
    start_image = Image.open("../assets/start_screen.png").convert("RGBA").resize((width, height))
    draw = ImageDraw.Draw(start_image)
    
    # 작은 폰트 크기 사용 (15)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', size=15)
    
    # 기록 표시 - 오른쪽 아래에 정렬
    top_three_records = load_records()
    for i, record in enumerate(top_three_records):
        text = f"{i+1}: Level {record}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 위치 계산: 오른쪽 여백 10px, 아래 여백 10px
        x = width - text_width - 10
        y = height - (len(top_three_records) - i) * (text_height + 5) - 10
        
        draw.text((x, y), text, font=font, fill="pink")
    
    disp.image(start_image)

def draw_tutorial_screen(disp, width, height):
    tutorial_image = Image.open("../assets/tutorial.png").convert("RGBA").resize((width, height))
    disp.image(tutorial_image)
    
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

    # select_font 이미지 로드
    select_font_image = Image.open("../assets/select_font.png").convert("RGBA").resize((width - 20, 60))
    
    while True:
        # 화면 초기화
        draw.rectangle((0, 0, width, height), fill=(255, 255, 255))  # 배경 흰색
        image.paste(select_font_image, (0, 0), mask=select_font_image)  # select_font 이미지 그리기
        
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

        # L 버튼: 왼쪽 이동, R 버튼: 오른쪽 이동, B 버튼: 선택
        if not button_L.value:
            selected_index = (selected_index - 1) % num_characters
            time.sleep(0.2)  # 버튼 반복 방지
        if not button_R.value:
            selected_index = (selected_index + 1) % num_characters
            time.sleep(0.2)  # 버튼 반복 방지
        if not button_B.value:  # 선택 버튼
            print(f"Character {selected_index + 1} selected!")
            return characters[selected_index]

        # 화면 업데이트
        disp.image(image)
        time.sleep(0.01)

def main(disp, width, height, character):
    # 게임 시작 시간 기록
    character.start_time = datetime.datetime.now()

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

    # 임무 전달 이미지
    mission_image = Image.open("../assets/ment.png").convert("RGBA").resize((width, 50))
    new_mission_image = Image.open("../assets/new_mission.png").convert("RGBA").resize((width, 50))

    # 게임 루프
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
            if character.level == 1:
                image.paste(mission_image, (0, 0), mask=mission_image)

                # A 버튼이 눌렸는지 확인
                if not button_A.value:
                    result = attack(disp, width, height, character, character_size, ground)
                    if result in ["clear", "over"]:
                        if game_end(disp, width, height, result):
                            continue  # 메인으로 돌아가기
                        else:
                            return
            else:
                image.paste(new_mission_image, (0, 0), mask=mission_image)

                if not button_A.value:
                    result = weedCleanup(disp, width, height, character)
                    if result in ["clear", "over"]:
                        if game_end(disp, width, height, result):
                            continue  # 메인으로 돌아가기
                        else: 
                            return
                elif not button_B.value:
                    result = attack(disp, width, height, character, character_size, ground)
                    if result in ["clear", "over"]:
                        if game_end(disp, width, height, result):
                            continue  # 메인으로 돌아가기
                        else:  
                            return
                    
        disp.image(image)

        time.sleep(0.01)

def attack(disp, width, height, character, character_size, ground):
    monster_size = 70

    monster = Monster("../assets/kimera.png", (monster_size, monster_size))
    monster.size = ((monster_size, monster_size))
    monster_attack_image = Image.open('../assets/moster_attack_effect.png').convert("RGBA").resize((80, 80))
    
    shield_image = Image.open("../assets/shield.png").convert("RGBA").resize((character_size + 50, character_size + 50))
    
    # 캐릭터 이름 사용
    attack_image_path = f"../assets/{character.name}_attack_effect.png"
    
    # 쿠리만주의 경우 다른 크기로 이미지 로드 (너무 큼)
    if character.name == "kurimanju":
        attack_image = Image.open(attack_image_path).convert("RGBA").resize((50, 50))
    else:
        attack_image = Image.open(attack_image_path).convert("RGBA").resize((80, 80))
    
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
            monster.attack_interval = random.randint(10, 30)  # 공격 간격 감소
            monster.attack_count = random.randint(1, 3)  # 1~3회 연속 공격
            monster.multi_attack = True
            print("Monster Attack!")

        # 몬스터 공격 이동
        if monster.attack_active:
            monster.attack_x -= monster.attack_speed  # 공격 이동 속도로 왼쪽으로 이동
            
            # 공격과 캐릭터 충돌 체크
            if (monster.attack_x < character.x + character.size[0] and 
                monster.attack_x + 80 > character.x and 
                monster.attack_y < character.y + character.size[1] and 
                monster.attack_y + 80 > character.y):
                
                if not character.is_shielding:
                    character.hp -= monster.attack_damage
                    print(f"Player HP: {character.hp}")

                monster.attack_active = False
                
                # 다중 공격 처리
                if monster.multi_attack and monster.attack_count > 0:
                    monster.attack_count -= 1
                    monster.attack_active = True
                    monster.attack_x = monster.x
                    print(f"Continuous Attack! Remaining: {monster.attack_count}")
                else:
                    monster.multi_attack = False

            # 공격이 화면 왼쪽 끝에 도달하면 처리
            if monster.attack_x < 0:
                monster.attack_active = False
                # 다중 공격 처리
                if monster.multi_attack and monster.attack_count:
                    monster.attack_count -= 1
                    monster.attack_active = True
                    monster.attack_x = monster.x
                else:
                    monster.multi_attack = False

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
            character.level_up() # 레벨업
            monster.level_up()  # 몬스터 레벨업 -> 게임 난이도 증가
            return "clear"

        # 게임 오버 체크
        if character.hp <= 0:
            print("Game Over!")
            game_end(disp, width, height, "over")
            character.clear_time = datetime.datetime.now() - character.start_time
            save_record(character.level)  # 레벨 저장
            return "over"

        disp.image(image)
        time.sleep(0.01)

def game_end(disp, width, height, status):
    if status == "clear":
        image = Image.open("../assets/game_clear.png").convert("RGBA").resize((width, height))
    else:
        image = Image.open("../assets/game_over.png").convert("RGBA").resize((width, height))
    disp.image(image)

    while True:
        if not button_A.value:
            return status == "clear"
        time.sleep(0.1)

def weedCleanup(disp, width, height, character):
    # 잡초 이미지 로드
    weed_image = Image.open("../assets/weed.png").convert("RGBA").resize((30, 30))
    
    # 잡초 위치 리스트 생성
    weeds = []
    for _ in range(10):  # 10개의 잡초 생성
        x = random.randint(0, width - 30)
        y = random.randint(0, height - 30)
        weeds.append([x, y])

    start_time = time.time()
    score = 0  # 초기 점수

    # 캐릭터 초기 위치 설정
    character.y = height - character.size[1]

    while True:
        # 화면 초기화
        image = Image.new("RGBA", (width, height), (135, 206, 235, 255))  # 하늘색 배경
        draw = ImageDraw.Draw(image)

        # 잡초 그리기
        for weed in weeds:
            image.paste(weed_image, (weed[0], weed[1]), mask=weed_image)

        # 캐릭터 그리기
        image.paste(character.image, (character.x, character.y), mask=character.image)

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

        if character.y < 0:
            character.y = 0

        # 점프 처리
        if character.is_jumping:
            character.velocity_y += character.gravity
            character.y += character.velocity_y

            if character.y >= height - character.size[1]:  # 바닥 이미지 위에 위치하도록 설정
                character.y = height - character.size[1]
                character.is_jumping = False
                character.velocity_y = 0

        # 잡초와 캐릭터 충돌 체크
        i = 0
        while i < len(weeds):
            weed = weeds[i]
            if (character.x < weed[0] + 30 and
                character.x + character.size[0] > weed[0] and
                character.y < weed[1] + 30 and
                character.y + character.size[1] > weed[1]):
                del weeds[i]
                score += 1  # 잡초 제거 시 점수 증가
            else:
                i += 1

        # 25초까지 랜덤하게 잡초 추가
        if time.time() - start_time <= 25:
            if random.random() < 0.1:  # 10% 확률로 새로운 잡초 추가
                x = random.randint(0, width - 30)
                y = random.randint(0, height - 30)
                weeds.append([x, y])

         # 남은 시간 계산
        elapsed_time = time.time() - start_time
        remaining_time = max(0, 30 - elapsed_time)

        # 남은 시간 표시
        time_text = f"Time: {remaining_time:.1f}s"
        draw.text((10, 10), time_text, fill=(255, 255, 255), font=font)

        # 현재 점수 표시
        score_text = f"Score: {score}"
        draw.text((width - 100, 10), score_text, fill=(255, 255, 255), font=font)

        # 모든 잡초를 제거하면 클리어
        if len(weeds) == 0:
            print("Weed Cleanup Clear!")
            character.hp += score * 10  # 스코어 * 10 만큼 캐릭터의 HP 증가
            return "clear"

        # 30초가 지나면 실패
        if elapsed_time > 30:
            print("Weed Cleanup Fail!")
            save_record(character.level)  # 레벨 저장
            return "over"

        disp.image(image)
        time.sleep(0.01)

        # A 버튼 디바운스 처리
        if not button_A.value:
            time.sleep(0.2)  # 200ms 지연 시간 추가
            character.x = 0  # 캐릭터 위치 초기화

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

# character = character_select(disp, width, height)
# main(disp, width, height, character)

# 메인 실행
if __name__ == "__main__":
    draw_start_screen(disp, width, height)
    while True:
        if not button_A.value:
            draw_tutorial_screen(disp, width, height)
            character = character_select(disp, width, height)
            result = main(disp, width, height, character)
            if result == "over":
                continue  # 캐릭터 선택부터 다시 시작
        time.sleep(0.1)