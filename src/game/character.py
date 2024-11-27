from PIL import Image

def setup_character(image_path):
    character = Image.open(image_path).convert("RGBA").resize((70, 70))
    character_x = 0
    character_y = 240 - 50 - 70 + 10  # 바닥 이미지 위에 위치하도록 설정
    return character, character_x, character_y

def update_character(character_x, character_y, move_speed, jump_speed, gravity, is_jumping, jump_velocity, button_L, button_R, button_U):
    if not button_L.value:
        character_x -= move_speed
    if not button_R.value:
        character_x += move_speed
    if not button_U.value and not is_jumping:
        is_jumping = True
        jump_velocity = -jump_speed

    if character_x < 0:
        character_x = 0
    if character_x > 240 - 70:
        character_x = 240 - 70

    if is_jumping:
        character_y += jump_velocity
        jump_velocity += gravity
        if character_y >= 240 - 50 - 70 + 10:
            character_y = 240 - 50 - 70 + 10
            is_jumping = False
        elif character_y < 0:
            character_y = 0
            jump_velocity = 0

    return character_x, character_y, is_jumping, jump_velocity