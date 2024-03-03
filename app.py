###############################################################################
###############################################################################

#     ██ ███    ███ ██████   ██████  ██████  ████████ ███████ 
#     ██ ████  ████ ██   ██ ██    ██ ██   ██    ██    ██      
#     ██ ██ ████ ██ ██████  ██    ██ ██████     ██    ███████ 
#     ██ ██  ██  ██ ██      ██    ██ ██   ██    ██         ██ 
#     ██ ██      ██ ██       ██████  ██   ██    ██    ███████ 
#                                                             


import discord
import os
# from openai import OpenAI
import credentials
import appchat
import appdb
import requests
from datetime import datetime
import pytz
import time
import re
import warnings
import asyncio
from concurrent.futures import ThreadPoolExecutor
import ddgfn
import unicodedata


###############################################################################
###############################################################################


#      ██████  ██       ██████  ██████   █████  ██      ███████ 
#     ██       ██      ██    ██ ██   ██ ██   ██ ██      ██      
#     ██   ███ ██      ██    ██ ██████  ███████ ██      ███████ 
#     ██    ██ ██      ██    ██ ██   ██ ██   ██ ██           ██ 
#      ██████  ███████  ██████  ██████  ██   ██ ███████ ███████ 
#                                                               
                                                              

warnings.filterwarnings("ignore", category=RuntimeWarning)

lastboot = None

# Define the intents your bot requires
intents = discord.Intents.default()  # This will enable most, but not all, intents
intents.messages = True  # If your bot needs to receive and send messages
intents.guilds = True    # If your bot needs information about guilds (servers)
intents.message_content = True  # To receive the content of the messages
# intents.guild_messages = True  # To receive messages in guilds (servers)
# intents.direct_messages = True  # To receive direct messages

# Create the client with the specified intents
client = discord.Client(intents=intents)


###############################################################################
###############################################################################

#     ███████ ██    ██ ██████  ██████   ██████  ██████  ████████     ███████ ███    ██ ███████ 
#     ██      ██    ██ ██   ██ ██   ██ ██    ██ ██   ██    ██        ██      ████   ██ ██      
#     ███████ ██    ██ ██████  ██████  ██    ██ ██████     ██        █████   ██ ██  ██ ███████ 
#          ██ ██    ██ ██      ██      ██    ██ ██   ██    ██        ██      ██  ██ ██      ██ 
#     ███████  ██████  ██      ██       ██████  ██   ██    ██        ██      ██   ████ ███████ 



###############################################################################
def prlog(outstr):
    _isHydraLogs = True
    _isPrint     = False
    _hydraLogFile = "hydralogs.txt"
    
    writestr = f'{outstr}\r'

    if (_isPrint):
        print(outstr)

    if (_isHydraLogs):
        f = open(_hydraLogFile,"a")
        f.write(writestr)
        f.close()

###############################################################################
def getHelpMessage():
    msg  = 'This is the list of commands:\n'
    msg += '```\n'
    msg += '\t!test     = test\n'
    msg += '\t!examples = show some examples of how to use commands\n'
    msg += '\t!ping     = confirm the server is running\n'
    msg += '\t!info     = provide debugging info\n'
    msg += '\t!reset    = reset the bot and start a new topic (alt is 🔄)\n'
    msg += '\t!models   = list available LLMs\n'
    msg += '\t!persona  = show the current persona and list available choices\n'
    msg += '\t!topic    = list or modify the channel topic\n'
    msg += '\t!again    = show the last response from the LLM\n'
    msg += '\t?^news    = search the web for news headlines for the string that follows news\n'
    msg += '\t?^web     = search the web for the string that follows news\n'
    msg += '\t?news     = search the web for news headlines and process via LLM (alt is 📰)\n'
    msg += '\t?web      = search the web and process via LLM (alt is 🔍)\n'
    msg += '\t^         = display the raw output from an image or sound\n'
    msg += '\t//        = start a comment that the bot will ignore\n'
    msg += '```'

    return msg

