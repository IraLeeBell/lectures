import math
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def transform_points(base_points, scale=1.0, rotation_deg=0.0, offset=(0.0, 0.0)):
    """
    1. Translate to centroid
    2. Scale
    3. Rotate by rotation_deg about centroid
    4. Translate by offset
    """
    # Compute centroid
    xs = [p[0] for p in base_points]
    ys = [p[1] for p in base_points]
    centroid_x = sum(xs) / len(xs)
    centroid_y = sum(ys) / len(ys)

    # Convert rotation degrees to radians
    theta = math.radians(rotation_deg)

    transformed = []
    for (x, y) in base_points:
        # Translate to centroid
        x_t = x - centroid_x
        y_t = y - centroid_y

        # Scale
        x_s = x_t * scale
        y_s = y_t * scale

        # Rotate
        x_r = x_s * math.cos(theta) - y_s * math.sin(theta)
        y_r = x_s * math.sin(theta) + y_s * math.cos(theta)

        # Translate back + offset
        x_final = x_r + centroid_x + offset[0]
        y_final = y_r + centroid_y + offset[1]

        transformed.append((x_final, y_final))

    return transformed

def empty_black_squares_with_titles():
    # --- LEFT (EARTH VIEW) DIPPERS ---
    little_dipper_base = [
        (2.5, 4.0),  # handle tip
        (2.3, 3.6),
        (2.0, 3.3),
        (1.6, 3.1),
        (1.1, 3.1),
        (0.9, 2.7),
        (1.3, 2.5),
        (1.6, 3.1)
    ]

    # LITTLE DIPPER: scale 60%
    little_dipper_pts_left = transform_points(
        base_points=little_dipper_base,
        scale=0.60,
        rotation_deg=0.0,
        offset=(0.0, 0.0)
    )

    # BIG DIPPER: scale 1.4×, rotate -90°, offset some
    big_dipper_pts_left = transform_points(
        base_points=little_dipper_base,
        scale=1.4,
        rotation_deg=-90.0,
        offset=(0.9, 0.9)
    )

    # --- RIGHT (SPACE VIEW) ZIGZAGS ---
    # Rather than using the same shape, just define some
    # arbitrary / somewhat-random zigzag lines:
    
    # "Little Dipper" on the right: random-ish zigzag
    # (just some points that make a wiggly line)
    little_dipper_pts_right = [
        (0.5, 4.8),
        (0.1, 2.2),
        (1.7, 4.6),
        (2.1, 3.9),
        (2.6, 4.3),
        (3.0, 3.7)
    ]

    # "Big Dipper" on the right: another random-ish zigzag
    big_dipper_pts_right = [
        (1.6, 2.8),
        (1.2, 3.7),
        (1.9, 3.3),
        (2.5, 4.1),
        (3.0, 3.5),
        (3.4, 4.3),
        (3.8, 3.9)
    ]

    # Create the figure and subplots (two black squares)
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(8, 4))

    # ---- MAIN FIGURE TITLE ----
    fig.suptitle("How Constellations Change Depending on Perspective",
                 color="black", y=0.93, fontsize=14)

    # ---- LEFT SUBPLOT (EARTH VIEW) ----
    ax_left.set_facecolor("black")
    ax_left.set_aspect("equal")
    ax_left.set_xticks([])
    ax_left.set_yticks([])
    ax_left.set_title("Big & Little Dipper - Earth View", color="black", fontsize=12)

    # Plot the Little Dipper (yellow)
    x_ld_left, y_ld_left = zip(*little_dipper_pts_left)
    ax_left.plot(x_ld_left, y_ld_left, marker='o', color='yellow', markersize=5, linestyle='-')

    # Plot the Big Dipper (white)
    x_bd_left, y_bd_left = zip(*big_dipper_pts_left)
    ax_left.plot(x_bd_left, y_bd_left, marker='o', color='white', markersize=5, linestyle='-')

    # Lock axis limits
    ax_left.set_xlim(0, 4)
    ax_left.set_ylim(2, 5.5)

    # Legend
    big_dipper_handle = mlines.Line2D([], [], color='white', marker='o', linestyle='',
                                      label='Big Dipper')
    little_dipper_handle = mlines.Line2D([], [], color='yellow', marker='o', linestyle='',
                                         label='Little Dipper')
    ax_left.legend(handles=[big_dipper_handle, little_dipper_handle],
                   facecolor='black', edgecolor='white', labelcolor='white')

    # ---- RIGHT SUBPLOT (SPACE VIEW) ----
    ax_right.set_facecolor("black")
    ax_right.set_aspect("equal")
    ax_right.set_xticks([])
    ax_right.set_yticks([])
    ax_right.set_title("Big & Little Dipper - Space View", color="black", fontsize=12)

    # Plot the "Little Dipper" zigzag on the right (yellow)
    x_ld_right, y_ld_right = zip(*little_dipper_pts_right)
    ax_right.plot(x_ld_right, y_ld_right, marker='o', color='yellow', markersize=5, linestyle='-')

    # Plot the "Big Dipper" zigzag on the right (white)
    x_bd_right, y_bd_right = zip(*big_dipper_pts_right)
    ax_right.plot(x_bd_right, y_bd_right, marker='o', color='white', markersize=5, linestyle='-')

    # Match axis limits so both squares appear the same size
    ax_right.set_xlim(0, 4)
    ax_right.set_ylim(2, 5.5)

    # Same legend handles
    big_dipper_handle_2 = mlines.Line2D([], [], color='white', marker='o', linestyle='',
                                        label='Big Dipper')
    little_dipper_handle_2 = mlines.Line2D([], [], color='yellow', marker='o', linestyle='',
                                           label='Little Dipper')
    ax_right.legend(handles=[big_dipper_handle_2, little_dipper_handle_2],
                    facecolor='black', edgecolor='white', labelcolor='white')

    # ---- Layout adjustments ----
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)

    plt.show()

if __name__ == "__main__":
    empty_black_squares_with_titles()
