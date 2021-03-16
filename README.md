# Pro.*V.A*.

ProVA – Prolifics Virtual Assistant sits on top of PEP portal that understands user’s natural language, sentiments and provides a one stop 
shop for day to day scenarios like ticketing across all operations, concerns. This helps various helpdesks; with less tickets since major queries are 
resolved by the assistant, employees now feel more confident about policies and know the correct hierarchy to follow for any further concerns. 

## Server Details
```
Use your favorite SSH Client to access.

IP Address: 10.11.12148  
Username: ppmuser
Password: Pro0987!

MySQL DB is residing on the same IP

-   From MySQL Workbench; Setup a new connection with connection mode:  Standard TCP/IP over SSH  
    
Username: prova_admin

Password : admin123
```
## Environment setup

-   Make sure the Microsoft VC++ Compiler is installed, so python can compile any dependencies. You can get the compiler from [Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/). Download the installer and select VC++ Build tools in the list.
    
-   Install [Python 3](https://www.python.org/downloads/windows/) (64-bit version) for Windows.
    

## Rasa Installation

-   Run below command on your favorite terminal
    

	> pip install rasa==1.5.3  

### Initialize a Rasa Project

	> rasa init

This creates the following files:
|||
|--|--|
| `__init__.py` | an empty file that helps python find your actions |
|actions.py| code for your custom actions | 
| config.yml | configuration of your NLU and Core models |
| credentials.yml | details for connecting to other services | 
|data/nlu.md | your NLU training data |
| data/stories.md | your stories|
| domain.yml | your assistant’s domain| 
| endpoints.yml | details for connecting to channels like fb messenger|
| models/`<timestamp>`.tar.gz | your initial model |

## Messaging and Voice Channels
If you just want an easy way for users to test your bot, the best option is usually the chat interface that ships with Rasa X, where you can  [invite users to test your bot](https://rasa.com/docs/rasa-x/user-guide/share-assistant/#share-your-bot).

If you already have an existing website(in our case it is PeP Portal) and want to add a Rasa assistant to it, you can use  [Chatroom](https://github.com/scalableminds/chatroom), a widget which you can incorporate into your existing webpage by adding a HTML snippet. Alternatively, you can also build your own chat widget.

> **NOTE:**  We at ProVA are using websockets messaging channel.

#### Websocket Channel

The SocketIO channel uses websockets and is real-time. To use the SocketIO channel, add the credentials to your  `credentials.yml`:
```
socketio:
	user_message_evt: user_uttered
	bot_message_evt: bot_uttered
	session_persistence: true/false
```

## Training Data Format
Markdown is the easiest Rasa NLU format for humans to read and write. Examples are listed using the unordered list syntax, e.g. minus -, asterisk *, or plus +. Examples are grouped by intent, and entities are annotated as Markdown links, e.g. [entity](entity name).
```
## intent:check_balance`
	- what is my balance < no entity >  
	- how much do I have on my `[savings](source_account)` <entity "source_account" has value "savings" >  
	- how much do I have on my `[savings account](source_account:savings)` <synonyms, method 1>  
	- Could I pay in `[yen](currency)`? < entity matched by lookup table >  

## intent:greet`
	- hey
	- hello

## synonym:savings`   <synonyms, method 2 >
	- pink pig

## regex:zipcode`
	- [0-9]{5}

## lookup:currencies`   < lookup table list >
	- Yen
	- USD
	- Euro

## lookup:additional_currencies`  < no list to specify lookup table file>
	path/to/currencies.txt
```

## Stories

Rasa stories are a form of training data used to train the Rasa’s dialogue management models.

A story is a representation of a conversation between a user and an AI assistant, converted into a specific format where user inputs are expressed as corresponding intents (and entities where necessary) while the responses of an assistant are expressed as corresponding action names.

A training example for the Rasa Core dialogue system is called a story. This is a guide to the story data format.

#### Format
Here’s an example of a dialogue in the Rasa story format:

>`## greet + location/price + cuisine + num people`    < name of the story - just for debugging >
\* greet
	&nbsp;&nbsp;-- action_ask_howcanhelp
\* inform{"location": "rome", "price": "cheap"} < user utterance, in format intent{entities} >
  &nbsp;&nbsp; -- action_on_it
   &nbsp;&nbsp;&nbsp;-- action_ask_cuisine
\* inform{"cuisine": "spanish"}
   &nbsp;&nbsp;-- action_ask_numpeople        < action that the bot should execute >
\* inform{"people": "six"}
  &nbsp;&nbsp; -- action_ack_dosearch

## Domains

The Domain defines the universe in which your assistant operates. It specifies the intents, entities, slots, and actions your bot should know about. Optionally, it can also include templates for the things your bot can say.
#### An example of a Domain

As an example, the  `DefaultDomain`  has the following yaml definition:
```
intents:
  - greet
  - goodbye
  - affirm
  - deny
  - mood_great
  - mood_unhappy
  - bot_challenge

actions:
- utter_greet
- utter_cheer_up
- utter_did_that_help
- utter_happy
- utter_goodbye
- utter_iamabot

templates:
  utter_greet:
  - text: "Hey!  How  are  you?"

  utter_cheer_up:
  - text: "Here  is  something  to  cheer  you  up:"
    image: "https://i.imgur.com/nGF1K8f.jpg"

  utter_did_that_help:
  - text: "Did  that  help  you?"

  utter_happy:
  - text: "Great,  carry  on!"

  utter_goodbye:
  - text: "Bye"

  utter_iamabot:
  - text: "I  am  a  bot,  powered  by  Rasa."
```
## Responses


If you want your assistant to respond to user messages, you need to manage these responses. In the training data for your bot, your stories, you specify the actions your bot should execute. These actions can use utterances to send messages back to the user.

There are three ways to manage these utterances:

1.  Utterances are normally stored in your domain file

2.  Retrieval action responses are part of the training data

#### Including the utterances in the domain

The default format is to include the utterances in your domain file. This file then contains references to all your custom actions, available entities, slots and intents.
```
# all hashtags are comments :)
intents:
 - greet
 - default
 - goodbye
 - affirm
 - thank_you
 - change_bank_details
 - simple
 - hello
 - why
 - next_intent

entities:
 - name

slots:
  name:
    type: text

templates:
  utter_greet:
    - text: "hey  there  {name}!"  # {name} will be filled by slot (same name) or by custom action
  utter_channel:
    - text: "this  is  a  default  channel"
    - text: "you're  talking  to  me  on  slack!"  # if you define channel-specific utterances, the bot will pick
      channel: "slack"                        # from those when talking on that specific channel
  utter_goodbye:
    - text: "goodbye  😢"   # multiple templates - bot will randomly pick one of them
    - text: "bye  bye  😢"
  utter_default:   # utterance sent by action_default_fallback
    - text: "sorry,  I  didn't  get  that,  can  you  rephrase  it?"

actions:
  - utter_default
  - utter_greet
  - utter_goodbye
```
In this example domain file, the section  `templates`  contains the template the assistant uses to send messages to the user.

    

## Actions

Actions are the things your bot runs in response to user input. There are four kinds of actions in Rasa:

1.  Utterance actions: start with utter_ and send a specific message to the user
    

2.  Retrieval actions: start with respond_ and send a message selected by a retrieval model
    

3.  Custom actions: run arbitrary code and send any number of messages (or none).
    

4.  Default actions: e.g. action_listen, action_restart, action_default_fallback
    
**NOTE**:
>Your project’s `config.yml` file takes a policies key which you can use to customize the policies your assistant uses. 

## Fallback Policy

The `FallbackPolicy` has one fallback action, which will be executed if the intent recognition has a confidence below `nlu_threshold` or if none of the dialogue policies predict an action with confidence higher than `core_threshold`.

The thresholds and fallback action can be adjusted in the policy configuration file as parameters of the `FallbackPolicy`.
```
policies: 
- name: "FallbackPolicy"  
	nlu_threshold: 0.4 
	core_threshold: 0.3 
	fallback_action_name: "action_default_fallback"
```
`action_default_fallback` is a default action in Rasa Core which sends the `utter_default` template message to the user. Make sure to specify the `utter_default` in your domain file. It will also revert back to the state of the conversation before the user message that caused the fallback, so that it will not influence the prediction of future actions

## Tracker Stores

All conversations are stored within a tracker store. Rasa Core provides implementations for different store types out of the box. If you want to use another store, you can also build a custom tracker store by extending the `TrackerStore` class.


## Cheat Sheet

The command line interface (CLI) gives you easy-to-remember commands for common tasks.

Command | Effect
 -|-
rasa init |Creates a new project with example training data, actions, and config files.
rasa train | Trains a model using your NLU data and stories, saves trained model in `./models`.
rasa shell | Loads your trained model and lets you talk to your assistant on the command line.
rasa run | Starts a Rasa server with your trained model. See the [Running the Server](https://legacy-docs-v1.rasa.com/1.5.3/user-guide/running-the-server/#running-the-server) docs for details.
rasa run actions | Starts an action server using the Rasa SDK.
rasa visualize | Visualizes stories.
rasa x | Launch Rasa X locally.
rasa -h | Shows all available commands.
