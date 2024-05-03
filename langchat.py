import yaml
import openai
import credentials
import tiktoken
import json
import numpy as np
import appdb
import pickle
import urllib.request
import requests
from tempfile import NamedTemporaryFile
import os
import time
from bs4 import BeautifulSoup

###############################################################################
from langchain_community.vectorstores     import FAISS
from langchain_openai                     import OpenAIEmbeddings
from langchain_openai                     import ChatOpenAI
from langchain.prompts                    import ChatPromptTemplate
from langchain.schema.output_parser       import StrOutputParser
from langchain.schema.runnable            import RunnablePassthrough
from langchain_core.messages              import SystemMessage,AIMessage,HumanMessage
from langchain_anthropic                  import ChatAnthropic
from langchain_google_genai               import ChatGoogleGenerativeAI,HarmBlockThreshold,HarmCategory
from langchain_mistralai.chat_models      import ChatMistralAI
from langchain_fireworks                  import ChatFireworks
from langchain_groq                       import ChatGroq

###############################################################################
###############################################################################

#     ######   ##        #######  ########     ###    ##        ######  
#    ##    ##  ##       ##     ## ##     ##   ## ##   ##       ##    ## 
#    ##        ##       ##     ## ##     ##  ##   ##  ##       ##       
#    ##   #### ##       ##     ## ########  ##     ## ##        ######  
#    ##    ##  ##       ##     ## ##     ## ######### ##             ## 
#    ##    ##  ##       ##     ## ##     ## ##     ## ##       ##    ## 
#     ######   ########  #######  ########  ##     ## ########  ######  


oai = None
yamlfile = 'instructions.yaml'
aiyaml   = 'ai.yaml'
aimodel  = credentials.aimodel
embedmodel = credentials.embedmodel

# maxtokens   = 128000
avgmsgtkn   = 500
# poptokens   = maxtokens - avgmsgtkn
gSimilarity = .84

libraryurl  = "http://www.morrisheart.com/pauth/"

oai = openai.OpenAI(api_key=credentials.openaikey)

aimodels   = None #{"gpt4":"gpt-4","gpt4t":"gpt-4-turbo","gpt35t":"gpt-3.5-turbo","claude":"claude-3-opus-20240229","mixtral":"open-mixtral-8x7b","google":"gemini-1.0-pro","llama":"llama-v3-70b-instruct"}
maxtokens  = {"gpt-4":8192,  "gpt-4-turbo":128000, "gpt-3.5-turbo":16384,   "claude-3-opus-20240229":200000,  "open-mixtral-8x7b":16384,    "gemini-1.0-pro":999999,  "llama-v3-70b-instruct":65535}
# chatmodels = {"gpt-4":ChatOpenAI, "gpt-4-turbo":ChatOpenAI, "gpt-3.5-turbo":ChatOpenAI, "claude":ChatAnthropic,           "mixtral":ChatMistralAI,      "google":ChatGoogleGenerativeAI}

modelsobj = None


################################################################################
def getModels():

    aimodels = {}

    with open('modelconfig.yaml', 'r') as file:
        try:
            aiconfig = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
    
    #traverse the dictionary and if the value of the key 'active' is True, add it to the aimodels dictionary
    for key, value in aiconfig.items():
        if value['active']:
            aimodels[key] = value

    # print(aiconfig)
    return aimodels


################################################################################
def getModelNames(modelobj):
    # create a new dictionary from aimodels of just the model name and the model type
    modeldict = {}
    for key, value in modelobj.items():
        modeldict[key] = value['model']

    return modeldict

###############################################################################
def refreshModels():
    global modelsobj
    global aimodels

    modelsobj = getModels()
    aimodels = getModelNames(modelsobj)


###############################################################################
def loadJson(fname=None):

    f = open(fname)
    jdata = json.load(f)
    f.close()

    return jdata


###############################################################################
def loadPickle(fname=None):

    with open(fname, "rb") as f:
        d = pickle.load(f)
        return d
    

###############################################################################
def getchatty():
    
    chatty = {}
    
    with open(yamlfile, 'r') as file:
        try:
            chatty = yaml.safe_load(file)
            # print()
        except yaml.YAMLError as exc:
            print(exc)

    return chatty


###############################################################################
def getlines():
    
    lines = []
    while True:
        line = input()
        if line == "```":
            break
        lines.append(line)

    intxt = "\n".join(lines)

    return intxt


