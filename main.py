from Events import make_events
from Contests import get_contests

#Colors to use
red = '\033[38;5;196m'
green = '\033[38;5;40m'
blue = '\033[34m'
gold = '\033[38;5;220m'
white = '\33[37m'
magenta = '\033[35m'
bold = '\033[01m'
reset = '\033[0m'

def main():
    
    # get contests from the APIs
    contests = get_contests()
    
    print(f'\n{white}{len(contests)} contests fetched successfully 🔥{reset}\n')
    
    # make events for these contests
    make_events(contests)
    print(f'\n{magenta}Events created successfully ✨{reset}\n')


if __name__ == '__main__':
    main()