#!/bin/bash

. ./scripts/utils/utils.sh

function print_usage {
    usage_header ${0}
    usage_option " -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)"
    usage_option " -r <referendum ID> : The referendum ID"
    usage_option " -a <answer index> : The array indexed answer"
    usage_option " -w <weight> : The voter weight for the corresponding answer"
    usage_footer
    exit 1
}

function process {
    if [[ ("$network" == "") || ("$referendum_id" == "") || ("$answer" == "") || ("$weight" == "") ]]; then
        print_usage
    fi

    command=$(cat <<-COMMAND
    tbears sendtx <(
        python ./scripts/score/dynamic_call/vote.py
            ${network@Q}
            ${referendum_id@Q}
            ${answer@Q}
            ${weight@Q}
        )
        -c ./config/${network}/tbears_cli_config.json
COMMAND
)

    txresult=$(./scripts/icon/txresult.sh -n "${network}" -c "${command}")
    echo -e "${txresult}"
}

# Parameters
while getopts "n:r:a:w:" option; do
    case "${option}" in
        n)
            network=${OPTARG}
            ;;
        r)
            referendum_id=${OPTARG}
            ;;
        a)
            answer=${OPTARG}
            ;;
        w)
            weight=${OPTARG}
            ;;
        *)
            print_usage 
            ;;
    esac 
done
shift $((OPTIND-1))

process