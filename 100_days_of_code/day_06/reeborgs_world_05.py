def turn_right():
    turn_left()
    turn_left()
    turn_left()
    
def jump():
    if wall_in_front():
        turn_left()
    while wall_on_right():
        if not front_is_clear():
            turn_left()
        else:
            move()
    turn_right()
    move()
    turn_right()

while not at_goal():
    if front_is_clear():
        move()
    elif at_goal():
        done()
    else:
        jump()