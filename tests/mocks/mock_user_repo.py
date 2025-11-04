class MockUserRepo:
    def __init__(self):
        self.users = []

    async def add(self, user):
        self.users.append(user)
        return user

    async def list(self):
        return self.users
