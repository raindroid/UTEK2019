# UTEK-SKULE
Programming Competition 2019

NOTE: Addional testcases will be released about 1 hour before the end of the competetion.

## Scoring

Parts 1 and 6 will be graded manually. Parts 2-5 will be auto-graded using the provided script (parser.py). Please make sure your output passes the script or you will receive no points for correctness or speed. 

The parser verifies that: 
* the max weight (100 kg) is never exceeded
* the robot only takes one step at a time
* all items are collected
* the robot never leaves the field (0,0) to (100, 100) inclusive
* the robot never occupies the same space as another robot. (Note that swapping spaces with another robot is allowed)
* the robot never touches an obstacle. x1 <= x <= x2, y1 <= y <= y2 is never true

Points for correctness will be awarded if the robot(s) collect all of the items and never crash. Full points for speed will be awarded to the team with the fastest solution (by number of timesteps). Other teams will be awarded points based on the following formula: 
```
15 * min_timesteps / your_timesteps
```
Note that the fastest team receives a bonus 5 points per test case. In the case of a tie, both/ all teams that are tied will receive the bonus

| Part | Maximum points for correctness | Maximum points for speed |
| :---:|      :---:                     |:---:                     |
|   1  |30 (across all 3 test cases)    |    0                     |
|   2  |30                              |   60                     |
|   3  |30                              |   60                     |
|   4  |30                              |   60                     |
|   5  |30                              |   60                     |


## Advice
* Part 1 is useful to ensure you’re parsing the input correctly
* Parts 3 and 4 can be worked on independently, but your solution should allow for them to be combined in part 5
* You can submit suboptimal solutions if you don’t finish parts
* Part 6 can be worked on independently, and may be useful for debugging other parts

### Good luck! 

