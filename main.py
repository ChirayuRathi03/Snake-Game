from turtle import Turtle, Screen
import time
import random

startingPos = [(0, 0), (-20, 0), (-40, 0)]
moveDist = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0


class Snake:

    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for position in startingPos:
            self.addSegment(position)

    def addSegment(self, position):
        newSegment = Turtle("square")
        newSegment.color("green")
        newSegment.penup()
        newSegment.goto(position)
        self.segments.append(newSegment)

    def extend(self):
        self.addSegment(self.segments[-1].position())

    def move(self):
        for seg_num in range(len(self.segments) - 1, 0, -1):
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x, new_y)
        self.head.forward(moveDist)

    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)

    def reset(self):
        for segment in self.segments:
            segment.goto(10000, 10000)
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]


class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(0.5, 0.5)
        self.color("red")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        self.goto(random.randint(-250, 250), random.randint(-250, 250))


class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        with open("data.txt") as data:
            self.highscore = int(data.read())
        self.color("white")
        self.penup()
        self.goto(0, 280)
        self.updateScore()
        self.hideturtle()

    def updateScore(self):
        self.clear()
        self.write(f"Score: {self.score}\tHigh Score: {self.highscore}", align="center", font=("Arial", 10, "bold"))

    def refreshScore(self):
        self.score += 1
        self.clear()
        self.updateScore()

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("data.txt", "w") as data:
                data.write(f"{self.highscore}")
        self.score = 0
        self.updateScore()


screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

snake = Snake()
food = Food()
scoreboard = ScoreBoard()

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game = True
while game:
    screen.update()
    time.sleep(0.1)
    snake.move()

    # detect if food is eaten
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.refreshScore()

    # detect if the snake reached the wall
    if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 290 or snake.head.ycor() < -290:
        scoreboard.reset()
        snake.reset()

    # detect if the snake hit its tail
    for x in snake.segments:
        if x == snake.head:
            pass
        elif snake.head.distance(x) < 10:
            scoreboard.reset()
            snake.reset()

screen.exitonclick()