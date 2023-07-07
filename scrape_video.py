# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from urllib.request import urlopen

# Function to download a video
def downloadVideo(link, id):
    print(f"Downloading video {id} from: {link}")
    
    # Cookies and headers for the request
    cookies = {
        # Please get this data from the console network activity tool
        # This is explained in the video :)
    }

    headers = {
        # Please get this data from the console network activity tool
        # This is explained in the video :)
    }

    # Parameters for the request
    params = {
        'url': 'dl',
    }

    # Data payload for the request
    data = {
        'id': link,
        'locale': 'en',
        'tt': '',  # NOTE: This value gets changed, please use the value that you get when you copy the curl command from the network console
    }
    
    print("STEP 4: Getting the download link")
    print("If this step fails, PLEASE read the steps above")
    
    # Sending a POST request to the specified URL with cookies, headers, and data
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    # Extracting the download link and video title from the response
    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    print("STEP 5: Saving the video :)")
    mp4File = urlopen(downloadLink)
    
    # Saving the video file to the specified directory
    with open(f"videos/{id}-{videoTitle}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

# Step 1: Opening Chrome browser
print("STEP 1: Open Chrome browser")
options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)

# Change the tiktok link to the desired TikTok profile
driver.get("https://www.tiktok.com/@papayaho.cat")

# IF YOU GET A TIKTOK CAPTCHA, CHANGE THE TIMEOUT HERE
# to 60 seconds, just enough time for you to complete the captcha yourself.
time.sleep(1)

scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

print("STEP 2: Scrolling page")
# Step 2: Scrolling the page to load all videos
while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break 

# Class name for TikTok video elements (may change, need to inspect the page to find the correct class)
className = "tiktok-1s72ajp-DivWrapper"

# JavaScript code to extract video URLs from the page
script  = "let l = [];"
script += "document.getElementsByClassName(\""
script += className
script += "\").forEach(item => { l.push(item.querySelector('a').href)});"
script += "return l;"

# Executing the JavaScript code to retrieve the video URLs
urlsToDownload = driver.execute_script(script)

print(f"STEP 3: Time to download {len(urlsToDownload)} videos")
# Step 3: Downloading the videos
for index, url in enumerate(urlsToDownload):
    print(f"Downloading video: {index}")
    downloadVideo(url, index)
    time.sleep(10)  # Pause between video downloads
