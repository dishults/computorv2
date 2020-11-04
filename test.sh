#!/bin/bash

TESTS=(
"varA = 2"
"varB = 4.242"
"varC = -4.3"
"varA = 2*i + 3"
"varB = -4i - 4"
"varA = [[2,3];[4,3]]"
"varB = [[3,4]]"
"m = [[[1,2];[2,1]];[[1,2];[2,1]]]"
"x = 4i + 4"
"x = 4*i + 4"
"x = 4 + 4i"
"x = 4 + 4*i"
"a = 4i - 4"
"a = 4*i - 4"
"a = 4 - 4i"
"a = 4 - 4*i"
"c = 3 / 4i"
"c = 3 / 4*i"
"c = 4i / 3"
"c = 4*i / 3"
"d = 10 % 4i"
"d = 10 % 4*i"
"d = 10i % 3"
"d = 10*i % 3"
"d = 9*i % 3"
"b = 3 * 4i"
"b = 3 * 4*i"
"b = 4i * 3"
"b = 4*i * 3"
"b = -4*i * 3"
"m = [[3+4i, 2-3i]]"
"f(x) = 2 * x - 5"
"funC(z) = -2 * z - 5"
"f(x) = 4x^2 - 5*x^1 + 4x^0"
"funA(x) = 2*x^5 + 4x^2 - 5*x + 4"
) # 2*x^5+4x^2-5*x+4

CORRECT=(
"  2"
"  4.242"
"  -4.3"
"  3 + 2i"
"  -4 - 4i"
"  \[ 2 , 3 \]
  \[ 4 , 3 \]"
"  \[ 3 , 4 \]"
"  \[ 1 , 2 \]
  \[ 2 , 1 \]
  \[ 1 , 2 \]
  \[ 2 , 1 \]"
"  4 + 4i"
"  4 + 4i"
"  4 + 4i"
"  4 + 4i"
"  -4 + 4i"
"  -4 + 4i"
"  4 - 4i"
"  4 - 4i"
"  0.75i"
"  0.75i"
"  1.3333333333333333i"
"  1.3333333333333333i"
"  2i"
"  2i"
"  i"
"  i"
"  0"
"  12i"
"  12i"
"  12i"
"  12i"
"  -12i"
"  [  3 + 4i ,  2 - 3i ]"
"  2 \* x - 5"
"  -2 \* z - 5"
""
"  2 \* x^5 + 4 \* x^2 - 5\*x + 4"
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