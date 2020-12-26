from question_model import Question
from data import question_data

question_bank = []

for q_data in question_data:
    # print(dict["text"])
    # print(dict["answer"])
    question_bank.append(Question(q_data["text"], q_data["answer"]))

# print(len(question_bank))
# print(question_bank[0].text)
# print(question_bank[0].answer)

