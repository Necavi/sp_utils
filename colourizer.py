import re

from colors import Color

colours = {
    "aliceblue": Color(240, 248, 255),
    "allies": Color(77, 121, 66),
    "ancient": Color(235, 75, 75),
    "antiquewhite": Color(250, 235, 215),
    "aqua": Color(0, 255, 255),
    "aquamarine": Color(127, 255, 212),
    "arcana": Color(173, 229, 92),
    "axis": Color(255, 64, 64),
    "azure": Color(0, 127, 255),
    "beige": Color(245, 245, 220),
    "bisque": Color(255, 228, 196),
    "black": Color(0, 0, 0),
    "blanchedalmond": Color(255, 235, 205),
    "blue": Color(153, 204, 255),
    "blueviolet": Color(138, 43, 226),
    "brown": Color(165, 42, 42),
    "burlywood": Color(222, 184, 135),
    "cadetblue": Color(95, 158, 160),
    "chartreuse": Color(127, 255, 0),
    "chocolate": Color(210, 105, 30),
    "collectors": Color(170, 0, 0),
    "common": Color(176, 195, 217),
    "community": Color(112, 176, 74),
    "coral": Color(255, 127, 80),
    "cornflowerblue": Color(100, 149, 237),
    "cornsilk": Color(255, 248, 220),
    "corrupted": Color(163, 44, 46),
    "crimson": Color(220, 20, 60),
    "cyan": Color(0, 255, 255),
    "darkblue": Color(0, 0, 139),
    "darkcyan": Color(0, 139, 139),
    "darkgoldenrod": Color(184, 134, 11),
    "darkgray": Color(169, 169, 169),
    "darkgrey": Color(169, 169, 169),
    "darkgreen": Color(0, 100, 0),
    "darkkhaki": Color(189, 183, 107),
    "darkmagenta": Color(139, 0, 139),
    "darkolivegreen": Color(85, 107, 47),
    "darkorange": Color(255, 140, 0),
    "darkorchid": Color(153, 50, 204),
    "darkred": Color(139, 0, 0),
    "darksalmon": Color(233, 150, 122),
    "darkseagreen": Color(143, 188, 143),
    "darkslateblue": Color(72, 61, 139),
    "darkslategray": Color(47, 79, 79),
    "darkslategrey": Color(47, 79, 79),
    "darkturquoise": Color(0, 206, 209),
    "darkviolet": Color(148, 0, 211),
    "deeppink": Color(255, 20, 147),
    "deepskyblue": Color(0, 191, 255),
    "dimgray": Color(105, 105, 105),
    "dimgrey": Color(105, 105, 105),
    "dodgerblue": Color(30, 144, 255),
    "exalted": Color(204, 204, 205),
    "firebrick": Color(178, 34, 34),
    "floralwhite": Color(255, 250, 240),
    "forestgreen": Color(34, 139, 34),
    "frozen": Color(73, 131, 179),
    "fuchsia": Color(255, 0, 255),
    "fullblue": Color(0, 0, 255),
    "fullred": Color(255, 0, 0),
    "gainsboro": Color(220, 220, 220),
    "genuine": Color(77, 116, 85),
    "ghostwhite": Color(248, 248, 255),
    "gold": Color(255, 215, 0),
    "goldenrod": Color(218, 165, 32),
    "gray": Color(204, 204, 204),
    "grey": Color(204, 204, 204),
    "green": Color(62, 255, 62),
    "greenyellow": Color(173, 255, 47),
    "haunted": Color(56, 243, 171),
    "honeydew": Color(240, 255, 240),
    "hotpink": Color(255, 105, 180),
    "immortal": Color(228, 174, 51),
    "indianred": Color(205, 92, 92),
    "indigo": Color(75, 0, 130),
    "ivory": Color(255, 255, 240),
    "khaki": Color(240, 230, 140),
    "lavender": Color(230, 230, 250),
    "lavenderblush": Color(255, 240, 245),
    "lawngreen": Color(124, 252, 0),
    "legendary": Color(211, 44, 230),
    "lemonchiffon": Color(255, 250, 205),
    "lightblue": Color(173, 216, 230),
    "lightcoral": Color(240, 128, 128),
    "lightcyan": Color(224, 255, 255),
    "lightgoldenrodyellow": Color(250, 250, 210),
    "lightgray": Color(211, 211, 211),
    "lightgrey": Color(211, 211, 211),
    "lightgreen": Color(153, 255, 153),
    "lightpink": Color(255, 182, 193),
    "lightsalmon": Color(255, 160, 122),
    "lightseagreen": Color(32, 178, 170),
    "lightskyblue": Color(135, 206, 250),
    "lightslategray": Color(119, 136, 153),
    "lightslategrey": Color(119, 136, 153),
    "lightsteelblue": Color(176, 196, 222),
    "lightyellow": Color(255, 255, 224),
    "lime": Color(0, 255, 0),
    "limegreen": Color(50, 205, 50),
    "linen": Color(250, 240, 230),
    "magenta": Color(255, 0, 255),
    "maroon": Color(128, 0, 0),
    "mediumaquamarine": Color(102, 205, 170),
    "mediumblue": Color(0, 0, 205),
    "mediumorchid": Color(186, 85, 211),
    "mediumpurple": Color(147, 112, 216),
    "mediumseagreen": Color(60, 179, 113),
    "mediumslateblue": Color(123, 104, 238),
    "mediumspringgreen": Color(0, 250, 154),
    "mediumturquoise": Color(72, 209, 204),
    "mediumvioletred": Color(199, 21, 133),
    "midnightblue": Color(25, 25, 112),
    "mintcream": Color(245, 255, 250),
    "mistyrose": Color(255, 228, 225),
    "moccasin": Color(255, 228, 181),
    "mythical": Color(136, 71, 255),
    "navajowhite": Color(255, 222, 173),
    "navy": Color(0, 0, 128),
    "normal": Color(178, 178, 178),
    "oldlace": Color(253, 245, 230),
    "olive": Color(158, 195, 79),
    "olivedrab": Color(107, 142, 35),
    "orange": Color(255, 165, 0),
    "orangered": Color(255, 69, 0),
    "orchid": Color(218, 112, 214),
    "palegoldenrod": Color(238, 232, 170),
    "palegreen": Color(152, 251, 152),
    "paleturquoise": Color(175, 238, 238),
    "palevioletred": Color(216, 112, 147),
    "papayawhip": Color(255, 239, 213),
    "peachpuff": Color(255, 218, 185),
    "peru": Color(205, 133, 63),
    "pink": Color(255, 192, 203),
    "plum": Color(221, 160, 221),
    "powderblue": Color(176, 224, 230),
    "purple": Color(128, 0, 128),
    "rare": Color(75, 105, 255),
    "red": Color(255, 64, 64),
    "rosybrown": Color(188, 143, 143),
    "royalblue": Color(65, 105, 225),
    "saddlebrown": Color(139, 69, 19),
    "salmon": Color(250, 128, 114),
    "sandybrown": Color(244, 164, 96),
    "seagreen": Color(46, 139, 87),
    "seashell": Color(255, 245, 238),
    "selfmade": Color(112, 176, 74),
    "sienna": Color(160, 82, 45),
    "silver": Color(192, 192, 192),
    "skyblue": Color(135, 206, 235),
    "slateblue": Color(106, 90, 205),
    "slategray": Color(112, 128, 144),
    "slategrey": Color(112, 128, 144),
    "snow": Color(255, 250, 250),
    "springgreen": Color(0, 255, 127),
    "steelblue": Color(70, 130, 180),
    "strange": Color(207, 106, 50),
    "tan": Color(210, 180, 140),
    "teal": Color(0, 128, 128),
    "thistle": Color(216, 191, 216),
    "tomato": Color(255, 99, 71),
    "turquoise": Color(64, 224, 208),
    "uncommon": Color(176, 195, 217),
    "unique": Color(255, 215, 0),
    "unusual": Color(134, 80, 172),
    "valve": Color(165, 15, 121),
    "vintage": Color(71, 98, 145),
    "violet": Color(238, 130, 238),
    "wheat": Color(245, 222, 179),
    "white": Color(255, 255, 255),
    "whitesmoke": Color(245, 245, 245),
    "yellow": Color(255, 255, 0),
    "yellowgreen": Color(154, 205, 50),
    "default": "\x01"
}

re_colourize = re.compile("c=\(([a-zA-Z]+)\)")


def replace_colour(match):
    if match.group(1) in colours:
        return str(colours[match.group(1)])
    return ""


def colourize(message):
    return re_colourize.sub(replace_colour, message)


def strip_colours(message):
    return re_colourize.sub("", message)

