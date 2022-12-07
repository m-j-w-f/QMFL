# 🍕 Quick Mensa Food Lookup

A small command line tool to look up the food of the KIT mensa.

## 🍦 Sample Output
![](/screen.png)

## 🍽️ Usage
to install the requirements run
```
pip install -r requirements.txt
```

Run main.py with different arguments
| Argument                  | Description                                                                                                     |
|---------------------------|-----------------------------------------------------------------------------------------------------------------|
| -h, --help                | show this help message and exit                                                                                 |
| -s, --side                | also display side dishes                                                                                        |
| -f, --full                | display food for the full week (overwrites -d)                                                                  |
| -d --days DAYS [DAYS ...] | days from today for which you want to display the menu today=0, tomorrow=1, ... only works for the current week |

## 🍭 Example
To display the menue of today and tomorrow
```
python3 qmfl.py -d 0 1
```
To display the the full menue with side dishes for the rest of the week
```
python3 qmfl.py -f -s
```
To get the menue of today
```
python3 qmfl.py
```