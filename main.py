from utils import *

if __name__ == "__main__":

    args = init_arguments()

    if not args.internet and not args.bandwidth:
        print("You have to pick at least one of those two options: internet and bandwidth")
    else:
        main_loop(ConsoleClient(), args)