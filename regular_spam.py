from pyautogui import typewrite
from time import sleep
from datetime import datetime

#Variables
msg = input("Enter the message: ")
delay = float(input("How much delay do you want between messages? "))



def format_time():
    """
    Returns the current date as a string with te chosen digits
    """
    t = datetime.now()
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return "date: " + s[5:-7] + "-> "

def regular_spam(msg, delay):
    """
    Automates de keyboard presses of the current value followed by the inputed 
    msg value and also sets a delay between consequent message
    """
    # typewrite(format_time() + msg + '\n')
    typewrite(msg + '\n')                    #uncomment if you want the spam message without date and time
    sleep(delay)



choice= input("Do you want a regular spam, infinite spam or instant spam waiting times?[regular, infinite or instant]")


if choice.lower() == "instant":
    n = int(input("How many times do you want the message to repeat?: "))
    sleep(5)
    for i in range(0, n):
        for k in range(9):
            regular_spam(msg, delay)
        sleep(5)               
    
    
if choice.lower() == "regular":
    n = int(input("How many times do you want the message to repeat?: ")) 
    sleep(5)
    for i in range(0, n):
        regular_spam(msg, delay)
        
        
if choice.lower() == "infinite":
    sleep(5)
    while True:
        regular_spam(msg, delay)
