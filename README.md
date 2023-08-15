## To run the bot, you can use docker or run it manually
### To run it manually
1. Install python3.9 or higher
2. Install requirements.txt
    - Use `python3 -m pip install -r requirements.txt`
3. Populate the 'env.py' file, a sample is provided in the `sample-env.py`

    - You can get the bot token from [BotFather](https://t.me/BotFather) and creating a new bot
    - After you create the bot, send a message to it and go to `https://api.telegram.org/bot<yourtoken>/getUpdates` and get the chat id of your chat with it.
    - You can get canvas api key by going to [canvas](https://canvas.nus.edu.sg/profile/settings) and clicking on `+ New Access Token`
    - You can get the course id of the course by clicking on the course in canvas. It should be displayed in the URL as `https://canvas.nus.edu.sg/courses/<courseid>`
    - Set the number of `MINUTES` in advance you want the bot to remind you before the quiz starts. The bot will filter by the unlock time, due time and lock time of the task.
4. Run the `main.py` file
    - Use `python3 main.py`

### Running it using docker
1. Install docker
2. Build the docker project after following step 3 above to formulate the `env.py` file
    - Use `docker build -t <yourimagename> .`
3. Run the docker project
    - Use `docker run -d --name <yourcontainername> <yourimagename>`

> Credits to [Russell](https://github.com/russelldash332) for writing the initial canvas api