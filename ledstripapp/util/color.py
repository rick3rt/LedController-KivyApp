
def hsv2rgb(hsv):
    """
    Convert hsv to rgb colorspace.
    """
    H = hsv[0] % 360  # hue, between 0 and 360
    S = hsv[1]  # saturation, between 0 and 1
    V = hsv[2]  # value, between 0 and 1
    C = V * S
    X = C * (1 - abs((H / 60) % 2 - 1))
    m = V - C
    if H >= 0 and H < 60:
        Rp, Gp, Bp = C, X, 0
    elif H >= 60 and H < 120:
        Rp, Gp, Bp = X, C, 0
    elif H >= 120 and H < 180:
        Rp, Gp, Bp = 0, C, X
    elif H >= 180 and H < 240:
        Rp, Gp, Bp = 0, X, C
    elif H >= 240 and H < 300:
        Rp, Gp, Bp = X, 0, C
    elif H >= 300 and H < 360:
        Rp, Gp, Bp = C, 0, X

    # rgb values between 0 and 1 in kivy
    R = (Rp + m)  # * 255
    G = (Gp + m)  # * 255
    B = (Bp + m)  # * 255
    return (R, G, B)


def hsv2rgba(hsv):
    """
    Convert hsv to rgba colorspace.
    Sets alpha value to 1.
    """
    return hsv2rgb(hsv) + (1,)
