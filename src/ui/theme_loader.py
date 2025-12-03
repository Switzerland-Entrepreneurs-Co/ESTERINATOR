class ThemeLoader:
    def load(self, theme):
        with open("src/resources/qss/base.qss") as f1, open(theme) as f2:
            return f1.read() + "\n" + f2.read()
