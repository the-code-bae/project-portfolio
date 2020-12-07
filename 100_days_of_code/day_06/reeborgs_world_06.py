def turn_right():
    turn_left()
    turn_left()
    turn_left()

# beginner solution
while not at_goal():
    if right_is_clear():
        turn_right()
        move()
    elif front_is_clear():
        move()
    else:
        turn_left()

# return for intermediate task at day 15