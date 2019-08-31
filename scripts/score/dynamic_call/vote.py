import json
import sys

if __name__ == '__main__':
    network = sys.argv[1]
    referendum_id = sys.argv[2]
    answer = sys.argv[3]
    weight = sys.argv[4]

    score_address_txt = "./config/" + network + "/score_address.txt"

    call = json.loads(open("./calls/vote.json", "rb").read())
    call["params"]["to"] = open(score_address_txt, "r").read()

    call["params"]["data"]["params"]["referendum_id"] = referendum_id
    call["params"]["data"]["params"]["answer"] = answer
    call["params"]["data"]["params"]["weight"] = weight

    print(json.dumps(call))
