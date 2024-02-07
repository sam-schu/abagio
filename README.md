# Abagio

A two-player recreation of the board game Abagio using Python and
Pygame. Note that this project is incomplete, but most major gameplay
features have been implemented.

### Important Notes

- Abagio is a two-player game and AI
players have not been implemented, so players are expected to take turns
on the same computer when playing the game.
- The end-game rules, including win detection, have not been
implemented. Thus, the game in its current state serves as a
demonstration of the setup and main gameplay of the game, but
the game will not end until you close the game window.
- The game pieces are called frogs.

### Getting Started

First, make sure to install the pygame package for your Python
interpreter if you do not already have it installed. Then, making sure
not to modify the original directory structure of the game, simply run
the game.py file to start the game. A game window will appear with
instructions to start playing, and all game interactions will take place
in this window. Just follow the instructions and play!

### Project Overview

This project uses Python and the Pygame game creation and graphics
library to create a version of the board game Abagio playable by two
players with an interactive UI. The interface includes a message panel
that displays instructions and feedback for the players, the game board,
and interactive dice. Once the players have rolled for position (i.e.,
to see who goes first), the board is set up, and players take turns
rolling the dice and moving their frogs toward the center of the board.
On each turn, the current player rolls both dice, each of which can be
used separately to move different frogs. The player inputs their
selection by clicking on the die they want to use and then clicking on
the frog they want to move the corresponding number of spaces. If they
roll doubles, each die can be used twice. Clicking on a frog after
selecting a die causes the frog to move around the board, one space at
a time, and potentially stack on top of other frogs at its destination
space. If its final destination
lands it directly on top of a single frog of the opponent's color, that
frog is sent home! Other Abagio rules also apply, including the ability
to block your opponent from landing on a space with a "heap" of three
frogs of the same color, the maximum capacities of the different spaces
(5 frogs for most spaces on the main board), and the splitting of the
board's inner path into separate tracks for each color.

### Features

- ***Game setup sequence.*** Both players roll a single die to determine
the starting player, with ties broken by a reroll. The frogs on the
board are then set up differently depending on the starting player.
- ***Animated dice.*** Dice switch randomly between different numbers
as they are "shaken," and pressing the Stop button stops the dice on
their current numbers. If your reflexes were good enough, you could
theoretically stop the dice on the numbers you wanted to roll!
- ***Multifunctional die indicators.*** After the dice have been rolled,
each die has an indicator that signifies whether the die is unused
(solid green), currently selected (blinking red), or expended (solid
red). This helps the player know which numbers are still available to
use, and helps to prevent them from accidentally clicking the wrong
die. Additionally, when a player rolls doubles, two independent
indicators appear below each die, which emphasizes to the player that
each die can be used two separate times.
- ***Responsive instructions.*** The instructions panel on the left side
of the window gives general instructions for each player during their
turn, and also updates to let the player know when they have attempted
to make an invalid move (so that they know the game is not ignoring
their input).
- ***Frog stacking rules.*** The full set of stacking rules for standard
red and purple frog pieces has been implemented. Specifically:
  - The special diamond spaces between the outer and inner paths of the
  board and between the inner path and the end spaces can have
  a maximum of 2 frogs at a time. All other board spaces (other than the
  starting and ending stacks) can hold a maximum of 5 frogs.
  - If a frog lands directly on top of a single frog of the opposing
  color, the frog landed on is sent home. (This occurs regardless of
  whether the frog being sent home was the only frog on its space or was
  stacked above a frog of the opposite color.)
  - A frog cannot land directly on top of three consecutive frogs of
  the opposing color.
- ***Smooth, consistent movement of frogs regardless of
framerate.*** Time delta calculations are used to ensure that frogs
always move at the same speed around the board regardless of the game's
current framerate. Additionally, two types of movement are implemented.
Stepwise movement, which allows frogs to move one space at a time around
the board, is used when a frog moves a certain number of spaces forward
from a die roll; frogs performing stepwise movement move to the top of
the stack on each space they are passing by to mimic the player
physically moving
the frog piece from one space to the next on the board. Direct movement,
which allows frogs to move directly to a specified space, is used when a
frog is being sent home.
- ***Render priority rules.*** Frogs are assigned different render
priorities depending on their movement state and their position within
a stack so that frog stacks are rendered in the correct order, moving
frogs appear
above stationary frogs, and a frog being sent home appears to slide
out of its stack underneath the frog that is replacing it.
- ***Unique paths for each color.*** Frogs split into two different
halves of the inner path depending on their color, but merge
back together (and can send each other home) on the final diamond space
between the inner path and the end spaces.

### Features/Tasks Not Yet Completed

- *The Top Frog.* This is a special piece in the original Abagio game
that allows any player who has no frogs left at their Root (starting
space) to protect one of their frogs at the end of their turn. This
gameplay feature has not been implemented.
- *Passing.* Automatic passing when a player's roll leaves them unable
to move has not been implemented.
- *End-game rules.* Special rules that take effect near the end of the
game to quicken gameplay have not been added. Additionally, win
detection has not yet been implemented; the game continues running until
the window is closed.
- *Code restructuring.* In the future, I would like to restructure this
project to make use of the model-view-controller (MVC) architecture.
Although the Window class does exist to encapsulate some rendering
operations, the Game class currently not only serves as the game model
but also performs many view- and controller-related functions, leading
to unnecessary code complexity. This also causes
the ways the game is modeled, rendered, and interacted with by the
players to be more tightly coupled than is desirable, meaning that
changing any of these behaviors often requires updating code that
handles the others as well.

### Project Structure

This project contains two top-level directories: *src*, where all game
source code is stored, and *res*, which contains all image files needed
for the game. Within the abagio package of the src directory, the code
is divided into 4 modules: *game*, *gamepieces*, *interface*, and
*timer*.
The game module contains the Game class, which includes the core logic
for the main game loop and the progression of the game through different
states and turns, as well as associated enums and a script to run the
game. The gamepieces module includes classes to represent the dice,
board, spaces, and frogs in the game, which themselves contain a
significant amount of logic needed for the movements of the frogs across
the game board to be validated, tracked, and properly displayed. The
interface module contains classes that simplify the process of rendering
items onto
the game window as well as loading and using game assets, and the
timer module contains a simple utility timer class that enables events
to be scheduled within the game loop.