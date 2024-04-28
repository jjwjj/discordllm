# credentials.py
import os

######################################################################################

#        ###    ########  ####       ##    ## ######## ##    ##  ######  
#       ## ##   ##     ##  ##        ##   ##  ##        ##  ##  ##    ## 
#      ##   ##  ##     ##  ##        ##  ##   ##         ####   ##       
#     ##     ## ########   ##        #####    ######      ##     ######  
#     ######### ##         ##        ##  ##   ##          ##          ## 
#     ##     ## ##         ##        ##   ##  ##          ##    ##    ## 
#     ##     ## ##        ####       ##    ## ########    ##     ######  

openaikey = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Your OpenAI key
discord_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Your Discord Token
googleaikey    = 'AIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
tavilyaikey    = 'tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
fireworksaikey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
anthropicaikey = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
huggingfacekey = 'hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
exaapikey      = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
mistralkey     = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
groqkey        = 'gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'




######################################################################################

#       ###    ####       ##     ##  #######  ########  ######## ##        ######  
#      ## ##    ##        ###   ### ##     ## ##     ## ##       ##       ##    ## 
#     ##   ##   ##        #### #### ##     ## ##     ## ##       ##       ##       
#    ##     ##  ##        ## ### ## ##     ## ##     ## ######   ##        ######  
#    #########  ##        ##     ## ##     ## ##     ## ##       ##             ## 
#    ##     ##  ##        ##     ## ##     ## ##     ## ##       ##       ##    ## 
#    ##     ## ####       ##     ##  #######  ########  ######## ########  ######  


aimodel  = 'gpt-4-turbo'
embedmodel = "text-embedding-ada-002"



######################################################################################
# export to environment variables -- this is limited to runtime -- they are ephemeral

#     ######## ##    ## ##     ##          ##     ##    ###    ########   ######  
#     ##       ###   ## ##     ##          ##     ##   ## ##   ##     ## ##    ## 
#     ##       ####  ## ##     ##          ##     ##  ##   ##  ##     ## ##       
#     ######   ## ## ## ##     ##          ##     ## ##     ## ########   ######  
#     ##       ##  ####  ##   ##            ##   ##  ######### ##   ##         ## 
#     ##       ##   ###   ## ##              ## ##   ##     ## ##    ##  ##    ## 
#     ######## ##    ##    ###                ###    ##     ## ##     ##  ######       
                                                            
os.environ['OPENAI_API_KEY']           = openaikey 
os.environ['TAVILY_API_KEY']           = tavilyaikey  
os.environ["FIREWORKS_API_KEY"]        = fireworksaikey
os.environ['GOOGLE_API_KEY']           = googleaikey
os.environ['ANTHROPIC_API_KEY']        = anthropicaikey
os.environ['HUGGINGFACEHUB_API_TOKEN'] = huggingfacekey
os.environ['MISTRAL_API_KEY']          = mistralkey
os.environ['EXA_API_KEY']              = exaapikey
os.environ['GROQ_API_KEY']             = groqkey
os.environ['OPENAI_MODEL_NAME']        = aimodel




######################################################################################
rebootserver = "!YOUR_REBOOT_COMMAND"

