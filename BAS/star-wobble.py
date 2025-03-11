import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

def star_planet_wobble_demo():
    """
    Demonstrates the 'wobble' of a star due to an orbiting planet,
    with the star color fading from red to blue and back
    (simulating Doppler shift).
    """

    # -------------------------
    # SYSTEM PARAMETERS
    # -------------------------
    star_mass = 1.0        # Arbitrary star mass
    planet_mass = 0.3      # Planet mass (relatively large to make wobble visible)
    total_mass = star_mass + planet_mass

    # Distance between star & planet (center to center)
    separation = 2.0

    # Orbital radius of star around barycenter
    R_star_orbit = (planet_mass / total_mass) * separation

    # Orbital radius of planet around barycenter
    R_planet_orbit = (star_mass / total_mass) * separation

    # Star & planet radii
    star_radius = 0.5   # Star is bigger
    planet_radius = 0.1 # Planet is 20% of the star's size

    # Animation timing
    frames = 200   # frames per orbit
    interval = 50  # ms delay between frames

    # -------------------------
    # FIGURE SETUP
    # -------------------------
    fig, ax = plt.subplots(figsize=(5, 5))

    fig.suptitle("Star Wobble & Doppler Effect", color="black", fontsize=14, y=0.95)
    fig.text(0.5, 0.89, "Blue-shift is Toward, Redishift is Away", color="black", fontsize=10, ha='center')
    ax.set_facecolor("black")
    ax.set_aspect("equal", "box")

    # Provide extra room so the star doesn't go off-canvas
    pad = 1.0
    orbit_max = max(R_star_orbit + star_radius, R_planet_orbit + planet_radius)
    ax.set_xlim(-orbit_max - pad, orbit_max + pad)
    ax.set_ylim(-orbit_max - pad, orbit_max + pad)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Star & Planet Wobble (Radial Velocity Demo)", color="white", fontsize=12)

    # Create the star & planet patches
    # By default, start the star as red:
    star_patch = Circle((R_star_orbit, 0), star_radius, color="white", zorder=2)
    planet_patch = Circle((-R_planet_orbit, 0), planet_radius, color="white", zorder=3)
    ax.add_patch(star_patch)
    ax.add_patch(planet_patch)

    # -------------------------
    # HELPER: COLOR INTERPOLATION
    # -------------------------
    def red_to_blue(fraction):
        """
        Interpolate from red (1,0,0) to blue (0,0,1) with fraction in [0..1].
        Returns an (r,g,b) tuple.
        """
        r = 1 - fraction
        g = 0
        b = fraction
        return (r, g, b)

    def blue_to_red(fraction):
        """
        Interpolate from blue (0,0,1) to red (1,0,0) with fraction in [0..1].
        Returns an (r,g,b) tuple.
        """
        r = fraction
        g = 0
        b = 1 - fraction
        return (r, g, b)

    # -------------------------
    # ANIMATION UPDATE
    # -------------------------
    def update(frame):
        # fraction of orbit from 0..1
        frac = frame / frames

        # Star orbit
        angle = 2.0 * np.pi * frac
        x_star = R_star_orbit * np.cos(angle)
        y_star = R_star_orbit * np.sin(angle)
        star_patch.center = (x_star, y_star)

        # Planet orbit (180° out of phase)
        x_planet = -R_planet_orbit * np.cos(angle)
        y_planet = -R_planet_orbit * np.sin(angle)
        planet_patch.center = (x_planet, y_planet)

        # ----- Doppler color shift for the star -----
        # We'll fade from red->blue for half the orbit (frac in [0..0.5])
        # then blue->red for the other half (frac in [0.5..1.0]).
        if frac <= 0.5:
            # 0..0.5 => fraction ranges 0..1 => star goes red -> blue
            alpha = frac / 0.5  # maps [0..0.5] => [0..1]
            color = red_to_blue(alpha)
        else:
            # 0.5..1 => fraction ranges 0..1 => star goes blue -> red
            alpha = (frac - 0.5) / 0.5  # maps [0.5..1] => [0..1]
            color = blue_to_red(alpha)

        star_patch.set_facecolor(color)

        return star_patch, planet_patch

    ani = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=interval,
        blit=False,
        repeat=True
    )

    plt.show()

if __name__ == "__main__":
    star_planet_wobble_demo()
