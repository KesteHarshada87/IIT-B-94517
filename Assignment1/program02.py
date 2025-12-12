numbers = input("Enter numbers (comma-separated): ")

# convert to list of integers
nums = numbers.split(",")
nums = [int(n.strip()) for n in nums]

even_count = 0
odd_count = 0

for n in nums:
    if n % 2 == 0:
        even_count += 1
    else:
        odd_count += 1

print("Even numbers:", even_count)
print("Odd numbers:", odd_count)
