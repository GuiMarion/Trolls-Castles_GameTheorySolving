#!/bin/bash

mkdir -p field{9..13..2}
mkdir -p field{17..21..2}

for i in {9..13..2} {17..21..2}: do
  wget -P field${i} http://kalnar.eu/assets/game-theory/field${i}/distributions.pkl 
  wget -P field${i} http://kalnar.eu/assets/game-theory/field${i}/utilities.pkl 
done