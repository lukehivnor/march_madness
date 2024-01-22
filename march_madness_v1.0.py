import csv
import bs4
import os
import sys
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

def ncaa_rankings_fetcher():
    intro = "C:\\Users\\lukeh\\PycharmProjects\\MLB_Proj\\"
    for j in intro:
        if j == '\\':
            j.replace('\\', '/')
    url = 'https://kenpom.com/'
    options = Options()
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    shitshow = driver.page_source

    print('SHITSHOW DONE')

    h = driver.find_elements(By.CLASS_NAME, 'hard_left')
    j = driver.find_elements(By.CLASS_NAME, 'next_left')
    w = driver.find_elements(By.CLASS_NAME, 'wl')
    o = driver.find_elements(By.CLASS_NAME, 'td-left divide')
    d = driver.find_elements(By.CLASS_NAME, 'td-left')
    t = driver.find_elements(By.CLASS_NAME, 'td-right')

    hard_left = []
    next_left = []
    win_loss = []
    o_eff = []
    d_eff = []
    eff = []
    tempo = []
    eight = []
    for i in h:
        hard_left.append(i.get_attribute('innerHTML'))
    for i in j:
        next_left.append(i.get_attribute('innerHTML'))
    for i in w:
        win_loss.append(i.get_attribute('innerHTML'))
    for i in o:
        print(i.get_attribute('innerHTML'))
    for i in d:
        eight.append(i.get_attribute('innerHTML'))
    for i in range(0, len(eight), 8):
        tempo.append(eight[i:i+8])
    driver.quit()
    next_left = next_left[2:]
    for i in range(len(next_left)):
        try:
            l = next_left[i].split('>')
            k = l[1].split('<')
            next_left[i] = k[0]
        except IndexError:
            pass


    head = ["Team", "Adj Off Eff", "Adj Def Eff", "Adj Tempo", "Luck", "SOS", "Opp O EFF", "Opp D EFF", "SOS-NON CONF"]
    row = []
    col = []
    send = []
    row.append(head)
    teams = []
    tester = []
    for j in range(len(next_left)):
        if next_left[j] == '':
            continue
        else:
            tester.append(next_left[j])
    for j in tester:
        print(j)
    for j in tester:
        if j == 'Team':
            continue
        else:
            teams.append(j)
    if len(tempo) < len(teams):
        teams = teams[:len(tempo)]
    for i in range(len(tempo)):
        col.append(teams[i])
        for j in range(0,7):
            col.append(tempo[i][j])
        row.append(col)
        col = []

    df = pd.DataFrame(row)
    df.to_csv(intro+'test6_march_madness_2-28.csv', mode='a+')


ncaa_rankings_fetcher()