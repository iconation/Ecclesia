#!/bin/bash

. ./scripts/utils/utils.sh

function print_usage {
    usage_header ${0}
    usage_option " -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)"
    usage_option " -u <Referendum ID> : The pool ID"
    usage_option " -a <answer index> : The array indexed answer"
    usage_footer
    exit 1
}

function process {
    if [[ ("$network" == "") || ("$uid" == "") || ("$answer" == "") ]]; then
        print_usage
    fi

    command=$(cat <<-COMMAND
    tbears sendtx <(
        python ./scripts/score/dynamic_call/vote.py
            ${network@Q}
            ${uid@Q}
            ${answer@Q}
        )
        -c ./config/${network}/tbears_cli_config.json
COMMAND
)

    txresult=$(./scripts/icon/txresult.sh -n "${network}" -c "${command}")
    echo -e "${txresult}"
}

# Parameters
while getopts "n:u:a:" option; do
    case "${option}" in
        n)
            network=${OPTARG}
            ;;
        u)
            uid=${OPTARG}
            ;;
        a)
            answer=${OPTARG}
            ;;
        *)
            print_usage 
            ;;
    esac 
done
shift $((OPTIND-1))

process