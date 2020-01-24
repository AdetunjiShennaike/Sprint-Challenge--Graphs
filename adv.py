from room import Room
from player import Player
from world import World
from stack import Stack
from queue import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def dft_recursive(room, traveled, visited = None, revisited = None):
  if visited is None:
    visited = set()
  visited.add(room)
  if revisited is None:
    revisited = set()
  print(room)
  if len(visited) == len(room_graph):
    return traveled
  if room.n_to is not None and room.n_to not in visited:
    traveled.append('n')
    dft_recursive(room.n_to, traveled, visited, revisited)
  elif room.s_to is not None and room.s_to not in visited:
    traveled.append('s')
    dft_recursive(room.s_to, traveled, visited, revisited)
  elif room.e_to is not None and room.e_to not in visited:
    traveled.append('e')
    dft_recursive(room.e_to, traveled, visited, revisited)
  elif room.w_to is not None and room.w_to not in visited:
    traveled.append('w')
    dft_recursive(room.w_to, traveled, visited, revisited)
  elif room.w_to is not None and room.w_to not in revisited:
    revisited.add(room)
    traveled.append('w')
    dft_recursive(room.w_to, traveled, visited, revisited)
  elif room.e_to is not None and room.e_to not in revisited:
    revisited.add(room)
    traveled.append('e')
    dft_recursive(room.e_to, traveled, visited, revisited)
  elif room.s_to is not None and room.s_to not in revisited:
    revisited.add(room)
    traveled.append('s')
    dft_recursive(room.s_to, traveled, visited, revisited)
  elif room.n_to is not None and room.n_to not in revisited:
    revisited.add(room)
    traveled.append('n')
    dft_recursive(room.n_to, traveled, visited, revisited)
  

dft_recursive(world.starting_room, traversal_path)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
