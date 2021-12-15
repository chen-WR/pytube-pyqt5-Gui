from pytube import YouTube,Playlist
import requests
from bs4 import BeautifulSoup
import json

video_list = list()

url = "https://www.youtube.com/results?search_query=jpop"

res = requests.get(url)

soup = BeautifulSoup(res.text,'lxml')

# source will contain all youtube page element tag of "Script"
source = soup.find_all('script')

# the 34th or index 33 of those script is the one containing all the video data to the links of the videos
javascript = str(source[33])

# remove all unneccessary string from the data to make it json like
json1 = javascript.split('var ytInitialData = ')

# continue remove unneccessary string from the data
json2 = json1[1].split(';</script>')

# use json lib to load the string data in as a dictionary
hashmap = json.loads(json2[0])

# after going through all the keys, the contents will be revealed
data = hashmap["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

# create json file to see how the data is like with indentation
with open('example.json',"w") as file:
	json.dump(data,file,indent=4)

# only grabbing videoRenderer and playlistRenderer from the contents
for obj in data:
	if "videoRenderer" in obj.keys():
		url = obj["videoRenderer"]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
	elif "playlistRenderer" in obj.keys():
		url = obj["playlistRenderer"]["viewPlaylistText"]["runs"][0]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]

	video_list.append(url)

for i in video_list:
	print(i)


