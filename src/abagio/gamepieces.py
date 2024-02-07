"""
Contains classes representing the Abagio game pieces.

Classes:
    Die - a 6-sided die that can be used for animated die rolls.
    Board - an Abagio game board.
    Space - a space on an Abagio game board.
    Frog - a frog in the Abagio game.
"""

import random

from abagio.timer import Timer


class Die:
    """
    A representation of a 6-sided die suitable for simple animation.
    
    The die is always (internally) either rolling or not rolling. When
    the die is rolling, it can be updated to change its state if a
    certain amount of time has elapsed.
    
    Note that the die's state is not randomized again when it stops
    rolling - if the roll is animated and the speed is sufficiently
    slow / the player is sufficiently skilled, they may be able to stop
    the die on a desired number.
    
    Methods: start_roll, update, stop_roll
    
    Instance variables:
        state - the number the die is currently showing (an integer
            from 1 to 6).
        speed - the number of Pygame ticks that must elapse before
            attempting to update the die will cause it to display a new
            number if it is rolling.
        use_count - convenience variable that can optionally be used to
            store the number of times this die has been used in
            gameplay. Not updated automatically after initialization.
    """
    
    # Non-public instance variables:
    #    _timer - the Timer used to keep track of whether a sufficient
    #        amount of time has passed for the die's state to be
    #        updated.
    
    def __init__(self, state=None, speed=75):
        """
        Create the die.
        
        Arguments:
            state - the number the die initially shows (should be an
                integer from 1 to 6). If not provided or None, a
                random integer from 1 to 6 is used.
            speed - the number of Pygame ticks that must elapse before
                attempting to update the die will cause it to display a
                new number if it is rolling (default 75).
        
        The die starts out not rolling, and the use count starts at 0.
        """
        if state is None:
            state = random.randint(1, 6)
        self.state = state
        self.speed = speed
        self._timer = Timer()
        self.use_count = 0
    
    def _update_state(self):
        # Set the die's state to a random integer from 1 to 6 other
        # than its current state.
        possible_states = [1, 2, 3, 4, 5, 6]
        possible_states.remove(self.state)
        self.state = random.choice(possible_states)

    def start_roll(self):
        """
        Start the roll.
        
        Set the die's state to a random integer from 1 to 6 other than
        its current state, and make the die start rolling so that
        attempting to update the die will change its state if the
        amount of time indicated by the die's current speed value has
        passed since it was last started or successfully updated. The
        roll does not need to be stopped in order to be started again.
        """
        self._update_state()
        self._timer.start(self.speed)
    
    def update(self):
        """
        If sufficient time has passed, update state and restart roll.
        
        If the die is rolling (the roll was started more recently than
        it was stopped) and the amount of time indicated by the die's
        speed value at the time the roll was last started or updated
        has passed since the roll was last started or updated, set the
        die's state to a random integer from 1 to 6 other than its
        current state, and restart the roll using the current speed
        value.
        """
        if self._timer.is_done():
            self.start_roll()
    
    def stop_roll(self):
        """
        Stop the roll so that updating the die will do nothing.
        
        Note that this does not update the die's state again after the
        die was last updated.
        """
        self._timer.stop()


