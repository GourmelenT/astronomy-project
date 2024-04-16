import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
SUN = (255, 255, 0)
MERCURY = (150, 82, 0)
VENUS = (178, 77, 0)
EARTH = (54, 146, 226)
MARS = (209, 52, 0)
JUPITER = (204, 156, 0)
SATURN = (232, 178, 71)
URANUS = (32, 191, 180)
NEPTUNE = (31, 107, 183)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11       # Gravitational constant       
    SCALE = 50 / AU      # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24  # Represent one day

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                px, py = point
                px = px * self.SCALE + WIDTH / 2
                py = py * self.SCALE + HEIGHT / 2
                updated_points.append((px, py))
            
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
        # Affichage du nom de la planète
        name_text = FONT.render(self.name, 1, WHITE)
        win.blit(name_text, (x - name_text.get_width() / 2, y + self.radius + 5))

    def attraction(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(dy, dx)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 15, SUN, 1.98892 * 10**30, "Sun")
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, MERCURY, 3.3010 * 10**23, "Mercury")
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 12, VENUS, 4.8673 * 10**24, "Venus")
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 14, EARTH, 5.9722 * 10**24, "Earth")
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, MARS, 6.4169 * 10**23, "Mars")
    mars.y_vel = 24.077 * 1000

    jupiter = Planet(-5.204 * Planet.AU, 0, 26, JUPITER, 1.898 * 10**27, "Jupiter")
    jupiter.y_vel = 13.06 * 1000

    saturn = Planet(-9.573 * Planet.AU, 0, 22, SATURN, 5.6832 * 10**26, "Saturn")
    saturn.y_vel = 9.67 * 1000

    uranus = Planet(-19.165 * Planet.AU, 0, 18, URANUS, 8.6811 * 10**25, "Uranus")
    uranus.y_vel = 6.69 * 1000

    neptune = Planet(-30.178 * Planet.AU, 0, 19, NEPTUNE, 1.02409 * 10**26, "Neptune")
    neptune.y_vel = 5.45 * 1000

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    zoom_factor = 1.0

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Handle mouse scroll events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    zoom_factor *= 1.1  # Increase zoom by 10%
                elif event.button == 5:  # Scroll down
                    zoom_factor /= 1.1  # Decrease zoom by 10%

            # Handle keyboard events
            keys = pygame.key.get_pressed()
            if keys[pygame.K_EQUALS] and keys[pygame.K_LCTRL]:  # Ctrl +
                zoom_factor *= 1.1
            elif keys[pygame.K_MINUS]:  # -
                zoom_factor /= 1.1

        # Apply the zoom factor to the SCALE parameter
        Planet.SCALE = 250 / Planet.AU * zoom_factor

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
