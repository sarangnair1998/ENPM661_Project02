import time
import copy
import cv2
from queue import PriorityQueue
import numpy as np
from math import cos, sin, pi


def action_move_up(node, canvas):
    return move_node(node, canvas, 0, -1)

def action_move_down(node, canvas):
    return move_node(node, canvas, 0, 1)

def action_move_right(node, canvas):
    return move_node(node, canvas, 1, 0)

def action_move_left(node, canvas):
    return move_node(node, canvas, -1, 0)

def action_move_up_right(node, canvas):
    return move_node(node, canvas, 1, -1)

def action_move_down_right(node, canvas):
    return move_node(node, canvas, 1, 1)

def action_move_down_left(node, canvas):
    return move_node(node, canvas, -1, 1)

def action_move_up_left(node, canvas):
    return move_node(node, canvas, -1, -1)


def valid(node, canvas, xdot, ydot):
    x, y = node
    new_x, new_y = x + xdot, y + ydot
    return (0 <= new_x < canvas.shape[1] and 0 <= new_y < canvas.shape[0] 
            and canvas[new_y][new_x][2] < 255)

def move_node(node, canvas, xdot, ydot):
    next_node = (node[0] + xdot, node[1] + ydot)
    if valid(node, canvas, xdot, ydot):
        return True, next_node
    else:
        return False, node
    
def draw_regular_polygon_with_clearance(canvas, color, vertex_count, radius, position, rotation=0, clearance=0,thickness = -1):
    n = vertex_count
    r = radius + clearance 
    x, y = position
    rotation_rad = pi / 180 * rotation 

    vertices = []
    for i in range(n):
        x_i = x + r * cos(rotation_rad + 2 * pi * i / n)
        y_i = y + r * sin(rotation_rad + 2 * pi * i / n)
        vertices.append((int(x_i), int(y_i)))
    
    return vertices



def obstacles_map(canvas):
    
    cv2.polylines(canvas, [np.array([(0, 0), (1200, 0), (1200, 500), (0, 500)])], isClosed=True, color=(0, 0, 255), thickness=5)
    
    cv2.fillPoly(canvas, pts = [np.array([(100,400), (175,400), (175,0), (100,0)])], color = (255, 0, 0))
    cv2.polylines(canvas, pts = [np.array([(100,400), (175,400), (175,0), (100,0)])],isClosed=True, color=(0, 0, 255), thickness=5)
    
    cv2.fillPoly(canvas, pts = [np.array([(275,100), (350,100), (350,500), (275,500)])], color = (255, 0, 0))
    cv2.polylines(canvas, pts = [np.array([(275,100), (350,100), (350,500), (275,500)])],isClosed=True, color=(0, 0, 255), thickness=5)
    
    hexagon1_center = (650, 250)
    hexagon1_radius = 150
    hexagon1_rotation = 90
    clearance1 = 0
    clearance2 = 5
    vertices1 = draw_regular_polygon_with_clearance(canvas, (0, 0, 255), 6, hexagon1_radius, hexagon1_center, hexagon1_rotation, clearance1)
    vertices2 = draw_regular_polygon_with_clearance(canvas, (0, 0, 255), 6, hexagon1_radius, hexagon1_center, hexagon1_rotation, clearance2)
    cv2.fillPoly(canvas, pts = [np.array(vertices1)], color = (255, 0, 0))
    cv2.polylines(canvas, pts = [np.array(vertices2)],isClosed=True, color=(0, 0, 255), thickness=5)
    
    cv2.fillPoly(canvas, pts = [np.array([(900,375), (1020,375), (1020,125), (900,125),(900,50),(1100,50),
                                          (1100,450),(900,450)])], color = (255, 0, 0))
    cv2.polylines(canvas, pts = [np.array([(900,375), (1020,375), (1020,125), (900,125),(900,50),(1100,50),
                                          (1100,450),(900,450)])],isClosed=True, color=(0, 0, 255), thickness=5)
    
    return canvas


