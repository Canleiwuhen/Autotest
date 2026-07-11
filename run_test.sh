#!/bin/bash

test_case=$1
test_severity=$2
test_ignore_path=$3

# workon api-forward

pytest .${test_case} --alluredir=allure_results --clean-alluredir --allure-severities=${test_severity} --ignore=.${test_ignore_path}

exit 0