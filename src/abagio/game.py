"""
Contains classes and a script used to run and manage the Abagio game.

Classes:
    State - an Enum representing the overall game state.
    TurnStage - an Enum representing the stage of a player's turn.
    RollState - an Enum representing the roll state of a turn.
    MoveState - an Enum representing the movement state of a turn.
    Game - manages an Abagio game.

The script, which runs if this module is executed directly, starts /
runs the Abagio game.
"""

# Hide the Pygame welcome message.
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from enum import Enum

import pygame

from abagio.interface import Window, ResourceManager
from abagio.timer import Timer
from abagio.gamepieces import Die, Board, Frog

State = Enum("State", ("SETUP", "SETUP_TIE", "SETUP_WAITING", "MAIN_GAME"))
"""
Represents the overall state of an Abagio game. Subclass of Enum.

Additional methods: none

Additional enum class constants: SETUP, SETUP_TIE, SETUP_WAITING,
    MAIN_GAME
"""

TurnStage = Enum("Turn Stage", ("ROLL", "MOVE"))
"""
Represents the stage of a player's turn in an Abagio game.

Should be used within the MAIN_GAME State. Subclass of Enum.

Additional methods: none

Additional enum class constants: ROLL, MOVE
"""

RollState = Enum("Roll State", ("BEFORE_ROLL", "DURING_ROLL", "AFTER_ROLL"))
"""
Represents the state of a roll in an Abagio game.

Should be used within the SETUP state, or within the ROLL TurnStage
within the MAIN_GAME State. Subclass of Enum.

Additional methods: none

Additional enum class constants: BEFORE_ROLL, DURING_ROLL, AFTER_ROLL
"""

MoveState = Enum("Move State", ("BEFORE_DIE", "BEFORE_FROG",
                                "BEFORE_FROG_ERROR", "DURING_FROG_MOVEMENT"))
"""
Represents the state of movement in a turn in an Abagio game.

Should be used within the MOVE TurnStage within the MAIN_GAME State.
Subclass of Enum.

Additional methods: none

Additional enum class constants: BEFORE_DIE, BEFORE_FROG,
    BEFORE_FROG_ERROR, DURING_FROG_MOVEMENT
"""