###############################################################################
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613",modelcode="gpt4t"):
    """Return the number of tokens used by a list of messages."""

    
    model = modelsobj[modelcode]['model']

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        "gpt-4-1106-preview",
        "gpt-4-turbo-preview",
        "gpt-4-turbo",
        "claude-3-opus-20240229",
        "open-mixtral-8x7b",
        "gemini-1.0-pro",
        "gemini-1.5-pro-latest",
        "llama-v3-70b-instruct"
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        # print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        # print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens



###############################################################################
def convertToLangChain(messages):
    langarr = []

    for message in messages:
        role = message["role"]
        content = message["content"]
    
        if role == "user":
            langarr.append(HumanMessage(content=content))
        elif role == "assistant":
            langarr.append(AIMessage(content=content))
        elif role == "system":
            langarr.append(SystemMessage(content=content))

    return langarr
                  

###############################################################################
def dochat(messagearray,gptmodel,modelcode):
    # gptmodel = aimodel

    tryagain = True
    # poptokens = maxtokens[gptmodel] - avgmsgtkn
    poptokens = int(modelsobj[modelcode]['maxtokens']) - avgmsgtkn
    
    tokencount = num_tokens_from_messages(messagearray,gptmodel,modelcode)

    while tokencount > poptokens:
        messagearray.pop(1)
        tokencount = num_tokens_from_messages(messagearray,gptmodel,modelcode)

    print('#########################',tokencount,'#########################')

    llm = getChatModel(gptmodel,modelcode)

    while tryagain:
        try:
            # response = oai.chat.completions.create(model=gptmodel,
            #     messages = messagearray
            # )
            langarr  = convertToLangChain(messagearray)
            response = llm.invoke(langarr)

            # print(f'dochat: {response}')
            tryagain = False
        except Exception as err:
            if (str(err).find('maximum context length') > -1):
                messagearray.pop(1)
            else:
                tryagain = False
                print(err)
                exit()

    return response,messagearray


###############################################################################
def getinput(persona):
    
    print('\n\n---')
    intxt = input(">>> ")
    if (intxt == "```"):
        intxt = getlines()
    # prlog(f'\n\n---\n>>> {persona}: {intxt}\n---\n')
    print('---')

    return intxt


###############################################################################
def getafterkeyword(txt,key,keyend):
    offset = 0 #1

    word0   = txt.find(key) + len(key)
    word1   = txt.find(keyend,word0) + offset
    wordtxt = txt[word0:word1]

    # print(f'getafterkeyword: {txt[word0:]} {word0}:{word1}')

    return wordtxt


###############################################################################
def embed(inputtxt):
    global gtotaltokens


    response = oai.embeddings.create(input=inputtxt, model=embedmodel)
    embedding = response.data[0].embedding


    # gtotaltokens += response.usage.total_tokens 
    print(inputtxt,'=',response.usage.total_tokens,'tokens')
    


    return embedding


###############################################################################
def compare_embeddings(embedding1, embedding2):
    cosine_similarity = np.dot(embedding1, embedding2)
    return cosine_similarity



###############################################################################
def listDrugs(jobj):
    for ii in range(len(jobj)):
        print(jobj[ii]["Name"])

    return


###############################################################################
def matchDrugs(drugvector,jobj):
    bestsimilar = -1.0
    bestanswer  = None

    for ii in range(len(jobj)):
        answervector = jobj[ii]["NameVectors"]
        similarity = compare_embeddings(drugvector, answervector)
        if (similarity > gSimilarity) and (similarity > bestsimilar):
            bestsimilar = similarity
            bestanswer  = jobj[ii]["Name"]
        
    return bestanswer

###############################################################################
def listForms(jobj):
    for ii in range(len(jobj)):
        print(jobj[ii]["Form"])

    return


###############################################################################
def matchForms(drugname,formvector,jobj):
    bestsimilar = -1.0
    bestanswer  = None
    dfltanswer  = ""

    for ii in range(len(jobj)):
        print(f'comapring {drugname.lower()} to {jobj[ii]["Name"].lower()}')
        if (drugname.lower() == jobj[ii]["Name"].lower()):
            if (jobj[ii]["Form"].lower() == 'default'):
                dfltanswer = jobj[ii]["Information"]
            else:
                answervector = jobj[ii]["FormVectors"]
                similarity = compare_embeddings(formvector, answervector)
                print(f'{jobj[ii]["Form"]} is a {similarity:.2f} match')
                if (similarity > gSimilarity) and (similarity > bestsimilar):
                    bestsimilar = similarity
                    bestanswer  = jobj[ii]["Information"]
    
    if bestanswer is None:
        bestanswer = dfltanswer
        
    return bestanswer



