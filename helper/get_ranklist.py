from bs4 import BeautifulSoup
from aiohttp import ClientSession
import asyncio
import pandas as pd
from io import StringIO

UOFA_URL = "https://open.kattis.com/universities/ualberta.ca"


async def get_ranklist():
    http = ClientSession()
    async with http.get(UOFA_URL) as resp:
        assert resp.status == 200, "Kattis responsed with non 200 status code!"
        html = await resp.text(encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")
        table, *_ = pd.read_html(StringIO(str(soup)), flavor='bs4')
        table['Contributed'] = table.apply(
            lambda row: 0.2 * (0.8 ** row['Rank']) * row['Score [?]'], axis=1)
        # TODO: what do
        print(table)

    await http.close()


asyncio.run(get_ranklist())
