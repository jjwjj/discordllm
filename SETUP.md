There are a few discrete parts of this system:

1. A dedicated server running Python
2. A discord server
3. An OpenAI account
4. The code

____________________________
Contents:
[Set up AWS](#1-AWS)


## 1 AWS 
**AWS:**<br/>
I've been using AWS since 2010, so the easiest path for me was to set up a "Lightsail Amazon Linux" instance.

If you are new to AWS, here's a quick overview:
![image](https://github.com/jjwjj/discordllm/assets/9681066/dc1fc8bb-4bd3-49a6-b76a-922cfc4daca5)


Setting up a new one is pretty easy.
![image](https://github.com/jjwjj/discordllm/assets/9681066/21032d19-f231-4916-97f7-64cb6fc9700a)

Create or Choose an SSH Keypair then save it locally somewhere safe. You will need this later if you want to connect using tools other than AWS' default terminal.
![image](https://github.com/jjwjj/discordllm/assets/9681066/03d40582-da67-420a-babc-8261ab35da40)

Select a plain vanilla Amazon Linux Instance type:
![image](https://github.com/jjwjj/discordllm/assets/9681066/8e8490cc-6114-455c-9502-517085cecc1f)

I have been using the 1GB instance which is good for multiple development projects. If the plan is to just run a few bots, the 512MB is plenty.
![image](https://github.com/jjwjj/discordllm/assets/9681066/ebbb3b53-10c8-487f-866a-1f46f2354838)

Create your Linux Server Instance:
Give it a name so you can find it again later. Then click Create Instance:
![image](https://github.com/jjwjj/discordllm/assets/9681066/f6b01a9a-e7d6-494b-b4b0-402ca7ba0d0c)

____________________________

#2.
**Set Up a Discord Bot:**

Create a new bot on the Discord Developer Portal. https://discord.com/developers/applications
Get the bot token, which you'll use to authenticate your bot with Discord's servers.

![image](https://github.com/jjwjj/discordllm/assets/9681066/6f09a226-29ec-4a8c-b149-213e10c63cfb)

<br/>
Create a Python Script for the Bot:

**Deploy the Bot:**

Host your bot on a server or a cloud platform to keep it running.
Ensure your hosting environment has all necessary dependencies installed.
Add the Bot to Your Discord Server:

Use the invite link generated in the Discord Developer Portal to add your bot to the desired server.
Handling Messages and Responding:

The bot should listen to messages on a channel, pass them to the OpenAI API, and send back the response it receives.
Ensure to implement command handling, so the bot only responds when intended (e.g., with a specific command prefix).
Security and Rate Limits:

Be mindful of the security implications. Do not allow the bot to execute arbitrary code or reveal sensitive information.
Be aware of the rate limits imposed by both Discord and OpenAI to avoid service disruptions.
 
**Step 1:** Access the Discord Developer Portal
Navigate to the Discord Developer Portal.
Log in with your Discord account.
Click on the application that corresponds to your bot.

**Step 2:** Configure Bot Permissions
In the application dashboard, select the "Bot" tab on the left-hand side.<br/>
Under the "Privileged Gateway Intents" section, ensure that the necessary intents are enabled. For a basic chat bot, you might need the following intents:<br/>
Presence Intent: If your bot needs to track user presence updates.<br/>
Server Members Intent: If your bot needs information about server members.<br/>
Message Content Intent: For reading message content in guilds.<br/>
![image](https://github.com/jjwjj/discordllm/assets/9681066/28e53a78-aef7-43b3-97da-05f267378811)


**Step 3:** Generate the Bot Invite Link
In the application dashboard, select the "OAuth2" tab on the left-hand side.<br/>
Under "Scopes," select bot. This allows your application to connect to Discord as a bot.<br/>
Additional options will appear below. Under “Bot Permissions,” select the permissions your bot requires. For basic interactions, you might need:<br/>
Read Messages/View Channels<br/>
Send Messages<br/>
Embed Links (if your bot sends embedded links)<br/>
Read Message History (if needed)<br/>
Add Reactions (if needed)<br/>
(Any other permissions your specific bot requires)<br/>
![image](https://github.com/jjwjj/discordllm/assets/9681066/1828147e-ae4f-415d-b9d0-98f2b3ff64e3)


Step 4: Copy and Use the Invite Link
After selecting the appropriate scopes and permissions, an invite URL will be generated at the bottom of the "Scopes" section.
Copy this URL.
Paste the URL into your web browser, and you will be directed to a Discord page to add your bot to a server.
Select the server to which you want to add your bot and confirm the action.<br/>
![image](https://github.com/jjwjj/discordllm/assets/9681066/beb021cd-14b8-4e61-91c1-131a1ff72af2)


Step 5: Add the Bot to Your Server
After confirming the permissions, click on the "Authorize" button.
Complete any CAPTCHA required by Discord.
Once these steps are completed, your bot should be added back to your server with the specified permissions. Make sure you are logged in to a Discord account that has permissions to add bots to the desired server. 

For Users to Adjust DM Settings:
Open User Settings:

Users should click on the gear icon near their username at the bottom left of the Discord interface to open "User Settings."
Navigate to Privacy & Safety:

In the sidebar of the User Settings menu, users should find and click on "Privacy & Safety."
Allow Direct Messages:

Within the "Privacy & Safety" settings, users will find a section titled "Server Privacy Defaults."
Users should ensure the option "Allow direct messages from server members" is enabled. This setting allows members of servers the user is part of (including bots) to send them direct messages.
If this setting is disabled, users should toggle it on to allow DMs from server members.
Save Changes:

____________

#3 
**OpenAI:**<br/>
You will need an OpenAI key. <br/>
Navigate to https://platform.openai.com<br/>
![image](https://github.com/jjwjj/discordllm/assets/9681066/b063988a-3a63-4b94-b9b3-11e1502ec047)

Either create a new API Key, or copy an existing key.<br/>
![image](https://github.com/jjwjj/discordllm/assets/9681066/7c74ee1f-6928-4be2-8421-0dc66dc3482c)

You will want to save this API Key in a safe place.

____________

#4 
**Accessing the Remote Linux Command line:**<br/>
Now that we have all of our keys, we need to access the instance and install the relevant software on the instance. I am running from a Windows machine, and have
been partial to [bitvise](https://www.bitvise.com/ssh-client) as an SSH client. It does not matter which SSH client you use, in fact you can log into the terminal directly from AWS.

The most important thing is that you will need to use your SSH key from Step #1 above in order to access the Linux instance.

Here are some helpful links to SSH tools.<br/>
[bitvise](https://www.bitvise.com/ssh-client)<br/>
[macos ssh](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-linux-inst-ssh.html)<br/>
[cyber duck](https://cyberduck.io/)<br/>
[mountain duck](https://mountainduck.io/<br/>)


____________

#5 
**Installing the latest version of Python:** <br/>
As of this writing, the Linux instance comes installed with Python 3.9.  In previous versions of working with LLM libraries, I was working with a Python 3.8 base and as new LLMs 
emerge, they are not good at backward compatibility. Most recently, Google's LLM did not work with 3.8, and I was able to move forward with newer versions of Python via virtual environments.

Whatever version of Python is on your Linux instance will run as default. This is largely due to the operating system's reliance on that specific version. What we are going to do is install a newer version, and let it run in parallel so it does not interfere with the base version. We will be using Python's virtual environment to run the newer version which will keep things nicely
separated.

The first step is to install the latest Python version. I am running Python 3.11, so we will base the install on 3.11<br/>
At the command prompt, you will need to use dnf to install it with root permissions. The command below uses the -y switch to skip the prompts

$ sudo dnf install python3.11 -y 
$ sudo dnf install python3-pip

Now we should have the latest version of Python installed. We can list the versions as follows:

$ ls -ls /usr/bin/python*

#6 
**Creating a Virtual Environment** <br/>
Once you've confirmed you have the latest python installed, you will make a virtual enviroment where we will add our working code.  I'm assuming some level of git understanding since you are here and won't go into the installation, workings, etc of git.  If you don't have a firm grasp on git, just download the code as a zip file and use sftp to drop the code here when we are done with the setup of the instance.

Assuming you are in the ~/home folder on you instance, you'll want to create a virtual environment using the latest python version.  Here's how we do it with 3.11

$ /usr/bin/python3.11 -m venv discordbot

This will create a new folder called **discordbot** which we will copy the code into and use as our discord bot server.  We activate the virtual enviroment like this:

$ source discordllm/bin/activate

To exit the virtual environment we simply use:

$ deactivate

I like to add one more folder inside the discordbot folder called **src** which will hold all of the code.  For me, it keeps the folder structure cleaner. However you want to get the code into the src folder is outside the scope of this SETUP.md, and I will stipulate that you are able to get the code copied over, or with a git clone.

Now that we have the basics in place, we will need to keep a perpetual bot server running.  There are a number of ways to do this, and if you are handy with bash scripting and the workings of linux feel free to implement as you desire. I myself have been taking an easier route by just using **screen**. Linux screen will keep everything running even if you disconnect from the instance. Here's a quick overview:

List any running screen sessions:<br/>
$ screen -ls 

Create a new screen session:<br/>
$ screen -S mybot

If you disconnect, and want to get back to the running session:<br/>
$ screen -r mybot

To exit the screen session:<br/>
$ exit

____________

#7 **Bot Software Setup**<br/>

Now we should have all the pieces in place.  We will then need to set up the software. I will stipulate that you have installed the software in **/home/ec2-user/discordllm/src** if your path is different please adapt it to the path that you are using. 

**A.** Lets get your API keys in the proper place.  Copy credentials_template.py to credentials.py the template is just a placeholder, and credentials.py is the live file. Needless to say, credentials.py is your secret and you should not share it.

Inside credentials.py you will see two lines:

openaikey = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Your OpenAI key <br/>
discord_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Your Discord Token <br/>

Paste the corresponding keys/tokens in the correct places, and save the file.

**B.**  Navigate to the bot source code folder:

$ cd /home/ec2-user/discordbot/src


**C.** you will need to change the permissions on the shell files to be executable from the command line.

$ chmod 755 *.sh

**D.** Run the setup script:

$ ./setup.sh

**E.** Now if everything has gone according to plan, you should be able to use your bot.  First we will create a new screen (if you didn't do so in step #6). If you have already created it, then connect to it.

$ screen -S mybot

or if it is already running

$ screen -r mybot

Now start a virtual environment

$ source /home/ec2-user/discordbot/bin/activate

Navigate to the bot source code folder:

$ cd /home/ec2-user/discordbot/src

You can run the bot as follows:

$ ./runbot.sh








