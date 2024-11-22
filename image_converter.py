from PIL import Image

# 이미지 열기
img = Image.open("character.png").convert("RGBA")

# 투명 배경으로 변환
data = img.getdata()
new_data = []
for item in data:
    # 검정 배경(0, 0, 0)에 대해 투명 처리
    if item[:3] == (0, 0, 0):
        new_data.append((255, 255, 255, 0))  # 투명 (255, 255, 255, 0)
    else:
        new_data.append(item)

img.putdata(new_data)
img.save("output_image.png")
print("image save!")