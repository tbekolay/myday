class Service:
    def __init__(self, name):
        self.name = name

        self.token = None

    def save_token(self):
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, "wb") as fp:
            pickle.dump(token, fp)

    def load_token(self):
        with open(token_path, "rb") as fp:
            return pickle.load(fp)
