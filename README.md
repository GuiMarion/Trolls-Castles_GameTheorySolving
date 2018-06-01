# Trolls-Castles_GameTheorySolving
This short project shows a way to find a good strategy to play the game
Trolls&Castels using GameTheory and linear programming.

## Report

A short report about the strategies and simulation can be found [here](https://github.com/GuiMarion/Trolls-Castles_GameTheorySolving/blob/master/Report.pdf). 


## How to use

### Dependencies

```shell
pip install pulp
pip install pylatex
pip install numpy
pip install tqdm
apt install glpk-utils 
```

### Pickles

Strategies can be calculated in advance and saved in pickles. You can find in the directory pickles for Size 7 and 15.

### Running strategy_nash.py

This program can be used for several things : compute the distribution for a given state represented by the number of rock of each player, the position of the troll and the distance between the two castles. Or fill a pickle with all the distributions that can be used for fast simulations.

To compute a single distribution : 

```shell
Usage: Python3 strategy_nash.py -s <size> x y t
```

With x the number of rock for the player 1 and y the number of rock for the player 2 and t the position of the troll (0 is the middle), and size the distance between the two castles,by default size = 7.


To generate pickles use the -p option.

```shel
python3 strategy_nash.py -s -p
```

```shell
python3 strategy_nash.py -h
```
produces

```
Usage: strategy_nash.py [options]

Options:
  -h, --help                    show this help message and exit
  -s SIZE, --size=SIZE          number of fields between the castles
  -p PICKLE, --pickle=PICKLE    create pickles
```

### Create Report

You can make simulations and see the results in a Tex file very easily with 

		python3 create_report.py

This will use the pickles in the directory to make fast simulations against several other strategies.

### game.py

In ``game.py`` there are some simulations commented. To run a simulation,
uncomment the desired situation in the ``main``. Furthermore, for exterior use
cases, import the file and use the functions ``get_strategy_nash(int)`` and
``get_strategy_nash_eager(int)`` as this is done in ``create_report.py``.


