if __name__ == "__main__":
    import time
    try:
        import wink
    except ImportError as e:
        import sys
        sys.path.insert(0, "..")
        import wink

    w = wink.init("../config.cfg")

    groups = w.group_list()
    
    print "Turn off the groups"
    for group in groups:
        group.activate(dict(desired_state=dict(powered=False)))
    
    time.sleep(1)
    print "Turn on the groups"
    for group in groups:
        group.activate(dict(desired_state=dict(powered=True)))
    
    time.sleep(1)
    print "Dimm the lights"
    for group in groups:
        group.activate(dict(desired_state=dict(brightness=0.01, powered=True)))
    
    time.sleep(1)
    print "Restore 100% brightness"
    for group in groups:
        group.activate(dict(desired_state=dict(brightness=1.0, powered=True)))
