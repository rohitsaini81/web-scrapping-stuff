import time
# from create import *
from create_mongo import insert_document
from download import *
from upload2 import *
import requests
# from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://hotxv.com/new/'
url2 = 'https://hotxv.com/video-7ekhw7kkn1v/she-fucked-her-bestie-s-boyfriend-after-party-and-don-t-regret-about-it.html'

url_list = [
    url+"/new/2",
    url+"/new/3",
    url+"/new/4",
    url+"/new/5",
    url+"/new/6",
    url+"/new/7",
    url+"/new/8",
    url+"/new/9",
    # url+"/new/1000",
]
# print(url_list)

def extract_video(vid_url):
    video = ""
    keywords = []
    html_content = scrape(vid_url)
    soup = BeautifulSoup(html_content, "html.parser")
    for div in soup.find_all("video"):
        source_tag = div.find("source")
        if source_tag:
            video = source_tag["src"]
        else:
            return "not found or error "
    keywords.append(video)
    
    
    for div in soup.find_all("p"):
        anchor_tags = div.find_all("a") # it's actually a anchor tag containing a keyword
        # keywords.append(div.text.strip())
        for anchor_tag in anchor_tags:
            if anchor_tag and anchor_tag.text.strip():
                keywords.append(anchor_tag.text.strip())
    return keywords    




def extract_data(my_url_i):
    html_content = scrape(my_url_i)
    print("Extracting...")
    soup = BeautifulSoup(html_content, "html.parser")
    videos = []
    print("Extracting from Preview page...")

    # Find all video containers
    for div in soup.find_all("div", class_="w3-third w3-container w3-margin-bottom"):
        title_tag = div.find("p")
        img_tag = div.find("img")
        span_tag = div.find("span")
        anchor_tag = div.find("a")

        if title_tag and img_tag and span_tag and anchor_tag:
            title = title_tag.text.strip()
            duration = span_tag.text.strip().split(":", 1)
            img_url = img_tag["src"]
            video_url = anchor_tag["href"]
            videos.append(
                {"title": title, "Duration": duration[1], "image": img_url, "video": video_url})
    count =0
    # Print extracted data
    for video in videos:

        title = f"{video['title']}"
        image = f"https://www.hotxv.com{video['image']}"
        
        print("Extracting from Preview page...")
        video_url = f"https://www.hotxv.com{video['video']}"
        video_data = extract_video(video_url)
        if len(video_data[0]) < 8:
            print("No... - "+video_data[0])
            continue
        print("item : "+count)
        # continue
        final_img_url = downloads(image, True)
        image = final_img_url 
        
        
        print("Downloading video...")
        file_url = video_data[0]
        # save_path = f"/tmp/{urlparse(file_url).path.rsplit('/', 1)[-1]}"  # Save location
        # print(save_path)
        # downloaded_file = download_file_temp(file_url, save_path)
        # if downloaded_file:
        #     video_url = upload_file(downloaded_file)
        #     print(f"✅ File uploaded successfully: {video_url}")
            
        # continue
        # video_url =  downloads(file_url, False)
        print("-" * 40)
        # continue
        tags = video_data[1:]
        # print("Tags: ", tags)
        
        description = "test"
        
        category = ["porn"]
        
        duration = f"{video['Duration']}"

        

        if title is None or image is None or video_url is None or len(video_url)<10 or tags is None or description is None or category is None or duration is None:
            print("Error: Missing data")
            print("title", title)
            print("image", image)
            print("video", video_url)
            print("tags", tags)
            print("description", description)
            print("category", category)
            print("duration", duration)
            print("-" * 40)
            
        else:
            print("Creating data...")
            print("-" * 40)
            insert_document(title, image, file_url, tags, description, category, duration)
            #create_video(title, image, video_url, tags, description, category, duration)
            time.sleep(1)


def set_links(i):
    print("Reading Database...")
    maindata = read_videos()
    count = 0
    if maindata is None:
        print("Error: No data to process.")
    else:
        for row in maindata:
            try:
                isImage = True
                print(count)
                print(" -" * 40)
                time.sleep(1)
                count += 1
                link = row[i]
                print("link : "+link)
            
                if i == 7:
                    isImage = False
                download_file(link, isImage)
            except Exception as e:
                print(f"Error processing row: {row}, Error: {e}")
                continue


def scrape(url_to_scrape=url):
    response = requests.get(url_to_scrape, verify=False)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    if response.status_code == 200:
        html_content = response.text
        return html_content
        # extractdata(html_content)
    else:
        print(
            f"Failed to retrieve the webpage. Status code: {response.status_code}")


def main():
    print("Starting...")    
    
    extract_data(url+"new/2")
    # for i in range(11,15):
        # extract_data(url+str(i))



if __name__ == "__main__":
    main()
