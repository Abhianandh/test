import csv
import sys

from util import Node,StackFrontier,QueueFrontier

#Data structures to store information about people, movies, and stars
names = {}
people = {}
movies = {}

#Load data from CSV files into data structures
def load_data(directory):
    #Load people
    with open(f"{directory}/people.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": int(row["birth"])
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = set()
            names[row["name"].lower()].add(row["id"])

    #Load movies
    with open(f"{directory}/movies.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": int(row["year"]),
                "stars": set()
            }

    #Load stars
    with open(f"{directory}/stars.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                people_id = row["person_id"]
                movie_id = row["movie_id"]
                people[people_id]["movies"].add(movie_id)
                movies[movie_id]["stars"].add(people_id)
            except KeyError:
                pass

#Find neighbors for a given person
def neighbors_for_person(person_id):
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            if person_id != person_id:
                neighbors add((movie_id, person_id))
    return neighbors

#Find the shortest path between two actors using different frontiers
def shortest_path(source, target, frontier_type):
    explored = set()
    initial_node = Node(source, None, None)
    
    if frontier_type == "stack":
        frontier = StackFrontier()
    elif frontier_type == "queue":
        frontier = QueueFrontier()
    else:
        sys.exit("Invalid frontier type")

    frontier.add(initial_node)
    
    while not frontier.empty():
        node = frontier.remove()
        if node.state == target:
            path = []
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path
        explored.add(node.state)
        neighbors = neighbors_for_person(node.state)
        for movie_id, person_id in neighbors:
            if person_id not in explored and not frontier.contains_state(person_id):
                child = Node(person_id, node, movie_id)
                frontier.add(child)
    
    return None

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python degrees.py [directory] [frontier_type]")
    directory = sys.argv[1]
    frontier_type = sys.argv[2]

    load_data(directory)

    while True:
        source = person_id_for_name(input("Name: "))
        if source is None:
            sys.exit("Person not found.")
        target = person_id_for_name(input("Name: "))
        if target is None:
            sys.exit("Person not found.")

        path = shortest_path(source, target, frontier_type)

        if path is None:
            print("Not connected.")
        else:
            degrees = len(path)
            print(f"{degrees} degrees of separation.")
            for i, (movie_id, person_id) in enumerate(path):
                person = people[person_id]["name"]
                movie = movies[movie_id]["title"]
                print(f"{i + 1}: {person} and {movie}")

#Helper function to get a person's ID by their name
def person_id_for_name(name):
    name_lower = name.lower()
    if name_lower in names:
        if len(names[name_lower]) == 1:
            return names[name_lower].pop()
        else:
            print("Which one?")
            for person_id in names[name_lower]:
                person = people[person_id]
                print(f"ID: {person_id}, Name: {person['name']}, Birth Year: {person['birth']}")
            try:
                person_id = input("Enter the person's ID: ")
                if person_id in names[name_lower]:
                    return person_id
            except ValueError:
                pass
    return None

if __name__ == "__main__":
    main()
