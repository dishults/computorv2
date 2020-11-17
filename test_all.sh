#!/usr/bin/env bash

TESTS=(
"test_subject_examples"
"test_assignments"
"test_calculations"
"test_errors"
)

green="\033[32m"
red="\033[31m"
end="\033[0m"

run_test() {
    echo -e "\n$green$1$end"
    ./$1.py
}

if [ $# = 0 ]; then
    for i in "${!TESTS[@]}"; do
        run_test "${TESTS[i]}"
    done
else
    test=${TESTS[$1]}
    run_test "$test"
fi