"""
Contains classes related to displaying the Abagio game.

Classes:
    Window - the game window (with methods to display various items).
    ResourceManager - loads and stores game assets.
"""

from pathlib import Path

import pygame
from pygame import gfxdraw


class Window:
    """
    The Abagio game window.
    
    Contains a number of methods that simplify the process of drawing
    items onto the game window. This class should only be instantiated
    once.
    
    Note that changes made to the window will not be reflected in the
    visible Pygame display until the update method is called.
    
    Methods: fill, update, draw_text, draw_multi_line_text,
        draw_button, draw_rectangle, draw_circle, draw_frog,
        draw_circle_outline, draw_image
    
    Instance variables:
        game_display - the pygame display Surface used for the game
            display.
        font - the Font used to display text in the window.
    """
    
    def __init__(self):
        """
        Initialize Pygame and create and display the window.
        
        The game_display and font instance variables are also
        initialized.
        """
        pygame.init()
        
        self.game_display = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Abagio")
        
        self.font = pygame.font.SysFont(None, 35)
    
        self.update()
        
    def fill(self, color):
        """
        Fill the window with the specified color.
        
        Arguments:
            color - a string representing a Pygame color.
        """
        self.game_display.fill(pygame.Color(color))
        
    def update(self):
        """
        Update the Pygame display.
        
        This is necessary for changes previously made to the window to
        be reflected in the visible Pygame display.
        """
        pygame.display.update()
        
    def draw_text(self, x, y, text, color, center_on_coordinates=False):
        """
        Draw a single line of text onto the window.
        
        Arguments:
            x - the x coordinate used to display the text (see
                center_on_coordinates below).
            y - the y coordinate used to display the text (see
                center_on_coordinates below).
            text - a string representing a single line of text (should
                not include newline characters).
            color - a string representing the Pygame color the text
                should be displayed in.
            center_on_coordinates - if True, the x and y coordinates
                provided represent where the center of the text Surface
                should be displayed in the window. If False, the x and
                y coordinates provided represent where the top-left
                corner of the text Surface should be displayed in the
                window. Default False.
        
        The font instance variable is used to render the text.
        """
        screen_text = self.font.render(text, True, pygame.Color(color))
        if center_on_coordinates:
            self.game_display.blit(
                screen_text, (x - screen_text.get_rect().width / 2,
                              y - screen_text.get_rect().height / 2))
        else:
            self.game_display.blit(screen_text, (x, y))
    
    def draw_multi_line_text(self, x, y, text, color):
        """
        Draw one or more lines of text onto the window.
        
        Arguments:
            x - the x coordinate where the top-left corner of the text
                Surface should be displayed in the window.
            y - the y coordinate where the top-left corner of the text
                Surface should be displayed in the window.
            text - a string representing one or more lines of text,
                with lines separated by newline characters (\\n).
            color - a string representing the Pygame color the text
                should be displayed in.
        
        The font instance variable is used to render the text.
        """
        for index, line in enumerate(text.split("\n")):
            self.draw_text(x, y + index * self.font.get_linesize(), line,
                           color, False)
    
    def draw_button(self, x, y, width, height, text, button_color, text_color):
        """
        Draw a button onto the window and return its bounding Rect.
        
        Arguments:
            x - the desired x coordinate of the top-left corner of the
                button in the window.
            y - the desired y coordinate of the top-left corner of the
                button in the window.
            width - the desired width of the button (in pixels).
            height - the desired height of the button (in pixels).
            text - a string with no newline characters representing the
                single line of text to be centered inside the button.
            button_color - a string representing the Pygame color the
                button Rect should be displayed in.
            text_color - a string representing the Pygame color the
                button text should be displayed in.

        The font instance variable is used to render the button text.
        """
        button = pygame.draw.rect(self.game_display,
                                  pygame.Color(button_color),
                                  (x, y, width, height))
        self.draw_text(x + width / 2, y + height / 2, text, text_color, True)
        return button
    
    def draw_rectangle(self, x, y, width, height, color):
        """
        Draw a rectangle onto the window.
        
        Arguments:
            x - the desired x coordinate of the top-left corner of the
                rectangle in the window.
            y - the desired y coordinate of the top-left corner of the
                rectangle in the window.
            width - the desired width of the rectangle (in pixels).
            height - the desired height of the rectangle (in pixels).
            color - a string representing the Pygame color the rectangle
                should be displayed in.
        """
        pygame.draw.rect(
            self.game_display, pygame.Color(color), (x, y, width, height))
    
    def draw_circle(self, x, y, radius, color):
        """
        Draw a filled, antialiased circle onto the window.
        
        Arguments:
            x - the desired x coordinate of the center of the circle in
                the window.
            y - the desired y coordinate of the center of the circle in
                the window.
            radius - the desired radius of the circle (in pixels).
            color - a string representing the Pygame color the circle
                should be displayed in.
        """
        gfxdraw.aacircle(self.game_display, x, y, radius, pygame.Color(color))
        gfxdraw.filled_circle(self.game_display, x, y, radius,
                              pygame.Color(color))
    
    def draw_frog(self, x, y, radius, color):
        """
        Draw an Abagio frog onto the window and return bounding Rect.
        
        Arguments:
            x - the desired x coordinate of the center of the circle
                representing the frog in the window.
            y - the desired y coordinate of the center of the circle
                representing the frog in the window.
            radius - the desired radius of the circle representing the
                frog (in pixels).
            color - a string representing the Pygame color the circle
                representing the frog should be displayed in.
        
        The frog will be displayed as a filled, antialiased circle with
        the desired parameters, with a black circular border.
        
        Return the circumscribed Rect around the circle drawn (the
        bounding box of the frog).
        """
        gfxdraw.aacircle(self.game_display, x, y, radius, pygame.Color(color))
        bounding_rect = pygame.draw.circle(
            self.game_display, pygame.Color(color), (x, y), radius)
        self.draw_circle_outline(x, y, radius, "black", 5)
        return bounding_rect
    
    def draw_circle_outline(self, x, y, radius, color, thickness=1):
        """
        Draw an antialiased outline of a circle onto the window.
        
        Arguments:
            x - the desired x coordinate of the center of the circle
                whose outline is being drawn in the window.
            y - the desired y coordinate of the center of the circle
                whose outline is being drawn in the window.
            radius - the desired radius of the circle whose outline
                is being drawn (in pixels). Represents the distance from
                the center to the outermost part of the outline.
            color - a string representing the Pygame color the circle
                outline should be displayed in.
            thickness - the desired thickness of the circle outline, in
                pixels (default 1). Should be an integer >= 1; if > 1,
                the thickness of the outline extends toward the center
                of the circle whose outline is being drawn. Must not be
                greater than radius. Large values may potentially cause
                performance issues.
        """
        for _ in range(thickness):
            gfxdraw.aacircle(self.game_display, x, y, radius,
                             pygame.Color(color))
            gfxdraw.circle(self.game_display, x, y, radius,
                           pygame.Color(color))
            radius -= 1
    
    def draw_image(self, x, y, image):
        """
        Draw an image onto the window and return its bounding Rect.
        
        Arguments:
            x - the desired x coordinate of the top-left corner of the
                image in the window.
            y - the desired y coordinate of the top-left corner of the
                image in the window.
            image - the Pygame Surface representing the image to be
                drawn onto the window.
        """
        return self.game_display.blit(image, (x, y))


