from aiogram.utils import executor
from create_bot import dp 
from core.handlers import client, admin, game

    
async def on_startup(_):
    print('Запуск бота')
    

client.register_handlers_client(dp)
game.register_handlers_client(dp)


    

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)