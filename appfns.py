###############################################################################
###############################################################################

#    #### ##     ## ########   #######  ########  ########  ######  
#     ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ## 
#     ##  #### #### ##     ## ##     ## ##     ##    ##    ##       
#     ##  ## ### ## ########  ##     ## ########     ##     ######  
#     ##  ##     ## ##        ##     ## ##   ##      ##          ## 
#     ##  ##     ## ##        ##     ## ##    ##     ##    ##    ## 
#    #### ##     ## ##         #######  ##     ##    ##     ######    

import openai
import credentials
import json

###############################################################################
###############################################################################

#     ######   ##        #######  ########     ###    ##        ######  
#    ##    ##  ##       ##     ## ##     ##   ## ##   ##       ##    ## 
#    ##        ##       ##     ## ##     ##  ##   ##  ##       ##       
#    ##   #### ##       ##     ## ########  ##     ## ##        ######  
#    ##    ##  ##       ##     ## ##     ## ######### ##             ## 
#    ##    ##  ##       ##     ## ##     ## ##     ## ##       ##    ## 
#     ######   ########  #######  ########  ##     ## ########  ######      


###############################################################################
###############################################################################

#   ######## ##    ##       ########  ########  ######   ######  ########  #### ########  ######## 
#   ##       ###   ##       ##     ## ##       ##    ## ##    ## ##     ##  ##  ##     ##    ##    
#   ##       ####  ##       ##     ## ##       ##       ##       ##     ##  ##  ##     ##    ##    
#   ######   ## ## ##       ##     ## ######    ######  ##       ########   ##  ########     ##    
#   ##       ##  ####       ##     ## ##             ## ##       ##   ##    ##  ##           ##    
#   ##       ##   ###       ##     ## ##       ##    ## ##    ## ##    ##   ##  ##           ##    
#   ##       ##    ##       ########  ########  ######   ######  ##     ## #### ##           ##    



functionDescriptions = [
    {
        "name": "getlocation",
        "description": "Get the city and country of a location",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city, eg 'Chicago'"

                },
                "country": {
                    "type": "string",
                    "description": "The name of the country, eg 'USA'"
                }
            },
            "required": ["city", "country"],
        },

        "name": "getauthor",
        "description": "Get the author of the story being described",
        "parameters": {
            "type": "object",
            "properties": {
                "story": {
                    "type": "string",
                    "description": "The name of the story, eg 'The Thing'"
                },
                "author": {
                    "type": "string",
                    "description": "The name of the author, eg 'John Carpenter'"
                }
            },
            "required": ["story", "author"]
        },

        "name": "getdx",
        "description": "Create a list of icd-10 codes for a given diagnosis based on the patient's symptoms and history",
        "parameters": {
            "type": "object",
            "properties": {
                "icd10": {
                    "type": "string",
                    "description": "A list of semi-colon separated icd-10 codes for the diagnosis, eg 'J45.909','R07.9'"
                },
                "diagnosis": {
                    "type": "string",
                    "description": "A list of semi-colon sepatated diagnosis that matches the icd-10 codes, eg 'Asthma'"
                }
            },
            "required": ["icd10", "diagnosis"]
        }

    }
]

matchcommandsysrole = """
    Your job is to determine the appropriate function to call based on the user's input.

    You are trying to identify if the request is a command. The following commands are valid and are defined as:
    !help     = the user is specifically asking for a list of available commands that the system recognizes
    !ping     = confirm the server is running and responding to requests
    !info     = the user is asking for information which can be used to debug the system
    !reset    = the user wishes to reset the message array of the bot and start a new discussion
    !models   = the user is asking for a list of available large-language-models that the system can use
    !topic    = the channel has a topic. list or modify the channel topic
    !persona  = show the current bot persona and list available personality choices
    !again    = show the last response from the LLM
    !examples = the is requesting that the bot show some examples of how to use commands
    !news     = search the web for news headlines for the string that follows the request for news
    !web      = search the web for the string that follows the request for web search
    !image    = create an image from the string that follows the request for image search
    !embed    = does the content contiain an embedded or attached file
    !url      = does the content contain a URL? meaning it starts with http:// or https://
    !barada   = klaatu barada nikto

    If the user's input does not equate to any of the predefined commands, you should return a value of 'no match'
    Only return the specific name of the command including the ! character. 
    """

    # The return value should be a key:value pair where the key is the name of the command and the value is the command itself.

trimcommandsysrole = """
    Your job is to identify the words that identify the command that the user is trying to execute and return only those words. The matched words must be verbatim so that I can remove them from the original string.

    For example if the user types: change the topic to persona=default
    and this matches the command !topic, then you should return the words "change the topic" to so that I can remove it from the original string and pass the remaining text to the command processor.

    Only return the words that match the command.
    """

###############################################################################
###############################################################################

#      ###    ####       ######## ##     ## ##    ##  ######  ######## ####  #######  ##    ##  ######  
#     ## ##    ##        ##       ##     ## ###   ## ##    ##    ##     ##  ##     ## ###   ## ##    ## 
#    ##   ##   ##        ##       ##     ## ####  ## ##          ##     ##  ##     ## ####  ## ##       
#   ##     ##  ##        ######   ##     ## ## ## ## ##          ##     ##  ##     ## ## ## ##  ######  
#   #########  ##        ##       ##     ## ##  #### ##          ##     ##  ##     ## ##  ####       ## 
#   ##     ##  ##        ##       ##     ## ##   ### ##    ##    ##     ##  ##     ## ##   ### ##    ## 
#   ##     ## ####       ##        #######  ##    ##  ######     ##    ####  #######  ##    ##  ######  



###############################################################################
def getCommand(usrmsg):
    
    toolmodel = "gpt-3.5-turbo"

    sysrole = "Your job is to determine the appropriate function to call based on the user's input."
    msgarr   = [{"role": "system", "content": sysrole}]

    oai = openai.OpenAI()
    response = oai.chat.completions.create(model=toolmodel,
        messages  = msgarr,
        functions = functionDescriptions,
        function_call = "auto"
)
    
###############################################################################
def preProcessCommand(command,rawmsg):

    moreinfo = ["!topic","!image","!news","!web","!embed","!url"]

    if command.startswith("!"):
        if command in moreinfo:
            trimtext  = f"the command identified was {command}. It was derived from the following string:{rawmsg}"
            trimwords = matchCommand(trimtext,sysrole=trimcommandsysrole)
            # remove the trimwords from the rawmsg
            print(f"trimwords: {trimwords}")
            noncmdmsg = rawmsg.replace(trimwords,"")
            newmsg = f"{command} {noncmdmsg}"
        else:
            newmsg = command
    else:
        newmsg = rawmsg
        
    return newmsg
    
###############################################################################
def matchCommand(rawquery,sysrole=matchcommandsysrole):
    toolmodel = "gpt-3.5-turbo"
    msgarr   = [{"role": "system", "content": sysrole}]

    print(f"rawquery: {rawquery}")

    if len(rawquery) > 16383:
        userquery = rawquery[:16383]
    else:
        userquery = rawquery

    msgarr.append({"role": "user", "content": userquery})

    oai = openai.OpenAI()
    response = oai.chat.completions.create(model=toolmodel,
        messages  = msgarr,
        temperature = 0.0
    )

    print(f"response: {response.choices[0].message.content}")

    return response.choices[0].message.content