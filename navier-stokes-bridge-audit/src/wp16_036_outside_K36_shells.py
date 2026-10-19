"""Summarize already reconstructed outside-K36 source groups by wavevector radius."""

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


def radius(row):
    return max(math.sqrt(sum(x*x for x in row[k])) for k in ("left_orbit","right_orbit"))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--breakdown-json",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    payload=json.loads(a.breakdown_json.read_text())
    result={"status":"post-hoc shell decomposition of outside K36", "bins":["<8","8-10","10-12","12-13"],"N":{}}
    for N,states in payload["N"].items():
        result["N"][N]={}
        for state,data in states.items():
            acc=defaultdict(lambda:{"count":0,"signed":0.0,"absolute":0.0})
            for row in data["outside_groups_ranked_by_absolute_contribution"]:
                R=radius(row)
                key="<8" if R<8 else "8-10" if R<10 else "10-12" if R<12 else "12-13"
                value=row["alpha_dot_contribution"]
                acc[key]["count"]+=1
                acc[key]["signed"]+=value
                acc[key]["absolute"]+=abs(value)
            result["N"][N][state]=dict(acc)
    a.output.write_text(json.dumps(result,indent=2)+"\n")
    print("SAVED",a.output)


if __name__=="__main__":main()
