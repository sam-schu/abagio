"""
Contains a utility timer class.

Class:
    Timer - a reusable, internal timer.
"""

import pygame


class Timer:
    """
    A timer mirroring the functions of a physical countdown timer.

    A single timer can be reused for multiple non-overlapping intervals.
    The timer is non-blocking and can be set to wait any number of
    Pygame ticks before it is considered done. The timer is intended for
    internal use, rather than for display.

    The usage of the start, stop, and is_done methods mirrors the
    corresponding actions of a real-world electronic countdown timer.
    Namely, the start method corresponds to pressing the timer's start
    button, the stop method corresponds to pressing its stop button,
    and the is_done method corresponds to whether or not the timer is
    currently ringing/beeping.
    
    Methods: start, is_done, stop

    Instance variables:
        done_time - the timestamp, as obtained from pygame.time's
            get_ticks() method, at which the timer will be considered
            done. -1 if the timer has not been started or is stopped.
    """
    
    def __init__(self, time_to_wait=None, start_time=None):
        """
        Create and, if desired, start the timer.
        
        Arguments:
            time_to_wait - if not provided or None, do not start the
                timer. If provided, start the timer using the start
                method and wait this number of Pygame ticks after the
                start time before the timer is done.
            start_time - the timestamp, as obtained from pygame.time's
                get_ticks() method, to be used as the start time of the
                timer if time_to_wait is provided and not None. If
                start_time is not provided or None, the current Pygame
                time is used. Discarded if time_to_wait is not provided
                or None.
        """
        if start_time is None:
            start_time = pygame.time.get_ticks()
        if time_to_wait is None:
            self.done_time = -1
        else:
            self.start(time_to_wait, start_time)
    
    def start(self, time_to_wait, start_time=None):
        """
        Start the timer.
        
        Arguments:
            time_to_wait - the number of Pygame ticks to wait after the
                start time before the timer is done.
            start_time - the timestamp, as obtained from pygame.time's
                get_ticks() method, to be used as the start time of the
                timer. If not provided or None, the current Pygame time
                is used.
        
        The timer does not need to be stopped in order to be started
        again.
        """
        if start_time is None:
            start_time = pygame.time.get_ticks()
        self.done_time = start_time + time_to_wait
    
    def is_done(self, current_time=None):
        """
        Return whether or not the timer is done (and not stopped).

        This corresponds to whether or not a corresponding real-world
        timer would be ringing/beeping.
        
        Arguments:
            current_time - the timestamp, as obtained from pygame.time's
                get_ticks() method, to be used as the current time to
                compare the timer against. If not provided or None, the
                current Pygame time is used.
        
        If the timer is stopped or was never started, return False.
        Otherwise, return whether or not the current time (determined
        as described previously) is the same as or after the done time.
        """
        if current_time is None:
            current_time = pygame.time.get_ticks()
        return self.done_time != -1 and current_time >= self.done_time
    
    def stop(self):
        """
        Stop the timer, so that it is no longer considered done.
        
        The timer will not be considered done until it is started and
        the necessary time has elapsed again.
        """
        self.done_time = -1
