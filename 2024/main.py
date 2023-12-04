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
      
def day3():      
  already_added = []
  gearshift_sum = 0
  gearratio_sum = 0
  
  def is_numeric(section):
    for character in section:
      if character.isnumeric():
        return True
    return False
    
  def get_number_left_side(section):
    number = ""
    left_i = 1
    while True:
      sub_section = section[len(section) - left_i:]
      if sub_section.isnumeric() and left_i <= len(section):
        number = sub_section
        left_i += 1
      else:
        break
    return dict(number=number, index=len(section) - left_i + 1)
  
  def get_number_right_side(section):
    number = ""
    right_i = 0
    while True:
      sub_section = section[:right_i + 1]
      if sub_section.isnumeric() and right_i < len(section):
        number = sub_section
        right_i += 1
      else:
        break
    return dict(number=number, index=right_i)
    
  
  def get_gearshifts(line_index, line, character_index, already_added):
    gearshifts = []
    left_character = line[character_index - 1]
    center_character  = line[character_index]
    right_character = line[character_index + 1]
    if center_character.isnumeric():
      number = center_character
      
      left_i = 2
      right_i = 2
      while True:
        if left_character.isnumeric():
          number = left_character + number
          left_character = line[character_index - left_i]
          left_i += 1
        elif right_character.isnumeric():
          number = number + right_character
          right_character = line[character_index + right_i]
          right_i += 1
        else:
          break
        
      if not (number in already_added[line_index] and character_index - left_i + 1 in already_added[line_index][number]):
        gearshifts.append(int(number))
        line_dict = already_added[line_index]
        number_set = line_dict[number] if number in line_dict else []
        number_set.append(character_index - left_i + 1)
        line_dict[number] = number_set
        already_added[line_index] = line_dict
    else:
      if left_character.isnumeric():
        gear_shift = get_number_left_side(line[:character_index])
        number = gear_shift["number"]
        index = gear_shift["index"]
        if number != "" and not (number in already_added[line_index] and index in already_added[line_index][number]):
          gearshifts.append(int(number))
          line_dict = already_added[line_index]
          number_set = line_dict[number] if number in line_dict else []
          number_set.append(index)
      if right_character.isnumeric():
        gear_shift = get_number_right_side(line[character_index + 1:])
        number = gear_shift["number"]
        index = gear_shift["index"]
        if number != "" and not (number in already_added[line_index] and index in already_added[line_index][number]):
          gearshifts.append(int(number))
          line_dict = already_added[line_index]
          number_set = line_dict[number] if number in line_dict else []
          number_set.append(index)
          line_dict[number] = number_set
          already_added[line_index] = line_dict
      
    return gearshifts
  
  with open("day3.txt", "r") as input:
    previous_line = ""
    current_line = ""
    next_line = ""
      
    debug = True
    
    line_index = 0
    for line in input:
      line = line.strip()
      already_added.append({})
      
      previous_line = current_line
      current_line = next_line
      next_line = line
        
      character_index = 0
      for symbol in current_line:
        # Find only the symbols
        if symbol != "." and not symbol.isnumeric():
          # Look for any numbers within range
          top_section = previous_line[character_index - 1:character_index + 2]
          middle_section = current_line[character_index - 1:character_index + 2]
          bottom_section = next_line[character_index - 1:character_index + 2]
          all_gearshifts = []
          
          if debug and (is_numeric(top_section) or is_numeric(middle_section) or is_numeric(bottom_section)):
            print(top_section)
            print(middle_section)
            print(bottom_section)
          
          # Find the numbers
          if is_numeric(top_section):
            gearshifts = get_gearshifts(line_index - 2, previous_line, character_index, already_added)
            all_gearshifts += gearshifts
            gearshift_sum += sum(gearshifts)
            if debug:
              print("Added", gearshifts, "from top")
          if is_numeric(middle_section):
            gearshifts = get_gearshifts(line_index - 1, current_line, character_index, already_added)
            all_gearshifts += gearshifts
            gearshift_sum += sum(gearshifts)
            if debug:
              print("Added", gearshifts, "from middle")
          if is_numeric(bottom_section):
            gearshifts = get_gearshifts(line_index, next_line, character_index, already_added)
            all_gearshifts += gearshifts
            gearshift_sum += sum(gearshifts)
            if debug:
              print("Added", gearshifts, "from bottom")
          
          if symbol == "*" and len(all_gearshifts) == 2:
            gearratio_sum += all_gearshifts[0] * all_gearshifts[1]
            if debug:
              print("Added gear ratio", all_gearshifts[0] * all_gearshifts[1])

          if debug and (is_numeric(top_section) or is_numeric(middle_section) or is_numeric(bottom_section)):
            print()
        character_index += 1
      line_index += 1
      
    print("Gearshift Sum:", gearshift_sum)
    print("Gearratio Sum:", gearratio_sum)
    
def day4():
  final_answer = 0
  part_2 = 0
  cards = {}
  with open("day4.txt", "r") as input:
    i = 0
    for line in input:
      line = line.strip()
      card = line[line.index("Card ") + 5:line.index(":")].strip()
      numbers = line[line.index(":") + 1:]
      winning_numbers = numbers[:numbers.index("|")].split(" ")
      your_numbers = numbers[numbers.index("|") + 1:].split(" ")
      points = 0
      cards_won_count = int(card) + 1
      cards_won = []
      for number in your_numbers:
        if number in winning_numbers and number != "":
          points = points * 2 if points > 0 else 1
          cards_won.append(str(cards_won_count))
          cards_won_count += 1
      cards[card] = cards_won
      final_answer += points
      i += 1
      print("card", card)
      print("numbers", numbers)
      print("winning numbers", winning_numbers)
      print("your numbers", your_numbers)
      print("points", points)
      print()
      
  def get_cards_won(card):
    cards_won = []
    if not card in cards:
      print("Card", card, "not in cards")
      return cards_won
    
    for card_won in cards[card]:
      cards_won.append(card_won)
      cards_won += get_cards_won(card_won)
    return cards_won
  
  for card in cards:
    print(card)
    part_2 += 1
    part_2 += len(get_cards_won(card))

  print("Final Answer:", final_answer)
  print("Part 2:", part_2)
            
day4()