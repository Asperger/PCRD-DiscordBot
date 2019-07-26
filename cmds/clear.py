class clear:
    def __init__(self):
        self.usage = 'clear usage'
    def run(self, *param):
        if not param:
            return 'clear'
        return self.usage

if __name__ == '__main__':
    print(clear().run())