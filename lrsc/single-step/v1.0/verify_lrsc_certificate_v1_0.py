#!/usr/bin/env python3
import numpy as np, math
M=99; k_idx=49; theta=0.08; A=0.50
i=np.arange(M); k=2*np.pi*k_idx/M
X=1.0+A*np.cos(k*i)
left=np.roll(X,1); right=np.roll(X,-1)
j=X-np.minimum(np.minimum(left,X),right)
C=.5*((X-left)**2+(X-right)**2)
m=(C>theta).astype(float)
hm=np.fft.fft(m)/M; hj=np.fft.fft(j)/M; hy=np.fft.fft(m*j)/M
q=np.arange(M); stencil=np.cos(2*np.pi*q/M)-1
E=stencil*hy; n=np.linalg.norm(E)
V=np.zeros((50,M),complex)
V[0]=stencil*(hj[0]*hm)
for r in range(1,50):
    rc=M-r
    V[r]=stencil*(hj[r]*np.roll(hm,r)+hj[rc]*np.roll(hm,rc))
closure=np.linalg.norm(E-V.sum(axis=0))/n
ledger={1:(49,),2:(48,49),3:(0,1,49),4:(0,1,48,49),5:(0,1,3,48,49),6:(0,1,46,47,48,49),7:(0,1,45,46,47,48,49),8:(0,1,44,45,46,47,48,49),9:(0,1,43,44,45,46,47,48,49),10:(0,1,42,43,44,45,46,47,48,49),11:(0,1,3,42,43,44,45,46,47,48,49)}
print("LRSC SINGLE-STEP SPECTRAL CERTIFICATE v1.0")
print("M=99 k_idx=49 theta=0.08 A=0.50 channels=50")
print("N_act =",int(m.sum()))
print("closure_error =",format(closure,'.17g'))
for K,S in ledger.items():
    err=np.linalg.norm(E-V[list(S)].sum(axis=0))/n
    print(K,S,format(err,'.17g'),"PASS" if err<=.001 else "FAIL")
assert int(m.sum())==81
assert closure<1e-14
assert np.linalg.norm(E-V[list(ledger[10])].sum(axis=0))/n>.001
assert np.linalg.norm(E-V[list(ledger[11])].sum(axis=0))/n<=.001
print("THRESHOLD BRACKET VERIFIED: K10 fails, K11 passes.")
