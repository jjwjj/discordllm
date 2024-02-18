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


Select a plain vanilla Amazon Linux Instance type:
![image](https://github.com/jjwjj/discordllm/assets/9681066/8e8490cc-6114-455c-9502-517085cecc1f)

I have been using the 1GB instance which is good for multiple development projects. If the plan is to just run a few bots, the 512MB is plenty.
![image](https://github.com/jjwjj/discordllm/assets/9681066/ebbb3b53-10c8-487f-866a-1f46f2354838)


#2.
Bot Setup -- Get a new Token
![image](https://github.com/jjwjj/discordllm/assets/9681066/6f09a226-29ec-4a8c-b149-213e10c63cfb)
