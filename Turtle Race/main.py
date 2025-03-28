from turtle import Turtle, Screen
import random

is_race_on = False
screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")

# Convert user input to lowercase to avoid case sensitivity issues
if user_bet:
    user_bet = user_bet.lower()

colors = ["red", "orange", "yellow", "green", "blue", "purple"]
y_positions = [-70, -40, -10, 20, 50, 80]
all_turtles = []

# Create 6 turtles
for turtle_index in range(6):
    new_turtle = Turtle(shape="turtle")
    new_turtle.penup()
    new_turtle.color(colors[turtle_index])
    new_turtle.goto(x=-230, y=y_positions[turtle_index])
    all_turtles.append(new_turtle)

if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 230:
            is_race_on = False
            winning_color = turtle.pencolor()

            # Create a new Turtle to display the result
            result_turtle = Turtle()
            result_turtle.hideturtle()
            result_turtle.penup()
            result_turtle.goto(-100, 0)  # Position text at center

            if winning_color == user_bet:
                result_turtle.write(f"You've won! The {winning_color} turtle is the winner! 🎉", align="center", font=("Arial", 14, "bold"))
            else:
                result_turtle.write(f"You've lost! The {winning_color} turtle is the winner. 😞", align="center", font=("Arial", 14, "bold"))

        # Make each turtle move a random amount.
        rand_distance = random.randint(0, 10)
        turtle.forward(rand_distance)

screen.exitonclick()
