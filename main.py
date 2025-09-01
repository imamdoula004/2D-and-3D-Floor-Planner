import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math

DOOR_WIDTH = 3
DOOR_HEIGHT = 7
WALL_THICKNESS = 0.2

# ------------------------------
# Parse rooms from text
# ------------------------------
def parse_rooms_from_text(text):
    parts = [p.strip() for p in text.split(",")]
    rooms = []
    for part in parts:
        words = part.split()
        if len(words) >= 2 and words[0].isdigit():
            count = int(words[0])
            room_name = " ".join(words[1:])
            for _ in range(count):
                rooms.append(room_name.title())
        else:
            rooms.append(part.title())
    return rooms

# ------------------------------
# Get room sizes
# ------------------------------
def get_room_sizes(rooms, total_sqft):
    sizes=[]
    used_sqft=0
    for room in rooms:
        size = float(input(f"Enter size in sqft for {room}: "))
        sizes.append((room, size))
        used_sqft += size
    if abs(used_sqft-total_sqft) > 1e-6:
        print(f"⚠️ Warning: Total allocated sqft ({used_sqft}) != house size ({total_sqft})")
    return sizes

# ------------------------------
# BSP allocation
# ------------------------------
def bsp_allocate(x, y, w, h, sized_rooms):
    if len(sized_rooms) == 1:
        room, size = sized_rooms[0]
        return [(x, y, w, h, room)]
    half = len(sized_rooms)//2
    group1, group2 = sized_rooms[:half], sized_rooms[half:]
    size1, size2 = sum(s for _, s in group1), sum(s for _, s in group2)
    ratio = size1 / (size1 + size2)
    if w > h:
        split = w * ratio
        return bsp_allocate(x, y, split, h, group1) + bsp_allocate(x + split, y, w - split, h, group2)
    else:
        split = h * ratio
        return bsp_allocate(x, y, w, split, group1) + bsp_allocate(x, y + split, w, h - split, group2)

def allocate_rooms(total_sqft, sized_rooms):
    side = math.sqrt(total_sqft)
    return bsp_allocate(0, 0, side, side, sized_rooms)

# ------------------------------
# Adjacent rooms for doors
# ------------------------------
def find_adjacent_rooms(rooms):
    adjacent_pairs = []
    for i, (x1, y1, w1, h1, _) in enumerate(rooms):
        for j, (x2, y2, w2, h2, _) in enumerate(rooms):
            if i >= j:
                continue
            if (x1 + w1 == x2 or x2 + w2 == x1) and (y1 < y2 + h2 and y1 + h1 > y2):
                adjacent_pairs.append(((x1, y1, w1, h1), (x2, y2, w2, h2)))
            elif (y1 + h1 == y2 or y2 + h2 == y1) and (x1 < x2 + w2 and x1 + w1 > x2):
                adjacent_pairs.append(((x1, y1, w1, h1), (x2, y2, w2, h2)))
    return adjacent_pairs

# ------------------------------
# 2D floorplan
# ------------------------------
def plot_2d_floorplan(rooms):
    fig, ax = plt.subplots(figsize=(10,10))
    for x, y, w, h, name in rooms:
        ax.add_patch(plt.Rectangle((x, y), w, h, fill=None, edgecolor="black", linewidth=2))
        ax.text(x + w/2, y + h/2, name, ha="center", va="center", fontsize=10, fontweight="bold")
    for r1, r2 in find_adjacent_rooms(rooms):
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2
        if x1 + w1 == x2 or x2 + w2 == x1:
            door_x = max(x1, x2) - DOOR_WIDTH/2
            door_y = max(y1, y2) + (min(h1, h2) - DOOR_WIDTH)/2
            ax.add_patch(plt.Rectangle((door_x, door_y), DOOR_WIDTH, WALL_THICKNESS, facecolor="brown"))
        else:
            door_x = max(x1, x2) + (min(w1, w2) - DOOR_WIDTH)/2
            door_y = max(y1, y2) - WALL_THICKNESS
            ax.add_patch(plt.Rectangle((door_x, door_y), WALL_THICKNESS, DOOR_WIDTH, facecolor="brown"))
    ax.set_aspect('equal')
    max_x = max([x + w for (x, y, w, h, _) in rooms]) + 2
    max_y = max([y + h for (x, y, w, h, _) in rooms]) + 2
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, max_y)
    ax.set_xlabel("Feet")
    ax.set_ylabel("Feet")
    ax.set_title("2D Floorplan with Doors and Labels")
    plt.show()

