import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

def exoplanet_transit_simulation():
    """
    Demonstrates a simple star+planet orbit system (face-on):
      - Left subplot: star & orbiting planet
      - Right subplot: light-curve showing flux dips when the planet transits
    Both subplots appear as black squares of the same physical size.
    The flux line on the right resets once it reaches the end of the orbit.
    """

    # -----------------------
    # PARAMETERS
    # -----------------------
    R_star = 1.0        # Star radius
    R_planet = 0.2      # Planet radius
    orbit_radius = 2.0  # Distance from star center to planet center
    period_frames = 100 # Frames per orbit in the animation

    # Arrays for the light-curve
    time_data = []
    flux_data = []

    # -----------------------
    # FIGURE & SUBPLOTS
    # -----------------------
    # Using (8,4) so each subplot is ~4×4 inches
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(8, 4))

    # -----------------------
    # LEFT SUBPLOT (System View)
    # -----------------------
    ax_left.set_facecolor('black')
    ax_left.set_aspect('equal', 'box')
    ax_left.set_xlim(-3, 3)
    ax_left.set_ylim(-3, 3)
    ax_left.set_xticks([])
    ax_left.set_yticks([])
    ax_left.set_title('Face-On Orbit (No Blocking of Light)', color='black', fontsize=12)

    # Draw the star and planet
    star_patch = Circle((0, 0), R_star, color='yellow')
    ax_left.add_patch(star_patch)
    planet_patch = Circle((orbit_radius, 0), R_planet, color='white')
    ax_left.add_patch(planet_patch)

    # -----------------------
    # RIGHT SUBPLOT (Light Curve)
    # -----------------------
    ax_right.set_facecolor('black')
    ax_right.set_title('Observed Flux vs. Time', color='black', fontsize=12)
    ax_right.set_xlim(0, period_frames)
    ax_right.set_ylim(0.95, 1.05)

    # Axis labels
    ax_right.set_xlabel("Time", color='black')
    ax_right.set_ylabel("Star's Flux", color='black')

    # Position labels closer to the axes
    ax_right.xaxis.set_label_coords(0.5, -0.006)
    ax_right.yaxis.set_label_coords(-0.008, 0.5)

    # Tick labels in white
    ax_right.tick_params(axis='x', colors='white')
    ax_right.tick_params(axis='y', colors='white')

    # Prepare the line for flux
    (flux_line,) = ax_right.plot([], [], color='cyan', lw=2)

    # Star & Planet areas (for flux dip calc)
    star_area = np.pi * (R_star ** 2)
    planet_area = np.pi * (R_planet ** 2)
    transit_depth = planet_area / star_area  # Fraction of star blocked

    # -----------------------
    # INIT FUNCTION (to reset the line each loop)
    # -----------------------
    def init():
        """Clears old line data so the flux plot restarts each time the animation loops."""
        time_data.clear()
        flux_data.clear()
        flux_line.set_data([], [])
        return flux_line,

    # -----------------------
    # UPDATE FUNCTION
    # -----------------------
    def update(frame):
        # Planet's angular position in one orbit
        angle = 2.0 * np.pi * (frame / period_frames)

        # Planet's (x,y)
        px = orbit_radius * np.cos(angle)
        py = orbit_radius * np.sin(angle)
        planet_patch.center = (px, py)

        # Simple check for transit
        if abs(px) < (R_star + R_planet) and abs(py) < 0.1:
            flux = 1.0 - transit_depth
        else:
            flux = 1.0

        # Record flux data
        time_data.append(frame)
        flux_data.append(flux)
        flux_line.set_xdata(time_data)
        flux_line.set_ydata(flux_data)

        return planet_patch, flux_line

    # -----------------------
    # RUN ANIMATION
    # -----------------------
    ani = FuncAnimation(
        fig,
        update,
        frames=range(period_frames + 1),
        init_func=init,   # <-- This resets the flux line on each new loop
        interval=100,
        blit=False,
        repeat=True
    )

    # If you find tight_layout repositions labels too aggressively, feel free to remove:
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    exoplanet_transit_simulation()
