sentence = input("Enter a sentence: ")

# number of characters
num_chars = len(sentence)

# number of words
words = sentence.split()
num_words = len(words)

# number of vowels
vowels = "aeiouAEIOU"
num_vowels = 0

for ch in sentence:
    if ch in vowels:
        num_vowels += 1

print("Number of characters:", num_chars)
print("Number of words:", num_words)
print("Number of vowels:", num_vowels)
