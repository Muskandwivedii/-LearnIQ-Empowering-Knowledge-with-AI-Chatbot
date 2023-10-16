import random
import time
import webbrowser
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


class ProgrammingChatbot:
    def __init__(self):
        self.user_profile = {}
        self.quiz_questions = []
        self.load_quiz_questions()
        self.user_scores = {}
        self.twilio_account_sid = "AC6226ef0b50b7efc6271066bc97c7b884"
        self.twilio_auth_token = "3d8ffa156e6264d7357ac7d347956f35"
        self.twilio_phone_number = "+12293674506"
        self.your_phone_number = "+919301682453"
        self.game_duration = 10 

    def load_quiz_questions(self):
        try:
            with open("questions_quiz.txt", "r") as file:
                lines = file.read().split("\n")
                question = {}
                for line in lines:
                    if line.startswith("Question "):
                        if question:
                            self.quiz_questions.append(question)
                        question = {"question": line}
                    elif line.startswith("Correct Answer: "):
                        question["correct_answer"] = line.replace("Correct Answer: ", "")
                    else:
                        question.setdefault("options", []).append(line)
                if question:
                    self.quiz_questions.append(question)
        except FileNotFoundError:
            print("Quiz file not found. Please create a 'questions_quiz.txt' file.")
            exit(1)

    def run(self):
        print("Welcome to the Advanced Programming Language Learning Chatbot!")
        self.create_user_profile()
        if not self.select_skill_level():
            return

        while True:
            if self.user_profile["skill_level"].lower() == "beginner":
                self.provide_study_material()
                print("The web browser will automatically close after 10 seconds (for demo).")
                time.sleep(self.game_duration)  


                print("Time's up! Restarting the game...")
                self.create_user_profile()  
            else:
                self.start_quiz()

            restart_game = input("Do you want to play again? (yes/no): ").lower()
            if restart_game != "yes":
                break

        print(f"Thank you for using the Advanced Programming Language Learning Chatbot, {self.user_profile['name']}!")

    def create_user_profile(self):
        self.user_profile["name"] = input("Please enter your name: ")
        self.user_profile["language"] = input("Please select a programming language (Java, Python, C++, etc.): ")

    def select_skill_level(self):
        print(f"Great! You've selected {self.user_profile['language']}.")

        valid_languages = ["java", "python", "c++"]
        if self.user_profile['language'].lower() not in valid_languages:
            print("Selected language is not supported. No quiz available.")
            return False

        self.user_profile["skill_level"] = input("Are you a Beginner, Intermediate, or Advanced learner? ")
        return True

    def provide_study_material(self):
        study_materials = {
            "java": "https://www.sanfoundry.com/java-questions-answers-freshers-experienced/",
            "python": "https://www.sanfoundry.com/1000-python-questions-answers/",
            "c++": "https://www.interviewbit.com/cpp-mcq/"
        }

        language = self.user_profile["language"].lower()

        if language in study_materials:
            study_url = study_materials[language]
            print(f"Study material for {language}: {study_url}")

            webbrowser.open(study_url)
        else:
            print(f"Study material for {language} is not available.")

    def send_sms(self, message):
        client = Client(self.twilio_account_sid, self.twilio_auth_token)

        try:
            client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=self.your_phone_number
            )
            print("SMS sent successfully!")
        except TwilioRestException as e:
            print(f"Error sending SMS: {e}")


    def start_quiz(self):
        print(f"Fantastic, {self.user_profile['name']}! Let's test your knowledge in {self.user_profile['language']}.")

        if self.user_profile["skill_level"].lower() == "beginner":
            print("You are at a beginner level. Take some time to study the content.")
            self.provide_study_material()
            print("The web browser will automatically close after 10 seconds (for demo).")
            time.sleep(self.game_duration)  # Sleep for 10 seconds
            print("Web browser closed. Welcome back! Let's continue with the quiz.")
        elif self.user_profile["skill_level"].lower() == "advanced":
            print(f"You are at an advanced level. You will start the quiz now.")
        elif self.user_profile["skill_level"].lower() == "intermediate":
            print(f"You are at an intermediate level. You will start the quiz now.")

        score = 0
        num_questions = min(5, len(self.quiz_questions))

        for question in random.sample(self.quiz_questions, num_questions):
            print(question["question"])
            for idx, option in enumerate(question["options"]):
                print(f"{idx + 1}. {option}")

            while True:
                user_answer = input("Your answer (1-4): ")
                if user_answer.isdigit() and 1 <= int(user_answer) <= 4:
                    user_answer = int(user_answer)
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 4.")

            if question["options"][user_answer - 1].strip().lower() == question["correct_answer"].strip().lower():
                print("Correct!")
                score += 1
                print(score)
            else:
                print(f"Incorrect. The correct answer is: {question['correct_answer']}")

        print(f"Quiz completed. Your score: {score}/{num_questions}")

        skill_level_response = ""
        if score >= num_questions - 1:
            skill_level_response = "Congratulations! You are at an Advanced level."
        elif score >= num_questions // 2:
            skill_level_response = "Well done! You are at an Intermediate level."
        else:
            skill_level_response = "Great effort! You are at a Beginner level."

        sms_message = f"Quiz completed: Score {score}/{num_questions}. {skill_level_response}"
        self.send_sms(sms_message)

        print(skill_level_response)

if __name__ == "__main__":
    chatbot = ProgrammingChatbot()
    chatbot.run()
