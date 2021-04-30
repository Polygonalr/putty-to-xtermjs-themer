# Takes in Putty .reg theme files and convert it to xterm.js json files

import sys
import json
from os import path

putty_to_xterm_colour_mapping = {
    "Colour0": "foreground",
    "Colour2": "background",
    "Colour4": "cursorAccent",
    "Colour5": "cursor",
    "Colour6": "black",
    "Colour7": "brightBlack",
    "Colour8": "red",
    "Colour9": "brightRed",
    "Colour10": "green",
    "Colour11": "brightGreen",
    "Colour12": "yellow",
    "Colour13": "brightYellow",
    "Colour14": "blue",
    "Colour15": "brightBlue",
    "Colour16": "magenta",
    "Colour17": "brightMagenta",
    "Colour18": "cyan",
    "Colour19": "brightCyan",
    "Colour20": "white",
    "Colour21": "brightWhite"
}

if __name__ == "__main__":
    # Checking command line args and handling accordingly
    if len(sys.argv) != 3:
        print("Usage: python {} [puttyTheme.reg] [output.json]".format(path.basename(__file__)))
        sys.exit()
    try:
        f = open(sys.argv[1],"r")
    except(IOError):
        print("Error: {} does not appear to exist.".format(sys.argv[1]))
        sys.exit()

    output_dict = {
        "theme": {}
    }
    # Procesing each line within the input file
    for line in f:
        if 'Colour' not in line:
            continue
        # Split each line and strip inverted commands
        l = list(map(lambda x: x.rstrip().strip('"'), line.split('=')))
        # Now l[0] is "ColourXX" and l[1] is "RR,GG,BB"
        rgb = list(map(lambda x: int(x), l[1].split(",")))
        rgb_hex_str = "#" + "".join(list(map(lambda x: hex(x)[2:].zfill(2), rgb)))
        # rgb_hex_str is now "#xxxxx"
        mapped_colour = putty_to_xterm_colour_mapping.get(l[0])
        if mapped_colour == None:
            continue
        output_dict['theme'][putty_to_xterm_colour_mapping[l[0]]] = rgb_hex_str

    with open(sys.argv[2], 'w') as fp:
        json.dump(output_dict, fp)
        print("Converted putty theme and saved to {}".format(sys.argv[2]))