class Board:
    """
    A representation of an Abagio game board and its spaces and frogs.
    
    Methods: add, render_frogs
    
    Instance variables:
        frogs - the list of Frogs on the board. (read-only property)
        spaces - a dictionary from the name of each space on the board
            to the Space object it is represented by. (read-only
            property)
    """
    
    def __init__(self):
        """
        Create the board.
        
        The spaces dictionary is filled with every space on an Abagio
        game board. There are initially no frogs on the board.
        """
        self._frogs = []
        self._spaces = {
            "sw": Space("sw", 12, 52, 548),
            "se": Space("se", 12, 147, 548),
            "1": Space("1", 5, 52, 450),
            "2": Space("2", 5, 52, 350),
            "3": Space("3", 5, 52, 250),
            "4": Space("4", 5, 52, 150),
            "5": Space("5", 5, 52, 52),
            "6": Space("6", 5, 150, 52),
            "7": Space("7", 5, 250, 52),
            "8": Space("8", 5, 350, 52),
            "9": Space("9", 5, 450, 52),
            "10": Space("10", 5, 548, 52),
            "11": Space("11", 5, 548, 150),
            "12": Space("12", 5, 548, 250),
            "13": Space("13", 5, 548, 350),
            "14": Space("14", 5, 548, 450),
            "15": Space("15", 5, 548, 548),
            "16": Space("16", 5, 450, 548),
            "17": Space("17", 5, 350, 548),
            "18": Space("18", 5, 252, 548),
            "19": Space("19", 2, 300, 500),
            "20r": Space("20r", 5, 248, 446),
            "21r": Space("21r", 5, 154, 446),
            "22r": Space("22r", 5, 154, 350),
            "23r": Space("23r", 5, 154, 250),
            "24r": Space("24r", 5, 154, 154),
            "25r": Space("25r", 5, 248, 154),
            "20p": Space("20p", 5, 352, 446),
            "21p": Space("21p", 5, 446, 446),
            "22p": Space("22p", 5, 446, 350),
            "23p": Space("23p", 5, 446, 250),
            "24p": Space("24p", 5, 446, 154),
            "25p": Space("25p", 5, 352, 154),
            "26": Space("26", 2, 299, 199),
            "er": Space("er", 12, 248, 350),
            "ep": Space("ep", 12, 352, 350),
        }
    
    @property
    def frogs(self):
        """
        Get a copy of the frogs on the board.
        
        Get a shallow copy of the list of the Frog objects on the
        board. (read-only property)
        """
        return self._frogs[:]
    
    @property
    def spaces(self):
        """
        Get a copy of the dictionary of the spaces on the board.
        
        Get a shallow copy of the dictionary from the name of each
        space on the board to the Space object it is represented by.
        (read-only property)
        """
        return self._spaces.copy()
    
    def add(self, frog):
        """
        Add a frog to the board.
        
        Arguments:
            frog - the Frog object to be added to the end of the list
                of frogs on the board.

        Note that this does not automatically add the frog to any Space
        on the board.
        """
        self._frogs.append(frog)
    
    def render_frogs(self, dt):
        """
        Render the board's frogs onto the Window in their window field.
        
        The update_render_priority method is called on all frogs on the
        board, and the frogs are rendered from low to high render
        priority.
        
        Arguments:
            dt - the difference between the current time and the time
                when the frogs' coordinates were last updated (which
                occurs when the frogs are rendered), in milliseconds.
        """
        for frog in self._frogs:
            frog.update_render_priority()
        
        sorted_frogs = sorted(self._frogs,
                              key=lambda frg: frg.render_priority)
        for frog in sorted_frogs:
            frog.render(dt)


