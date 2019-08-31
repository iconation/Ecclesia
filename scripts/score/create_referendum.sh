#!/bin/bash

. ./scripts/utils/utils.sh

function print_usage {
    usage_header ${0}
    usage_option " -n <network> : Network to use (localhost, yeouido, euljiro or mainnet)"
    usage_option " -e <end> : Epoch timestamp for the end of the referendum"
    usage_option " -l <quorum> : Quorum (percentage between 0-100)"
    usage_option " -q <question> : Question of the referendum"
    usage_option " -a <answers> : JSON formatted array with all answers"
    usage_option " -v <voters> : JSON formatted array with all voters"
    usage_footer
    exit 1
}

function process {
    if [[ ("$network" == "") || ("$end" == "") || ("$quorum" == "") || ("$question" == "") || ("$answers" == "") || ("$voters" == "") ]]; then
        print_usage
    fi

    command=$(cat <<-COMMAND
    tbears sendtx <(
        python ./scripts/score/dynamic_call/create_referendum.py
            ${network@Q}
            ${end@Q}
            ${quorum@Q}
            ${question@Q}
            ${answers@Q}
            ${voters@Q}
        )
        -c ./config/${network}/tbears_cli_config.json
COMMAND
)

    txresult=$(./scripts/icon/txresult.sh -n "${network}" -c "${command}")
    echo -e "${txresult}"
}

# Parameters
while getopts "n:e:l:q:a:v:" option; do
    case "${option}" in
        n)
            network=${OPTARG}
            ;;
        e)
            end=${OPTARG}
            ;;
        l)
            quorum=${OPTARG}
            ;;
        q)
            question=${OPTARG}
            ;;
        a)
            answers=${OPTARG}
            ;;
        v)
            voters=${OPTARG}
            ;;
        *)
            print_usage 
            ;;
    esac 
done
shift $((OPTIND-1))

process