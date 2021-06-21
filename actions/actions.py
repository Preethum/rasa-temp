# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType,  AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

current_command=" "

def get_latest_event(events):
    latest_actions = []
    for e in events:
        if e['event'] == 'action':
            latest_actions.append(e)

    return latest_actions[-2:][1]['name']


# show_help-------------------------------------------------

class ValidateControlForm(Action):
    def name(self) -> Text:
        return "action_help"

    current_command = "show_control"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        dispatcher.utter_message("""
        ask to show system <hostname>
        ask to show control <device>
        ask to show interface <device>
        ask to show wan <device>
        ask to ticket open <device>, <title>
        ask to help""")

        dispatcher.utter_message(
            json_message={"response": tracker.latest_message['text'],
                            # "time sent": now.strftime("%H:%M:%S"),
                            # "date sent": now.strftime("%d/%m/%Y"),
                            # "intent" : list(reversed(tracker.events))[4],
                            "intent" : "help",
                            "confidence" : tracker.latest_message['intent'].get('confidence'),
                            "servername" : tracker.get_slot("servername"),
                            "ticketname" : tracker.get_slot("ticketname")

            }
        )       
        return []

# show_control-------------------------------------------------

class ValidateControlForm(Action):
    def name(self) -> Text:
        return "user_servername_form"

    current_command = "show_control"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["servername"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        
        # All slots are filled.
       
        return [SlotSet("requested_slot", None)]

# show_interface---------------------------------------------------------------

class ValidateInterfaceForm(Action):
    def name(self) -> Text:
        return "user_servername_interface_form"
    current_command = "show_interface"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["servername"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]
        
        # All slots are filled.
        print(tracker.get_slot("servername"))
        return [SlotSet("requested_slot", None)]

# show_wan -------------------------------------------------------------------

class ValidateInterfaceForm(Action):
    def name(self) -> Text:
        return "user_servername_wan_form"

    current_command = "show_wan"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["servername"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]
        
        # All slots are filled.
        print(tracker.get_slot("servername"))
        return [SlotSet("requested_slot", None)]

# ticket_open -----------------------------------------------------------------

class ValidateInterfaceForm(Action):
    def name(self) -> Text:
        return "user_servername_ticket_form"

    current_command = "ticket_open"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["servername","ticketname"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]
        
        # All slots are filled.
        print(tracker.get_slot("servername"))
        return [SlotSet("requested_slot", None)]

# show_system -----------------------------------------------------------------

class ValidateInterfaceForm(Action):
    def name(self) -> Text:
        return "user_system_form"


    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["servername"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]
        
        # All slots are filled.
        print(tracker.get_slot("servername"))
        return [SlotSet("requested_slot", None)]

# submit_actions---------------------------------------------------------------
class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_details_thanks",
                                 servername=tracker.get_slot("servername"),
                                 ticketname=tracker.get_slot("ticketname")
                                )

        dispatcher.utter_message(
            json_message={"response": tracker.latest_message['text'],
                            # "time sent": now.strftime("%H:%M:%S"),
                            # "date sent": now.strftime("%d/%m/%Y"),
                            # "intent" : list(reversed(tracker.events))[4],
                            "intent" : get_latest_event(tracker.events),
                            "confidence" : tracker.latest_message['intent'].get('confidence'),
                            "servername" : tracker.get_slot("servername"),
                            "ticketname" : tracker.get_slot("ticketname")

            }
        )

        return[AllSlotsReset()]

    

