ps aux | grep "bot.py" | grep -v grep | awk '{print $2}' | xargs -i kill -9 {}