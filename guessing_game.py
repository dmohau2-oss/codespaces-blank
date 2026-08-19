import random

print(" Welcome to the number Guessing Game!")
print(" i'm Thinking of a number between 1 and 100")

secret_number = random.randint(1, 100)
attempts = 0
guessed = False

while not guessed:
    try:
        guess = int(input("Enter your guess: "))
        
        if guess < 1 or guess > 100:
            print("Please enter a number between 1 and 100!")
            continue
        
        attempts += 1
        
        if guess == secret_number:
            guessed = True
            print(f"🎉 Correct! You guessed the number in {attempts} attempts!")
        elif guess < secret_number:
            print("Too low! Try again.")
        else:
            print("Too high! Try again.")
    
    except ValueError:
        print("Please enter a valid number!")

print(f"The number was: {secret_number}")
