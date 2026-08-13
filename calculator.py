print("=== Simple Calculator ===")
print("Choose an operation:")
print("1. Add (+)")
print("2. Subtract (-)")
print("3. Multiply (*)")
print("4. Divide (/)")

operation = input("Enter operation (1/2/3/4): ")

num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

if operation == "1":
    result = num1 + num2
    print(f"{num1} + {num2} = {result}")
elif operation == "2":
    result = num1 - num2
    print(f"{num1} - {num2} = {result}")
elif operation == "3":
    result = num1 * num2
    print(f"{num1} * {num2} = {result}")
elif operation == "4":
    if num2 == 0:
        print("Error: Cannot divide by zero!")
    else:
        result = num1 / num2
        print(f"{num1} / {num2} = {result}")
else:
    print("Invalid operation!")
