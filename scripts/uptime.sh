# run tests
rm -f x f
poetry run uptime > x
sleep 2

# print an update ...
echo -n "."

# look for 'FAIL' in the update output
grep FAIL x
fail=$?
if [ $fail == 0 ]; then
  # got an error...send a text to alert folks of the problem
  dt=`date`
  msg="Uptime tests failed on ${HOSTNAME} at ${dt}:"

  echo
  echo "$msg"
  cat x
  echo

  # format the output for a text, and send it via Mappy
  echo -n "$msg\n\n" > f
  awk '{printf "%s\\n", $0}' x >> f
  $HOME/server-config/chat_bot.sh f
  sleep 2
fi

rm -f x f
