class ThemeLoader:
    def load(self, theme):
        with open(theme) as f2:
            return f2.read()
