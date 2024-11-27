# import time
# import board
# from digitalio import DigitalInOut, Direction, Pull
# from PIL import Image, ImageDraw, ImageFont
# from adafruit_rgb_display import st7789

# # 디스플레이 설정
# cs_pin = DigitalInOut(board.CE0)
# dc_pin = DigitalInOut(board.D25)
# reset_pin = DigitalInOut(board.D24)
# BAUDRATE = 24000000

# spi = board.SPI()
# disp = st7789.ST7789(
#     spi,
#     height=240,
#     y_offset=80,
#     rotation=180,
#     cs=cs_pin,
#     dc=dc_pin,
#     rst=reset_pin,
#     baudrate=BAUDRATE,
# )

# # 입력 핀 설정
# button_A = DigitalInOut(board.D5)
# button_A.direction = Direction.INPUT
# button_A.pull = Pull.UP

# button_B = DigitalInOut(board.D6)
# button_B.direction = Direction.INPUT
# button_B.pull = Pull.UP

# button_L = DigitalInOut(board.D27)
# button_L.direction = Direction.INPUT
# button_L.pull = Pull.UP

# button_R = DigitalInOut(board.D23)
# button_R.direction = Direction.INPUT
# button_R.pull = Pull.UP

# button_U = DigitalInOut(board.D17)
# button_U.direction = Direction.INPUT
# button_U.pull = Pull.UP

# button_D = DigitalInOut(board.D22)
# button_D.direction = Direction.INPUT
# button_D.pull = Pull.UP

# button_C = DigitalInOut(board.D4)
# button_C.direction = Direction.INPUT
# button_C.pull = Pull.UP

# # 백라이트 켜기
# backlight = DigitalInOut(board.D26)
# backlight.switch_to_output()
# backlight.value = True


# def character_select(disp, width, height):
#     # 캐릭터 이미지 로드
#     characters = [
#         Image.open("../assets/chiikawa_thumbnail.png").convert("RGBA").resize((70, 70)),
#         Image.open("../assets/hachiware_thumbnail.png").convert("RGBA").resize((70, 70)),
#         Image.open("../assets/usagi_thumbnail.png").convert("RGBA").resize((70, 70)),
#         Image.open("../assets/kurimanju_thumbnail.png").convert("RGBA").resize((70, 70)),
#         Image.open("../assets/momonga_thumbnail.png").convert("RGBA").resize((70, 70)),
#         Image.open("../assets/rakko_thumbnail.png").convert("RGBA").resize((70, 70)),
#         Image.open("../assets/shisa_thumbnail.png").convert("RGBA").resize((70, 70))
#     ]
    
#     selected_index = 0  # 초기 선택된 캐릭터
#     num_characters = len(characters)
#     image = Image.new("RGBA", (width, height))
#     draw = ImageDraw.Draw(image)

#     while True:
#         # 화면 초기화
#         draw.rectangle((0, 0, width, height), fill=(255, 255, 255))  # 배경 흰색
#         draw.text((width // 2 - 50, 20), "Select Your Character", fill="black")

#         # 캐릭터 이미지를 가로로 정렬해서 표시
#         margin = 20
#         start_x = (width - (num_characters * (70 + margin) - margin)) // 2
#         y_position = height // 2 - 35

#         for i, char_img in enumerate(characters):
#             x_position = start_x + i * (70 + margin)
#             if i == selected_index:  # 선택된 캐릭터 강조
#                 draw.rectangle(
#                     (x_position - 5, y_position - 5, x_position + 75, y_position + 75),
#                     outline="red",
#                     width=3
#                 )
#             image.paste(char_img, (x_position, y_position), mask=char_img)

#         # A 버튼: 왼쪽 이동, B 버튼: 오른쪽 이동, U 버튼: 선택
#         if not button_A.value:
#             selected_index = (selected_index - 1) % num_characters
#             time.sleep(0.2)  # 버튼 반복 방지
#         if not button_B.value:
#             selected_index = (selected_index + 1) % num_characters
#             time.sleep(0.2)  # 버튼 반복 방지
#         if not button_U.value:  # 선택 버튼
#             print(f"Character {selected_index + 1} selected!")
#             return characters[selected_index]

#         # 화면 업데이트
#         disp.image(image)
#         time.sleep(0.01)