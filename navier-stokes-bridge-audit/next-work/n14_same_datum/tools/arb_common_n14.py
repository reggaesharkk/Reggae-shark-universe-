"""Shared decimal-outward and aggregate helpers for N14 Arb validation."""
from decimal import Decimal
from math import ceil, floor
import hashlib, json
import numpy as np
from flint import arb, ctx

H=.000025
STEPS=120

def decimal_upper(x,places=12):
    unit=10**places
    number=ceil(float(x)*unit)+2
    while not arb(str(Decimal(number)/unit))>x:
        number+=1
    return str(Decimal(number)/unit)

def decimal_lower(x,places=12):
    unit=10**places
    number=floor(float(x)*unit)-2
    while not arb(str(Decimal(number)/unit))<x:
        number-=1
    return str(Decimal(number)/unit)

def aggregate(directory):
    ctx.prec=128
    metadata=json.loads((directory/"metadata.json").read_text())
    nodes=np.load(directory/"nodes.npy",mmap_mode="r")
    rhs=np.load(directory/"rhs.npy",mmap_mode="r")
    if metadata["initial_error_bound_decimal"]!="0":
        raise ValueError("certificate requires exact zero initial error")
    E=arb(0); maximum_R=arb(0); maximum_M=arb(0)
    for step in range(STEPS):
        row=json.loads((directory/f"{step:03d}.json").read_text())
        if row["step"]!=step:
            raise ValueError("step mismatch")
        if step==0 and row.get("exact_rational_initial_field_sha256")!=metadata["witness_sha256"]:
            raise ValueError("segment zero must start at exact rational witness")
        digest=hashlib.sha256(b"".join(x.tobytes() for x in (
            nodes[step],nodes[step+1],rhs[step],rhs[step+1]
        ))).hexdigest()
        if digest!=row["input_binary_sha256"]:
            raise ValueError(f"segment {step} input hash mismatch")
        R=arb(row["residual_L2_upper_decimal"])
        M=arb(row["gradient_Fourier_l1_upper_decimal"])
        maximum_R=maximum_R.max(R); maximum_M=maximum_M.max(M)
        E=(M*arb("0.000025")).exp()*(E+arb("0.000025")*R)
        E=arb(decimal_upper(E,12))
    result={
        "status":"Arb residual and gradient segment bounds; endpoint F enclosure separate",
        "witness_sha256":metadata["witness_sha256"],
        "h":H,"steps":STEPS,
        "initial_L2_error_upper_decimal":metadata["initial_error_bound_decimal"],
        "maximum_residual_upper_decimal":decimal_upper(maximum_R,12),
        "maximum_gradient_l1_upper_decimal":decimal_upper(maximum_M,6),
        "terminal_L2_error_upper_decimal":decimal_upper(E,12),
        "endpoint_F_certified":False
    }
    (directory/"aggregate.json").write_text(json.dumps(result,indent=2)+"\n")
    return result
