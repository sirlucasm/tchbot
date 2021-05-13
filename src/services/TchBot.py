import asyncio
from pyppeteer import launch
import random
from faker import Faker
from unidecode import unidecode
from src.services.database import Database
import json
from pathlib import Path
import requests

global fake
fake = Faker('pt_BR')

def load_proxies_list() -> list[dict]:
    list_folder = Path(__file__).parent.parent.joinpath('proxies')

    proxies = [
        *json.load(list_folder.joinpath('proxy_list_1.json').open()),
        *json.load(list_folder.joinpath('proxy_list_2.json').open())
    ]
    return proxies


def verify_proxy_status(proxy_ip: str) -> bool:
    print(f'Checking proxy status of: {proxy_ip}')
    response = requests.get('https://www.twitch.tv/signup', proxies={'http': f'http://{proxy_ip}'})
    return response.status_code == 200

class TchBot:
    def __init__(self, username):
        self.username = username

    async def getEmail(self, browser):
        page = await browser.newPage()
        await page.goto('https://pt.emailfake.com/', {
            'waitUntil': 'networkidle2'
        })
        # url to seen current email -> https://pt.emailfake.com/homenhu.com/tsutsuma
        await asyncio.sleep(3)
        # select twitch message
        email = await page.evaluate('''() => document.getElementById('email_ch_text').textContent''')
        return email

    async def verifyEmail(self, browser):
        allPages = await browser.pages()
        page = allPages[2]
        await asyncio.sleep(2)

        # refresh mail page
        await page.click('#refresh')
        await asyncio.sleep(4)

        await page.evaluate('''() => {
            const message = document.getElementsByClassName("from_div_45g45gg")[1];
            const verify = document.querySelector('a[style="Margin: 0; border: 0 solid #9147ff; border-radius: 3px; color: #fff; display: inline-block; font-family: Helvetica,Arial,sans-serif; font-size: 14px; font-weight: 600; line-height: 1.3; margin: 0; padding: 10px 55px 10px 55px; text-align: left; text-decoration: none"]')document.querySelector('a[style="Margin: 0; border: 0 solid #9147ff; border-radius: 3px; color: #fff; display: inline-block; font-family: Helvetica,Arial,sans-serif; font-size: 14px; font-weight: 600; line-height: 1.3; margin: 0; padding: 10px 55px 10px 55px; text-align: left; text-decoration: none"]');
            //verify twitch acc button
            return verify.click();
        }
        ''')

    async def createAccounts(self, accountsNumber):
        proxies = load_proxies_list()
        for index in range(accountsNumber):
            random_proxy = random.choice(proxies)
            while True:
                if verify_proxy_status('111.93.30.66:3128'):
                    print('Funcionou')
                    break
                print('Não funfo')
                continue
            browser = await launch({ 'headless': False, 'args': [f'--proxy-server={random_proxy["proxyIp"]}'] })
            page = await browser.newPage()
            await page.goto('https://www.twitch.tv/signup', {
                'waitUntil': 'networkidle2',
                'timeout': 0
            })
            username = unidecode(fake.unique.first_name().lower()).strip() + unidecode(fake.name().split(' ')[1].lower()).strip() + str(random.randint(1, 3))
            password = 'Tch280119!Tch280119!'
            birthDay = '31'
            birthYear = '1994'
            email = ''
            proxyIp = random_proxy['proxyIp']
            
            await asyncio.sleep(6)
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
            
            email = await self.getEmail(browser)
            allPages = await browser.pages()
            page = allPages[1]

            await asyncio.sleep(0.7)
            await page.type('#email-input', email)
            await asyncio.sleep(1)
            # submit form button
            await page._keyboard.press('Enter')
            
            await asyncio.sleep(6)
            await self.verifyEmail(browser)

            await asyncio.sleep(2)
            await browser.close()

            await Database.insert('users', {
                'username': username,
                'password': password,
                'email': email,
                'proxyIp': 'undefined',
            })
            print('| Conta Twitch Criada | email -> ' + email)

# tests
if __name__ == '__main__':
    proxies = load_proxies_list()
    random_proxy = random.choice(proxies)
    print(random_proxy['proxyIp'])