###############################################################################
def getExamples():
    msg  = '**Here are some examples of how to use the tools**\n'
    msg += 'Search:'
    msg += '```\n'
    msg += 'Search the web:\n'
    msg += '\t if you want to find info about cats:\n'
    msg += '\t\t🔍information about cats\n\n'
    msg += '\t you can pipe the reponse through a query:\n'
    msg += '\t\t🔍information about cats | create a summary from this text:\n'
    msg += '```'

    msg += 'News:'
    msg += '```\n'
    msg += 'Search for news:\n'
    msg += '\t if you want to find headline news:\n'
    msg += '\t\t📰today\'s headline news\n\n'
    msg += '\t you can pipe the reponse through a query:\n'
    msg += '\t\t📰today\'s headline news | create a summary from this text:\n'
    msg += '```'

    msg += 'Image Generation:'
    msg += '```\n'
    msg += 'Text to image:\n'
    msg += '\t🎨create an image of a white cat in the style of a 70\'s cartoon\n'
    msg += '```'

    msg += 'Image to text:'
    msg += '```\n'
    msg += 'Just drag and drop an image into the chat\n'
    msg += 'You can add a command as part of the message:\n'
    msg += '\tWhat is this an image of:\n'
    msg += '```'

    msg += 'Audio to text:'
    msg += '```\n'
    msg += 'Just drag and drop an sound file into the chat\n'
    msg += 'You can add a command as part of the message:\n'
    msg += '\tSummarize this:\n'
    msg += '```'

    msg += 'Change channel topic:'
    msg += '```\n'
    msg += 'The channel topic contains additional commands.\n'
    msg += '\tmodel   - this is the LLM model that the channel is using\n'
    msg += '\tpersona - these are the instructions for the the chat\n'
    msg += '\tscope   - this a fine tune for the chat\n'
    msg += '\tExample:\n'
    msg += '\t\t!topic model=gpt4t persona=python scope=string functions\n'
    msg += '\t\t\tmodel=gpt4t            == use gpt4 turbo\n'
    msg += '\t\t\tpersona=python         == python specifc instructions\n'
    msg += '\t\t\tscope=string functions == focus the chat on string functions\n'
    msg += '```'


    # msg += '\t!info    = provide debugging info\n'
    # msg += '\t!reset   = reset the bot and start a new topic\n'
    # msg += '\t!models  = list available LLMs\n'
    # msg += '\t!persona = show the current persona and list available choices\n'
    # msg += '\t!topic   = list or modify the channel topic'
    # msg += '\t?^news   = search the web for news headlines for the string that follows news\n'
    # msg += '\t?^web    = search the web for the string that follows news\n'
    # msg += '\t?news    = search the web for news headlines and process via LLM (alt is 📰)\n'
    # msg += '\t?web     = search the web and process via LLM (alt is 🔍)\n'
    # msg += '\t^        = display the raw output from an image or sound\n'
    # msg += '\t//       = start a comment that the bot will ignore\n'
    # msg += '```'

    return msg


###############################################################################
def getGreeting():
    timezone = pytz.timezone("America/New_York")
    nytime = datetime.now(timezone)

    greetings = "Greetings"

    if 6 <= nytime.hour < 12:
        greetings = "Good Morning"
    elif 12 <= nytime.hour < 17:
        greetings = "Good Afternoon"
    elif 17 <= nytime.hour < 22:
        greetings = "Good Evening"
    
    return greetings