class Space:
    """
    A representation of an Abagio board space and its Frog stack.
    
    Methods: add, lowest_empty_layer, pop, pop_verify, is_on_top,
        can_legally_take, send_frogs_home, pull_out
    
    Instance variables:
        name - a string representing the name of the space.
        capacity - the maximum number of frogs allowed to occupy the
            space simultaneously. (read-only property)
        x - the x coordinate of the center of the space on the board.
        y - the y coordinate of the center of the space on the board.
    
    Note that (0, 0) represents the top-left corner of the board, not
    of the window.
    """
    
    # Non-public instance variables:
    #    _frogs - the list of frogs currently occupying the space,
    #        from bottom to top with no gaps.
    
    def __init__(self, name, capacity, x, y):
        """
        Create the space.
        
        Arguments:
            name - a string representing the name of the space.
            capacity - the maximum number of frogs allowed to occupy
                the space simultaneously.
            x - the x coordinate of the center of the space on the
                board.
            y - the y coordinate of the center of the space on the
                board.
        
        Note that (0, 0) represents the top-left corner of the board,
        not of the window.
        
        There are initially no frogs on the space.
        """
        self.name = name
        self._capacity = capacity
        self.x = x
        self.y = y
        self._frogs = []
    
    @property
    def capacity(self):
        """
        Get the maximum capacity of the space's frog stack.
        
        Get the maximum number of frogs allowed to occupy the space
        simultaneously. (read-only property)
        """
        return self._capacity
    
    def add(self, frog):
        """
        Add a frog to the space and return its new layer.
        
        Add a frog to the space at the top of the stack and return the
        layer where it was added. The frog's layer field is not
        updated. A RuntimeError is raised if the space is already at
        capacity.
        
        Arguments:
            frog - the Frog to be added.
        """
        layer = len(self._frogs)
        if layer >= self._capacity:
            raise RuntimeError("a new frog cannot be added to the stack - it "
                               "is already full")
        
        self._frogs.append(frog)
        return layer

    def lowest_empty_layer(self):
        """
        Return the space's lowest empty layer, or None if it is full.
        
        Return the lowest layer in the space's stack that is not
        occupied by a frog, or None if the space is at capacity.
        """
        layer = len(self._frogs)
        
        if layer >= self._capacity:
            return None
        else:
            return layer
    
    def pop(self):
        """
        Remove and return the highest frog in the space's stack.
        
        Remove the highest frog in the space's stack from the space,
        and return the popped Frog. A RuntimeError is raised if the
        space is empty.
        """
        if len(self._frogs) == 0:
            raise RuntimeError("the stack is empty, so a frog cannot be "
                               "popped from it")

        return self._frogs.pop()
    
    def pop_verify(self, frog):
        """
        Verify, remove, and return the highest frog in the stack.
        
        Remove the highest frog in the space's stack from the space,
        verifying it against the specified Frog, and return the popped
        Frog. A RuntimeError is raised if the given Frog is not at the
        top of the space's stack.
        
        Arguments:
            frog - the highest frog in the space's stack.
        """
        if not self.is_on_top(frog):
            raise RuntimeError("the specified frog is not at the top of the "
                               "stack")
        
        return self._frogs.pop()
    
    def is_on_top(self, frog):
        """
        Return whether the given frog is on top of the space's stack.
        
        Arguments:
            frog - the Frog object to check.
        """
        return len(self._frogs) > 0 and self._frogs[-1] is frog
    
    def can_legally_take(self, frog):
        """
        Return whether the space can legally accept the specified frog.
        
        Return whether or not the specified frog can be added to the
        top of the space's stack without breaking the rules of Abagio.
        This is True if the space is not at capacity and the 3 highest
        frogs on the space do not comprise a heap of a color different
        than the specified frog's, and False otherwise. Regardless of
        the return value, the frog is not actually added to the space.
        
        Arguments:
            frog - the Frog object to check.
        """
        if len(self._frogs) >= 3:
            highest_frog = self._frogs[-1]
            if (highest_frog.color != frog.color
                    and highest_frog.color == self._frogs[-2].color
                    and highest_frog.color == self._frogs[-3].color):
                return False
        return len(self._frogs) < self._capacity
    
    def send_frogs_home(self):
        """
        Send the second-highest frog on the space home if necessary.
        
        Should be called directly after a frog is added to the top of
        the space's stack that might require the frog underneath it to
        be sent home. If the second-highest frog in the space's stack
        is a blot being hit by the highest frog (which is assumed to
        have just landed on the space), give the highest frog a render
        priority offset of 51, give the rest of the stack (including
        the second-highest frog) a render priority offset of 50, and
        send the second-highest frog home by calling the send_home
        method on it. The list of frogs occupying this space is not
        updated, the frogs' layer fields are not updated, and the
        highest frog is not visually moved to its new position in the
        stack (unless the send_home call causes any of these actions to
        be performed).
        """
        if len(self._frogs) >= 2:
            sending_frog_home = False
            highest_frog = self._frogs[-1]
            send_home_frog = self._frogs[-2]
            if len(self._frogs) >= 3:
                if (highest_frog.color != send_home_frog.color
                        and send_home_frog.color != self._frogs[-3].color):
                    sending_frog_home = True
            else:
                if highest_frog.color != send_home_frog.color:
                    sending_frog_home = True
            
            if sending_frog_home:
                for frog in self._frogs:
                    frog.render_priority_offset = 50
                highest_frog.render_priority_offset += 1
                send_home_frog.send_home()
    
    def pull_out(self, frog):
        """
        Remove a frog from anywhere in the space's stack.
        
        Remove the specified frog from the space's stack and adjust the
        positions of the frogs above it in the stack by shifting them
        down in the space's stack and calling the shift_down method on
        them. A ValueError is raised if the specified frog is not in
        the stack.
        
        Arguments:
            frog - the Frog object to remove.
        """
        try:
            idx = self._frogs.index(frog)
            del self._frogs[idx]
            for fg in self._frogs[idx:]:
                fg.shift_down()
        except ValueError:
            raise ValueError("the specified frog is not in the stack")


