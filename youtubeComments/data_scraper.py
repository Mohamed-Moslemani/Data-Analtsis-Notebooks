from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd  

chromedriver_path = r"C:\chromedriver-win64\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument('--headless')  
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

def scrape_youtube_comments(video_url, num_scrolls=200):  
    driver.get(video_url)
    time.sleep(5)
    action = ActionChains(driver) 
    for _ in range(num_scrolls):
        action.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)  
    comment_elements = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
    comments = [comment.text for comment in comment_elements]
    return comments

video_url = 'https://www.youtube.com/watch?v=Pv0iVoSZzN8'
comments = scrape_youtube_comments(video_url)

for i, comment in enumerate(comments):
    print(f"{i+1}: {comment}")

df_comments = pd.DataFrame(comments, columns=["Comment"])
df_comments.to_csv("youtube_comments.csv", index=False)

driver.quit()