###############################################################################
# def chatty():
#     global oai

#     oai = openai.OpenAI(api_key=credentials.openaikey)

#     drugjson = loadJson('pauth.json')

#     chatty  = getchatty()
#     persona = 'pauth'

#     disclaimer = "I understand that this is an AI solution. Please refrain from providing anything that can be construed as a disclaimer."
#     params     = f'{disclaimer}'


#     sysreq = chatty[persona]["sys"]
#     usrtxt = chatty[persona]["usr"]
#     endtxt = chatty[persona]["suffix"]

#     uid = "U07856"
#     promptcount = 1

#     msgarr = [{"role": "system", "content": sysreq}]
#     appdb.updateUserData(uid,msgarr,promptcount)


#     doloop = True
#     restart = False

    


#     intxt = "Start a new auth"
#     while doloop:
        
        
#         usrreq = f'{params}{usrtxt}{intxt}{endtxt}'
#         print(usrreq)

#         usrdata = appdb.readUserData(uid)
#         msgarr = usrdata["MsgArray"] if usrdata and "MsgArray" in usrdata else []
#         promptcount = (usrdata["PromptCount"] + 1) if usrdata and "PromptCount" in usrdata else 0

#         msgarr.append({"role": "user", "content": usrreq})
#         response,msgarr = chatgpt(msgarr)    #.encode(encoding='ASCII',errors='ignore').decode()

#         choice = response.choices[0]
#         restxt = choice.message.content
#         tokens = response.usage.total_tokens

#         msgarr.append({"role": "assistant", "content":str(restxt)})
#         appdb.updateUserData(uid,msgarr,promptcount)
#         # print(msgarr)
#         # print(f'(tokens:{tokens}): {wraplines(restxt)}')
        

#         # if ("DRUGNAME:" in restxt) and ("FORMNAME:" in restxt):
#         #     drugname = getafterkeyword(restxt,"DRUGNAME:","\n")
#         #     formname = getafterkeyword(restxt,"FORMNAME:","\n")
#         #     print(f'Name of the drug is {drugname} and the name of the form is {formname}')

#         #     drugvector = embed(drugname)
#         #     formvector = embed(formname)

#         #     # listDrugs(drugjson)
#         #     # listForms(drugjson)

#         #     matcheddrug = matchDrugs(drugvector,drugjson)
#         #     matchedinfo = matchForms(matcheddrug,formvector,drugjson)

#         #     print(f'Information file is {libraryurl}{matchedinfo}')

#         #     # doloop = False

#         #     # pauthdb.resetUserData(uid)

#         # else:
#         #     print(f'(tokens:{tokens}): {restxt}')

#         intxt = getinput(persona)

#         if (intxt.startswith("!reset")):
#             intxt = "Start a new auth"
#             appdb.resetUserData(uid)
#         elif (intxt.startswith("!quit")):
#             doloop = False
#             appdb.resetUserData(uid)


    
#     return restart



###############################################################################
def newmsgarr(uid,sysreq):
    promptcount = 0
    msgarr = [{"role": "system", "content": sysreq}]
    # msgarr = [SystemMessage(content=sysreq)]
    print(SystemMessage(content=sysreq))

    appdb.updateUserData(uid,msgarr,promptcount)

    return msgarr


###############################################################################
def personas():
    chatty  = getchatty()
    # Get the keys as a list
    personalist = list(chatty.keys())
    personas = "```\n"

    for ii in range(len(personalist)):
        print(f'{ii} {personalist[ii]} {chatty[personalist[ii]]["title"]}')
        personas += f'{personalist[ii]:20} - {chatty[personalist[ii]]["title"]}\n'
    # personas += str(personalist)
    personas += "```"

    return personas


###############################################################################
def listModels():

    modellist = "These are the available models:\n```\n"
    for mm in aimodels:
        modellist += f'\t{mm:7} : {aimodels[mm]}\n'
    
    modellist += "```"

    # print(f'listModels: {modellist}')

    return modellist



###############################################################################
def decodeModel(modelname):
    model = credentials.aimodel


    # if modelname == 'gpt4':
    #     model = 'gpt-4'
    # elif modelname == 'gpt4turbo':
    #     model = 'gpt-4-turbo-preview'
    # elif modelname == 'gpt35turbo':
    #     # model = 'gpt-3.5-turbo'
    #     model = 'gpt-3.5-turbo-0125'

    if modelname in aimodels:
        model = aimodels[modelname]

    print(f'decodeModel({modelname}) = {model}')

    return model

