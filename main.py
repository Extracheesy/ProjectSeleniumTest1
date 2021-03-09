import os
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from json import loads
import pandas as pd

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def get_list_gainers(driver):

    driver.get('https://finance.yahoo.com/gainers?offset=0&count=100')
    html_src_1 = driver.page_source
    driver.get('https://finance.yahoo.com/gainers?count=100&offset=100')
    html_src_2 = driver.page_source

    html_src_str_1 = str(html_src_1)
    html_src_str_1 = html_src_str_1.replace("{",'\n')
    html_src_str_1 = html_src_str_1.replace("}",'\n')

    html_src_str_2 = str(html_src_2)
    html_src_str_2 = html_src_str_2.replace("{",'\n')
    html_src_str_2 = html_src_str_2.replace("}",'\n')

    match_1 = re.findall(r'"symbol":".*","shortName":', html_src_str_1)
    match_2 = re.findall(r'"symbol":".*","shortName":', html_src_str_2)

    list_gainers = []

    for i in range(0,len(match_1),1):
        tmp_string = match_1[i][10:]
        size = len(tmp_string)
        string = tmp_string[: size - 14]
        list_gainers.append(string)
        #print(string)

    for i in range(0,len(match_2),1):
        tmp_string = match_2[i][10:]
        size = len(tmp_string)
        string = tmp_string[: size - 14]
        list_gainers.append(string)
        #print(string)

    return list_gainers

def get_list_losers(driver):

    driver.get('https://finance.yahoo.com/losers?offset=0&count=100')
    html_src_1 = driver.page_source
    driver.get('https://finance.yahoo.com/losers?count=100&offset=100')
    html_src_2 = driver.page_source

    html_src_str_1 = str(html_src_1)
    html_src_str_1 = html_src_str_1.replace("{",'\n')
    html_src_str_1 = html_src_str_1.replace("}",'\n')

    html_src_str_2 = str(html_src_2)
    html_src_str_2 = html_src_str_2.replace("{",'\n')
    html_src_str_2 = html_src_str_2.replace("}",'\n')

    match_1 = re.findall(r'"symbol":".*","shortName":', html_src_str_1)
    match_2 = re.findall(r'"symbol":".*","shortName":', html_src_str_2)

    list_losers = []

    for i in range(0, len(match_1), 1):
        tmp_string = match_1[i][10:]
        size = len(tmp_string)
        string = tmp_string[: size - 14]
        list_losers.append(string)
        # print(string)

    for i in range(0, len(match_2), 1):
        tmp_string = match_2[i][10:]
        size = len(tmp_string)
        string = tmp_string[: size - 14]
        list_losers.append(string)
        # print(string)

    return list_losers

def get_list_trending_tickers(driver):

    driver.get('https://finance.yahoo.com/trending-tickers')
    html_src_1 = driver.page_source
    #driver.get('https://finance.yahoo.com/most-active?count=100&offset=100')
    #html_src_2 = driver.page_source

    html_src_str_1 = str(html_src_1)
    html_src_str_1 = html_src_str_1.replace("{",'\n')
    html_src_str_1 = html_src_str_1.replace("}",'\n')

    match_1 = re.findall(r'"YFINANCE:.*","fallbackCategory":', html_src_str_1)
    tmp_string = match_1[0][10:]
    size = len(tmp_string)
    string = tmp_string[: size - 21]
    list_trending_tickers = string.split(",")

    return list_trending_tickers

def get_list_most_actives(driver):

    driver.get('https://finance.yahoo.com/most-active?offset=0&count=100')
    html_src_1 = driver.page_source
    driver.get('https://finance.yahoo.com/most-active?count=100&offset=100')
    html_src_2 = driver.page_source

    html_src_str_1 = str(html_src_1)
    html_src_str_1 = html_src_str_1.replace("{", '\n')
    html_src_str_1 = html_src_str_1.replace("}", '\n')

    html_src_str_2 = str(html_src_2)
    html_src_str_2 = html_src_str_2.replace("{", '\n')
    html_src_str_2 = html_src_str_2.replace("}", '\n')

    match_1 = re.findall(r'"symbol":".*","shortName":', html_src_str_1)
    match_2 = re.findall(r'"symbol":".*","shortName":', html_src_str_2)

    list_most_actives = []

    for i in range(0, len(match_1), 1):
        tmp_string = match_1[i][10:]
        size = len(tmp_string)
        string = tmp_string[: size - 14]
        list_most_actives.append(string)
        # print(string)

    for i in range(0, len(match_2), 1):
        tmp_string = match_2[i][10:]
        size = len(tmp_string)
        string = tmp_string[: size - 14]
        list_most_actives.append(string)
        # print(string)

    return list_most_actives

if __name__ == '__main__':

    DRIVER_PATH = "C:/Users/despo/chromedriver_win32/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get('https://finance.yahoo.com/gainers')
    driver.find_element_by_name("agree").click()

    list_gainers = get_list_gainers(driver)
    list_losers = get_list_losers(driver)
    list_trending_tickers = get_list_trending_tickers(driver)
    list_most_actives = get_list_most_actives(driver)

    ticker_list = list_gainers + list_losers + list_trending_tickers + list_most_actives

    df = pd.DataFrame({'tic': ticker_list})

    df = df.drop_duplicates()
    # df = df.reset_index()
    df = df.sort_values(['tic'], ignore_index=True)
    df.to_csv("ticker_list_no_duplicate.csv", index=False)

    print_hi('PyCharm')
