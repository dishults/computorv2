#!/bin/bash

TESTS=(
"varA = 2"
"varB = 4.242"
"varC = -4.3"
"varA = 2*i + 3"
"varB = -4i - 4"
"a = 4i - 4"
"a = 4*i - 4"
"a = 4 - 4i"
"a = 4 - 4*i"
"varA = [[2,3];[4,3]]"
"varB = [[3,4]]"
)
#[[[1,2];[2,1]];[[1,2];[2,1]]]
CORRECT=(
"  2"
"  4.242"
"  -4.3"
"  3 + 2i"
"  -4 - 4i"
"  -4 + 4i"
"  -4 + 4i"
"  4 - 4i"
"  4 - 4i"
"  \[ 2 , 3 \]
  \[ 4 , 3 \]"
"  \[ 3 , 4 \]"
)

green="\033[32m"
red="\033[31m"
end="\033[0m"

run_test() {
    echo -e "\n$green$1$end" && ./computorv2.py "$1"    
    if ! ./computorv2.py "$1" | grep -q "$2"; then
        echo -e "$red$2$end"
    fi
}

if [ $1 = "all" ]; then
    for i in "${!TESTS[@]}"; do
        run_test "${TESTS[i]}" "${CORRECT[i]}"
    done
else
    test=${TESTS[$1 - 4]}
    correct=${CORRECT[$1 - 4]}
    run_test "$test" "$correct"
fi