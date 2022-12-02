calories = [0]

with open("input.txt") as f:
    for line in f:
        line = line.strip()
        if line == '':
            calories.append(0)
        else:
            calories[-1] += int(line)

calories.sort(reverse = True)
print("Top: ", calories[0])
print("Top 3: ", sum(calories[:3]))
