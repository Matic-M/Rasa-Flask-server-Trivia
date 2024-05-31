from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ActionReverted, FollowupAction
import requests
import time

class ActionGetQuestions(Action):
    def name(self) -> Text:
        return "action_trivia"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        userAnswer = tracker.get_slot("answer")
        counter = tracker.get_slot("nr")
        
        correctAnswer = tracker.get_slot("correct_answer")
      
        if counter is not None:
            counter = int(counter)

            if counter > 0:
                if correctAnswer is not None:
                    if str(userAnswer).lower() == str(correctAnswer).lower():
                        dispatcher.utter_message(text="Correct")
                    else:
                        dispatcher.utter_message(text="Incorrect")

                difficulty = tracker.get_slot("diff")

                api = f"https://opentdb.com/api.php?amount=1&difficulty={difficulty}&type=boolean"
                response = requests.get(api)
                data = response.json()

                if data.get('response_code') == 0:
                    question = data["results"][0]["question"]
                    correctAnswer = data["results"][0]["correct_answer"]
                    dispatcher.utter_message(text=question, buttons=[
                        {"payload": "/affirm", "title": "true"},
                        {"payload": "/deny", "title": "false"},
                    ])

                    counter -= 1
                    time.sleep(5)
                    return [SlotSet("answer", userAnswer), SlotSet("nr", counter), SlotSet("correct_answer", correctAnswer)]

            if counter == 0:

                if str(userAnswer).lower() == str(correctAnswer).lower():
                    dispatcher.utter_message(text="Correct")
                else:
                    dispatcher.utter_message(text="Incorrect")

                dispatcher.utter_message(text="You completed all questions :)")
                return []

        return []


