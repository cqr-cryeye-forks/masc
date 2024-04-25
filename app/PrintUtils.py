from termcolor import colored

from app.Constants import result_dict

"""
Some utility methods to print information on the screen
"""


def print_green(message, extra=None):
    if extra == "":
        print(colored(message, "green"), end="")
    else:
        print(colored(message, "green"))


def print_red(message, extra=None):
    if extra == "":
        print(colored(message, "red"), end="")
    else:
        print(colored(message, "red"))


def print_blue(message, extra=None):
    if extra == "":
        print(colored(message, "blue"), end="")
    else:
        print(colored(message, "blue"))


def print_yellow(message, extra=None):
    if extra == "":
        print(colored(message, "yellow"), end="")
    else:
        print(colored(message, "yellow"))


def print_debug(message, extra=None):
    if extra == "":
        print(colored("[DEBUG] " + message, "yellow"), end="")
    else:
        print(colored("[DEBUG] " + message, "yellow"))


def print_results(results):
    if len(results) == 0:
        print_green("Congratulations! No malware were found")
        result_dict["message"] = "Congratulations! No malware were found"
    else:
        print_red("Malware were found. Listing files . . .")
        result_dict["message"] = "Malware were found."

        if 'paths' not in result_dict:
            result_dict["paths"] = []

        for result in results:
            print("\t" + result["entry"].path + ": " + result["details"])
            result_dict["paths"].append({"path": result["entry"].path + ": " + result["details"]})


def print_info():
    print("\nmasc 0.2.2 (http://github.com/sfaci/masc)")
