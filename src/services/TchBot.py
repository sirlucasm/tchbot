import asyncio
from pyppeteer import launch
from faker import Faker
from unidecode import unidecode

global fake
fake = Faker('pt_BR')

class TchBot:
    def __init__(self, username):
        self.username = username

    async def emailVerify(self, username):
        browser = await launch({ 'headless': False })
        page = await browser.newPage()
        await page.goto('https://www.mohmal.com/', {
            'waitUntil': 'networkidle2'
        })
        await asyncio.sleep(1)
        await page.click('#choose')
        await asyncio.sleep(1)
        # inputs form
        await page.type('input[name="name"]', username)
        await asyncio.sleep(0.7)
        await page.click('#next')
        await asyncio.sleep(0.7)
        await page.click('#create')
        await asyncio.sleep(2)


    async def createAccounts(self, accountsNumber):
        for index in range(accountsNumber):
            browser = await launch({ 'headless': False })
            page = await browser.newPage()
            await page.goto('https://www.twitch.tv/signup', {
                'waitUntil': 'networkidle2'
            })
            username = unidecode(fake.unique.first_name().lower()) + '_' + unidecode(fake.name().split(' ')[1].lower())
            password = 'Tch280119!Tch280119!'
            birthDay = '31'
            birthYear = '1994'
            email = username + '@mozej.com'
            
            await asyncio.sleep(1)
            # inputs form
            await page.type('#signup-username', username)
            await asyncio.sleep(0.7)
            await page.type('#password-input', password)
            await asyncio.sleep(0.7)
            await page.type('#password-input-confirmation', password)
            await asyncio.sleep(0.7)
            await page.type('input[placeholder="Dia"]', birthDay)
            await asyncio.sleep(0.7)
            await page.select('#root > div > div.scrollable-area > div.simplebar-scroll-content > div > div > div > div.tw-mg-b-1 > form > div > div:nth-child(3) > div > div.tw-flex.tw-flex-row.tw-overflow-auto > div.tw-full-width.tw-mg-l-1 > select', '3')
            await asyncio.sleep(0.7)
            await page.type('input[placeholder="Ano"]', birthYear)
            await asyncio.sleep(0.7)
            await page.type('#email-input', email)
            await asyncio.sleep(2)
            # # submit form button
            # await page.keyboard.press('Enter')
            await asyncio.sleep(4)
            await self.emailVerify(username)
        
