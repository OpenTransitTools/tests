echo -n "."
rm -f x f

poetry run uptime > x
sleep 2

grep FAIL x
fail=$?
if [ $fail == 0 ]; then
  echo
  echo -n "Uptime tests failed! "
  date
  cat x
  echo

  awk '{printf "%s\\n", $0}' x > f
  $HOME/server-config/chat_bot.sh f
  sleep 2
fi

rm -f x f
