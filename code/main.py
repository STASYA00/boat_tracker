from tracker import *

if __name__ == "__main__":
    print("run")
    TrackerFactory().get(TRACKERS.MOSSE)()
    t = Tracker()