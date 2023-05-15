import sqlite3
import random
import sys
import os

def main():
    init_database()
    main_menu(force=True)
    return

def main_menu(force=False):
    if not force:
        os.system("pause")
    menu = fetch_menu()
    user_input = input("""
~~~ Foodbot 1.0: ~~~
What would you like to do?
1.Input recipe
2.Generate Menu
3.Generate Shopping List
4.View Current Menu
Q.Quit

Selection:  """)

    if user_input == "1":
        input_recipe()
    elif user_input == "2":
        generate_menu()
    elif user_input == "3":
        generate_shopping_list()
    elif user_input == "4":
        view_menu()
    elif user_input in ["Q", "q"]:
        sys.exit("Goodbye! \n")
    else:
        print("Input not recognized.")

    main_menu()

    return



def input_recipe():
    new_recipe = []
    new_recipe.append(str(input("Recipe name: ")))
    new_recipe.append(str(input("Ingredients: ")))
    new_recipe.append(float(input("Prep time: ")))
    new_recipe.append(float(input("Rating: ")))
    con = connect_database()
    cur = con.cursor()
    cur.execute("INSERT INTO recipes VALUES (?,?,?,?)", new_recipe)
    con.commit()
    con.close()

    return

def generate_menu():
    con = connect_database()
    cur = con.cursor()
    cur.execute("SELECT name FROM recipes")
    recipe_names = cur.fetchall()
    days = int(input("How many days of meals do you want? "))
    if days <= len(recipe_names):
        menu = random.sample(recipe_names,days)
        cur.execute("DELETE FROM menu")
        cur.executemany("INSERT INTO menu VALUES (?)", (menu))
        con.commit()
        view_menu()
    else:
        print("You don't have enough recipes for that.")
        generate_menu()
    con.close()
    return

def fetch_menu():
    con = connect_database()
    cur = con.cursor()
    cur.execute("SELECT * FROM menu")
    menu = cur.fetchall()
    con.close()
    return menu

def view_menu():
    print("""
~~~Current Menu~~~""")
    menu = fetch_menu()
    if menu:
        for item in menu:
            print(item[0])
    else:
        print("Menu is currently empty")
    print("")
    return

def generate_shopping_list():
    print("Coming Soon: Lists")
    return

def init_database():
    try:
        #Try to connect to the existing file to see if it exits
        con = connect_database()
    except:
        #If the database doesn't exist, create it and set it up.
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute("""CREATE TABLE recipes (
            name text,
            ingredients text,
            prep_time integer,
            rating integer)""")
        cur.execute("CREATE TABLE menu (menu text)")
        con.commit()
        print("Created New Database")
    con.close()
    return

def connect_database():
    con = sqlite3.connect("file:database.db?mode=rw", uri=True)
    return con

if __name__ == "__main__":
    main()
