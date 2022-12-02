with open("input.txt") as f:
    text = f.read().split(sep = "\n\n")
    text = [[int(item) for item in sublist.split("\n") if item != ""] for sublist in text]
    calories = sorted(map(sum, text), reverse = True)

print("Top: ", calories[0])
print("Top 3: ", sum(calories[:3]))
