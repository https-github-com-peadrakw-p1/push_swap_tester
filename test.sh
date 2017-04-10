#!/bin/bash


RANGE=$(seq "$1")
RUNTIME=$3
TOTAL=$((0))

print_status () {
	echo "list:"
	echo "$ARG"
	echo "is sorted:"
	echo "$RES"
	echo "line count:"
	echo "$LC"
}

print_final () {
	echo "average number of operations"
	echo $(($TOTAL / $RUNTIME))
	echo "times failed:"
	echo $((fail))
	echo "times ran:"
	echo $RUNTIME
	echo "Percentage failed (Rounded to the tenth place)"
	echo $(((fail * 1000) / $RUNTIME))
}

declare -i fail=$((0))

for ((i = 0; i < $RUNTIME; i++))
do
	ARG=$(echo "$RANGE" | tr " " "\n" | perl -MList::Util=shuffle -e 'print shuffle<STDIN>' | tr "\n" " ")
	INSTR=$(./push_swap "$ARG")
	RES=$(echo "$INSTR" | ./checker "$ARG")
	LC=$(echo "$INSTR" | wc -l | tr -d " ")
	TOTAL=$(($TOTAL + $LC))
	if [ "$RES" != "OK" ]
	then
		print_status
		break
	fi
	if [ "$LC" -gt $2 ]
	then
		print_status
		fail=$((fail + 1))
	fi
	echo "$((i)) $LC"
done
print_final