###############################################################################
def getChatModel(modelname,modelcode):
    temperature = 0

    print(f'getChatModel({modelname}) with aimodels={aimodels}')
    
    print('~'*40)
    print(modelsobj[modelcode]['provider'])
    print('~'*40)

    chatmodel = eval(modelsobj[modelcode]['provider'])

    # # if modelname in aimodels:
    # if modelname in maxtokens:
    #     # aimodel = decodeModel(modelname)
    #     aimodel = modelname

    #     if modelname == "claude-3-opus-20240229":
    #         chatmodel = ChatAnthropic(temperature=temperature,model_name=aimodel)
    #     elif modelname == "open-mixtral-8x7b":
    #         aimodel = "accounts/fireworks/models/mixtral-8x7b-instruct"
    #         # chatmodel = ChatMistralAI(temperature=temperature,model_name=aimodel)
    #         chatmodel = ChatFireworks(temperature=1,model=aimodel)
    #     elif modelname == "llama-v3-70b-instruct":
    #         aimodel = "accounts/fireworks/models/llama-v3-70b-instruct"
    #         chatmodel = ChatFireworks(temperature=temperature,model=aimodel)
    #     elif modelname == "gemini-1.0-pro":
    #         googlesafety = {
    #             HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    #             HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    #             HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    #             HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
    #         }
    #         chatmodel = ChatGoogleGenerativeAI(temperature=temperature,model=aimodel,convert_system_message_to_human=True,safety_settings=googlesafety)
    #     else:
    #         chatstring = f'ChatOpenAI(temperature={temperature},model_name="{aimodel}")'
    #         chatmodel = eval(chatstring)
    #         # chatmodel = ChatOpenAI(temperature=temperature,model_name=aimodel)


    return chatmodel

###############################################################################
def onelang(uid,intxt,persona="default",model=credentials.aimodel,modelcode="gpt35t"):
    global oai

    chatty  = getchatty()
    # print(chatty)

    if persona not in chatty:
        persona = "default"

    print(f'onechat: current persona is {persona} current model is {model}')

    disclaimer = "I understand that this is an AI solution. Please refrain from providing anything that can be construed as a disclaimer."
    params     = f'{disclaimer}'


    sysreq = chatty[persona]["sys"]
    usrtxt = chatty[persona]["usr"]
    endtxt = chatty[persona]["suffix"]
    chnobj = chatty[persona].get("chain")
    print('chnobj=',chnobj)

    usrdata = appdb.readUserData(uid)

    ##### how do we know the persona changed?
    # print(usrdata["MsgArray"][0]['content'])
    # print(chatty)

    if usrdata:
        print('we have data')
        if "MsgArray" in usrdata:
            msgarr = usrdata["MsgArray"]
            # print(msgarr[0])
            if msgarr is not None and len(msgarr) > 0 and msgarr[0] is not None:
                msgarr[0]['content'] = sysreq
            # print(msgarr[0])
        else:
            msgarr = newmsgarr(uid,sysreq)
    else:
        print('no data, restarting')
        msgarr = newmsgarr(uid,sysreq)

    if msgarr is None:
        msgarr = newmsgarr(uid,sysreq)


    usrreq = f'{params}{usrtxt}{intxt}{endtxt}'
    # print(usrreq)

    # usrdata = pauthdb.readUserData(uid)
    # msgarr = usrdata["MsgArray"] if usrdata and "MsgArray" in usrdata else []
    promptcount = (usrdata["PromptCount"] + 1) if usrdata and "PromptCount" in usrdata else 0

    
    
    msgarr.append({"role": "user", "content": usrreq})
    
    # msgarr.append({"role": "user", "content": intxt})
    # msgarr.append(HumanMessage(content=usrreq))

    # print(msgarr)


    response,msgarr = dochat(msgarr,model,modelcode)    #.encode(encoding='ASCII',errors='ignore').decode()

    # choice = response.choices[0]
    # restxt = choice.message.content
    # tokens = response.usage.total_tokens
    print(response)

    restxt = response.content

    msgarr.append({"role": "assistant", "content":str(restxt)})
    # msgarr.append(AIMessage(content=str(restxt)))

    # print(str(msgarr))

    appdb.updateUserData(uid,msgarr,promptcount)

    return restxt

