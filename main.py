import asyncio
import os

from src.App import App
from src.services.TchBot import TchBot
from src.services.database import Database

async def main():
    select = 0

    App.bot()
    App.selectUser()
    username = input('write here: ')

    while username.isnumeric():
        App.bot()
        App.selectUser()
        username = input('write here: ')
        if (username == '6'):
            break

    if (username == '6'):
        exit()

    bot = TchBot(username=username)

    while select == 0:
        Database.exec()
        App.bot()
        App.items()
        select = int(input('select an option: '))

        if (select > 4 or select < 1 or select == ''):
            print('Please select a valid option\n')
            os.system('pause')
            select = 0
        if (select == 4):
            App.consoleClear()
            print('\nbye!\n')
            break
        
        if select == 1:
            App.consoleClear()
            App.createAccounts()
            selectNewAccountsNumber = int(input('how many accounts do you want? '))
            await bot.createAccounts(selectNewAccountsNumber)
            # await bot.emailVerify('teste1')
            break

# exec main
asyncio.get_event_loop().run_until_complete(main())