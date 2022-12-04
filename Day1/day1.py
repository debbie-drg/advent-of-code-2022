if __name__ == "__main__":
    text = open("input.txt").read().split(sep = "\n\n")
    text = [[int(item) for item in sublist.split("\n") if item != ""] for sublist in text]
    calories = sorted(map(sum, text), reverse = True)

    print("Top: ", calories[0])
    print("Top 3: ", sum(calories[:3]))
