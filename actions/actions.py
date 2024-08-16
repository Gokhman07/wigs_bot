from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import random
from rasa_sdk.events import UserUtteranceReverted

class ActionAskPrice(Action):

    def name(self) -> Text:
        return "action_ask_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        category = tracker.get_slot('category')
        length = tracker.get_slot('length')

        price_list = {
            "Dark Brown": {
                "6": "10,000-14,000",
                "12": "16,000-20,000",
                "15": "17,000-21,000",
                "20": "18,000-22,000",
                "25": "20,000-24,000",
                "30": "22,000-26,000",
                "35": "24,000-28,000",
                "40": "26,000-30,000",
                "45": "28,000-32,000",
                "50": "30,000-34,000"
            },
            "Dark Blonde": {
                "6": "17,000-21,000",
                "12": "21,000-25,000",
                "15": "22,000-26,000",
                "20": "23,000-27,000",
                "25": "24,000-28,000",
                "30": "25,000-29,000",
                "35": "27,500-31,500",
                "40": "28,500-32,500",
                "45": "30,000-34,000",
                "50": "40,000-44,000"
            },
            "Medium": {
                "6": "17,000-21,000",
                "12": "21,000-25,000",
                "15": "22,000-26,000",
                "20": "23,000-27,000",
                "25": "24,000-28,000",
                "30": "25,000-29,000",
                "35": "27,500-31,500",
                "40": "28,500-32,500",
                "45": "30,000-34,000",
                "50": "40,000-44,000"
            },
            "Platinum": {
                "6": "17,000-21,000",
                "12": "21,000-25,000",
                "15": "22,000-26,000",
                "20": "23,000-27,000",
                "25": "24,000-28,000",
                "30": "25,000-29,000",
                "35": "27,500-31,500",
                "40": "28,500-32,500",
                "45": "30,000-34,000",
                "50": "40,000-44,000"
            }
        }

        random_phrases = [
            "Our wigs are made from extremely high quality.",
            "You will love the natural look and feel of our wigs.",
            "Our wigs are crafted to perfection.",
            "Experience the best quality with our wigs."
        ]

        if category not in price_list:
            dispatcher.utter_message(text=f"Sorry, we don't have the category '{category}'.")
            return []

        if length not in price_list[category]:
            dispatcher.utter_message(text=f"Sorry, we don't have the length {length} cm for {category}.")
            return []

        price = price_list[category][length]
        response = f"The price of {category} up to {length} cm is {price}."
        
        if random.random() < 0.3:  # 30% chance to add a random phrase
            response += f" {random.choice(random_phrases)}"
        
        dispatcher.utter_message(text=response)

        return []

class ActionAskWigTypes(Action):

    def name(self) -> Text:
        return "action_ask_wig_types"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        wig_types = ["Dark Brown", "Dark Blonde", "Medium", "Platinum"]
        response = f"We have a variety of wigs including {', '.join(wig_types)}."
        
        random_phrases = [
            "Our wigs are made from extremely high quality.",
            "You will love the natural look and feel of our wigs.",
            "Our wigs are crafted to perfection.",
            "Experience the best quality with our wigs."
        ]
        
        if random.random() < 0.3:  # 30% chance to add a random phrase
            response += f" {random.choice(random_phrases)}"
        
        dispatcher.utter_message(text=response)

        return []


class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Sorry, I didn't understand that. Can you please rephrase?")
        return [UserUtteranceReverted()]
