class Colors:
    empty = (26, 31, 40)
    one = (240, 240, 240)
    two = (225, 225, 225)
    three = (210, 210, 210)
    four = (195, 195, 195)
    five = (180, 180, 180)
    six = (165, 165, 165)
    seven = (150, 150, 150)
    white = (255, 255, 255)
    backg_color = (22, 22, 22)

    @classmethod
    def get_cell_colors(cls):
        return [cls.empty, cls.one, cls.two, cls.three, cls.four, cls.five, cls.six, cls.seven]
