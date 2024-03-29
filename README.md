**Here is a quick rundown of the files:**
```
app.py            == the main controler, contains the user input/output logic
appchat.py        == talks to the LLMs
appdb.py          == sqlite database connectivity
credentials.py    == API keys and Bot Tokens (I don't like env variables)
ddgfn.py          == duck duck go functionality
instructions.yaml == the different "personas". essentially fine-tuned instructions for the LLM to follow
runbot.sh         == bash script to run and restart the bot if it crashes
```

This is an integration of LLM APIs presented through Discord.

**Lets start with an overview:** I grew up playing text based adventures. Zork was an early entry into what feels like a conversational interaction. Fast forward many years, and we are experiencing the infantcy of Large Language Models. With all of the rapid advancements, I wanted a tool that can test different LLMs and incorporate new models as they become available. ChatGPT is great, but can also feel frustrating at times. It is too easy to make ChatGPT lose focus, and some of the UI could be improved. Instead of trying to create a new front end, it feels much more sensible to utilize a best-in-breed approach, and incorporate the functionality into a UI/UX that has already been matured. Currently Slack, Microsoft Teams, and Discord all have large user bases with established UI/UX norms. For this project, Discord's Python library was the easiest one for me to use and had most of the functionality that I wanted.

**Current Status:**
The tool is currently integrated with OpenAI for the LLM features, and DuckDuckGo for internet searches. With OpenAI it uses chat completions with GPT-3.5-Turbo, GPT-4 and GPT-4-Turbo. It has vision functionality to interpret images, whisper functionality to interpret audio, and image generation (Dall-e) for text to image. I wasn't really thrilled about the Bing searches that ChatGPT utilizes. DDG isn't as comprehensive as Google, but I use it in my browser daily with decent results. Additionally it does not require API keys. It also has a basic web scraper which can be used as part of the chat. It falls short on web pages that are powered entirely by javascript.

One of the interesting aspects of using Discord is that by nature of the tool itself is that multiple people can work with the same chat session. It is a group or team chat with the LLM.

**Future:**
With a little more work, other LLMs such as Google's AI can be added. When OpenAI Sora becomes available it should be a relatively easy integration into the bot.

_____________________

**Technical Execution:** For starters, this project assumes at least some familiarity with Python, Linux, and Discord.<br/><br/>
To get this going, it requires a discord server. It will all be documented in a separate setup/how-to file. For the time being, here are the current pieces that I am using:
- A discord server
- An AWS Linux instance (1GB 2vCPUs and 40GB storage)
  - Python 3.9
  - Python's virtual environments
  - Linux Screen
- OpenAI's API
  

