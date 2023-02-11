from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

def downloadVideo(link, id):
    cookies = {
        # Please get this data from the console network activity tool
        # This is explained in the video :)
    }

    headers = {
        # Please get this data from the console network activity tool
        # This is explained in the video :)
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'QmFhYW0_',
    }
    
    print("STEP 4: Getting the download link")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    print("STEP 5: Saving the video :)")
    mp4File = urlopen(downloadLink)
    # Feel free to change the download directory
    with open(f"videos/{id}-{videoTitle}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

print("STEP 1: Open Chrome browser")
driver = webdriver.Chrome()
# Change the tiktok link
driver.get("https://www.tiktok.com/@papayaho.cat")

# IF YOU GET A TIKTOK CAPTCHA, CHANGE THE TIMEOUT HERE
# to 60 seconds, just enough time for you to complete the captcha yourself.
time.sleep(1)

scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

print("STEP 2: Scrolling page")
while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break 

soup = BeautifulSoup(driver.page_source, "html.parser")
# this class may change, so make sure to inspect the page and find the correct class
videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper"})

print(f"STEP 3: Time to download {len(videos)} videos")
for index, video in enumerate(videos):
    print(f"Downloading video: {index}")
    downloadVideo(video.a["href"], index)
    time.sleep(10)
