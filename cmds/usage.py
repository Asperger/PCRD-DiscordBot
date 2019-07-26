class usage:
    def __init__(self):
        self.usage = 'usage'
    def run(self, *param):
        return self.usage

if __name__ == '__main__':
    print(usage().run())