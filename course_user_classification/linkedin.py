import os
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
import numpy as np

def listToString(s): 
    # initialize an empty string
    str1 = " " 
    # return string  
    return (str1.join(s))

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://linkedin.com/uas/login")
time.sleep(3)
username = driver.find_element_by_id("username")
username.send_keys("kilua1231@gmail.co")
pword = driver.find_element_by_id("password")
pword.send_keys("okemamen123")
driver.find_element_by_xpath("//button[@type='submit']").click()

file = open("/home/moseshubert/Documents/bangkit_project/scraping/selenium/linkedin/profil_test2.txt", "r")

for line in file:
    profile_url = line
    driver.get(profile_url)     
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
    name_loc = intro.find("h1")
    name = name_loc.get_text().strip()
    works_at_loc = intro.find("div", {'class': 'text-body-medium'})
    works_at = works_at_loc.get_text().strip()

    time.sleep(3)

    try:
        driver.find_element_by_xpath("/html/body/div[7]/div[3]/div/div/div[2]/div/div/main/section[5]/div[3]/div/div/a").click()
        driver.find_element_by_xpath("/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[5]/div[3]/div/div/a").click()
        driver.find_element_by_xpath("/html/body/div[7]/div[3]/div/div/div[2]/div/div/main/section[3]/div[3]/ul/li[2]/div/div[2]/div[2]/div/div/a").click()
        driver.find_element_by_xpath("/html/body/div[7]/div[3]/div/div/div[2]/div/div/main/section[4]/div[3]/div/div/a").click()
    except: 
        pass

    time.sleep(3)

    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    time.sleep(3)

    experience = soup.find_all('span', {'class': 'mr1 t-bold'})
    experience2 = soup.find_all('span',{'class': 'mr1 hoverable-link-text t-bold'})

    exp_list=[]
    for k in range(len(experience)):
        exp = experience[k].find('span')
        experience_text= exp.get_text().strip()
        if experience_text.find("hasn't posted lately")!=-1:
            pass
        else:
            exp_list.append(experience_text)
        
    for j in range(len(experience2)):
        exp2 = experience2[j].find('span')
        experience_text2= exp2.get_text().strip()
        exp_list.append(experience_text2)
        
    time.sleep(3)

    try:
        driver.find_element_by_xpath("/html/body/div[7]/div[3]/div/div/div[2]/div/div/main/section/div[1]/button").click()
        time.sleep(3)
        driver.find_element_by_xpath("/html/body/div[7]/div[3]/div/div/div[2]/div/div/main/section[7]/div[3]/div/div/a").click()
    except:
        pass

    time.sleep(3)

    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    time.sleep(3)

    experience3 = soup.find_all('span',{'class': 'mr1 hoverable-link-text t-bold'})

    for l in range(len(experience3)):
        exp3 = experience3[l].find('span')
        experience_text3= exp3.get_text().strip()
        exp_list.append(experience_text3)

    time.sleep(3)

    try:
        driver.find_element_by_xpath("/html/body/div[7]/div[3]/div/div/div[2]/div/div/main/section/div[1]/button").click()
        time.sleep(2)
    except:
        pass

    time.sleep(3)

    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    experience4 = soup.find_all('span', {'class': 'mr1 t-bold'})

    for m in range(len(experience4)):
        exp4 = experience4[m].find('span')
        experience_text4= exp4.get_text().strip()
        if experience_text4.find("hasn't posted lately")!=-1:
            pass
        else:
            exp_list.append(experience_text4)
        #print(experience_text4)
        
    time.sleep(3)

    exp_list.append(works_at)
    exp_array = np.array(exp_list)
    exp_unique = np.unique(exp_array)
    exp_unique = listToString(exp_unique)

    try:
        df = pd.read_csv("/home/moseshubert/Documents/bangkit_project/scraping/selenium/linkedin/profil_test2.csv")
        df_update = pd.DataFrame([[name,exp_unique]],columns=["Name","Experience"])
        df = pd.concat([df,df_update], ignore_index=True)
        df.to_csv("/home/moseshubert/Documents/bangkit_project/scraping/selenium/linkedin/profil_test2.csv",index=False)
    except:
        df = pd.DataFrame([[name,exp_unique]],columns=["Name","Experience"])
        df.to_csv("/home/moseshubert/Documents/bangkit_project/scraping/selenium/linkedin/profil_test2.csv",index=False)

print(df)

"""
Label
0: Android Developer
1: Machine Learning
2: Cloud Computing
"""