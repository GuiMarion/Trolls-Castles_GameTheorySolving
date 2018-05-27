# Trolls-Castles_GameTheorySolving
This short project shows a way to find a good strategy to play the game Trolls&Castels using GameTheory and linear programming.


## How to use

### Dependencies

```shell
pip install pulp
pip install pylatex
pip install numpy
pip install tqdm
apt install glpk-utils 
```

### Download pickles

If you don't want to generate the pickles, you can download them:

```shell
mkdir -p field{7,15}

wget -P field7 http://kalnar.eu/assets/game-theory/field7/distributions.pkl 
wget -P field7 http://kalnar.eu/assets/game-theory/field7/utilities.pkl 
wget -P field15 http://kalnar.eu/assets/game-theory/field15/distributions.pkl 
wget -P field15 http://kalnar.eu/assets/game-theory/field15/utilities.pkl 
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
