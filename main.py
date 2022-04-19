from Events import make_events
from Contests import get_contests
from Colors import bcolors

def main():
    
    # get contests from the APIs
    contests = get_contests()
    
    print(f'\n{bcolors.white}{len(contests)} contests fetched successfully 🔥{bcolors.reset}\n')
    
    # make events for these contests
    make_events(contests)
    print(f'\n{bcolors.magenta}Events created successfully ✨{bcolors.reset}\n')


if __name__ == '__main__':
    main()