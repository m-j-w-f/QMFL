import argparse
import bs4
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from halo import Halo
import os
import random
import requests


class color:
   BOLD = '\033[1m'
   END = '\033[0m'


def emojify(food:str) -> str:
    emj_dict = {
        "apfel":"🍎",
        "baguette":"🥖",
        "birne":"🍐",
        "brot":"🥖",
        "burger":"🍔",
        "creme":"🍨",
        "dessert":"🍦",
        "duftreis":"🍚",
        "fisch":"🐠",
        "fleisch":"🍖",
        "frites":"🍟",
        "geflügel":"🐓",
        "gemüse":"🥦",
        "gnocchi":"🥣",
        "gurke":"🥒",
        "hähn":"🐓",
        "hühn":"🐓",
        "kabeljau":"🐟",
        "karotte":"🥕",
        "kartoffel":"🥔",
        "käse":"🧀",
        "keule":"🍗",
        "lachs":"🐟",
        "mais":"🌽",
        "nudel":"🍝",
        "obst":"🍏",
        "pasta":"🍝",
        "pfanne":"🥘",
        "pizza":"🍕",
        "pommes":"🍟",
        "rind":"🥩",
        "salat":"🥗",
        "schinken":"🥓",
        "schwein":"🐖",
        "solidaritätsessen":"😀",
        "spätausgabe":"🌚",
        "steak":"🥩",
        "suppe":"🍜",
        "tomate":"🍅",
        "wurst":"🌭"
        }
    
    substrings = [substring for substring in emj_dict.keys() if substring in food.lower()]
    if substrings:
        emj_list = [emj_dict[sub] for sub in substrings]
        food = random.choice(emj_list) + food 
    else:
        food = "🍴" + food
    return food


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="qmfl",
                                     description="Quick Mensa Food Lookup")

    # Add arguments to the parser
    parser.add_argument("-s", "--side", action="store_true", help="also display side dishes")
    parser.add_argument("-f", "--full", action="store_true", help="display food for the full week (overwrites -d)")
    parser.add_argument("-d", "--days", nargs="+", type=int, help="days from today for which you want to display the menu\ntoday=0, tomorrow=1, ...\nonly works for the current week")

    # Parse the command line arguments
    args = parser.parse_args()

    # Return the parsed arguments
    return args


def pretty_print(name:str, dishes:list[str], prices:list[str], date:datetime, args:argparse.Namespace):
    if (datetime.today() - date).days == 0:
        date_formated = "Heute"
    elif (datetime.today() + timedelta(days=1) - date).days == 0:
        date_formated = "Morgen"
    else: 
        date_formated = date.strftime("%-d. %B")
    
    i = 5 + (date - datetime.today()).days
    if i >= 7:
        i -= 6 
    day_color = f"\33[3{i}m"

    print(color.BOLD + day_color + name + " (" + date_formated + ")" + color.END)
    
    if not (len(dishes) == len(prices)):
        raise Exception
    if not dishes or not prices:
        print("❌No Food available\n")
        return
    if args.side == False:
        food_dict = {dishes[0]:prices[0]}
    else:
        food_dict = dict(zip(dishes,prices))
    for food, price in food_dict.items():
        size = os.get_terminal_size().columns - 15
        text = f"{{:<{size}}}  {{:>6}}"
        text = text.format(emojify(food), price)
        print(text)
    print()


def print_menu(day: bs4.element.Tag, date:datetime, args: argparse.Namespace):
    lines = day.find_all(class_="mensatype_rows")
    names = [line.find(class_="mensatype").get_text(separator=" ").strip() for line in lines]
    # Split day manually since bs4 doesn't work
    day_str = str(day)
    rows = day_str.split("<tr class=\"mensatype_rows\">")[1:]
    for row, name in zip(rows, names):
        soup = BeautifulSoup(row, "html.parser")
        dishes = soup.find_all(class_="first")
        dishes_list = [dish.find("b").text for dish in dishes]
        prices = soup.find_all(class_="price_1")
        prices_list = [price.text for price in prices]
        try:
            pretty_print(name=name, dishes=dishes_list, prices=prices_list, date=date ,args=args)
        except:
            print("❌An Error occurred")


def main():
    # Parse the command line arguments
    args = parse_args()
    # Generate Spinner
    spinner = Halo(text="Preparing Food 🍕", spinner="dots", color="magenta")
    spinner.start()
    
    URL = "https://www.sw-ka.de/de/hochschulgastronomie/speiseplan/mensa_adenauerring/"
    now = datetime.today()
    TD = timedelta(days=1)
    CALENDAR_WEEK = now.isocalendar()[1]
    PARAMS = {"kw":CALENDAR_WEEK}
    
    try:
        # Add kw argument and get HTML
        html = requests.get(URL, params=PARAMS).content
    except:
        spinner.fail("Couldn't reach https://sq-ka.de")
        quit(1)
    
    soup = BeautifulSoup(html, "html.parser")
    
    try:
        canteen_days = soup.find_all("div", class_="canteen-day")
    except:
        spinner.fail("A BeautifulSoup🍜 exception occured")
        quit(1)
    
    spinner.stop()
    
    # fullweek
    if args.full == True:
        for day in canteen_days:
            print_menu(day=day, date=now, args=args)
            now = now + TD
    # seleced days        
    elif args.days:
        for i, day in enumerate(canteen_days):
            if i in args.days:
                print_menu(day=day, date=now, args=args)
            now = now + TD
    # only today
    else:
        print_menu(day=canteen_days[0],date=now, args=args)
    
if __name__ == "__main__":
    main()