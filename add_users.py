#!/bin/python3.9
import sys
import subprocess as sp
import random as rand


VALID_GROUPS = ["pubsafety", "office"]
VALID_DEPTS = ["security", "ceo", "office"]

# processes the input csv file
# returns a list of dicts with the user info in each
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

# returns true if a string has numbers in it
def has_nums(string: str):
    for i in string:
        if str.isdigit(i):
            return True
    return False

# returns true if a string is only numbers
def only_nums(string: str):
    for i in string:
        if not str.isdigit(i):
            return False
    return True

# returns the string with al non alphanumeric chars removed
def rem_not_alnum(string: str):
    ret = ""
    for c in string:
        ret += "" if not str.isalnum(c) else c
    return ret

# adds the given user to the system
# returns how many issues were detected
def add_user(user: dict):
    print(f"\nProcessing ID {user['id']}")
    issues = []
    
    # checks    
    # id
    if not user["id"]:
        issues.append("No ID provided")
    else:
        if not only_nums(user["id"]):
            issues.append("ID does not contain only numbers")
    
    # names
    if not user["first_name"]:
        issues.append("Missing first name")
    else:
        if has_nums(user["first_name"]):
            issues.append("First name contains numbers")
    
    if not user["last_name"]:
        issues.append("Missing last name")
    else:
        if has_nums(user["last_name"]):
            issues.append("Last name contains numbers")
    
    # office not needed
    # if not user["office"]:
    #     issues.append("Missing office number")
    # else:
    #     try:
    #         int(user["office"][0:2])
    #         int(user["office"][3:])
    #         if len(user["office"]) != 7:
    #             issues.append("Office number is not in correct format")
    #         if user["office"][2] != "-":
    #             issues.append("Office format is incorrect")
    #     except:
    #         issues.append("Office number is invalid")
    
    # phone not needed
    # if not user["phone_number"]:
    #     issues.append("Missing phone number")
    # else:
    #     try:
    #         int(user["phone_number"][0:3])
    #         int(user["phone_number"][4:])
    #         if len(user["phone_number"]) != 8:
    #             issues.append("Phone number is not of correct length")
    #         if user["phone_number"][3] != "-":
    #             issues.append("Phone number format is incorrect")
    #     except:
    #         issues.append("Phone number is invalid")
    
    # dept
    if not user["dept"]:
        issues.append("Missing department")
    else:
        if user["dept"] not in VALID_DEPTS:
            issues.append("Department name is invalid")

    # group
    if not user["group"]:
        issues.append("Missing group")
    else:
        if user["group"] not in VALID_GROUPS:
            issues.append("Group is invalid")

    # print issues and break if needed
    if len(issues) != 0:
        for issue in issues:
            print(f"\t{issue}")
        return len(issues)

    # do
    # add user flast
    uname = f"{str.lower(user['first_name'][0] + user['last_name'])}{rand.randint(0,9)}{rand.randint(0,9)}{rand.randint(0,9)}{rand.randint(0,9)}"
    uname = rem_not_alnum(uname)
    shell = "/bin/csh" if user["group"] == "office" else "/bin/bash"
    passwd = "password"
    sp.run(["sudo", "mkdir", f"/home/{user['dept']}"], check=False, stderr=sp.DEVNULL)
    sp.run(["sudo", "groupadd", f"{user['group']}"], check=False, stderr=sp.DEVNULL)
    sp.run(["sudo", "useradd", uname,
                    "-d", f"/home/{user['dept']}/{uname}",
                    "-s", shell,
                    "-g", user["group"]
                    #"-p", "changeme",
                    #"-u", user["id"]
                    ],
                    check=True)
    # set + expire passwd
    sp.run(["sudo", "passwd", uname], input=f"{passwd}\n{passwd}".encode(), check=True, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
    sp.run(["sudo", "passwd", "-e", uname], check=True, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
    print(f"\tSuccessfully added user {uname}")

    return 0
    

def main(args: list):
    if len(args) != 2:
        print("\nIncorrect usage\nTry \"add_users.py [file]\"\n")
        exit(1)
    filename = args[1]
    print(f"\nProcessing file {filename}...")
    try:
        listings = process_file(filename)
    except Exception as e:
        print(f"Error reading {filename}\n")
        print(e)
        exit(1)
    # remove header line
    listings.remove(listings[0])

    # process
    for user in listings:
        add_user(user)

    print(f"\nCompleted processing of {filename}\n")
    print("All users created have password set to \"password\" until first login, upon which they will be asked to change it")


if __name__ == "__main__":
    main(sys.argv)