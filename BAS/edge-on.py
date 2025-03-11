import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

def edge_on_transit_demo():
    """
    A planet transits left->right in front of the star, then right->left behind the star.
    The light curve on the right resets each time.
    Both subplots appear as black squares of the same physical size.
    We use manual label coordinates to bring x & y labels closer.
    """

    # -------------------------
    # PARAMETERS
    # -------------------------
    R_star = 1.0
    R_planet = 0.3
    x_left = -2.0
    x_right = 2.0
    frames = 200
    half = frames // 2

    time_data = []
    flux_data = []

    star_area = np.pi * (R_star**2)
    planet_area = np.pi * (R_planet**2)
    max_block_fraction = planet_area / star_area

    def compute_flux(planet_x):
        dist = abs(planet_x)
        sum_r = R_star + R_planet
        diff_r = abs(R_star - R_planet)
        if dist >= sum_r:
            return 1.0
        elif dist <= diff_r:
            return 1.0 - max_block_fraction
        else:
            overlap_range = sum_r - diff_r
            overlap_dist = sum_r - dist
            coverage_fraction = overlap_dist / overlap_range
            return 1.0 - coverage_fraction * max_block_fraction

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(8, 4))

    # Left subplot
    ax_left.set_facecolor("black")
    ax_left.set_aspect("equal")
    ax_left.set_xlim(-2.5, 2.5)
    ax_left.set_ylim(-2.5, 2.5)
    ax_left.set_xticks([])
    ax_left.set_yticks([])
    ax_left.set_title("Edge-On Orbit (Front Then Behind)", color="black", fontsize=12)

    star_patch = Circle((0, 0), R_star, color="yellow", zorder=2)
    planet_patch = Circle((x_left, 0), R_planet, color="blue", zorder=3)
    ax_left.add_patch(star_patch)
    ax_left.add_patch(planet_patch)

    # Right subplot
    ax_right.set_facecolor("black")
    ax_right.set_xlim(0, frames)
    ax_right.set_ylim(0.8, 1.02)
    ax_right.set_title("Observed Flux vs Time", color="black", fontsize=12)

    (flux_line,) = ax_right.plot([], [], color='cyan', lw=2)

    # 1) Remove default padding:
    ax_right.set_xlabel("Time", color="black", labelpad=0)
    ax_right.set_ylabel("Star's Flux", color="black", labelpad=0)
    ax_right.tick_params(axis='x', colors='white')
    ax_right.tick_params(axis='y', colors='white')

    # 2) Manually set label coordinates as fractions of the Axes dimensions
    #    (x=0.5 => center horizontally, y=... => a bit below the x-axis)
    ax_right.xaxis.set_label_coords(0.5, -0.008)
    #    (x=... => left side, y=0.5 => center vertically)
    ax_right.yaxis.set_label_coords(-0.008, 0.5)

    def init():
        time_data.clear()
        flux_data.clear()
        flux_line.set_data([], [])
        return flux_line,

    def update(frame):
        if frame < half:
            frac = frame / (half - 1)
            planet_x = x_left + (x_right - x_left) * frac
            planet_patch.set_zorder(3)
            flux = compute_flux(planet_x)
        else:
            frac = (frame - half) / (half - 1)
            planet_x = x_right + (x_left - x_right) * frac
            planet_patch.set_zorder(1)
            flux = 1.0

        planet_patch.center = (planet_x, 0)
        time_data.append(frame)
        flux_data.append(flux)

        flux_line.set_xdata(time_data)
        flux_line.set_ydata(flux_data)
        return planet_patch, flux_line

    ani = FuncAnimation(
        fig,
        update,
        frames=frames,
        init_func=init,
        interval=50,
        blit=False,
        repeat=True
    )

    # If you find tight_layout re-adjusts the labels too much,
    # comment the next line out or tweak subplots_adjust manually.
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    edge_on_transit_demo()