class Frog:
    """
    A frog in the Abagio game.
    
    Methods: update_coords, render, direct_space_move,
        stepwise_move, is_moving, is_on_top, can_make_legal_leap,
        update_render_priority, send_home, shift_down
    
    Instance variables:
        color - a string, either "red" or "purple", representing the
            color of the frog. (read-only property)
        layer - the frog's layer in the frog stack it is in (an
            integer; layers are counted from bottom to top, starting at
            0). Should always match the frog's position in the list of
            frogs occupying the Space it is on, unless the frog is
            moving, in which case these values may be temporarily out
            of sync. May be 1 higher than should be allowed by the
            capacity of a Space it is moving to in the middle of a
            stepwise movement if that space is full; in this case, the
            frog will not be in that Space's list of frogs. (read-only
            property)
        collision_rect - the bounding box of the frog when it was most
            recently rendered, as a Rect that can be used to check for
            (approximate) collision with the frog. None if the frog has
            not been rendered yet.
        x - the current x coordinate of the center of the frog where it
            should be displayed in the window. (read-only property)
        y - the current y coordinate of the center of the frog where it
            should be displayed in the window. (read-only property)
        render_priority - an integer indicating the order in which the
            frog should be rendered relative to other frogs. Frogs
            should be rendered from LOW TO HIGH render priority. Is
            updated using the standard render priority calculation by
            calling the update_render_priority method, but this value
            can also be manually set if desired. If not manually set,
            the value of this field should only be used directly after
            calling update_render_priority. Initially set to 0.
        render_priority_offset - an integer offset added to the base
            render priority value when the update_render_priority
            method is called. Initially set to 0. When a frog being
            sent home reaches the root, all frogs on the same board as
            that frog have their render priority offsets reset to 0;
            when a frog engaged in stepwise movement reaches its final
            destination, the render priority offsets of the frogs on
            that space may be updated by Space's send_frogs_home
            method (see that method's documentation for details).
            Otherwise, must be manually set.
    
    Class constants:
        PIXELS_PER_MS - the (maximum) fractional number of pixels a
            frog should move each millisecond, in Euclidean (straight-
            line) distance from its starting point to its ending point.
        DISPLAY_RADIUS - the radius of the rendered frogs (drawn as
            circles).
    """
    
    # Non-public instance variables:
    #    _board - the Board the frog is a part of.
    #    _space - the Space the frog is on (is updated internally at
    #        varying times when the frog moves).
    #    _path - the ordered list of spaces the frog will traverse
    #        around the board.
    #    _window - the Window the frog should be rendered onto.
    #    _is_being_sent_home - whether or not the frog is currently
    #        being sent / moving back to the root.
    #    _x_target - the x coordinate of the position the frog is
    #        currently moving to. If the frog is currently doing a
    #        stepwise movement, only represents the x coordinate of the
    #        next space in the sequence, not the x coordinate of the
    #        ultimate target (unless the frog is on its last step). If
    #        the frog is not moving, will be equal to _x.
    #    _x_move - the signed, fractional number of pixels the frog
    #        should move each millisecond along the x axis.
    #    _y_target - the y coordinate of the position the frog is
    #        currently moving to. If the frog is currently doing a
    #        stepwise movement, only represents the y coordinate of the
    #        next space in the sequence, not the y coordinate of the
    #        ultimate target (unless the frog is on its last step). If
    #        the frog is not moving, will be equal to _y.
    #    _y_move - the signed, fractional number of pixels the frog
    #        should move each millisecond along the y axis.
    #    _target_space - the destination Space the frog is currently
    #        moving toward. If the frog is currently doing a stepwise
    #        movement, this represents the final destination space, not
    #        just the target of its current step. Not guaranteed to be
    #        used for all types of movement, so may still have an old
    #        value left over from a previous type of movement. Initially
    #        equal to the frog's starting space.
    #    _stepwise_movement - whether or not the frog is currently
    #        engaged in stepwise movement - a type of movement that
    #        allows a frog to move toward a final destination space by
    #        moving directly to each space along the way, one at a time.
    #    _x_offset - the offset that should be added to the x coordinate
    #        of the space the frog is on when determining the x
    #        coordinate of the frog, to account for the location of the
    #        board in the display window.
    #    _y_offset - the offset that should be added to the y coordinate
    #        of the space the frog is on when determining the y
    #        coordinate of the frog, to account for the location of the
    #        board in the display window.

    # Non-public class constants:
    #    _LAYER_SPACING - the difference in y coordinate between frogs
    #        at adjacent layers of the same space.
    
    PIXELS_PER_MS = 0.2
    DISPLAY_RADIUS = 20
    _LAYER_SPACING = 10
    
    def __init__(self, color, starting_space_name, path_space_names, board,
                 window, x_offset, y_offset):
        """
        Create the frog.
        
        Arguments:
            color - the color of the frog, used to determine both how
                it is rendered and how it behaves (i.e., which player
                it belongs to). Must be either "red" or "purple".
            starting_space_name - the name of the space on the frog's
                board that the frog should start on (as a string).
            path_space_names - an ordered list of the names of the
                spaces on the frog's board the frog should be able to
                traverse (i.e., the list of the names of the spaces on
                the frog's board the frog should be allowed to travel
                on, ordered from the beginning to the end of the
                board), as strings.
            board - the Board the frog should be a part of.
            window - the Window the frog should be rendered onto when
                the render method is called.
            x_offset - the offset that should be added to the x
                coordinate of the space the frog is on when determining
                the x coordinate of the frog, to account for the
                location of the board in the display window.
            y_offset - the offset that should be added to the y
                coordinate of the space the frog is on when determining
                the y coordinate of the frog, to account for the
                location of the board in the display window.
        
        The frog is added to the specified board and to the top of the
        stack on the space on that board whose name matches the
        specified starting space name; the layer field is set
        accordingly. The collision_rect field is initialized to None
        until the frog is rendered. The frog's x and y coordinates are
        set according to the space it is on, the layer it is on within
        that space, and the provided x and y offsets. The frog's render
        priority and render priority offset are initialized to 0. A
        RuntimeError is raised if the frog cannot be added to the
        specified space because the space is already full.
        """
        self._color = color
        self._board = board
        self._board.add(self)
        self._space = self._board.spaces[starting_space_name]
        self._path = [self._board.spaces[space_name]
                      for space_name in path_space_names]
        self._layer = self._space.add(self)
        self._window = window
        self._x_offset = x_offset
        self._y_offset = y_offset
        self.collision_rect = None
        self._is_being_sent_home = False

        self._x = self._space.x + self._x_offset
        self._x_target = self._x
        self._x_move = 0
        # Frogs at adjacent layers of the same space are separated by
        # 10 pixels.
        self._y = (self._space.y + self._y_offset
                   - self._layer * Frog._LAYER_SPACING)
        self._y_target = self._y
        self._y_move = 0
        self._target_space = self._space
        self._stepwise_movement = False
        self.render_priority = 0
        self.render_priority_offset = 0
    
    @property
    def color(self):
        """Get the color (string) of the frog. (read-only property)"""
        return self._color
    
    @property
    def layer(self):
        """
        Get the frog's layer (when not moving). (read-only property)
        
        Get the layer of the frog in the frog stack it is in (an
        integer; layers are counted from bottom to top, starting at 0).
        Results are undefined if the frog is moving.
        """
        return self._layer
    
    @property
    def x(self):
        """Get the x coordinate of the frog. (read-only property)"""
        return self._x
    
    @property
    def y(self):
        """Get the y coordinate of the frog. (read-only property)"""
        return self._y
    
    def update_coords(self, dt):
        """
        Update the x and y coordinates of the frog.
        
        Use the specified time delta since the last update to update the
        x and y coordinates of the frog if it is currently engaged in
        movement (which must have been initiated with a different
        method) such that the frog will move at the same speed
        regardless of the time between calls, helping to ensure smooth
        movement with a variable frame rate. (This means that, if the
        frog is engaged in movement, it will always move at the
        Euclidean (straight-line) rate given by the value of
        PIXELS_PER_MS when the movement was initiated, except that it
        will not overshoot its destination.)
        
        If this call makes the frog reach its destination while being
        sent home, add the frog to the top of its new space, update the
        frog's layer field accordingly, and reset the render priority
        offsets of all frogs on the same board as this frog to 0. If
        this call makes the frog reach one of the spaces in the middle
        of a stepwise movement, start a direct space move to the next
        space in the sequence. If this call makes the frog reach its
        final destination in a stepwise movement, send frogs home on
        the destination space if necessary.
        
        Arguments:
            dt - the difference between the current time and the time
                the frog's coordinates were last updated (which occurs
                when the update_coords or render method is called), in
                milliseconds.
        """
        # Calculate the signed x amount and y amount that the frog
        # should move this frame.
        x_move_dt = self._x_move * dt
        y_move_dt = self._y_move * dt
        
        # Make sure the frog doesn't overshoot its target in x.
        if x_move_dt >= 0:
            if self._x + x_move_dt >= self._x_target:
                self._x = self._x_target
                finished_one_space_x_movement = True
            else:
                self._x += x_move_dt
                finished_one_space_x_movement = False
        else:
            if self._x + x_move_dt <= self._x_target:
                self._x = self._x_target
                finished_one_space_x_movement = True
            else:
                self._x += x_move_dt
                finished_one_space_x_movement = False
        
        # Make sure the frog doesn't overshoot its target in y.
        if y_move_dt >= 0:
            if self._y + y_move_dt >= self._y_target:
                self._y = self._y_target
                finished_one_space_y_movement = True
            else:
                self._y += y_move_dt
                finished_one_space_y_movement = False
        else:
            if self._y + y_move_dt <= self._y_target:
                self._y = self._y_target
                finished_one_space_y_movement = True
            else:
                self._y += y_move_dt
                finished_one_space_y_movement = False
        
        # If the frog has made it one space...
        if finished_one_space_x_movement and finished_one_space_y_movement:
            if self._is_being_sent_home:
                self._is_being_sent_home = False
                self._space = self._target_space
                self._layer = self._space.add(self)
                # When a frog being sent home reaches the root, all
                # frogs on the same board have their render priority
                # offset reset to 0.
                for frog in self._board.frogs:
                    frog.render_priority_offset = 0
            
            if self._stepwise_movement:
                if self._space == self._target_space:
                    self._space.send_frogs_home()
                    self._stepwise_movement = False
                else:
                    self.direct_space_move(self._increment_space(1))
        
    def render(self, dt):
        """
        Update the coordinates of and then render the frog.
        
        Call the update_coords method with the specified time delta to
        update the x and y coordinates of the frog, and then render the
        frog onto the window at its current coordinates with the
        correct color. Set the collision_rect field to the bounding box
        of the drawn frog.
        
        Arguments:
            dt - the difference between the current time and the time
                the frog's coordinates were last updated (which occurs
                when the update_coords or render method is called), in
                milliseconds.
        """
        self.update_coords(dt)
        self.collision_rect = self._window.draw_frog(
            int(self._x), int(self._y), Frog.DISPLAY_RADIUS, self._color)
    
    def _increment_space(self, increment, current_space=None):
        # Return the Space that is increment spaces after current_space
        # on the frog's path, or None if the increment is too high.
        #
        # Arguments:
        #    increment - a nonnegative integer indicating the number of
        #        spaces past current_space the desired space is on the
        #        frog's path.
        #    current_space - the space to start at. If not provided or
        #        None, the value of self._space is used.
        if current_space is None:
            current_space = self._space
        
        new_space_index = self._path.index(current_space) + increment
        if new_space_index >= len(self._path):
            return None
        else:
            return self._path[new_space_index]

    def direct_space_move(self, space):
        """
        Start a direct movement to a space (not for being sent home!).
        
        Initiate direct movement to the specified space. Assumes that
        no other frogs on the board are moving from when this method is
        called until the movement is complete, and that the frog is
        currently on the top of its stack. Remove the frog from its
        current space (unless it is in a temporary layer), update its
        layer to the lowest empty layer at the space it will be moving
        to, and add the frog to the new space if the space has room. If
        the new space does not have room, assign the frog a temporary
        layer 1 higher than should be allowed by the capacity of the
        space; this is intended to allow movements to full spaces in
        the middle of a stepwise movement.
        
        Should not be used to send a frog home; instead, the send_home
        method should be called to correctly handle internal states.
        
        As with other methods that initiate movement, does not actually
        adjust the frog's coordinates, internally or visually; the
        update_coords or render method must be called (after calling
        this method) to do so.

        A RuntimeError is raised if the frog is not in a temporary layer
        but is not on the top of its stack.
        
        Arguments:
            space - the Space the frog should move to.
        """
        
        # If the frog is in a temporary layer, there is no need to pop
        # since it is not included in any Space's list of frogs.
        if self._layer < self._space.capacity:
            self._space.pop_verify(self)
        self._space = space
        self._layer = self._space.lowest_empty_layer()
        if self._layer is None:
            # If the space is full (which should only potentially occur
            # if the frog is engaged in stepwise movement and the space
            # is not the frog's final destination), give the frog a
            # temporary layer one above the actual highest layer of the
            # space. (There is no need to update the Space since it does
            # not have enough room and is not the frog's final
            # destination.)
            self._layer = self._space.capacity
        else:
            self._space.add(self)

        # Frogs at adjacent layers of the same space are separated by 10
        # pixels.
        self._direct_coords_move(
            self._space.x + self._x_offset,
            self._space.y + self._y_offset - self._layer * Frog._LAYER_SPACING)
    
    def _direct_coords_move(self, x_target, y_target):
        # Initiate direct movement to the given x and y coordinates by
        # doing math to set the necessary internal fields to their
        # correct values. Only numerical fields relating directly to
        # the movement path are updated.
        #
        # As with other methods that initiate movement, does not
        # actually adjust the frog's coordinates, internally or
        # visually; the update_coords or render method must be called
        # (after calling this method) to do so.
        #
        # Arguments:
        #    x_target - the x coordinate of the position the frog
        #        should move to.
        #    y_target - the y coordinate of the position the frog
        #        should move to.
        self._x_target = x_target
        self._y_target = y_target
        
        # If the frog is already at the correct x position, move in a
        # straight vertical line toward the y target. A special case is
        # needed to avoid division by 0.
        if self._x_target - self._x == 0:
            self._x_move = 0
            if self._y_target >= self._y:
                self._y_move = Frog.PIXELS_PER_MS
            else:
                self._y_move = - Frog.PIXELS_PER_MS
        else:
            # It is impossible for the large denominator to be 0
            # because that would require
            # ((y_target - y) / (x_target - x)) ^ 2 to equal -1.
            self._x_move = (
                ((Frog.PIXELS_PER_MS * Frog.PIXELS_PER_MS)
                 / (1 + (((self._y_target - self._y)
                          / (self._x_target - self._x))
                    * ((self._y_target - self._y)
                       / (self._x_target - self._x))))) ** 0.5)
            self._y_move = abs(((self._y_target - self._y)
                                / (self._x_target - self._x)) * self._x_move)
            
            # Make x_move and y_move appropriately signed.
            if self._x_target < self._x:
                self._x_move *= -1
            if self._y_target < self._y:
                self._y_move *= -1

    def stepwise_move(self, spaces_to_move):
        """
        Start movement along the frog's path, one space at a time.
        
        Initiate movement that will bring the frog the specified number
        of spaces forward along its path, moving one space at a time.
        First, initiate a direct space move to the next space on the
        frog's path. When the update_coords method (which is called by
        the render method) is called, if the frog has finished moving
        to a space but has not yet reached its final destination, a
        direct space move to the next space on the frog's path will be
        initiated.
        
        The can_make_legal_leap method should be called immediately
        before calling this method to check that the spaces_to_move
        value used will be valid.
        
        As with other methods that initiate movement, does not actually
        adjust the frog's coordinates, internally or visually; the
        update_coords or render method must be called (after calling
        this method) to do so.

        Raises a ValueError if the provided spaces_to_move value would
        bring the frog out of bounds.
        
        Arguments:
            spaces_to_move - a positive integer (>= 1) indicating the
                number of spaces forward along its path the frog should
                move. Must not be too high such that a space that
                number of spaces forward along its path does not exist.
        """
        self._target_space = self._increment_space(spaces_to_move)
        if self._target_space is None:
            raise ValueError("the provided spaces_to_move value would bring "
                             "the frog out of bounds")
        self._stepwise_movement = True
        self.direct_space_move(self._increment_space(1))
        
    def is_moving(self):
        """
        Return whether or not the frog is moving.
        
        Specifically, return whether at least one of the coordinates of
        the frog differs from the corresponding coordinate of its
        target, which is based on the last time movement was initiated.
        """
        return self._x != self._x_target or self._y != self._y_target
    
    def is_on_top(self):
        """
        Return whether or not the frog is on top of its space's stack.
        
        Results are undefined if the frog is moving.
        """
        return self._space.is_on_top(self)
    
    def can_make_legal_leap(self, spaces_to_move):
        """
        Return whether or not the frog can legally move to a space.
        
        Return whether or not the frog can legally move to the space
        that is the specified number of spaces on its path past its
        current space. This requires that such a space exists and that
        the desired destination space can legally take the frog, which
        itself requires that the space is not at capacity and that the 3
        highest frogs on the space do not comprise a heap of a color
        different than this frog's color. Assumes that no frogs on the
        frog's board are moving. Regardless of the return value,
        movement is not initiated for the frog by this method.
        
        This method should be called before initiating movement to a
        new space in order to check that the movement is valid.
        
        Arguments:
            spaces_to_move - a positive integer (>= 1) indicating the
                number of spaces forward along the frog's path
                (relative to the frog's current space) the space is
                that should be checked.
        """
        new_space = self._increment_space(spaces_to_move)
        return new_space is not None and new_space.can_legally_take(self)
    
    def update_render_priority(self):
        """
        Update the frog's render_priority field with a new calculation.
        
        Calculate the frog's render priority according to the standard
        render priority calculation: add the frog's current layer to
        its render priority offset, and add another 100 to the render
        priority if the frog is moving but is not being sent home.
        Then, set the frog's render_priority field to the result of
        this calculation. This calculation is sufficient to ensure that
        frog stacks and moving frogs are displayed correctly as long as
        the Space class correctly updates render priority offsets when
        a frog is sent home and frogs are rendered from LOW TO HIGH
        render priority.
        """
        self.render_priority = self._layer + self.render_priority_offset
        if self.is_moving() and not self._is_being_sent_home:
            self.render_priority += 100
    
    def send_home(self):
        """
        Send the frog home.
        
        Remove the frog from its current space, which causes the
        shift_down method to be called on the frog(s) above it, and
        initiate a direct movement to the coordinates of the frog's
        root (starting space). Note that this method does not update
        any frogs' render priority offsets - this should be done by the
        caller of this method before calling this method. Also note
        that neither is the frog's layer updated nor is it added to its
        starting space's (root's) stack until it reaches that space.
        Assumes that no frogs on the frog's board are moving and that
        the set of frogs at the root the frog is being sent to will not
        change between when this method is called and when the frog
        finishes moving / being sent home.
        
        This method should be used rather than direct_space_move for
        sending a frog home.
        
        As with other methods that initiate movement, does not actually
        adjust the frog's coordinates, internally or visually; the
        update_coords or render method must be called (after calling
        this method) to do so.
        """
        self._is_being_sent_home = True
        self._target_space = self._path[0]
        self._space.pull_out(self)
        
        # Frogs at adjacent layers of the same space are separated by 10
        # pixels.
        self._direct_coords_move(
            self._target_space.x + self._x_offset,
            self._target_space.y + self._y_offset
            - (self._target_space.lowest_empty_layer() * Frog._LAYER_SPACING))
    
    def shift_down(self):
        """
        Move the frog down a layer (use only after updating its Space).
        
        Decrease the frog's layer by 1, and initiate a direct movement
        to coordinates that will visually cause the frog to shift down
        1 layer. Should only be called after the frog's Space is
        updated such that the frog is 1 layer below where it previously
        was in the stack.
        
        As with other methods that initiate movement, does not actually
        adjust the frog's coordinates, internally or visually; the
        update_coords or render method must be called (after calling
        this method) to do so.
        """
        self._layer -= 1
        self._direct_coords_move(self.x, self.y + Frog._LAYER_SPACING)
