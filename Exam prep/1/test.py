
class StackLogin:

    def __init__(self,username, email, password):
        self.username = username
        self.email = email
        self.password = password


    def __str__(self):
        return f"Hello {self.username}!"

class UploadedQuestions(StackLogin):
    def __init__(self, question, username, email, password):
        super().__init__(username, email, password)
        self.question = question

    def __str__(self):
        return f"The user {self.username} has a question for you: {self.question}\n Please provide the answer!"


def __main__():
    print('Crate your account')
    username = input("Username:")
    email = input("Email:")
    password = input("Password:")

    user = StackLogin(username, email, password)
    print(user.__str__())

    question = input("Question:")
    user_question = UploadedQuestions(question, username, email, password)
    print(user_question)
