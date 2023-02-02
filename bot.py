import asyncio
from PIL import ImageFilter
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import constants
from func import *


storage = MemoryStorage()
TOKEN = ''
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot,storage=storage)

class FSMAdmin(StatesGroup):
    photo = State()
    description = State()
    sign = State()

async def on_startup(_):
    print("Бот запущен")


@dp.message_handler(commands=['start','help'],state=None)
async def cmd_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.answer(constants.START_COMMAND,parse_mode='HTML')



@dp.message_handler(state='*',commands='cancel')
async def cancel_handler(message:types.Message,state:FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

@dp.message_handler(lambda message:not message.photo,state=FSMAdmin.photo)
async def check_photo(message:types.Message):
    await message.reply('Это не фотография')

@dp.message_handler(content_types=['photo'],state=FSMAdmin.photo)
async def load_photo(message:types.Message, state:FSMContext):
    async  with  state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await FSMAdmin.next()
    await message.answer(constants.IMAGE_PROCESSING,parse_mode='HTML')

@dp.message_handler(state=FSMAdmin.description)
async  def load_description(message:types.Message,state:FSMContext):
    async  with  state.proxy() as data:
        data['description'] = message.text

        if data['description'] != '/resize':
            if data['description'] == '/pencil':
                await get_photo(message, data,state,ImageFilter.CONTOUR_PENCIL())
            elif data['description'] == '/paper':
                await get_photo(message, data,state,ImageFilter.CONTOUR_TRACING_PAPER())
            elif data['description'] == '/paper_deep':
                await get_photo(message, data,state,ImageFilter.CONTOUR_TRACING_PAPER_DEEP())
            elif data['description'] == '/exotic_pencil':
                await get_photo(message, data,state, ImageFilter.EXOTIC_PENCIL())
            elif data['description'] == '/marble':
                await get_photo(message, data,state, ImageFilter.EMBOSS())
            elif data['description'] == '/coal':
                await get_photo(message, data,state, ImageFilter.FIND_EDGES())
            elif data['description'] == '/black_white':
                # await black_white(message, data,state)
                await get_photo(message,data,state)

        else:
            await FSMAdmin.next()
            await message.answer(constants.RESIZE_COMMAND,parse_mode='HTML')


@dp.message_handler(state=FSMAdmin.sign)
async def load_resize(message:types.Message, state:FSMContext):

    async  with  state.proxy() as data:
        data['sign'] = message.text

    await cmd_resize(message, data)
    await state.finish()
    await message.answer('Еще фото?\n/start\n')

if __name__ ==  '__main__':
    import platform
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        executor.start_polling(dp, skip_updates=True,on_startup=on_startup)
