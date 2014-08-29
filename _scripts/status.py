import sys

# -------------------------------------------------------------------------------
#
# Print status either to log file or to scrren
#
# -------------------------------------------------------------------------------

# Shortcut to print status along with the name of the script
def log(NAME, s):
    if isinstance(s,list) or isinstance(s,tuple):
        s = ' '.join(s)
    S = "[{}]".format(NAME) + ' ' + s
    with open('publish.log', 'a') as f:
        f.write(S+"\n")
    return

# Print important message to screen
def important(NAME, s):
    print "[{NAME}] ** IMPORTANT!\n\n{s}\n**\n".format(NAME=NAME,s=s)
    return

# Stop execution
def stop(NAME):
    important(NAME, "Stopping execution here!")
    sys.exit(0)
