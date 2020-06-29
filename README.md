# pong

Plays a squash type game of pong either manually or automatically by linearly interpolating on a previous game

Inspired by Computerphile video:

https://www.youtube.com/watch?v=VyrAVNoEf0g

## Requires 

Pygame

Sklearn

## To run

1) python pong_full.py      
   
   Play full manual 
   
2) python pong_full.py --record
 
    Play manually record play in file game.csv
   
3) python pong_full.py   --ai

   Play automatically by linearly interpolating on paddle positions recorded in game.csv
   
4) python pong_full.py --record --ai

   Play automatically by linearly interpolating on paddle positions recorded in game.csv and record the game in the file 

