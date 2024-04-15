import matplotlib.pyplot as plt
from shapely.geometry import Polygon

panel_sizes = [(2, 1), (2.3, 1), (1.8, 0.9)]

rooftop1_coords = [(0,0), (0, 100), (50, 0)]
rooftop2_coords = [(1.12, 130.83), (1.12, 160.83), (31.12, 160.83), (31.12, 130.83), (11.12, 100.83), (-11.12, 90.83), (-30.12, 90.83), (-20.182, 120.273)]
rooftop3_coords = [(2, 100), (2,160), (131, 160), (35, 200), (11, 300), (-20 , 90), (30, 90)]

# Permutations:
# 1. Row/panel distance
# 2. Angle of rotation: 0, 90
# 3. Shift

class LayoutOptimisation:
    panel_distance = 0.02
    row_distance = 0.5
    # Assume distance from boundary is panel distance
    boundary_distance = panel_distance

    def __init__(self, selected_rooftop, panel):
        rooftop = Polygon(selected_rooftop)
        self.rooftop = rooftop

        xs, ys = zip(*rooftop.exterior.coords) 
        self.xs = xs
        self.ys = ys

        self.min_x = min(xs)
        self.max_x = max(xs)
        self.min_y = min(ys)
        self.max_y = max(ys)

        self.panel_length = panel[0]
        self.panel_width = panel[1]


    def get_panel_coords(self, x, y, length, width):
        return [(x, y), (x + length, y), (x, y + width), (x + length, y + width)]
        

    def get_layout(self, panel_length, panel_width, x_gap, y_gap):
        x = self.min_x + self.boundary_distance
        coord_list = []

        while (self.max_x > x):
            y = self.min_y + self.boundary_distance

            while (self.max_y > y):
                panel_coords = self.get_panel_coords(x, y, panel_length, panel_width)
                panel_geometry = Polygon(panel_coords)

                if self.rooftop.contains_properly(panel_geometry):             
                    coord_list.append((x,y))

                y += panel_width
                y += y_gap

            x += panel_length
            x += x_gap

        return coord_list
    

    def get_best_layout(self):
        permutations = [{"panel_length": self.panel_length, "panel_width": self.panel_width, "x_gap": self.row_distance, "y_gap": self.panel_distance},
                        {"panel_length": self.panel_length, "panel_width": self.panel_width, "x_gap": self.panel_distance, "y_gap": self.row_distance},
                        {"panel_length": self.panel_width, "panel_width": self.panel_length, "x_gap": self.row_distance, "y_gap": self.panel_distance},
                        {"panel_length": self.panel_width, "panel_width": self.panel_length, "x_gap": self.panel_distance, "y_gap": self.row_distance}]

        chosen_permutation = permutations[0]
        chosen_permutation_coords = []

        for permutation in permutations:
            coord_list = self.get_layout(panel_length=permutation["panel_length"], 
                                         panel_width=permutation["panel_width"], 
                                         x_gap=permutation["x_gap"], 
                                         y_gap=permutation["y_gap"])
                
            if len(coord_list) > len(chosen_permutation_coords):
                chosen_permutation = permutation
                chosen_permutation_coords = coord_list

        return {"chosen_permutation": chosen_permutation, "chosen_permutation_coords": chosen_permutation_coords}
    

    def visualise(self, chosen_permutation, chosen_permutation_coords):
        plt.figure()
        plt.plot(self.xs, self.ys)    

        for i, j in chosen_permutation_coords:
            rectangle = plt.Rectangle((i, j), chosen_permutation["panel_length"], chosen_permutation["panel_width"], facecolor='g', edgecolor="b")
  
            plt.gca().add_patch(rectangle)
            
        plt.show()


def generate_layout(selected_rooftop, panel):
    layout = LayoutOptimisation(selected_rooftop, panel)

    best_layout = layout.get_best_layout()
    chosen_permutation = best_layout["chosen_permutation"]
    chosen_permutation_coords = best_layout["chosen_permutation_coords"]

    layout.visualise(chosen_permutation=chosen_permutation, chosen_permutation_coords=chosen_permutation_coords)


generate_layout(rooftop1_coords, panel_sizes[0])


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