###############################################################################
def nonchat(uid,intxt,restxt,persona="default"):

    chatty  = getchatty()
    # print(chatty)

    if persona not in chatty:
        persona = "default"


    sysreq = chatty[persona]["sys"]

    usrdata = appdb.readUserData(uid)

    ##### how do we know the persona changed?
    # print(usrdata["MsgArray"][0]['content'])
    # print(chatty)

    if usrdata:
        print('we have data')
        if "MsgArray" in usrdata:
            msgarr = usrdata["MsgArray"]
            # print(msgarr[0])
            if msgarr is not None and len(msgarr) > 0 and msgarr[0] is not None:
                msgarr[0]['content'] = sysreq
            # print(msgarr[0])
        else:
            msgarr = newmsgarr(uid,sysreq)
    else:
        print('no data, restarting')
        msgarr = newmsgarr(uid,sysreq)

    if msgarr is None:
        msgarr = newmsgarr(uid,sysreq)

    promptcount = (usrdata["PromptCount"] + 1) if usrdata and "PromptCount" in usrdata else 0

    msgarr.append({"role": "user", "content": intxt})
    msgarr.append({"role": "assistant", "content":str(restxt)})

    # print(str(msgarr))

    appdb.updateUserData(uid,msgarr,promptcount)



    


###############################################################################
def getMatchedInfo(rtxt,drugjson):

    drugname = getafterkeyword(rtxt,"DRUGNAME:","\n")
    formname = getafterkeyword(rtxt,"FORMNAME:","\n")
    print(f'Name of the drug is {drugname} and the name of the form is {formname}')

    drugvector = embed(drugname)
    formvector = embed(formname)

    # listDrugs(drugjson)
    # listForms(drugjson)

    matcheddrug = matchDrugs(drugvector,drugjson)
    matchedinfo = matchForms(matcheddrug,formvector,drugjson)

    urlstr = f"{libraryurl}{matchedinfo}"

    print(f'Information file is {urlstr}')

    return urlstr



###############################################################################
def transcribe(audioFile):
    transcript = oai.audio.transcriptions.create(
        model="whisper-1",
        file=audioFile,
        response_format="text"
    )

    return transcript


###############################################################################
def readAndProcessBinary(url,fname):
    resp = ""

    namefile, suffix = os.path.splitext(fname)

    imgfiles = ('.png','.jpg')
    sndfiles = ('.mp3', '.mp4', '.mpeg', '.mpga', '.m4a','.wav','.webm')


    # Define a User-Agent to mimic a browser request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    req = urllib.request.Request(url, headers=headers)

    # Use a temporary file to avoid managing filesystem cleanup manually
    with NamedTemporaryFile(delete=True, suffix=suffix) as tempBinaryFile:
        # Download the file directly into the temporary file
        t0 = time.time()
        with urllib.request.urlopen(req) as response:
            # Write the content of the downloaded file into the temp file
            tempBinaryFile.write(response.read())
            # Ensure data is written to disk
            tempBinaryFile.flush()
        
        t1 = time.time()
        print(t1-t0,'seconds for reading file')
        # Re-open the temporary file in binary read mode to send for transcription
        with open(tempBinaryFile.name, 'rb') as binaryFile:           
            if (fname.lower().endswith(sndfiles)):
                resp = transcribe(binaryFile)
            
            elif (fname.endswith(imgfiles)):
                resp = "Not processing images yet"

            t2 = time.time()
            print(t2-t1,'seconds for whisper to process')

    return resp


###############################################################################
def processImageVision(url,usrtext):

    response = oai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
            "role": "user",
            "content": [
                # {"type": "text", "text": "What’s in this image?"},
                {"type": "text", "text": usrtext},
                {
                "type": "image_url",
                "image_url": {
                    "url": url
                },
                },
            ],
            }
        ],
        max_tokens=300,
    )

    # print(response.choices[0])
    return response.choices[0].message.content


###############################################################################
def makeImage(usrtext):
    # print(f'makeImage: {usrtext}')
    response = oai.images.generate(
        model="dall-e-3",
        prompt=usrtext,
        size="1792x1024",
        quality="standard",
        n=1,
    )   

    image_url = response.data[0].url

    # print(f'makeImage: url={image_url}')

    return image_url


###############################################################################
def scrapeWebPage(url):
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    # }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }
    

    try:
        # Send HTTP request to the URL
        response = requests.get(url, headers=headers)
        # Ensure the response is in utf-8 encoding to handle special characters
        response.encoding = 'utf-8'

        print(f'scrapeWebPage: {response.text}\n\n')
        
        # Initialize BeautifulSoup with the response content and specify an HTML parser
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all text from the webpage
        # Use .get_text() to extract all the text inside the webpage, you can adjust it according to your needs
        allText = soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(e)
        allText = 'request failed'
    
    return allText



###############################################################################
refreshModels()


###############################################################################
if __name__ == '__main__':

    print("this is a support module")