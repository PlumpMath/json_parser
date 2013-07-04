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
        raise ValueError("Oops, I wasn't done but your JSON string was.")
    return ret


def parse_hash():
    """ Generator that slowly parses a JSON hash
    """
    hsh = {}

    # Eat the {
    yield PARSING

    c = (yield PARSING)
    while c != "}":
        # json keys are strings, so lets use yet another generator
        key = PARSING
        g = parse_string()
        g.send(None)
        while key is PARSING:
            # so this is fun, send a character to be parsed
            key = g.send(c)
            # and then go back to the top to get another character
            c = (yield PARSING)

        if c != ":":
            raise ValueError("Missing a colon, it looks like this: :")

        # values can be more than just strings, pretending they can't be for now
        value = PARSING
        g = parse_string()
        g.send(None)
        c = (yield PARSING)
        while value is PARSING:
            value = g.send(c)
            c = (yield PARSING)

        hsh[key] = value

    yield hsh


def parse_string():
    """ Generator that slowly parses a string
    """
    string = []  # we have to use an array because python strings are immutable
    c = (yield PARSING)
    if c != '"':
        raise ValueError("String start with double quotes, none of this single-quote stuff")

    c = (yield PARSING)
    while c != '"':
        string.append(c)
        c = (yield PARSING)

    yield ''.join(string)
