from PIL import Image
import requests
from io import BytesIO
from pywinauto import Application

scale = 24 # пока подсчёт работает только для масштаба 24

app = Application(backend='uia')
try:
    app.connect(title_re=f".*-hd-{scale}.*.png.*")
except:
    print("Откройте страницу скриншота перед запуском программы")
    exit()

addr_ctrl = app.top_window().child_window(title="Поле адреса", control_type="Edit") #.print_control_identifiers() #.child_window(title_re="*Address*", control_type="Edit")
url = addr_ctrl.get_value()

#url = "https://minesweeper.online/screen/4060987635-hd-24-64549.png"
filename_not_hit_cell = "not_hit_cell.png"
dx = dy = scale

response = requests.get(url)
if response.status_code == 200:
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    img_cropped = img.crop((18, 81, width - 18, height - 17))
    #img_not_hit = img_cropped.crop((0, dy, dx, dy + dy)) # выдернуть и сохранить картинку ненажатой клетки
    #img_not_hit.save(filename_not_hit_cell)
    img_not_hit = Image.open(filename_not_hit_cell)
    not_hit_count = 0
    for x in range(0, width - 1 - dx, dx):
        for y in range(0, height - 1 - dy, dy):
            if list(img_not_hit.getdata()) == list(img_cropped.crop((x, y, x + dx, y + dy)).getdata()):
                not_hit_count += 1

    print(f"Количество ненажатых клеток: {not_hit_count}")
else:
    print("Не удалось загрузить картинку")
