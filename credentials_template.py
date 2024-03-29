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



######################################################################################

#       ###    ####       ##     ##  #######  ########  ######## ##        ######  
#      ## ##    ##        ###   ### ##     ## ##     ## ##       ##       ##    ## 
#     ##   ##   ##        #### #### ##     ## ##     ## ##       ##       ##       
#    ##     ##  ##        ## ### ## ##     ## ##     ## ######   ##        ######  
#    #########  ##        ##     ## ##     ## ##     ## ##       ##             ## 
#    ##     ##  ##        ##     ## ##     ## ##     ## ##       ##       ##    ## 
#    ##     ## ####       ##     ##  #######  ########  ######## ########  ######  


aimodel  = 'gpt-4-turbo-preview'
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
                                                            
os.environ['OPENAI_API_KEY'] = openaikey 




######################################################################################
rebootserver = "!YOUR_REBOOT_COMMAND"