class Game:
    """
    The Abagio game manager.

    To run the game, create an instance of this class and call its run
    method.
    
    Methods: tick, run, quit_game
    
    Instance variables: none

    Class constants:
        BOARD_X - the x coordinate where the game board image is drawn
            onto the window.
        BOARD_Y - the y coordinate where the game board image is drawn
            onto the window.
    """
    
    # Non-public instance variables:
    #    _window - the Window the game will be displayed onto.
    #    _resource_manager - the ResourceManager holding the assets for
    #        the game.
    #    _board - the Board holding the frogs for the game.
    #    _frogs - the list of Frogs currently in the game.
    #    _die1 - the left Die used by the game.
    #    _die2 - the right Die used by the game.
    #    _selected_die - the Die currently selected by the user, or
    #        None if no die is selected.
    #    _die1_collision_rect - the bounding box of the left die when
    #        it was most recently rendered, as a Rect that can be used
    #        to check for collision with the die. Initialized to None.
    #    _die2_collision_rect - the bounding box of the right die when
    #        it was most recently rendered, as a Rect that can be used
    #        to check for collision with the die. Initialized to None.
    #    _ok_button - the bounding box of the "OK" button when it was
    #        most recently rendered, as a Rect that can be used to
    #        check for collision with the button. Initialized to None.
    #    _roll_button - the bounding box of the "Roll" / "Stop" button
    #        when it was most recently rendered, as a Rect that can be
    #        used to check for collision with the button. Initialized
    #        to None.
    #    _rolls - a dictionary used to store the rolls of "red" and
    #        "purple" during the roll for position.
    #    _setup_timer - a Timer used to time the pause between the end
    #        of the final roll for position and the start of the main
    #        game (to time the length of the SETUP_WAITING state).
    #    _indicator_timer - a Timer used for the timing of blinking die
    #        indicators.
    #    _clock - a Pygame Clock used to calculate time deltas between
    #        the rendering of frogs from one tick to the next.
    #    _state - a State representing the current overall part of the
    #        game.
    #    _turn_stage - a TurnStage representing the current stage of
    #        the current player's turn (within the MAIN_GAME state).
    #    _roll_state - a RollState representing the current state of
    #        the game within the SETUP state or ROLL turn stage.
    #    _move_state - a MoveState representing the current state of
    #        the game within the MOVE turn stage.
    #    _rolling_player - a string, typically either "red" or
    #        "purple", representing the player whose turn it is. "done"
    #        is used when both players have finished rolling for
    #        position.
    #    _has_rolled_before - whether or not the first player has
    #        finished rolling for position at least once (SETUP state)
    #        or whether or not the first player has finished rolling
    #        for movement at least once (MAIN_GAME state).
    #    _indicator_on - whether or not the currently blinking die
    #        indicator is in the on state, if applicable.
    #    _doubles - whether or not the player rolled doubles.

    BOARD_X = 320
    BOARD_Y = 60
    
    def __init__(self):
        """
        Create the game manager.
        
        The Pygame window will appear but will not remain visible
        unless the tick or run method is called.
        """
        self._window = Window()
        self._resource_manager = ResourceManager()
        self._board = Board()
        self._frogs = []
        
        self._die1 = Die()
        self._die2 = Die()
        self._selected_die = None
        self._die1_collision_rect = None
        self._die2_collision_rect = None
        self._ok_button = None
        self._roll_button = None
        
        self._rolls = {}
        self._setup_timer = Timer()  # does not start yet
        self._indicator_timer = Timer()  # does not start yet
        self._clock = pygame.time.Clock()
        
        self._state = State.SETUP
        self._turn_stage = TurnStage.ROLL
        self._roll_state = RollState.BEFORE_ROLL
        self._move_state = MoveState.BEFORE_DIE
        self._rolling_player = "red"
        
        self._has_rolled_before = False
        self._indicator_on = True
        self._doubles = False

    def _handle_events(self):
        # Handle the events in the Pygame event queue by performing the
        # appropriate action for each "mouse button up" event. If a
        # "quit" event is found, immediately return True and stop
        # processing events. If no "quit" event is found, return False.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up()
        return False
    
    def _handle_mouse_up(self):
        # Handle a "mouse button up" event by checking for mouse
        # collision with buttons, dice, and/or frogs and performing the
        # appropriate action.
        if self._state is State.SETUP:
            # If the roll button exists and the mouse is on it...
            if (self._roll_button is not None
                    and self._roll_button.collidepoint(
                        pygame.mouse.get_pos())):
                if self._roll_state is RollState.BEFORE_ROLL:
                    self._die1.start_roll()
                    self._roll_state = RollState.DURING_ROLL
                elif self._roll_state is RollState.DURING_ROLL:
                    self._die1.stop_roll()
                    self._roll_state = RollState.AFTER_ROLL
                    
        elif self._state is State.SETUP_TIE:
            if (self._ok_button is not None
                    and self._ok_button.collidepoint(pygame.mouse.get_pos())):
                self._rolling_player = "red"
                self._roll_state = RollState.BEFORE_ROLL
                self._state = State.SETUP
        
        elif self._state is State.MAIN_GAME:
            if (self._roll_button is not None
                    and self._roll_button.collidepoint(
                        pygame.mouse.get_pos())):
                if self._roll_state is RollState.BEFORE_ROLL:
                    self._die1.start_roll()
                    self._die2.start_roll()
                    self._roll_state = RollState.DURING_ROLL
                elif self._roll_state is RollState.DURING_ROLL:
                    self._die1.stop_roll()
                    self._die2.stop_roll()
                    self._roll_state = RollState.AFTER_ROLL
            
            if self._turn_stage is TurnStage.MOVE:
                self._handle_mouse_up_move_stage()

    def _handle_mouse_up_move_stage(self):
        # Handle a "mouse button up" event in the MOVE turn stage by
        # checking for mouse collision with dice and/or frogs and
        # performing the appropriate action.
        if (self._move_state is MoveState.BEFORE_DIE
                or self._move_state is MoveState.BEFORE_FROG
                or self._move_state is MoveState.BEFORE_FROG_ERROR):
            # If the mouse is on the die and the die hasn't been used
            # up yet...
            if (self._die1_collision_rect.collidepoint(pygame.mouse.get_pos())
                    and (self._die1.use_count == 0
                         or (self._doubles and self._die1.use_count == 1))):
                self._move_state = MoveState.BEFORE_FROG
                self._selected_die = self._die1
                self._indicator_on = True
                self._indicator_timer.start(500)
            elif (self._die2_collision_rect.collidepoint(
                    pygame.mouse.get_pos()) and (self._die2.use_count == 0
                        or (self._doubles and self._die2.use_count == 1))):
                self._move_state = MoveState.BEFORE_FROG
                self._selected_die = self._die2
                self._indicator_on = True
                self._indicator_timer.start(500)
        
        if (self._move_state is MoveState.BEFORE_FROG
                or self._move_state is MoveState.BEFORE_FROG_ERROR):
            self._handle_potential_frog_click()
    
    def _handle_potential_frog_click(self):
        # Handle a "mouse button up" event in the MOVE turn stage and
        # BEFORE_FROG or BEFORE_FROG_ERROR move state by checking
        # for mouse collision with all frogs and performing the
        # appropriate action, which may include moving the frog. (Once
        # a frog is moved, no further frogs are checked.)
        for frog in self._frogs:
            if (not frog.is_moving() and frog.collision_rect.collidepoint(
                    pygame.mouse.get_pos()) and frog.is_on_top()):
                spaces = self._selected_die.state
                if (frog.color == self._rolling_player
                        and frog.can_make_legal_leap(spaces)):
                    self._selected_die.use_count += 1
                    frog.stepwise_move(spaces)
                    self._selected_die = None
                    self._move_state = MoveState.DURING_FROG_MOVEMENT
                    return
                else:
                    self._move_state = MoveState.BEFORE_FROG_ERROR
    
    def _display_text(self, text):
        # Draw one or more lines of text (in black font) onto the yellow
        # text box in the window.
        #
        # Arguments:
        #    text - a string representing one or more lines of text,
        #        with lines separated by newline characters.
        self._window.draw_multi_line_text(
            Game.BOARD_X - 280, Game.BOARD_Y + 10, text, "black")
    
    def _get_die_indicator_color(self, die, indicator_no=1):
        # Return a string representing the Pygame color a die indicator
        # should be drawn in after updating internal states related to
        # that indicator if necessary.
        #
        # Arguments:
        #    die - the Die the indicator whose color is being checked
        #        belongs to.
        #    indicator_no - not used if self._doubles is False. If
        #        self._doubles is True, should be either 1 or 2 to
        #        indicate whether the die's 1st or 2nd indicator color
        #        is being checked. Default 1.
        #
        # Note: Die indicator colors have the following meaning:
        #    - Solid green: unused and unselected
        #    - Blinking red (alternating red and white): selected
        #    - Solid red: used
        if self._doubles:
            if die.use_count == 0:
                if die == self._selected_die and indicator_no == 1:
                    if self._indicator_timer.is_done():
                        self._indicator_on = not self._indicator_on
                        self._indicator_timer.stop()
                        self._indicator_timer.start(500)
                    if self._indicator_on:
                        return "red"
                    else:
                        return "white"
                else:
                    return "green"
            elif die.use_count == 1:
                if die == self._selected_die and indicator_no == 2:
                    if self._indicator_timer.is_done():
                        self._indicator_on = not self._indicator_on
                        self._indicator_timer.stop()
                        self._indicator_timer.start(500)
                    if self._indicator_on:
                        return "red"
                    else:
                        return "white"
                else:
                    if indicator_no == 1:
                        return "red"
                    elif indicator_no == 2:
                        return "green"
            else:
                return "red"
        else:
            if die == self._selected_die:
                if self._indicator_timer.is_done():
                    self._indicator_on = not self._indicator_on
                    self._indicator_timer.stop()
                    self._indicator_timer.start(500)
                if self._indicator_on:
                    return "red"
                else:
                    return "white"
            else:
                if die.use_count == 0:
                    return "green"
                else:
                    return "red"
    
    def tick(self):
        """
        Update the game and its display; return whether to quit.
        
        Render everything onto the window, update the game based on its
        current states, handle events, and return whether or not the
        game should quit. Each call to this method comprises one frame
        of the game; for optimal frame rate, this method should be
        repeatedly called as quickly as possible (until it returns
        True).
        """
        self._window.fill("white")
        
        self._window.draw_image(
            Game.BOARD_X, Game.BOARD_Y, self._resource_manager.images["board"])

        # Draw the text box onto which messages for the players will be
        # overlaid.
        self._window.draw_rectangle(Game.BOARD_X - 290, Game.BOARD_Y,
                                    260, 500, "yellow")
        
        self._board.render_frogs(self._clock.tick())
        
        if self._state is State.SETUP:
            self._tick_setup()
        elif self._state is State.SETUP_TIE:
            self._tick_setup_tie()
        elif self._state is State.SETUP_WAITING:
            self._tick_setup_waiting()
        elif self._state is State.MAIN_GAME:
            self._tick_main_game()
                        
        game_exit = self._handle_events()
        self._window.update()
        
        return game_exit
    
    def _tick_setup(self):
        # Render items onto the window and update the game in the SETUP
        # state.
        self._die1.update()
        self._draw_die(1050, 260, self._die1)
        
        if self._rolling_player == "red":
            if self._has_rolled_before:
                self._display_text("Red player, please\nroll for position.")
            else:
                self._display_text("Hello, and welcome\nto Abagio! Red\n"
                                   "player, please roll for\nposition.")
            if self._roll_state is RollState.BEFORE_ROLL:
                self._roll_button = self._window.draw_button(
                    1050, 385, 100, 50, "Roll", "green", "black")
            elif self._roll_state is RollState.DURING_ROLL:
                self._roll_button = self._window.draw_button(
                    1050, 385, 100, 50, "Stop", "red", "black")
            elif self._roll_state is RollState.AFTER_ROLL:
                self._has_rolled_before = True
                self._rolls["red"] = self._die1.state
                self._roll_state = RollState.BEFORE_ROLL
                self._rolling_player = "purple"
        
        elif self._rolling_player == "purple":
            self._display_text("Purple player, please\nroll for position.")
            if self._roll_state is RollState.BEFORE_ROLL:
                self._roll_button = self._window.draw_button(
                    1050, 385, 100, 50, "Roll", "green", "black")
            elif self._roll_state is RollState.DURING_ROLL:
                self._roll_button = self._window.draw_button(
                    1050, 385, 100, 50, "Stop", "red", "black")
            elif self._roll_state is RollState.AFTER_ROLL:
                self._rolls["purple"] = self._die1.state
                self._rolling_player = "done"
        
        elif self._rolling_player == "done":
            if self._rolls["red"] == self._rolls["purple"]:
                self._display_text("There was a tie!\nClick \"OK\" to\n"
                                   "continue.")
                self._state = State.SETUP_TIE
            elif self._rolls["red"] > self._rolls["purple"]:
                self._rolling_player = "red"
                self._setup_timer = Timer(1000)
                self._state = State.SETUP_WAITING
            else:
                self._rolling_player = "purple"
                self._setup_timer = Timer(1000)
                self._state = State.SETUP_WAITING
    
    def _tick_setup_tie(self):
        # Render items onto the window and update the game in the
        # SETUP_TIE state.
        self._die1.update()
        self._draw_die(1050, 260, self._die1)
        self._display_text("There was a tie!\nClick \"OK\" to\ncontinue.")
        self._ok_button = self._window.draw_button(110, 585, 100, 50, "OK",
                                                   "green", "black")
    
    def _tick_setup_waiting(self):
        # Render items onto the window and update the game in the
        # SETUP_WAITING state.
        self._die1.update()
        self._draw_die(1050, 260, self._die1)
        self._display_text("Purple player, please\nroll for position.")
        
        if self._setup_timer.is_done():
            self._setup_timer.stop()
            self._has_rolled_before = False
            
            if self._rolling_player == "red":
                self._add_frogs("red", "purple")
            else:
                self._add_frogs("purple", "red")
            
            self._state = State.MAIN_GAME
            self._turn_stage = TurnStage.ROLL
            self._roll_state = RollState.BEFORE_ROLL
    
    def _tick_main_game(self):
        # Render items onto the window and update the game in the
        # MAIN_GAME state.
        self._die1.update()
        self._die2.update()
        
        self._die1_collision_rect = self._draw_die(973, 260, self._die1)
        self._die2_collision_rect = self._draw_die(1126, 260, self._die2)
        
        if self._turn_stage is TurnStage.ROLL:
            self._tick_main_game_roll()
        
        elif self._turn_stage is TurnStage.MOVE:
            self._tick_main_game_move()
    
    def _tick_main_game_roll(self):
        # Render items onto the window and update the game in the ROLL
        # turn stage in the MAIN_GAME state.
        if self._has_rolled_before:
            self._display_text(self._rolling_player.capitalize()
                               + " player, please\nroll.")
        else:
            if self._rolling_player == "red":
                self._display_text("Red player will\ngo first.\n\n"
                                   "Red player, please\nroll.")
            else:
                self._display_text("Purple player will\ngo first.\n\n"
                                   "Purple player, please\nroll.")
        
        if self._roll_state is RollState.BEFORE_ROLL:
            self._roll_button = self._window.draw_button(
                1050, 385, 100, 50, "Roll", "green", "black")
        elif self._roll_state is RollState.DURING_ROLL:
            self._roll_button = self._window.draw_button(
                1050, 385, 100, 50, "Stop", "red", "black")
        elif self._roll_state is RollState.AFTER_ROLL:
            self._has_rolled_before = True
            self._turn_stage = TurnStage.MOVE
            self._move_state = MoveState.BEFORE_DIE
            if self._die1.state == self._die2.state:
                self._doubles = True
            else:
                self._doubles = False
    
    def _tick_main_game_move(self):
        # Render items onto the window and update the game in the MOVE
        # turn stage in the MAIN_GAME state.
        
        # Render the die indicators.
        if self._doubles:
            self._window.draw_circle(
                1009, 380, 8,
                self._get_die_indicator_color(self._die1, 1))
            self._window.draw_circle(
                1037, 380, 8,
                self._get_die_indicator_color(self._die1, 2))
            self._window.draw_circle(
                1162, 380, 8,
                self._get_die_indicator_color(self._die2, 1))
            self._window.draw_circle(
                1190, 380, 8,
                self._get_die_indicator_color(self._die2, 2))
        else:
            self._window.draw_circle(
                1023, 380, 8,
                self._get_die_indicator_color(self._die1))
            self._window.draw_circle(
                1176, 380, 8,
                self._get_die_indicator_color(self._die2))
            
        if self._move_state is MoveState.BEFORE_DIE:
            self._tick_move_before_die()
        elif self._move_state is MoveState.BEFORE_FROG:
            self._tick_move_before_frog()
        elif self._move_state is MoveState.BEFORE_FROG_ERROR:
            self._tick_move_before_frog_error()
        elif self._move_state is MoveState.DURING_FROG_MOVEMENT:
            self._tick_move_during_frog_movement()
    
    def _tick_move_before_die(self):
        # Render items onto the window and update the game in the
        # BEFORE_DIE move state in the MOVE turn stage in the MAIN_GAME
        # state.
        if self._die1.use_count + self._die2.use_count == 0:
            if self._doubles:
                self._display_text("You rolled doubles!\nYou may use each\n"
                                   + "die twice.\n\n"
                                   + self._rolling_player.capitalize()
                                   + " player, please\nclick on the die that\n"
                                   + "you would like to use\nfirst.")
            else:
                self._display_text(self._rolling_player.capitalize()
                                   + " player, please\nclick on the die that\n"
                                   + "you would like to use\nfirst.")
        else:
            self._display_text(self._rolling_player.capitalize()
                               + " player, please\nclick on the die that\nyou "
                               + "would like to use\nnext.")
    
    def _tick_move_before_frog(self):
        # Render items onto the window and update the game in the
        # BEFORE_FROG move state in the MOVE turn stage in the
        # MAIN_GAME state.
        
        # If both dice can still be selected...
        if ((self._die1.use_count == 0 and self._die2.use_count == 0)
                or (self._doubles and self._die1.use_count < 2
                    and self._die2.use_count < 2)):
            self._display_text(self._rolling_player.capitalize()
                               + " player, please\nclick on the frog\nthat "
                               + "you would like\nto move.\n\n"
                               + "(You may also\nchange your die\nselection "
                               + "if you\nwould like to.)")
        else:
            self._display_text(self._rolling_player.capitalize()
                               + " player, please\nclick on the frog\nthat "
                               + "you would like\nto move.")
    
    def _tick_move_before_frog_error(self):
        # Render items onto the window and update the game in the
        # BEFORE_FROG_ERROR move state in the MOVE turn stage in the
        # MAIN_GAME state.
        
        # If both dice can still be selected...
        if ((self._die1.use_count == 0 and self._die2.use_count == 0)
                or (self._doubles and self._die1.use_count < 2
                    and self._die2.use_count < 2)):
            self._display_text("Invalid target. Please\ntry again.\n\n"
                               + self._rolling_player.capitalize()
                               + " player, please\nclick on the frog\nthat "
                               + "you would like\nto move.\n\n"
                               + "(You may also\nchange your die\nselection "
                               + "if you\nwould like to.)")
        else:
            self._display_text("Invalid target. Please\ntry again.\n\n"
                               + self._rolling_player.capitalize()
                               + " player, please\nclick on the frog\n"
                               + "that you would like\nto move.")
    
    def _tick_move_during_frog_movement(self):
        # Render items onto the window and update the game in the
        # DURING_FROG_MOVEMENT move state in the MOVE turn stage in the
        # MAIN_GAME state.
        self._display_text("Moving...")

        for frog in self._frogs:
            if frog.is_moving():
                return

        # If no frog is moving and both dice are used up, reset for the
        # next turn.
        if (self._die1.use_count + self._die2.use_count == 4
                or (not self._doubles
                    and self._die1.use_count + self._die2.use_count == 2)):
            self._die1.use_count = 0
            self._die2.use_count = 0
            self._turn_stage = TurnStage.ROLL
            if self._rolling_player == "red":
                self._rolling_player = "purple"
            else:
                self._rolling_player = "red"
            self._roll_state = RollState.BEFORE_ROLL
        else:
            self._move_state = MoveState.BEFORE_DIE
    
    def _add_frogs(self, first_player, second_player):
        # Add the frogs onto the board in their starting positions.
        #
        # Arguments:
        #    first_player - a string, either "red" or "purple",
        #        representing the player who is going first.
        #    second_player - a string, either "red" or "purple",
        #        representing the player who is going second.
        first_player_path_space_names = [
            "sw", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
            "12", "13", "14", "15", "16", "17", "18", "19"
        ]
        second_player_path_space_names = [
            "se", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
            "12", "13", "14", "15", "16", "17", "18", "19"
        ]
        if first_player == "red":
            first_player_path_space_names += [
                "20r", "21r", "22r", "23r", "24r", "25r", "26", "er"
            ]
            second_player_path_space_names += [
                "20p", "21p", "22p", "23p", "24p", "25p", "26", "ep"
            ]
        else:
            first_player_path_space_names += [
                "20p", "21p", "22p", "23p", "24p", "25p", "26", "ep"
            ]
            second_player_path_space_names += [
                "20r", "21r", "22r", "23r", "24r", "25r", "26", "er"
            ]
        
        for _ in range(6):
            self._frogs.append(Frog(first_player, "sw",
                                    first_player_path_space_names, self._board,
                                    self._window, Game.BOARD_X, Game.BOARD_Y))
            self._frogs.append(Frog(second_player, "se",
                                    second_player_path_space_names,
                                    self._board, self._window, Game.BOARD_X,
                                    Game.BOARD_Y))
        self._frogs.append(Frog(first_player, "5",
                                first_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
        self._frogs.append(Frog(second_player, "5",
                                second_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
        self._frogs.append(Frog(first_player, "5",
                                first_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
        self._frogs.append(Frog(second_player, "5",
                                second_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
        self._frogs.append(Frog(second_player, "10",
                                second_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
        self._frogs.append(Frog(first_player, "10",
                                first_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
        self._frogs.append(Frog(second_player, "10",
                                second_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
        self._frogs.append(Frog(first_player, "10",
                                first_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
        self._frogs.append(Frog(first_player, "15",
                                first_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
        self._frogs.append(Frog(second_player, "15",
                                second_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
        self._frogs.append(Frog(first_player, "15",
                                first_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
        self._frogs.append(Frog(second_player, "15",
                                second_player_path_space_names, self._board,
                                self._window, Game.BOARD_X, Game.BOARD_Y))
    
    def _draw_die(self, x, y, die):
        # Draw a die onto the window and return its bounding box as a
        # Rect.
        #
        # Arguments:
        #    x - the desired x coordinate of the top-left corner of the
        #        die in the window.
        #    y - the desired y coordinate of the top-left corner of the
        #        die in the window.
        #    die - the Die to be drawn.
        return self._window.draw_image(
            x, y, self._resource_manager.images["die " + str(die.state)])
    
    def run(self):
        """
        Run the game by repeatedly calling the tick method.
        
        The game will continue running and the Pygame window will
        remain visible until the window is closed by the user. A call
        to this method will block until this occurs.
        """
        game_exit = False
        
        while not game_exit:
            game_exit = self.tick()
        
        self.quit_game()
    
    def quit_game(self):
        """
        Close the Pygame window and clean up internally.

        This method does not force quit the program, but Pygame will
        allow the application to exit if other code does not continue
        executing after the call to this method.
        """
        pygame.quit()


# Script to run the game if this module is executed directly.
if __name__ == "__main__":
    game = Game()
    game.run()
