from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

# Game Setup
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)

# Create Game Objects
r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

# Controls
screen.listen()
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")
screen.onkey(l_paddle.go_up, "w")
screen.onkey(l_paddle.go_down, "s")

# Game Loop
game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(ball.move_speed)  # Controls ball speed
    ball.move()

    # Detect collision with top and bottom walls
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Detect collision with paddles
    if (ball.distance(r_paddle) < 50 and ball.xcor() > 320) or (ball.distance(l_paddle) < 50 and ball.xcor() < -320):
        ball.bounce_x()

    # Right paddle misses
    if ball.xcor() > 380:
        scoreboard.l_point()
        ball.reset_position()

    # Left paddle misses
    if ball.xcor() < -380:
        scoreboard.r_point()
        ball.reset_position()

    # Check for winner (first to 5 points)
    if scoreboard.l_score >= 5:
        scoreboard.display_winner("Left Player Wins!")
        game_is_on = False
    elif scoreboard.r_score >= 5:
        scoreboard.display_winner("Right Player Wins!")
        game_is_on = False

screen.exitonclick()
