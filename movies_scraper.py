import requests
from bs4 import BeautifulSoup

url_list = {}
api_key = "54bd7f2622b655dd3c614947806b1b09fd1b6149"  # Replace this with your actual API key


def search_movies(query):
    movies_list = []
    website = BeautifulSoup(requests.get(f"https://mkvcinemas.skin/?s={query.replace(' ', '+')}").text, "html.parser")
    movies = website.find_all("a", {'class': 'ml-mask jt'})
    for movie in movies:
        movies_details = {}
        if movie:
            movies_details["id"] = f"link{movies.index(movie)}"
            movies_details["title"] = movie.find("span", {'class': 'mli-info'}).text
            url_list[movies_details["id"]] = movie['href']
            movies_list.append(movies_details)
    return movies_list


def get_movie(query):
    movie_details = {}
    try:
        movie_page_link = BeautifulSoup(requests.get(f"{url_list[query]}").text, "html.parser")
        if movie_page_link:
            title = movie_page_link.find("div", {'class': 'mvic-desc'}).h3.text
            movie_details["title"] = title
            img = movie_page_link.find("div", {'class': 'mvic-thumb'})['data-bg']
            movie_details["img"] = img
            links = movie_page_link.find_all("a", {'rel': 'noopener', 'data-wpel-link': 'internal'})
            final_links = {}
            for i in links:
                url = f"https://urlshortx.com/api?api={api_key}&url={i['href']}"
                response = requests.get(url)
                link = response.json()
                final_links[f"{i.text}"] = link['shortenedUrl']
            movie_details["links"] = final_links
    except Exception as e:
        print("Error:", e)
    return movie_details


# Example usage:
# movies = search_movies("your_query_here")
# print(movies)
# movie_details = get_movie("link0")  # Provide the id obtained from search_movies
# print(movie_details)
