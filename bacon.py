import csv
from collections import deque

class Baconator:
    def __init__(self, filename):
        self.actors = {} #key:value pair of Actor Name and Actor Object
        self.movies = {} #key:value pair of Movie Name and Movie Object
        self.filename = filename
        self.load_csv()

    class Actor:
        def __init__(self, name):
            self.name = name
            self.movies = set() #set of movie objects actor is part of

    class Movie:
        def __init__(self, title):
            self.title = title 
            self.actors = set() #set of actor objects within movie

    class BaconLink: #linking of the two actors and their movies they have been a part of
        def __init__(self, actor1, actor2, movie):
            self.actor1 = actor1
            self.actor2 = actor2
            self.movie = movie

    def load_csv(self):
        with open(self.filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                title = row[0] #index 0 is the movie title in the csv
                actor_list = row[1:] #the rest of the line contains the actor titles
                movie_obj = self.Movie(title)

                for actor_name in actor_list:
                    if actor_name not in self.actors: #create Actor object if we haven't already seen them and add to our actor dictionary else retrieve the actor object we already had
                        actor_obj = self.Actor(actor_name) 
                        self.actors[actor_name] = actor_obj
                    else:
                        actor_obj = self.actors[actor_name]

                    actor_obj.movies.add(movie_obj) #add the movie into the actor object set of movies theyve been in 
                    movie_obj.actors.add(actor_obj)

                self.movies[title] = movie_obj

    def get_bacon_path(self, name):
        if name == "Kevin Bacon":
            return ["Kevin Bacon"]

        queue = deque()
        visited = set() #keeps track of the actors we have visited
        paths = {} #dictionary of baconlinks

        starting_actor = self.actors.get(name)
        if starting_actor:
            queue.append(starting_actor)

        while queue:
            curr_actor = queue.popleft()
            visited.add(curr_actor)

            for movie in curr_actor.movies: #Check all the movies within the actor object and check all the coactors inside the movie objects
                for co_actor in movie.actors:
                    if co_actor not in visited: #append coactor if not visited yet into queue and visited and creating the baconlink with the current actor
                        queue.append(co_actor)
                        visited.add(co_actor)
                        paths[co_actor] = self.BaconLink(curr_actor, co_actor, movie)

                        if co_actor.name == "Kevin Bacon": #when we encounter Kevin Bacon we found our stopping point to build our path
                            path = [] #list of strings which is the path for the shortest path from one actor to kevin bacon
                            current = co_actor 

                            while current != starting_actor: #keep building our path until we reach the starting actor
                                link = paths.get(current) #get the baconlink between the current actor
                                path.append(current.name) #append their name onto the list and the movie title in between
                                path.append(link.movie.title)
                                current = link.actor1 #increment current actor to the coactor that linked with them

                            path.append(starting_actor.name) 
                            return path[::-1] #return reversed of the path since we are appending starting from Kevin Bacon

        return []

# Example usage:
if __name__ == "__main__":
    baconator = Baconator('movies.csv')
    print(baconator.get_bacon_path('Keanu Reeves'))
    print(baconator.get_bacon_path('Neil Fingleton'))
    baconator1 = Baconator('river.csv')
    print(baconator1.get_bacon_path("Wing"))
    print(baconator1.get_bacon_path("Wing"))

