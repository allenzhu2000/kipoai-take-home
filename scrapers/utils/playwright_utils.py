"""
This module contains utility functions for scraping data from the web using Playwright.
"""
from playwright.async_api import Page, BrowserContext, ElementHandle
from playwright_stealth import stealth_async
import random
import re
import asyncio

USER_AGENT_STRINGS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
]

# get random user agent string
def get_random_user_agent_string():
    return USER_AGENT_STRINGS[random.randint(0, len(USER_AGENT_STRINGS) - 1)]

def remove_special_chars_from_str(str: str):
    return re.sub(r'[^\w\s]', '', str.encode('ascii', 'ignore').decode())

async def extract_link_str_from_element(element: ElementHandle):
    return await element.get_attribute('href')

async def scrape_links_from_page(context: BrowserContext, path, selector, page_number):
    page = await context.new_page()
    await stealth_async(page)
    await page.goto(f'{path}?pg={page_number}')
    link_elements_on_page = await page.query_selector_all(selector)

    scrape_link_tasks = [extract_link_str_from_element(element) for element in link_elements_on_page]
    return await asyncio.gather(*scrape_link_tasks)

async def _scrape_table_row_data(row: ElementHandle):
    cells = await row.query_selector_all('td')
    key = remove_special_chars_from_str(await cells[0].inner_text())
    value = await cells[1].inner_text()
    return (key, value)

async def _scrape_table_text_data_from_page(page: Page, *, selector, skip_first_row=False):
    rows = await page.query_selector_all(selector)
    start_idx = 1 if skip_first_row else 0
    scrape_row_tasks = [_scrape_table_row_data(row) for row in rows[start_idx:]]
    row_data = await asyncio.gather(*scrape_row_tasks)
    return dict(row_data)

async def _scrape_element_text_data_from_page(page: Page, *, selector):
    element = await page.query_selector(selector)
    try: 
        return await element.inner_text()
    except AttributeError:
        return ""

async def scrape_data_from_page(context: BrowserContext, link, table_row_selectors, other_element_selectors):
    page = await context.new_page()
    await stealth_async(page)
    await page.goto(link)

    data = {}
    for selector in table_row_selectors:
        table_data = await _scrape_table_text_data_from_page(page, selector=selector)
        data.update(table_data)
    for key, selector in other_element_selectors.items():
        element_data = await _scrape_element_text_data_from_page(page, selector=selector)
        data[key] = element_data
    return data