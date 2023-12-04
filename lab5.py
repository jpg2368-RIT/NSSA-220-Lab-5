#!bin/python3.9
import sys
import subprocess as sp

def process_file(filename: str) -> list:
    listings = []
    with open(filename) as file:
        for line in file:
            split = line.split(",")
            listings.append(
                {
                    "id": split[0],
                    "last_name": split[1],
                    "first_name": split[2],
                    "office": split[3],
                    "phone_number": split[4],
                    "dept": split[5],
                    "group": split[6]
                }
            )
    return listings

def main(args: list):
    if len(args > 2):
        print("Incorrect usage\nTry \"lab5.py [file]\"")
        exit(1)
    elif len(args) == 2:
        filename = args[1]
    else:
        filename = input("Filename: ")
    listings = process_file(filename)
    print(f"Processed {filename}")


if __name__ == "__main__"():
    main(sys.argv)