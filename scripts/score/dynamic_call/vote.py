import json
import sys

if __name__ == '__main__':
    network = sys.argv[1]
    uid = sys.argv[2]
    answer = sys.argv[3]

    score_address_txt = "./config/" + network + "/score_address.txt"

    call = json.loads(open("./calls/vote.json", "rb").read())
    call["params"]["to"] = open(score_address_txt, "r").read()

    call["params"]["data"]["params"]["uid"] = uid
    call["params"]["data"]["params"]["answer"] = answer

    print(json.dumps(call))
