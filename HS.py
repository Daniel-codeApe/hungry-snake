import turtle
import random

width = 600
height = 600
bean_size = 10
score = 0

delay = 100

can_restart = True

# get turtles and screen
screen = turtle.Screen()
screen.setup(width, height)
screen.title("Hungry Snake")
screen.bgcolor('black')
screen.tracer(0)

h_snake = turtle.Turtle('square')
h_snake.color('orange')
h_snake.penup()

bean = turtle.Turtle('circle')
bean.color('yellow')
bean.shapesize(bean_size/20)
bean.penup()

# the pen to update score
pen = turtle.Turtle()
pen.penup()
pen.hideturtle()

# the start button
start = turtle.Turtle()
start.hideturtle()

# moving to different positions
directions = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
    }

def record():
    global score
    with open('score.txt', 'a') as s:
        s.write('Score: %s \n' % (score))
        s.write('\n')
        s.close()

def random_bean_position():
    x = random.randint(-width/2+bean_size, width/2-bean_size)
    y = random.randint(-width/2+bean_size, width/2-bean_size)
    return (x, y)

def go_up():
    global snake_direction
    if snake_direction != "down":
        snake_direction = "up"

def go_down():
    global snake_direction
    if snake_direction != "up":
        snake_direction = "down"

def go_left():
    global snake_direction
    if snake_direction != "right":
        snake_direction = "left"

def go_right():
    global snake_direction
    if snake_direction != "left":
        snake_direction = "right"

def eat():
    global bean_position, score
    if get_distance(snake[-1], bean_position) < 20:
        bean_position = random_bean_position()
        bean.goto(bean_position)
        score += 1
        pen.clear()
        pen.write("Score: %s" % (score), align='left', font=("Courier", 24, "normal"))
        return True
    return False

def move():
    global snake_direction, can_restart, score

    new_part = snake[-1].copy()
    new_part[0] = snake[-1][0] + directions[snake_direction][0]
    new_part[1] = snake[-1][1] + directions[snake_direction][1]

    # new position, if touch its body, restart the game
    if new_part in snake[:-1]:
        can_restart = True
        pen.clear()
        pen.goto(0, 0)
        pen.write("Your score is %s, press R to restart" % (score), align = 'center', font = ("Courier", 12, "normal"))
        record()
    else:
        snake.append(new_part)

        # pop off old part if it didn't eat a bean
        if not eat():
            snake.pop(0)

        # check boundaries
        if snake[-1][0] > width/2:
            snake[-1][0] -= width
        elif snake[-1][0] < -width/2:
            snake[-1][0] += width
        elif snake[-1][1] > height/2:
            snake[-1][1] -= height
        elif snake[-1][1] < -height/2:
            snake[-1][1] += height

        # delete old snake
        h_snake.clearstamps()
    
        # draw new snake
        for part in snake:
            h_snake.goto(part[0], part[1])
            h_snake.stamp()

        print(snake)

        screen.update()

        turtle.ontimer(move, delay)

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return ((x1-x2) ** 2 + (y1-y2) ** 2)**0.5

def set_game():
    global bean_position, snake, snake_direction, h_snake, score, can_restart
    if can_restart == True:
        score = 0
        pen.clear()
        pen.color('white')
        pen.goto(-width/2+bean_size, height/2-bean_size*4)
        pen.write("Score: %s" % (score), align='left', font=("Courier", 24, "normal"))
        snake = [[0,0], [0, 20]]
        snake_direction = "up"
        bean_position = random_bean_position()
        bean.goto(bean_position)
        move()
        can_restart = False


screen.listen()
screen.onkey(set_game, 'r')
screen.onkey(go_up, 'Up')
screen.onkey(go_down, 'Down')
screen.onkey(go_left, 'Left')
screen.onkey(go_right, 'Right')

set_game()
turtle.done()
