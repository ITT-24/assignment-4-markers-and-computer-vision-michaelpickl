import random
import pyglet

# List to store fruit sprites
fruits = []

# Constants
SIZES = [0.05, 0.075, 0.1, 0.2, 0.3]
TIMES = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
FALL_SPEEDS = [50, 60, 70, 80, 90, 100]

# Load fruit images once
FRUIT_IMAGES = {
    'cherry': pyglet.image.load('images/cherry.png'),
    'lemon': pyglet.image.load('images/lemon.png'),
    'pear': pyglet.image.load('images/pear.png'),
    'apple': pyglet.image.load('images/apple.png'),
    'strawberry': pyglet.image.load('images/strawberry.png'),
}

# List of fruit image keys
FRUIT_KEYS = list(FRUIT_IMAGES.keys())

def get_random_image():
    # Select a random fruit image
    fruit_key = random.choice(FRUIT_KEYS)
    return FRUIT_IMAGES[fruit_key]

def get_random_size():
    return random.choice(SIZES)

def get_random_rotation():
    return random.randrange(0, 360)

def create(dt):
    global fruits
    # Get random fruit image, size, and rotation
    fruit_img = get_random_image()
    scale_number = get_random_size()
    rotation = get_random_rotation()

    # Random position within window bounds
    x = random.randint(100, int(window_width - 100))
    y = random.randint(int(window_height / 2), int(window_height - 100))

    # Create sprite
    fruit = pyglet.sprite.Sprite(fruit_img, x, y)
    fruit.scale = scale_number
    fruit.rotation = rotation
    fruits.append(fruit)

    return fruits
