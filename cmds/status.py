class status:
    def __init__(self):
        self.usage = 'status usage'
    def another_func(self, *param):
        pass
    def run(self, *param):
        if not param:
            return self.usage
        return 'status first param: {0}'.format(param[0])

if __name__ == '__main__':
    print(status().run())