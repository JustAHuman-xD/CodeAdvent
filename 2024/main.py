def day1():
  # Create Dictionaries
  without_text = {}

  for i in range(10):
    without_text[str(i)] = str(i)
  
  with_text = dict(without_text, one = "1", two = "2", three = "3", four = "4",
                   five = "5", six = "6", seven = "7", eight = "8", nine = "9")

  # Which Dictionary to use, (Without for the first puzzle, With for the second)
  mappings = with_text
  
  total_frequency = 0
  
  with open("day1.txt", "r") as input:
    for line in input:
      first_index = None
      first_frequency = ""
      last_index = None
      last_frequency = ""

      # Go through every mapping, "one" -> "1", and keep only the leftmost and rightmost
      for potential_number in mappings:
        if potential_number in line:
          first_instance = line.index(potential_number)
          last_instance = line.rindex(potential_number)
          
          if (first_index is None or first_instance < first_index):
            first_index = first_instance
            first_frequency = mappings[potential_number]

          if (last_index is None or last_instance > last_index):
            last_index = last_instance
            last_frequency = mappings[potential_number]
            
      total_frequency += int(first_frequency + last_frequency)

  print("Total Frequency:", total_frequency)
  
def day2():
    # What cubes we have availible, for a game to be possible it must use no more than these at once
    red_cubes = 12
    blue_cubes = 14
    green_cubes = 13
    
    possible_games_sum = 0
    games_powerset_sum = 0
    
    with open("day2.txt", "r") as input:
        for line in input:
            game = int(line[line.index("Game ") + 5:line.index(":")])
            sets = line[line.index(":") + 1:].split(";")
            possible = True
            
            # These are used to create the "powerset" which is found by multiplying the minimum of each cube needed to perform a game together
            min_red = 1
            min_blue = 1
            min_green = 1
            
            for set in sets:
                cubes = set.split(",")
                for cube in cubes:
                    if "red" in cube:
                        red = int(cube[:cube.index("red")])
                        min_red = max(min_red, red)
                        possible = possible and red_cubes >= red
                    if "blue" in cube:
                        blue = int(cube[:cube.index("blue")])
                        min_blue = max(min_blue, blue)
                        possible = possible and blue_cubes >= blue
                    if "green" in cube:
                        green = int(cube[:cube.index("green")])
                        min_green = max(min_green, green)
                        possible = possible and green_cubes >= green
            
            if possible:
                possible_games_sum += game
            games_powerset_sum += min_red * min_green * min_blue
    
    print("Possible Games Sum:", possible_games_sum)
    print("Games Powerset Sum:", games_powerset_sum)
            
day2()