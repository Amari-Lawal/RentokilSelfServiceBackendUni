if [[ $1 == "" ]]
then
  python -m unittest aiunit.AIUnittest
else
  python -m unittest aiunit.AIUnittest.$1
fi