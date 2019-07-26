class fill:
    def __init__(self):
        self.usage = 'fill usage'
    def run(self, *param):
        if not param:
            return self.usage
        return 'fill first param: {0}'.format(param[0])

if __name__ == '__main__':
    print(fill().run())