import json
import sys

if __name__ == '__main__':
    network = sys.argv[1]
    end = sys.argv[2]
    quorum = sys.argv[3]
    question = sys.argv[4]
    answers = sys.argv[5]
    voters = sys.argv[6]

    score_address_txt = "./config/" + network + "/score_address.txt"

    call = json.loads(open("./calls/create_referendum.json", "rb").read())
    call["params"]["to"] = open(score_address_txt, "r").read()

    call["params"]["data"]["params"]["end"] = end
    call["params"]["data"]["params"]["quorum"] = quorum
    call["params"]["data"]["params"]["question"] = question
    call["params"]["data"]["params"]["answers"] = answers
    call["params"]["data"]["params"]["voters"] = voters

    print(json.dumps(call))
