import random
import time

# Represents a point with x and y coordinates
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Determines the quadrant of a point
def quad(p):
    if p.x >= 0 and p.y >= 0:
        return 1
    if p.x <= 0 and p.y >= 0:
        return 2
    if p.x <= 0 and p.y <= 0:
        return 3
    return 4

# Checks whether the line is crossing the polygon
def orientation(a, b, c):
    res = (b.y - a.y) * (c.x - b.x) - (c.y - b.y) * (b.x - a.x)
    if res == 0:
        return 0
    if res > 0:
        return 1
    return -1

# Compare function for sorting
def point_comparator(p1, p2):
    one = quad(Point(p1.x - mid.x, p1.y - mid.y))
    two = quad(Point(p2.x - mid.x, p2.y - mid.y))
    if one != two:
        return one - two
    return (p1.y * p2.x) - (p2.y * p1.x)

# Finds upper tangent of two polygons 'a' and 'b'
def merger(a, b):
    n1 = len(a)
    n2 = len(b)
    index_a = index_b = 0
    for i in range(1, n1):
        if a[i].x > a[index_a].x:
            index_a = i
    for i in range(1, n2):
        if b[i].x < b[index_b].x:
            index_b = i
    index_left = index_a
    index_right = index_b
    done = False
    while not done:
        done = True
        while orientation(b[index_right], a[index_left], a[(index_left + 1) % n1]) >= 0:
            index_left = (index_left + 1) % n1
        while orientation(a[index_left], b[index_right], b[(n2 + index_right - 1) % n2]) <= 0:
            index_right = (n2 + index_right - 1) % n2
            done = False
    upper_a = index_left
    upper_b = index_right
    index_left = index_a
    index_right = index_b
    done = False
    while not done:
        done = True
        while orientation(a[index_left], b[index_right], b[(index_right + 1) % n2]) >= 0:
            index_right = (index_right + 1) % n2
        while orientation(b[index_right], a[index_left], a[(n1 + index_left - 1) % n1]) <= 0:
            index_left = (n1 + index_left - 1) % n1
            done = False
    lowera = index_left
    lowerb = index_right
    result_points = []
    current_index = upper_a
    result_points.append(a[upper_a])
    while current_index != lowera:
        current_index = (current_index + 1) % n1
        result_points.append(a[current_index])
    current_index = lowerb
    result_points.append(b[lowerb])
    while current_index != upper_b:
        current_index = (current_index + 1) % n2
        result_points.append(b[current_index])
    return result_points

# Brute force algorithm to find convex hull for a set of less than 6 points
def brute_hull(a):
    s = set()
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            x1 = a[i].x
            x2 = a[j].x
            y1 = a[i].y
            y2 = a[j].y
            a1 = y1 - y2
            b1 = x2 - x1
            c1 = x1 * y2 - y1 * x2
            pos = 0
            neg = 0
            for k in range(len(a)):
                if a1 * a[k].x + b1 * a[k].y + c1 <= 0:
                    neg += 1
                if a1 * a[k].x + b1 * a[k].y + c1 >= 0:
                    pos += 1
            if pos == len(a) or neg == len(a):
                s.add(a[i])
                s.add(a[j])
    result_points = list(s)
    mid = Point(0, 0)
    n = len(result_points)
    for i in range(n):
        mid.x += result_points[i].x
        mid.y += result_points[i].y
        result_points[i].x *= n
        result_points[i].y *= n
    result_points.sort(key=lambda p: point_comparator(p, mid))
    for i in range(n):
        result_points[i].x /= n
        result_points[i].y /= n
    return result_points

# Returns the convex hull for the given set of points
def divide(a):
    if len(a) <= 5:
        return brute_hull(a)
    left = []
    right = []
    for i in range(len(a) // 2):
        left.append(a[i])
    for i in range(len(a) // 2, len(a)):
        right.append(a[i])
    left_hull = divide(left)
    right_hull = divide(right)
    return merger(left_hull, right_hull)

if __name__ == "__main__":
    n = int(input("Enter the number of points: "))
    a = []
    for _ in range(n):
        x = random.randint(-1000000, 10000000)
        y = random.randint(-1000000, 10000000)
        a.append(Point(x, y))

    mid = Point(0, 0)
    for i in range(n):
        mid.x += a[i].x
        mid.y += a[i].y

    # Record start time
    start_time = time.time()

    # Sort the set of points according to the x-coordinate
    a.sort(key=lambda p: p.x)

    ans = divide(a)

    end_time = time.time()
    duration = (end_time - start_time) * 1000000000

    # When the point set is too large, the specific convex hull points are not output 
    # print("Convex hull:")
    # for e in ans:
    #     print(e.x, e.y)

    print("Duration is", duration, "ns")