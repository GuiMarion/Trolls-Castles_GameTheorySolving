#!/bin/bash

mkdir -p field9
mkdir -p field11
mkdir -p field13
mkdir -p field17
mkdir -p field19
mkdir -p field21


for i in 9 11 13 17 19 21; do
  wget -P field${i} http://kalnar.eu/assets/game-theory/field${i}/distributions.pkl 
  wget -P field${i} http://kalnar.eu/assets/game-theory/field${i}/utilities.pkl 
done
