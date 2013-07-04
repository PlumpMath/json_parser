# We need a signal
PARSING = object()


def loads(string):
    """ Just like json.loads!
    """
    ret = PARSING

    c = string[0]
    if c == "{":
        p = parse_hash()
        p.send(None)
    else:
        raise NotImplemented("You're going too fast!")

    for c in string:
        ret = p.send(c)

    if ret is PARSING:
        raise ValueError("Oops, I wasn't done but your string was.")
    return ret


def parse_hash():
    """ Generator that slowly parses a JSON hash
    """
    hsh = {}

    c = (yield PARSING)
    if c != "{":
        raise ValueError("Hashes start with {, fyi. Well, not yours.")

    c = (yield PARSING)
    if c != "}":
        raise ValueError("Sorry I only support completely useless hashes at the moment.")

    yield hsh
