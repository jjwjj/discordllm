There are a few discrete parts of this system:

1. A dedicated server running Python
2. A discord server
3. An OpenAI account
4. The code

#1. I've been using AWS since 2010, so the easiest path for me was to set up a "Lightsail Amazon Linux" instance.

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



#2.



Set Up a Discord Bot:

Create a new bot on the Discord Developer Portal. https://discord.com/developers/applications
Get the bot token, which you'll use to authenticate your bot with Discord's servers.
Create a Python Script for the Bot:

Deploy the Bot:

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

_ 
Step 1: Access the Discord Developer Portal
Navigate to the Discord Developer Portal.
Log in with your Discord account.
Click on the application that corresponds to your bot.

Step 2: Configure Bot Permissions
In the application dashboard, select the "Bot" tab on the left-hand side.
Under the "Privileged Gateway Intents" section, ensure that the necessary intents are enabled. For a basic chat bot, you might need the following intents:
Presence Intent: If your bot needs to track user presence updates.
Server Members Intent: If your bot needs information about server members.
Message Content Intent: For reading message content in guilds.

Step 3: Generate the Bot Invite Link
In the application dashboard, select the "OAuth2" tab on the left-hand side.
Under "Scopes," select bot. This allows your application to connect to Discord as a bot.
Additional options will appear below. Under “Bot Permissions,” select the permissions your bot requires. For basic interactions, you might need:
Read Messages/View Channels
Send Messages
Embed Links (if your bot sends embedded links)
Read Message History (if needed)
Add Reactions (if needed)
(Any other permissions your specific bot requires)

Step 4: Copy and Use the Invite Link
After selecting the appropriate scopes and permissions, an invite URL will be generated at the bottom of the "Scopes" section.
Copy this URL.
Paste the URL into your web browser, and you will be directed to a Discord page to add your bot to a server.
Select the server to which you want to add your bot and confirm the action.

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


Bot Setup -- Get a new Token
![image](https://github.com/jjwjj/discordllm/assets/9681066/6f09a226-29ec-4a8c-b149-213e10c63cfb)