###############################################################################
def isFirstCharacterEmoji(inputString):

    try:
        firstChar = inputString[0]
        emojiProperty = unicodedata.name(firstChar)

        codePoint = ord(firstChar)

        # print(f'emojiProperty={emojiProperty} {codePoint}')

        # Basic range checks (this is NOT comprehensive)
        # Extracted from https://www.unicode.org/Public/emoji/13.1/emoji-data.txt
        # This includes only a small subset for demonstration purposes
        emojiRanges = [
            (0x1F600, 0x1F64F),  # Emoticons
            (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
            (0x1F680, 0x1F6FF),  # Transport and Map
            # Add more ranges as needed
        ]
        isemoji = any(start <= codePoint <= end for start, end in emojiRanges)
    except:
        isemoji = False
    
    return isemoji


###############################################################################
def extractScopeAndPersona(message):
    # print(f'parsing {inputString}')

    # if message.channel.topic is not None:
    if hasattr(message.channel, 'topic'):
        inputString = str(message.channel.topic)
    else:
        inputString = ""
    
    # Regular expressions to match "scope=" and "persona=" keys
    # Updated patterns to match any characters up until the next key or the end of the string
    # scopePattern = r"scope=(.*?)(?= persona=|$)"
    # personaPattern = r"persona=(.*?)(?= scope=|$)"
    # modelPattern = r"model=(.*?)(?= model=|$)"

    scopePattern = r"scope=(.*?)(?= persona=| model=|$)"
    personaPattern = r"persona=(.*?)(?= scope=| model=|$)"
    modelPattern = r"model=(.*?)(?= scope=| persona=|$)"

    scopeMatch = re.search(scopePattern, inputString)
    personaMatch = re.search(personaPattern, inputString)
    modelMatch = re.search(modelPattern, inputString)

    # print(f'finished parsing')

    # print(f'found scopeMatch={scopeMatch} personaMatch={personaMatch}')

    # Extracting values using the regular expression search results
    scopeValue = scopeMatch.group(1) if scopeMatch else None
    personaValue = personaMatch.group(1) if personaMatch else "default"
    modelCode = modelMatch.group(1) if modelMatch else None

    modelValue = appchat.decodeModel(modelCode)

        

    return scopeValue, personaValue, modelValue



###############################################################################
async def getPromptResponse(executor, func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func, *args)



###############################################################################
async def send_long_message(channel, message):
    """Sends a message in chunks if it's longer than 2000 characters, without splitting words,
    ensures mentions are on their own line, and block quotes are in separate chunks."""
    MAX_LENGTH = 2000

    # Check if the message starts with a mention and send it separately
    if message.startswith("<@") and ">" in message:
        end_of_mention = message.find(">") + 1
        mention = message[:end_of_mention]
        await channel.send(mention)  # Send the mention on its own line
        message = message[end_of_mention:].lstrip()  # Remove the mention from the message

    # Initialize the current chunk of the message
    chunk = ""

    # Split the message by backticks to separate block quotes
    parts = message.split('```')
    block_quote = False  # Keep track of whether we are inside a block quote

    for part in parts:
        if block_quote:
            # Send the current chunk before the block quote
            if chunk:
                await channel.send(chunk)
                chunk = ""
            # Send the block quote as a separate chunk
            block_quote_content = f"```{part}```"
            await channel.send(block_quote_content)
        else:
            words = part.split(' ')
            for word in words:
                if len(chunk) + len(word) + 1 > MAX_LENGTH:
                    await channel.send(chunk)
                    chunk = word + " "
                else:
                    chunk += word + " "
        block_quote = not block_quote  # Toggle the block quote flag

    # Send any remaining text if there is any
    if chunk.strip():
        await channel.send(chunk)


###############################################################################
async def typingSend(message,msgtxt):
    async with message.channel.typing():
        if message.guild:
            await send_long_message(message.channel,msgtxt)
        else:
            await send_long_message(message.author,msgtxt)


###########################################################################################
def urlFromText(text):
    """
    This function scans the provided text for any occurrences of URLs starting with
    http or https and returns the first URL found. If no URL is found, it returns None.
    """
    # Define the regex pattern for matching URLs
    urlPattern = r"https?://[^\s]+"

    # Search for URLs using the regex pattern
    match = re.search(urlPattern, text)

    # Check if a match was found
    if match:
        # Extract and return the URL
        return match.group()
    else:
        # Return None if no URL was found
        return None




###############################################################################
###############################################################################

#     ███████ ██    ██ ███████ ███    ██ ████████ ███████ 
#     ██      ██    ██ ██      ████   ██    ██    ██      
#     █████   ██    ██ █████   ██ ██  ██    ██    ███████ 
#     ██       ██  ██  ██      ██  ██ ██    ██         ██ 
#     ███████   ████   ███████ ██   ████    ██    ███████ 
#                                                         



###############################################################################
@client.event
async def on_ready():
    global lastboot
    timezone = pytz.timezone("America/New_York")
    nytime = datetime.now(timezone)

    # Convert datetime object to a string
    lastboot = nytime.strftime('%Y-%m-%d %H:%M:%S')
    print(f'We have logged in as {client.user}')
    # print(client)


###############################################################################

#      ██████  ███    ██     ███    ███ ███████ ███████ ███████  █████   ██████  ███████ 
#     ██    ██ ████   ██     ████  ████ ██      ██      ██      ██   ██ ██       ██      
#     ██    ██ ██ ██  ██     ██ ████ ██ █████   ███████ ███████ ███████ ██   ███ █████   
#     ██    ██ ██  ██ ██     ██  ██  ██ ██           ██      ██ ██   ██ ██    ██ ██      
#      ██████  ██   ████     ██      ██ ███████ ███████ ███████ ██   ██  ██████  ███████ 


@client.event
async def on_message(message):
    # print(f"Messasge: {message}")
    # print(f"Message received: {message.content}")  # Debugging print

    # get userid
    userid  = str(message.author)
    usrtext = message.content
    usrmention = message.author.mention
    channelobj = message.channel
    say = send_long_message


    # avoid the bot talking to itself
    if userid == str(client.user):
        return
    
    # ignore comments
    if usrtext.startswith('//'):
        return
    
    # reboot the server
    if usrtext.startswith(credentials.rebootserver):
        msg = "Launch Codes Received: **REBOOTING SERVER**"
        await typingSend(message,msg)
        # if message.guild:
        #     await send_long_message(channelobj,msg)
        # else:
        #     await send_long_message(userid,msg)
        os._exit(0)
    


    focustxt = ""
    persona  = "default"
    
    focustxt,persona,aimodel = extractScopeAndPersona(message)
    # print(aimodel,str(message.channel.topic))

    textattach = ""
    msgalert   = ""

    urltext = urlFromText(usrtext)

    if (urltext is not None) and (not message.attachments):
        # print(urltext)
        async with message.channel.typing():
            with ThreadPoolExecutor() as executor:
                textattach = await getPromptResponse(executor, appchat.scrapeWebPage, urltext)  
        
            print(f'extracted the following from {urltext}\n\n{textattach}')
            tmp = usrtext.replace(urltext, textattach)
            usrtext = tmp
            textattach = ""

            print()
            print('new usrtext=',usrtext)
            print('/\\'*50)

    elif message.attachments or message.embeds:
        isReject = True
        okfiles = ('.txt','.py','.yaml','.json','.csv','.sh','.xml','.md','.htm','.js','.html')
        imgfiles = ('.png','.jpg','.webp')
        sndfiles = ('.mp3', '.mp4', '.mpeg', '.mpga', '.m4a','.wav','.webm')
        if message.attachments:
            for attachment in message.attachments:
                # if attachment.filename.endswith('.txt') or attachment.filename.endswith('.py'):
                if attachment.filename.lower().endswith(okfiles):
                    response = requests.get(attachment.url)
                    if response.status_code == 200:
                        # Extract text from the file
                        textattach = response.text[:16384]
                        isReject = False

                        if (len(response.text) > 16383):
                            msgalert   = "**WARNING: The attachment has been truncated to 16k. The response might not be complete.**\n\n\n"
                        
                        # print(textattach)
                        # await send_long_message(message.author,msg)
                        # return
                elif attachment.filename.lower().endswith(imgfiles):
                    # textattach = "This is an image file. I am working on how to get this implemented right now. Acknowledge that this is a work in progress."
                    if usrtext == "" or usrtext == "?":
                        imgtxt = "describe this image in full detail"
                    else:
                        imgtxt = usrtext
                    async with message.channel.typing():
                        with ThreadPoolExecutor() as executor:
                            textattach = await getPromptResponse(executor, appchat.processImageVision, attachment.url, imgtxt)   

                    if (usrtext.startswith('^')):
                        # if message.guild:
                        #     # await send_long_message(message.channel,msg)
                        #     await say(channelobj,textattach)
                        # else:
                        #     # await send_long_message(message.author,msg)
                        #     await say(userid,textattach)
                        await typingSend(message,textattach)
                        

                    isReject = False
                    # await message.channel.send(textattach)
                elif attachment.filename.lower().endswith(sndfiles):
                    # response = requests.get(attachment.url)

                    async with message.channel.typing():
                        with ThreadPoolExecutor() as executor:
                            textattach = await getPromptResponse(executor, appchat.readAndProcessBinary, attachment.url, attachment.filename)   

                    print(textattach) 
                    
                    if (usrtext.startswith('^')):
                        await typingSend(message,textattach)
                        # if message.guild:
                        #     # await send_long_message(message.channel,msg)
                        #     await say(channelobj,textattach)
                        # else:
                        #     # await send_long_message(message.author,msg)
                        #     await say(userid,textattach)

                    isReject = False

                    # textattach = f"This is a sound file. I am working on how to get this implemented right now. Acknowledge that this is a work in progress. {attachment.url} {attachment.filename}"
                    # await message.channel.send(textattach)
        elif message.embeds:
            print(message.embeds)
                    
        if isReject:
            await message.channel.send("Sorry, I can only process text messages right now.\nI suggest regular ChatGPT for this request.")
            return




    
    prompt = str(usrtext) + ' ' + str(focustxt) + ' ' + textattach

    # print('prompt = ',prompt)


    # determine if in channel or if direct message
    if message.guild:  # in a channel -- multiple users can talk to the bot at once, use the channel id as the thread key
        threadseed = str(message.channel.id)
        msgalert   = f'{usrmention} {msgalert}'
    else: # direct message, use the userid as the thread key
        threadseed = userid




    #     ██████       ██████  ██████  ███    ███ ███    ███  █████  ███    ██ ██████  ███████ 
    #          ██     ██      ██    ██ ████  ████ ████  ████ ██   ██ ████   ██ ██   ██ ██      
    #       ▄███      ██      ██    ██ ██ ████ ██ ██ ████ ██ ███████ ██ ██  ██ ██   ██ ███████ 
    #       ▀▀        ██      ██    ██ ██  ██  ██ ██  ██  ██ ██   ██ ██  ██ ██ ██   ██      ██ 
    #       ██         ██████  ██████  ██      ██ ██      ██ ██   ██ ██   ████ ██████  ███████ 
    #                                                                                          

    # qcommands = ('?','🔍','📰','🎨')
    qcommands = ('?',)
    emojiCommand = isFirstCharacterEmoji(usrtext)
        
    # print(f'is First Char Emoji? {isFirstCharacterEmoji(usrtext)}')    
    
    # if usrtext.startswith('?')  or usrtext.startswith('🔍')  or usrtext.startswith('📰'):
    if usrtext.startswith(qcommands) or emojiCommand:
        # await typingSend(message,'Duck Duck Go Search')
        firstSpace = usrtext.find(' ')

        # print(f'special commands: {usrtext}')


        newscommands  = ('?news','?^news','📰')
        webcommands   = ('?web','?^web','🔍','🔎','🔍^','🔎^')
        artcommands   = ('🎨', '📷','🖌️')
        videocommands = ('🎥','🎦')
        startcommands = ("🔄","🔃")
        faisscommands = ("📡","🧠")
        validstarts  = newscommands + webcommands + artcommands + startcommands

        # if usrtext.startswith('?news') or usrtext.startswith('?^news') or usrtext.startswith('?web') or usrtext.startswith('?^web'):
        if usrtext.startswith(validstarts):
            tmptext = usrtext[firstSpace + 1:].strip() if firstSpace != -1 else ""
            cmdidx = tmptext.find(' |')  # Look for the next command to pipe the content through ' |'
            ddgresult = ""

            print(tmptext,cmdidx)

            if cmdidx > -1:
                usrcmd = tmptext[cmdidx + 2:].strip()  # Extract the command text after ' ?'
                searchtext = tmptext[:cmdidx]  # The search text is everything before the next command
            else:
                usrcmd = ""
                searchtext = tmptext  # If no subsequent command, all of tmptext is the search text

            if usrtext.startswith(newscommands):
                async with message.channel.typing(): # 📰
                    with ThreadPoolExecutor() as executor:
                        ddgresult = await getPromptResponse(executor, ddgfn.ddgNews, searchtext)

                # ddgresult = ddgfn.ddgNews(searchtext)

            # elif usrtext.startswith('?web') or usrtext.startswith('?^web'):
            elif usrtext.startswith(webcommands): # 🔍
                async with message.channel.typing():
                    with ThreadPoolExecutor() as executor:
                        ddgresult = await getPromptResponse(executor, ddgfn.ddgText, searchtext)
                
                # ddgresult = ddgfn.ddgText(searchtext)
                print(f'search results:\n{ddgresult}')

            elif usrtext.startswith(artcommands): # 🎨
                # print(f'found an art command {usrcmd}')
                # await typingSend(message,f'still implementing text to image')
                async with message.channel.typing():
                    with ThreadPoolExecutor() as executor:
                        imgurl = await getPromptResponse(executor, appchat.makeImage, searchtext)

                embed = discord.Embed()
                embed.set_image(url=imgurl)
                await message.channel.send(embed=embed)
                return
            
            
            elif usrtext.startswith(startcommands): # 🔄
                ddgresult = "Start a new conversation. Begin by simply asking the user what they want to do. Do not provide any solutions yet." + ' ' + str(focustxt) + ' ' + textattach
                appdb.resetUserData(threadseed)

            elif usrtext.startwith(faisscommands):
                ddgresult = ""
            
            tmpusrtext = f'{usrcmd} {ddgresult}'

            if usrtext.startswith('?^'):
                await typingSend(message,f'{searchtext} {usrcmd} {tmpusrtext}')
                return
            else:
                # await typingSend(message,f'{usrcmd} {tmpusrtext}')
                prompt = tmpusrtext
                


    #        ██      ██████  ██████  ███    ███ ███    ███  █████  ███    ██ ██████  ███████ 
    #        ██     ██      ██    ██ ████  ████ ████  ████ ██   ██ ████   ██ ██   ██ ██      
    #        ██     ██      ██    ██ ██ ████ ██ ██ ████ ██ ███████ ██ ██  ██ ██   ██ ███████ 
    #               ██      ██    ██ ██  ██  ██ ██  ██  ██ ██   ██ ██  ██ ██ ██   ██      ██ 
    #        ██      ██████  ██████  ██      ██ ██      ██ ██   ██ ██   ████ ██████  ███████ 

                                                                                            

    elif usrtext.startswith('!'): # check for commands
        if usrtext.startswith('!test'):
            await message.channel.send('Test message received')
            return

        elif usrtext.startswith('!lastboot'):
            await typingSend(message,f'server was last rebooted {lastboot}')
            return

        elif usrtext.startswith('!persona'):
            msg = f'current persona is **{persona}**\navailable: {appchat.personas()}'

            await typingSend(message,msg)
            return

        elif usrtext.startswith('!info'):
            channel_id = str(message.channel.id)
            guild_id = str(message.guild.id)

            msg = f'{userid} {channel_id} {guild_id} {prompt} '


            await typingSend(message,msg)
            return
        
        elif usrtext.startswith("!reset") or usrtext.startswith("!start"):
            prompt = "Start a new conversation. Begin by simply asking the user what they want to do. Do not provide any solutions yet." + ' ' + str(focustxt) + ' ' + textattach
            appdb.resetUserData(threadseed)
        
        elif usrtext.startswith('!ping'):
            greetings = getGreeting()
            msg = f'**{greetings}** {usrmention}. **I am completely operational, and all my circuits are functioning perfectly**.\n'
            # await message.channel.send(msg)
            await typingSend(message,msg)
            return

        elif usrtext.startswith('!help'):
            msg = getHelpMessage()

            await typingSend(message,msg)
            return
        
        elif usrtext.startswith('!examples'):
            msg = getExamples()

            await typingSend(message,msg)
            return
        
        elif usrtext.startswith('!topic'):

            if hasattr(message.channel, 'topic'):
                tmp = usrtext[len('!topic'):].strip()

                if len(tmp) < 1:
                    msg = f'Current topic is:\n```\n!topic {str(message.channel.topic)}\n```'
                else:
                    # Edit the channel's topic
                    await message.channel.edit(topic=tmp)
                    msg = f'updated topic to ```\n{tmp}\n```'
            else:
                    msg = 'This channel has no topic.'
            
            # print(msg)

            await typingSend(message,msg)

            return
        
        elif usrtext.startswith('!models'):
            msg  = appchat.listModels()
            msg += f'current model is {aimodel}'
            # print(msg)
            await typingSend(message,msg)
            return

        elif usrtext.startswith('!lastresponse') or usrtext.startswith('!again'):
            usrdata = appdb.readUserData(threadseed)
            
            # msg = sysreq
            lastmsg = len(usrdata["MsgArray"])
            msg = usrdata["MsgArray"][lastmsg-1]['content']

           
            await typingSend(message,msg)

            return
        
        elif usrtext.startswith('!system'):
            usrdata = appdb.readUserData(threadseed)
            
            # msg = sysreq
            msg = usrdata["MsgArray"][0]['content']

            
            await typingSend(message,msg)

            return
        
        else:
            msg = "No Matching Command"
            await typingSend(message,msg)
            return



    # # ###################################################################################################################
    # # ###################################################################################################################
    # # ###################################################################################################################
        
    # ██████  ██████   ██████  ███    ███ ██████  ████████     ██      ██      ███    ███ 
    # ██   ██ ██   ██ ██    ██ ████  ████ ██   ██    ██        ██      ██      ████  ████ 
    # ██████  ██████  ██    ██ ██ ████ ██ ██████     ██        ██      ██      ██ ████ ██ 
    # ██      ██   ██ ██    ██ ██  ██  ██ ██         ██        ██      ██      ██  ██  ██ 
    # ██      ██   ██  ██████  ██      ██ ██         ██        ███████ ███████ ██      ██ 
                                                                                        

    # print(prompt)

    t0 = time.time()
    async with message.channel.typing():
        with ThreadPoolExecutor() as executor:
            # print(f'calling onechat with aimodel={aimodel}')
            msg = await getPromptResponse(executor, appchat.onechat, threadseed, prompt, persona, aimodel)        
        

    t1 = time.time()
    print(f"response from openAI took {(t1-t0):.3f} seconds")
    
    msg = msgalert + msg
    
    # Check if the message is from a server channel and not a DM
    await typingSend(message,msg)
    # async with message.channel.typing():
    #     if message.guild:
    #         # await send_long_message(message.channel,msg)
    #         await say(channelobj,msg)
    #     else:
    #         # await send_long_message(message.author,msg)
    #         await say(userid,msg)
    return




###############################################################################
@client.event
async def on_message_edit(before,after):
    print("message edited")
    # await before.channel.send('Message edited. Was it an embed?')


###############################################################################
client.run(credentials.discord_token)