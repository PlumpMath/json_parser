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


def get_generator(c):
    """ Decides what generator to get, primes it, and returns it
    """
    if c == "{":
        g = parse_hash()
        g.send(None)
        return g
    if c == '"':
        g = parse_string()
        g.send(None)
        return g
    if c.isdigit():
        g = parse_int()
        g.send(None)
        return g
    raise ValueError("Unknown character alert: " + c)


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

        # values can be more than just strings...
        value = PARSING
        c = (yield PARSING)
        g = get_generator(c)
        while 1:
            value = g.send(c)
            if value is not PARSING:
                break
            c = (yield PARSING)

        hsh[key] = value
        # We have a dangling quote, nothing to do but eat it
        if c == '"':
            c = (yield PARSING)

    yield hsh


def parse_string():
    """ Generator that slowly parses a string
    """
    string = []  # we have to use an array because python strings are immutable

    yield PARSING  # eat the ", execution can't get in here without one
    c = (yield PARSING)
    while c != '"':
        string.append(c)
        c = (yield PARSING)

    yield ''.join(string)


def parse_int():
    """ Generator that slowly parses an integer
    """
    integer = []
    c = (yield PARSING)
    while c not in [',', '}']:
        integer.append(c)
        c = (yield PARSING)

    yield int(''.join(integer))