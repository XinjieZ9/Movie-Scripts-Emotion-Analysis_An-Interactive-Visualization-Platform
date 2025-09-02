import json
from collections import defaultdict


with open('movie_data_review1.json', 'r') as f:
    movies = json.load(f)


region_to_movies = defaultdict(list)
for movie in movies:
    region_to_movies[movie['region']].append(movie)


res = []
for region, movie_list in region_to_movies.items():
    top_5 = sorted(movie_list, key=lambda x: x['popularity'], reverse=True)[:5]
    if len(top_5) == 5:
        res.extend(top_5)



with open('top_5_movies_by_region.json', 'w') as f:
    json.dump(res, f)



