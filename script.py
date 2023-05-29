import sys
import random

image_path = sys.argv[1]

def main():
    message = "Anime!"
    randomVal = random.randint(1,3)
    if randomVal == 1:
        message = "Anime!"
    elif randomVal == 2:
        message = "Funko!"
    else:
        message = "Real!"
    return message

if __name__ == "__main__":
    print(main())