import sys

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"      
    text = open(file_name).read().split(sep = "\n\n")
    text = [[int(item) for item in sublist.split("\n") if item != ""] for sublist in text]
    calories = sorted(map(sum, text), reverse = True)

    print("Top: ", calories[0])
    print("Top 3: ", sum(calories[:3]))
