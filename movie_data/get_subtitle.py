import requests
import json
from tqdm import tqdm
from collections import defaultdict, Counter
def search_subtitle_file_id(tmdb_id, api_key):
    url = "https://api.opensubtitles.com/api/v1/subtitles"

    querystring = {"tmdb_id":str(tmdb_id),"languages":"en"}

    headers = {
        "User-Agent": "Kodi Plugin v0.1",
        "Api-Key": api_key
    }

    response = requests.get(url, headers=headers, params=querystring)
    

    try:
        response = response.json()
        file_id = response["data"][0]["attributes"]["files"][0]["file_id"]
    except Exception as e:
        print(f"no subtitle for tmdb: {tmdb_id} \n--{e} \n--{response}")
        return -1
    
    return file_id


def subtitle_file_link(file_id, api_key):

    url = "https://api.opensubtitles.com/api/v1/download"

    payload = { "file_id": file_id }
    headers = {
        "User-Agent": "Kodi Plugin v0.1",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Api-Key": api_key
    }

    response = requests.post(url, json=payload, headers=headers)
    

    try:
        response = response.json()
        return response["link"], response["remaining"]
    except Exception as e:
        print(f"file_id {file_id} fail to get file_link  \n--{e} \n-- {response}")
        return -1,-1
    

def download_subtitle(url):
    response = requests.get(url)

    try:
        subtitle_text = response.content.decode("utf-8", errors="replace")
        return subtitle_text
    except Exception as e:
        print(f"fail to dowanload {url} \n--{e} \n-- {response}")
        return url

    
def main_process(tmdb_json_file,output_file,clean_output_file, open_subtitle_api_list):
    api_key_idx = 0
    api_download_remaining = 100

    with open(tmdb_json_file) as f:
        movies = json.load(f)
    region_to_movies = defaultdict(list)
    for movie in movies:
        region_to_movies[movie['region']].append(movie)

    for region in region_to_movies:
        region_to_movies[region].sort(key=lambda m: m.get("popularity", 0), reverse=True)

    require_region_movie_count = {}
    for region, data_list in region_to_movies.items():
        with open(output_file, "a", encoding="utf-8") as out_f:
            for data in data_list:
                if require_region_movie_count.get("region", 0) == 5:
                    print(f"{region} finished")
                    break
                tmdb_id = data["movie_id"]
                if api_download_remaining <= 0:
                    api_key_idx +=1
                    print("API Idx change to: ", api_key_idx)
                    api_download_remaining = 100
                api_key = open_subtitle_api_list[api_key_idx] 
                file_id = search_subtitle_file_id(tmdb_id, api_key)
                data["subtitle_id"] = -1
                data["subtitle_text"] = -1
                if file_id != -1:
                    file_link, remaining_quota = subtitle_file_link(file_id, api_key)
                    api_download_remaining = remaining_quota
                    if file_link != -1:
                        subtitle_text = download_subtitle(file_link)
                        data["subtitle_id"] = file_id
                        data["subtitle_text"] = subtitle_text
                        require_region_movie_count[region] = require_region_movie_count.get("region",0)+1
                out_f.write(json.dumps(data, ensure_ascii=False) + "\n")
        
    print("finished download")

    #start to clean output file
    #remove the region which doesn't have 5 valid movies
    invalid_regions = []
    for key, value in require_region_movie_count.items():
        if value < 5:
            invalid_regions.append(key)

    res = []
    with open(output_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                region = str(data.get("region", ""))
                sub_id = data.get("subtitle_id")
                if region in invalid_regions:
                    continue
                if sub_id == -1:
                    continue
                res.append(data)

            except json.JSONDecodeError:
                continue
    with open(clean_output_file, 'w') as f:
        json.dump(res, f)
    print("finished clean")
    
if __name__ == "__main__":
        open_subtitle_api_list = [] #your open_subtitle api key. Each key can only retrive 100 subtitle, so you may need to create more than one
        main_process("movie_data_review1.json", "top5_movie_data_with_subtitle.jsonl", "clean_top5_movie_data_with_subtitle.json", open_subtitle_api_list)