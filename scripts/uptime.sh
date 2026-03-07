rm -f x f
poetry run uptime > x
grep FAIL x
fail=$?
if [ $fail == 0 ]; then
  date
  echo "Uptime tests failed!"
  awk '{printf "%s\\n", $0}' x > f
  cat x
  $HOME/server-config/chat_bot.sh f
fi
rm -f x f
