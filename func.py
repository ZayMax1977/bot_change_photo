import requests
from PIL import  Image
import io
import os
import secrets
import constants


async def get_photo(message, data, state, class_name=None):
    resp = requests.get(constants.URL_INFO + data['photo'])
    img_path = resp.json()['result']['file_path']
    img = requests.get(constants.URL + img_path)
    img = Image.open(io.BytesIO(img.content))
    if class_name:
        img = img.filter(class_name)
    else:
        global g
        r, g, b = img.split()


    if not os.path.exists('static'):
        os.mkdir('static')

    name_img = secrets.token_hex(8)
    if class_name:
        img.save(f'static/{name_img}.png', format='PNG')
    else:
        g.save(f'static/{name_img}.png', format='PNG')

    await message.answer_photo(photo=open(f'static/{name_img}.png', 'rb'),caption='Можете сохранить обработанное фото')
    await state.finish()
    await message.answer('Еще фото?\n/start\n')
    return

async  def cmd_resize(message,data):
    resp = requests.get(constants.URL_INFO + data['photo'])
    img_path = resp.json()['result']['file_path']
    img = requests.get(constants.URL + img_path)

    img = Image.open(io.BytesIO(img.content))
    img_img = img
    w_plus = int(img.width+(img.width * (int(data['sign'][1:]) / 100)))
    h_plus = int(img.height+(img.height * (int(data['sign'][1:]) / 100)))
    w_minus = int(img.width-(img.width * (int(data['sign'][1:]) / 100)))
    h_minus = int(img.height-(img.height * (int(data['sign'][1:]) / 100)))

    if data['sign'][0] == '+' and int(data['sign'][1:]) <= 150:
        img = img.resize((w_plus,h_plus))
    elif data['sign'][0] == '-' and int(data['sign'][1:]) <= 99:
        img = img.resize((w_minus,h_minus))
    else:
        await message.reply('Введенное число вне дозволенных диапазонах')
        return


    if not os.path.exists('static'):
        os.mkdir('static')

    name_img = secrets.token_hex(8)
    img.save(f'static/{name_img}.png', format='PNG')
    await message.answer_photo(photo=open(f'static/{name_img}.png', 'rb'),caption=f'Старый размер фото:\
 <b>{img_img.size}px</b>\n Новый размер данного фото:  <b>{img.size}px</b>\nМожете сохранить обработанное фото.',parse_mode='HTML')
    return