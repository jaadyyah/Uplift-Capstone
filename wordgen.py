#!/usr/bin/python3
import os, platform
if platform.system() == "Windows":
    python = "python"
else:
    python = "python3"
answer = input("Would you like to re-generate the babel config and .po files? (WARNING: THIS WILL WIPE TRANSLATION DATA!)\
\nEnter Y to re-generate configs or N to recompile current configs: ")
if answer == "y" or answer == "Y":
    os.system(python + " -m babel.messages.frontend extract -F babel.cfg -o messages.pot .")
    os.system(python + " -m babel.messages.frontend init -i messages.pot -d translations -l es")
    print("Please edit " + str(os.curdir) + "/translations/es/LC_MESSAGES/messages.po and run:\n")
    os.system(python + " -m babel.messages.frontend compile -d translations")
else:
    os.system(python + " -m babel.messages.frontend compile -d translations")


