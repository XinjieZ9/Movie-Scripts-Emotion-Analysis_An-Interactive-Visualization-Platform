
import requests
import json
import pandas as pd
import concurrent.futures


class  TMDBAPIUtils:

    # Do not modify
    def __init__(self, headers:str):
        self.api_headers = headers

    def get_available_regions(self):
        try:
            with open('tmdb_available_regions.json', 'r') as f:
                regions = json.load(f)
            return regions
        except:
            url = "https://api.themoviedb.org/3/configuration/countries?language=en-US"
            response = requests.get(url, headers=self.api_headers)
            regions = json.loads(response.text)
            with open('tmdb_available_regions.json', 'w') as f:
                json.dump(regions, f)
            return regions


    def get_top_rated_movies_by_region(self, region_code="US", page=1):
        """
        each page contains about 15 movie
        page = 1 contains highest rated movie from top 1 to top 15
        page = 2                              from top 16 to top 30
        """
        moive_list = []
     
        #https://www.themoviedb.org/talk/51b8d148760ee309a50c8a3d
        url = f"https://api.themoviedb.org/3/discover/movie?language=en-US&page={page}&sort_by=vote_average.desc&with_origin_country={region_code}"

        response = requests.get(url, headers=self.api_headers)
        response = json.loads(response.text)
        moive_list.extend(response["results"])
        return moive_list
    
    def get_top_popular_movies_by_region(self, region_code="US",page=1):
        moive_list = []

        url = f"https://api.themoviedb.org/3/discover/movie?language=en-US&page={page}&sort_by=popularity.desc&with_origin_country={region_code}"

        response = requests.get(url, headers=self.api_headers)
        response = json.loads(response.text)
        moive_list.extend(response["results"])
        return moive_list
    
    def get_movie_reviews(self, movie_id, num_reviews = 100):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1"
        response = requests.get(url, headers=self.api_headers)
        response =  json.loads(response.text)
        try:
            review_list = response["results"]
            count = len(review_list)
            total_reviews = response["total_results"]
            page = 2
            while count < total_reviews and count < num_reviews:
                url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page={page}"
                response = requests.get(url, headers=self.api_headers)
                response =  json.loads(response.text)
                review_list.extend(response["results"])
                count = len(review_list)
                page+=1
            return [review["content"] for review in review_list]
        except:
            return []
    
    def get_movie_poster(self, poster_path):
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    
    def process_region(self, region):
        movie_data = []
        review_size = []

        region_code = region["iso_3166_1"]
        print(region_code)
        region_movie_size = 0
        region_movie_page = 0

        while region_movie_size < 30:
            region_movie_page += 1
            movie_list = self.get_top_popular_movies_by_region(region_code, page=region_movie_page)
            if not movie_list:
                break
            for movie in movie_list:
                review_list = self.get_movie_reviews(movie["id"])
                if len(review_list) < 5:
                    continue
                review_size.append(len(review_list))
                movie_info = {
                    "movie_id": movie.get("id"),
                    "movie_title": movie.get("title"),
                    "release_date": movie.get("release_date"),
                    "poster_path": movie.get("poster_path"),
                    "region": region.get("english_name"),
                    "movie_rate": movie.get("vote_average"),
                    "vote_count": movie.get("vote_count"),
                    "review_list": review_list,
                    "overview": movie.get("overview")
                }
                movie_data.append(movie_info)
                region_movie_size += 1

        return movie_data, review_size

    def main_process(self):
        regions = self.get_available_regions()
        all_movie_data = []
        all_review_sizes = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_region, region) for region in regions]
            for future in concurrent.futures.as_completed(futures):
                movie_data, review_size = future.result()
                all_movie_data.extend(movie_data)
                all_review_sizes.extend(review_size)

        with open("movie_data_parrallel.json", "w", encoding="utf-8") as json_file:
            json.dump(all_movie_data, json_file)

        print("finished")
        # print("review_size: ", all_review_sizes)
        

if __name__ == "__main__":

    
    headers = {
            "accept": "application/json",
            "Authorization": "Bearer XXXXX" #add your TMDB Authoriztion token
    }
    tmdb_api_utils = TMDBAPIUtils(headers)

    tmdb_api_utils.main_process()

