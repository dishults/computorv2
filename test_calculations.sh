#!/bin/bash

TESTS=(
"a = 1 + 2"
"a = 5 - 2"
"a = 4 / 2"
"a = 5 % 2"
"a = 4 * 2"
"a = 3 / 2 + 3"
"a = 2 * (4 + 5)"
"a = 2 * (4 + 5) / 9"
"a = (4 + 5) / 2 + 1"
"a = (4 + 5) / (2 + 1) + 1"
"a = 1 + (2 + (3 * 5))"
"a = ((3 * 5) + 2) + 1"
"a = (2 + (3 * 5)) + 1"
"varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)"
)

CORRECT=(
"3"
"3"
"2"
"1"
"8"
"4.5"
"18"
"2"
"5.5"
"4"
"18"
"18"
"18"
"27"
)

green="\033[32m"
red="\033[31m"
end="\033[0m"

run_test() {
    #echo -e "\n$green$1$end" && ./computorv2.py "$1"    
    if ! ./computorv2.py "$1" | grep -q "  $2"; then
        echo -e "$red$2$end"
    fi
}

if [ $# = 0 ]; then
    for i in "${!TESTS[@]}"; do
        run_test "${TESTS[i]}" "${CORRECT[i]}"
    done
else
    test=${TESTS[$1 - 4]}
    correct=${CORRECT[$1 - 4]}
    run_test "$test" "$correct"
fi