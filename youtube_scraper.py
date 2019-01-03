import requests, datetime, os
key = "youtube-api-key-here"
current_timestamp = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
channels = filter(None,channels.split(","))
os.mkdir(current_timestamp)
os.chdir(current_timestamp)
for channel in channels:
	lastLine = False
	r = requests.get("https://www.googleapis.com/youtube/v3/search?key="+key+"&channelId="+channel+"&part=snippet,id&order=date&maxResults=50").json()
	videos = []
	for video in r["items"]:
		try:
			videos.append(video["id"]["videoId"])
		except Exception:
			continue
	if os.path.exists(channel+".csv"):
		f = open(channel+".csv","r")
		lastLine = f.readlines()
		f.close()
		lastLine = lastLine[-1].split(",")[3]
	r = requests.get("https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id="+",".join(videos)+"&key="+key).json()
	r["items"].reverse()
	for video in r["items"]:
		if not os.path.exists(channel+".csv"):
			f = open(channel+".csv","w")
			f.write("owner,url,title,timestamp,description,image,viewCount,likeCount,dislikeCount,commentCount\n")
			f.close()
		image = ""
		filename = channel+"$-ytb-$"+"".join(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.'))+".jpg"
		try:
			image = video["snippet"]["thumbnails"]["maxres"]["url"]
		except Exception:
			image = video["snippet"]["thumbnails"]["high"]["url"]
		payload = (video["snippet"]["channelId"]
		,video["id"]
		,video["snippet"]["title"].replace(","," ")
		,datetime.datetime.strptime(video["snippet"]["publishedAt"],"%Y-%m-%dT%H:%M:%S.%fZ").strftime("%s")
		,video["snippet"]["description"].strip().replace(","," ").replace("\n"," ")
		,image
		,video["statistics"]["viewCount"]
		,video["statistics"]["likeCount"]
		,video["statistics"]["dislikeCount"]
		,video["statistics"]["commentCount"]
		)
		if lastLine:
			if int(datetime.datetime.strptime(video["snippet"]["publishedAt"],"%Y-%m-%dT%H:%M:%S.%fZ").strftime("%s")) > int(lastLine):
				open(filename,"wb").write(requests.get(image,allow_redirects=True).content)
				f = open(channel+".csv","a")
				f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%payload)
				f.close()
		else:
			open(filename,"wb").write(requests.get(image,allow_redirects=True).content)
			f = open(channel+".csv","a")
			f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%payload)
			f.close()
os.chdir("..")