class total:
    def __init__(self):
        self.usage = 'total usage'
    def run(self, user_id, *param):
        if not param or len(param[0]) is 0:
            return 'total'
        return self.usage

if __name__ == '__main__':
    print(total().run(123))