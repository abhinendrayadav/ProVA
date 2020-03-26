# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ReminderScheduled
from datetime import datetime, timedelta
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="root")
mycursor = mydb.cursor()
mycursor.execute("use prova")


class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_template("utter_non_happy", tracker)

        return []
   
class ActionReminder(Action):
    def name(self) -> Text:
        return "action_reminder"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("actoin triggered")

        return[]

class ActionSendEmail(Action):
    
    def name(self) -> Text:
        return "action_send_it_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) ->List[Dict[Text,Any]]:

            input = tracker.latest_message.get('text')
            msg = input.replace(" ", "%20")

            dispatcher.utter_message("<a href=mailto:ithelpdesk@prolifics.com?subject={}&body=Hi,%20{}>Send Mail</a>".format(msg,msg))

            return[]
    

class ActionAccountLock(Action):
    
    def name(self) -> Text:
        return "action_acc_lock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) ->List[Dict[Text,Any]]:

            mycursor.execute("select enum from prova where code='E1'")
            result = mycursor.fetchone()
            for i in result:
                enum = i
            sen = enum.replace(" ", "%20")
            dispatcher.utter_message("<a href=mailto:ProU@prolifics.com?subject=LMS%20Account%20Lock&body={}>Send Mail</a>".format(sen))
            # class ReminderScheduled(action_name, trigger_date_time, name=None, kill_on_user_message=True, timestamp=None)
            
            return[ReminderScheduled("action_reminder", datetime.now() + timedelta(seconds=20), kill_on_user_message=False)]

class ActionStatus(Action):
    
    def name(self) -> Text:
        return "action_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) ->List[Dict[Text,Any]]:

            mycursor.execute("select enum from prova where code='E2'")
            result = mycursor.fetchone()
            for i in result:
                enum = i
            sen = enum.replace(" ", "%20")

            dispatcher.utter_message("<a href=mailto:ProU@prolifics.com?subject=Pending%20Courses&body={}>Send Mail</a>".format(sen))

            return[]


class ActionThinkHR(Action):
    
    def name(self) -> Text:
        return "action_thinkhr"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) ->List[Dict[Text,Any]]:

            dispatcher.utter_message("<a href=mailto:ProU@prolifics.com?subject=ThinkHR%20Courses>Send Mail</a>")

            return[]

class ActionExtTraining(Action):
    
    def name(self) -> Text:
        return "action_ext_trainings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) ->List[Dict[Text,Any]]:

            dispatcher.utter_message("<a href=mailto:ProU@prolifics.com?subject=External%20Trainings>Send Mail</a>")

            return[]