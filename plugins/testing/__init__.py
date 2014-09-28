from irc.events import BindEvent, fireEvent

@BindEvent("privmsg")
def testing(sender=None, target=None, message=None, *, event=None):
    print(target, sender, message)