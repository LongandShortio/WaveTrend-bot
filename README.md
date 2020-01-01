# Setup the bot

* Type your API key in main_trading and main_telegram
* Type your private key in main_trading and main_telegram
* Type your Telegram token in main_trading and main_telegram
* Type your Telegram chat ID in main_trading and main_telegram
* Choose your leverage in main_trading and main_telegram

# Trading setup

* By default the size position is $500, you can change this in real_bot
* By default the bot is looking at the daily timeframe, you can change this in real_bot

# Launch the bot
`````
chmod +x path/to/the/directory/main_trading.py
chmod +x path/to/the/directory/main_telegram.py
``````

``````
nohup path/to/the/directory/main_trading.py &
nohup path/to/the/directory/main_telegram.py &
``````

# Stop the bot

``````
ps -ef
kill -9 <pid of the script>

``````
