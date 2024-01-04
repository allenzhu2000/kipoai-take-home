"""
Functions for scraping data from mouser.com
"""
from utils.playwright_utils import scrape_links_from_page, scrape_data_from_page, get_random_user_agent_string
import csv
import asyncio
from playwright.async_api import async_playwright
import json 
import uuid
from multiprocessing import Pool
from utils.data_utils import join_json_files_in_directory, index_list_on_attribute

MOUSER_DATA_DIR = 'mouser_data'

def _scrape_mouser_circular_connectors_page(page_number, cookies_uri, base_url, path, link_element_selector, table_row_selectors, other_element_selectors):
    async def _scrape_mouser_circular_connectors_async(page_number):
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            with open(cookies_uri) as f:
                cookies = list(csv.DictReader(f))
            context = await browser.new_context(user_agent=get_random_user_agent_string(), java_script_enabled=True, base_url=base_url)
            await context.add_cookies(cookies)
            
            links = await scrape_links_from_page(context=context, path=path, selector=link_element_selector, page_number=page_number)
            data = [await scrape_data_from_page(context, link, table_row_selectors, other_element_selectors) for link in links]

            output_file_path = f'{MOUSER_DATA_DIR}/{uuid.uuid4()}.json'
            with open(output_file_path, "w") as outfile: 
                json.dump(data, outfile)
            
    print(f'Scraping page {page_number}')
    asyncio.run(_scrape_mouser_circular_connectors_async(page_number))

def scrape_mouser_circular_connectors():
    cookies_uri = 'cookies.csv' # cookies file must be formatted with headers: name, value, domain, path
    starting_path = '/c/connectors/circular-connectors/circular-mil-spec-connectors/'
    base_url = 'https://www.mouser.com'
    link_element_selector = f'[id*="lnkMfrPartNumber"]'
    table_row_selectors = ['[id*="pdp_specs_SpecList"]']
    other_element_selectors = {'description': '[id="spnDescription"]', 'mpn': '[id="spnMouserPartNumFormattedForProdInfo"]', 'info': '[id="detail-feature"]'}
    num_pages = 70

    # Unable to parallelize due to getting blocked by Mouser. Had to go page by page with one process.
    with Pool(1) as p:
        p.starmap(_scrape_mouser_circular_connectors_page, [(page_number, cookies_uri, base_url, starting_path, link_element_selector, table_row_selectors, other_element_selectors) for page_number in range(1, num_pages + 1)])



def clean_mouser_data():
    index_column = 'mpn'
    raw_data = join_json_files_in_directory(MOUSER_DATA_DIR)
    return list(index_list_on_attribute(raw_data, index_column).values())