# ------------------------------
# 3D floorplan
# ------------------------------
def draw_box(ax, x, y, z, dx, dy, dz, color):
    verts = [[(x,y,z),(x+dx,y,z),(x+dx,y+dy,z),(x,y+dy,z)],
             [(x,y,z+dz),(x+dx,y,z+dz),(x+dx,y+dy,z+dz),(x,y+dy,z+dz)]]
    sides = [[(x,y,z),(x+dx,y,z),(x+dx,y,z+dz),(x,y,z+dz)],
             [(x+dx,y,z),(x+dx,y+dy,z),(x+dx,y+dy,z+dz),(x+dx,y,z+dz)],
             [(x+dx,y+dy,z),(x,y+dy,z),(x,y+dy,z+dz),(x+dx,y+dy,z+dz)],
             [(x,y+dy,z),(x,y,z),(x,y,z+dz),(x,y+dy,z+dz)]]
    for v in verts + sides:
        ax.add_collection3d(Poly3DCollection([v], facecolors=color, edgecolors="black", linewidths=0.5, alpha=0.8))

def draw_doors_3d(ax, room_pairs, wall_height=9):
    for r1, r2 in room_pairs:
        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2
        if x1 + w1 == x2 or x2 + w2 == x1:
            door_x = max(x1, x2) - DOOR_WIDTH/2
            door_y = max(y1, y2) + (min(h1, h2) - DOOR_WIDTH)/2
            draw_box(ax, door_x, door_y, 0, DOOR_WIDTH, 0.2, DOOR_HEIGHT, "brown")
        else:
            door_x = max(x1, x2) + (min(w1, w2) - DOOR_WIDTH)/2
            door_y = max(y1, y2) - 0.2
            draw_box(ax, door_x, door_y, 0, 0.2, DOOR_WIDTH, DOOR_HEIGHT, "brown")

def plot_3d_floorplan(rooms):
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111, projection="3d")
    wall_height = 9
    colors = ["lightblue","lightgreen","wheat","lightgray"]

    for i, (x, y, w, h, name) in enumerate(rooms):
        color = colors[i % len(colors)]
        # floor
        floor = [[(x,y,0),(x+w,y,0),(x+w,y+h,0),(x,y+h,0)]]
        ax.add_collection3d(Poly3DCollection(floor, facecolors=color, linewidths=1, edgecolors="black", alpha=0.6))
        # walls
        verts = [
            [(x,y,0),(x+w,y,0),(x+w,y,wall_height),(x,y,wall_height)],
            [(x,y+h,0),(x+w,y+h,0),(x+w,y+h,wall_height),(x,y+h,wall_height)],
            [(x,y,0),(x,y+h,0),(x,y+h,wall_height),(x,y,wall_height)],
            [(x+w,y,0),(x+w,y+h,0),(x+w,y+h,wall_height),(x+w,y,wall_height)]
        ]
        ax.add_collection3d(Poly3DCollection(verts, facecolors="white", linewidths=1, edgecolors="black", alpha=0.4))
        ax.text(x + w/2, y + h/2, wall_height + 0.5, name, ha="center", va="bottom", fontsize=8, fontweight="bold")

    draw_doors_3d(ax, find_adjacent_rooms(rooms), wall_height)

    max_x = max([x + w for (x, y, w, h, _) in rooms]) + 2
    max_y = max([y + h for (x, y, w, h, _) in rooms]) + 2
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, max_y)
    ax.set_zlim(0, wall_height + 3)
    ax.set_xlabel("Feet")
    ax.set_ylabel("Feet")
    ax.set_zlabel("Height (ft)")
    ax.set_title("3D Floorplan with Doors")
    plt.show()

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    total_sqft = float(input("Enter total house size in sqft: "))
    text = input("Describe rooms (e.g., '2 bedrooms, 1 kitchen, 1 bathroom, 1 living room'): ")
    room_list = parse_rooms_from_text(text)
    sized_rooms = get_room_sizes(room_list, total_sqft)
    allocated = allocate_rooms(total_sqft, sized_rooms)
    plot_2d_floorplan(allocated)
    plot_3d_floorplan(allocated)