class ResourceManager:
    """
    Holds a dictionary of the images needed for the game.
    
    Instance variables:
        images - a dictionary of the images needed for the game. Images
            are associated with the keys "board", "die 1", "die 2",
            "die 3", "die 4", "die 5", and "die 6".
    """
    
    def __init__(self):
        """Load the game images into the images dictionary.

        A RuntimeError is raised if the image files cannot be
        successfully read.
        """
        self.images = {}
        try:
            self.images["board"] = self._load_image("board.jpg")
            self.images["die 1"] = self._load_image("die1.png")
            self.images["die 2"] = self._load_image("die2.png")
            self.images["die 3"] = self._load_image("die3.png")
            self.images["die 4"] = self._load_image("die4.png")
            self.images["die 5"] = self._load_image("die5.png")
            self.images["die 6"] = self._load_image("die6.png")
        except NameError:
            raise RuntimeError("The __file__ attribute is not defined, so the "
                               "image files needed for the game cannot be "
                               "read. Please make sure that the game code is "
                               "being run from a file.")
        except FileNotFoundError as e:
            raise RuntimeError("One or more of the image files needed for the "
                               "game cannot be found. Please make sure that "
                               "the directory structure of the game files has "
                               "not been modified.") from e

    def _load_image(self, file_name):
        # Load and return the Pygame Surface representing the image in
        # the "res" directory of the project with the given file name.
        #
        # Raises a NameError if the __file__ attribute is not set.
        # Raises a FileNotFoundError if the specified file cannot be
        # found.
        #
        # Arguments:
        #    file_name - the file name (with extension) of the image
        #        file from the "res" directory to be loaded.
        return pygame.image.load(
            Path(__file__) / f"../../../res/{file_name}").convert()
