import requests
from reusable_functions.movie_fetch import movie_fetch






def read_file(file):
    with open(file, "r") as fileObject:
        data = fileObject.readlines()
    return data


def display_recommended_movies():
    file = "recommended_file.txt"
    data = read_file(file)
    movies = []
    for line in data[1:10]:
        movies.append(line[3:30].split("-")[0])
    #print(movies)
    movies_list = []
    for movie in movies:
        movies_list.append(movie.split("(")[0])
    return movies_list


def movies_recommendations(movies_list):
    file = "recommended_file.txt"
    url = "https://open-ai21.p.rapidapi.com/chatgpt"

    question = f"""Give me a list of movies names recommended for a user, 
                        if a user likes the movies like {movies_list}"""

    payload = {
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "web_access": False
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "691c08c111msh5335e1236e5cd76p1198f6jsn78c550e39729",
        "X-RapidAPI-Host": "open-ai21.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    results = response.json()
    # print_texts(results["result"])

    data = results["result"]
    with open(file, "w") as fileObject:
        fileObject.write(data)


def recommended_movies_data_fech_list():
    fetch_list= []
    movies_list = display_recommended_movies()
    for movie in movies_list:
        response_data = movie_fetch(movie)
        fetch_list.append(response_data)
    valid_movies_list = []
    for movie in fetch_list:
        if 'Title' in movie:
            valid_movies_list.append(movie)
    return valid_movies_list, len(valid_movies_list)






#movies_list = [ "John Wick", "ninja"]


#movies_recommendations(movies_list)

movies_list, length = recommended_movies_data_fech_list()
#print(movies_list)
#print(length)

print("#####################")
#print(recommended_movie_list(movies_list))