def check_obstacle_map(x, y):
    hexagon1_center = (650, 250)
    hexagon1_radius = 150
    hexagon1_rotation = 90
    clearance = 5
    vertices1 = draw_regular_polygon_with_clearance(canvas, (0, 0, 255), 6, hexagon1_radius, hexagon1_center, hexagon1_rotation,clearance)
    obstacle_polygons = [
        [(95, 405), (180, 405), (180, 0), (95, 0)],
        [(270, 95), (355, 95), (355, 500), (270, 500)],
        vertices1,
        [(895, 380), (1025, 380), (1025, 120), (895, 120),
         (895, 55), (1095, 55), (1095, 445), (895, 445)]
    ]
    for obstacle in obstacle_polygons:
        if cv2.pointPolygonTest(np.array(obstacle), (x, y), False) >= 0:
            return True
    return False

def check_coordinates():    
    start_x = int(input("Enter the X coordinate of the start position: "))
    start_y = int(input("Enter the Y coordinate of the start position: "))
    goal_x = int(input("Enter the X coordinate of the goal position: "))
    goal_y = int(input("Enter the Y coordinate of the goal position: "))

    if not (5 <= start_x <= 1195 and 5 <= start_y <= 495):
        print("The start position is out of bounds or within the clearance area.")
        return None
    if not (5 <= goal_x <= 1195 and 5 <= goal_y <= 495):
        print("The goal position is out of bounds or within the clearance area.")
        return None
    
    if check_obstacle_map(start_x, start_y) or check_obstacle_map(goal_x, goal_y):
        print("Start or goal position falls within an obstacle.")
        return None
    else:
        print("Start and goal positions are not obstructed by obstacles.")
    
        return [start_x, start_y], [goal_x, goal_y]

def dijkstra_algo(start, goal, canvas):
    explored = set()
    final_list = {}
    new_list = PriorityQueue()
    new_list.put((0, start, start))  
    goal = tuple(goal)
    canvas = np.array(canvas)
    
    while not new_list.empty():
        cost, parent_node, present_node = new_list.get()
        
        present_node = tuple(present_node)
        
        if present_node in explored:
            continue
        
        explored.add(present_node)
        
        final_list[present_node] = parent_node
        
        if present_node == goal:
            back_track_flag = True
            print("Time to back track and find the solution")
            break
        
        for flag, next_node in [
            move_node(present_node, canvas, 0, -1),
            move_node(present_node, canvas, 1, -1),
            move_node(present_node, canvas, 1, 0),
            move_node(present_node, canvas, 1, 1),
            move_node(present_node, canvas, 0, 1),
            move_node(present_node, canvas, -1, 1),
            move_node(present_node, canvas, -1, 0),
            move_node(present_node, canvas, -1, -1)]:
            
            if flag:
                new_cost = cost + 1
                
                if next_node not in explored:
                    new_list.put((new_cost, present_node, next_node))
    
    if back_track_flag:
        back_track(start, goal, final_list, canvas)
    else:
        return None
    
def back_track(start, goal, final_list, canvas):
    
    # Define video parameters
    output_video = cv2.VideoWriter('Animation Video.mp4', cv2.VideoWriter_fourcc(*'XVID'), 800, (canvas.shape[1], canvas.shape[0]))
    frames_to_skip = 10
    frame_count = 0
    
    # Draw explored nodes and write to video
    for node in final_list:
        canvas[node[1], node[0]] = [255, 120, 200]  # Red color for explored nodes
        if frame_count % frames_to_skip == 0:
            output_video.write(canvas)
        frame_count += 1

    # Build backtracked path
    backstack = [goal]
    while backstack[-1] != start:
        backstack.append(final_list[tuple(backstack[-1])])

    # Draw start and goal nodes
    for state in (start, goal):
        cv2.circle(canvas, tuple(state), 3, ([0, 255, 0], [0, 0, 255])[state == goal], 3)

    # Draw backtracked path and write to video
    while backstack:
        path_node = backstack.pop()
        canvas[path_node[1], path_node[0]] = [0, 255, 0]  # White color for path nodes
        if frame_count % frames_to_skip == 0:
            output_video.write(canvas)
        frame_count += 1

    # Release video writer and display final canvas
    output_video.release()
    cv2.imshow("Backtracked Path", canvas)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    

