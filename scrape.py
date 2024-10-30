""" import time
from selenium import webdriver
from selenium.webdriver.safari.service import Service """

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

AUTH = 'brd-customer-hl_e056cc1f-zone-ai_scraper:4zv6m9kg19d6'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

def scrape_website(website):
    print('Launching from browser...')
    
    """ safari_driver_path='/usr/bin/safaridriver' 
   
    #testing using safariwebdriver
    options = webdriver.SafariOptions()
    driver = webdriver.Safari(service=Service(safari_driver_path, options=options))

    try:
        driver.get(website)
        print('Page loaded...')
        html=driver.page_source
        time.sleep

        return html
    finally:
        driver.quit() """
    
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
       #print('Taking page screenshot to file page.png')
        #driver.get_screenshot_as_file('./page.png')
        print('Waiting captcha to solve...')
        solve_res=driver.execute('executeCdpCommand',{
            'cmd' : 'Captcha.waitForSolve',
            'params' : {'detectTimeout':10000},
        })
        print('Captcha solve status :' ,solve_res['value']['status'])
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html
    
#extract html as preferred
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content,'html.parser')
    body_content= soup.body
    if body_content:
        return str(body_content)
    return ''

#clean htmlBodyContent
def clean_body_content(html_content):
    soup=BeautifulSoup(html_content,"html.parser")

    #check inside content for script and styles and remove them
    for script_or_style in soup(['script','style']):
        script_or_style.extract()

    #remove newline characters
    cleaned_content = soup.get_text(separator='\n')
    #remove unnecessary newline characters if no text between \n remove that unwanted space
    cleaned_content='\n'.join(
        line.strip() for line in cleaned_content.splitlines()
        if line.strip())
    
    return cleaned_content

def split_cleaned_content(cleaned_content, max_length=5000):
    return[
        #split cleaned content to chunks of 5000 characters
        cleaned_content[i:i + max_length ]for i in range(0, len(cleaned_content), max_length)
    ]
