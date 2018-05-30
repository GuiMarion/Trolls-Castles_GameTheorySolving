# Trolls-Castles_GameTheorySolving
This short project shows a way to find a good strategy to play the game
Trolls&Castels using GameTheory and linear programming.

## Report

A short report about the strategies and simulation can be found [here](https://github.com/GuiMarion/Trolls-Castles_GameTheorySolving/blob/master/report/report_with_strategies.pdf). 


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

Strategies can be calculated in advance and saved in pickles. Pickles for
distance ``7`` and ``15`` are included. You can generate others or if you don't
want to, you can download pickles for distances: ``9,11,13,17,19,21``:

```shell
mkdir -p field{9..13..2}
mkdir -p field{17..21..2}

for i in {9..13..2} {17..21..2}: do
  wget -P field${i} http://kalnar.eu/assets/game-theory/field${i}/distributions.pkl 
  wget -P field${i} http://kalnar.eu/assets/game-theory/field${i}/utilities.pkl 
done
```

### Running strategy_nash.py

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


to generate pickles:

```shel
python3 strategy_nash.py -p
```

to calculate the distribution for a single step in the game:

```shell
python3 strategy_nash.py 15 14 -1
```

this will calculate the distribution of stones to throw for the state
``(15,14,-1)``, which means that player one has 15 stones, player two has 14
stones and the troll is one step closer to player one than to player two.

If you want to change to size i.e. the distance between the castles, use
the flag ``-s --size``, e.g.:

```shell
python3 strategy_nash.py -s 15 15 14 -1
```

calculates the same thing as before, but the distance between the castles is
now 15.

You can use this for creating pickles as well, e.g.

```shell
python3 strategy_nash.py -s 15 -p
```

will create the pickles for the size 15.


### game.py

In ``game.py`` there are some simulations commented. To run a simulation,
uncomment the desired situation in the ``main``. Furthermore, for exterior use
cases, import the file and use the functions ``get_strategy_nash(int)`` and
``get_strategy_nash_eager(int)`` as this is done in ``create_report.py``.


