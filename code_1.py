import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.affinity import rotate

PANEL_SIZES = [(2, 1), (2.3, 1), (1.8, 0.9)]
PANEL_DISTANCE = 0.02
ROW_DISTANCE = 0.5
# Assume distance from boundary is panel distance
BOUNDARY_DISTANCE = PANEL_DISTANCE

rooftop1_coords = [(0,0), (0, 100), (50, 0)]
rooftop2_coords = [(1.12, 130.83), (1.12, 160.83), (31.12, 160.83), (31.12, 130.83), (11.12, 100.83), (-11.12, 90.83), (-30.12, 90.83), (-20.182, 120.273)]
rooftop3_coords = [(2, 100), (2,160), (131, 160), (35, 200), (11, 300), (-20 , 90), (30, 90)]

# Permutations:
# 1. Row/panel distance
# 2. Angle of rotation: 0, 90
# 3. Shift

def generate_layout(selected_rooftop, panel):
    selected_rooftop_coords = selected_rooftop + [selected_rooftop[0]]
   
    rotation_angle = 0

    rooftop = rotate(Polygon(selected_rooftop_coords), rotation_angle)
    xs, ys = zip(*rooftop.exterior.coords) 

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    panel_width = panel[0]
    panel_height = panel[1]

    def get_panel_coords(x, y, width, height):
        return [(x, y), (x + width, y), (x, y + height), (x + width, y + height)]


    def get_layout(panel_width, panel_height, x_gap, y_gap):
        x = min_x + BOUNDARY_DISTANCE
        coord_list = []

        while (max_x > x):
            y = min_y + BOUNDARY_DISTANCE

            while (max_y > y):
                panel_coords = get_panel_coords(x, y, panel_width, panel_height)
                panel_geometry = Polygon(panel_coords)

                if rooftop.contains_properly(panel_geometry):             
                    coord_list.append((x,y))

                y += panel_height
                y += y_gap

            x += panel_width
            x += x_gap

        return coord_list


    def get_best_layout():
        permutations = [{"panel_width": panel_width, "panel_height": panel_height, "x_gap": ROW_DISTANCE, "y_gap": PANEL_DISTANCE},
                        {"panel_width": panel_width, "panel_height": panel_height, "x_gap": PANEL_DISTANCE, "y_gap": ROW_DISTANCE}]
                        # {"panel_width": panel_height, "panel_height": panel_width, "y_gap": panel_distance, "x_gap": row_distance},
                        # {"panel_width": panel_height, "panel_height": panel_width, "y_gap": row_distance, "x_gap": panel_distance}]

        chosen_permutation = permutations[0]
        chosen_permutation_coords = []

        for permutation in permutations:
            coord_list = get_layout(panel_width=permutation["panel_width"], 
                                    panel_height=permutation["panel_height"], 
                                    x_gap=permutation["x_gap"], 
                                    y_gap=permutation["y_gap"])
            
            if len(coord_list) > len(chosen_permutation_coords):
                chosen_permutation = permutation
                chosen_permutation_coords = coord_list

        return {"chosen_permutation": chosen_permutation, "chosen_permutation_coords": chosen_permutation_coords}


    def visualise(chosen_permutation, chosen_permutation_coords):
        plt.figure()
        plt.plot(xs, ys, label="Rooftop")    

        for i, j in chosen_permutation_coords:
            rectangle = plt.Rectangle((i, j), chosen_permutation["panel_width"], chosen_permutation["panel_height"], color='g')
            # rectangle.set_angle(90)
            plt.gca().add_patch(rectangle)
            

        plt.show()


    best_layout = get_best_layout()
    chosen_permutation = best_layout["chosen_permutation"]
    chosen_permutation_coords = best_layout["chosen_permutation_coords"]

    print(len(chosen_permutation_coords))
    visualise(chosen_permutation=chosen_permutation, chosen_permutation_coords=chosen_permutation_coords)


generate_layout(rooftop1_coords, PANEL_SIZES[0])


# Rooftop 1
# Current max: 829, 728, 1010
# Current max: 921, 820, 1113
# 945

# Rooftop 2
# 843, 753, 1030
# 844, 753, 1030
# 883

# Rooftop 3
# 2418, 2191, 2933
# Similar
# 2546