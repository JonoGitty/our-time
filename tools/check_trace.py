#!/usr/bin/env python3
"""Rasterise a traced SVG back and score it against the source bitmap."""
import re, subprocess, sys
FF="/home/jonogunix/bin/ffmpeg"
src_img, svg_path, crop, W = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
raw=subprocess.run([FF,"-v","error","-i",src_img,"-vf",f"crop={crop},scale={W}:-1:flags=lanczos",
  "-f","rawvideo","-pix_fmt","gray","-"],capture_output=True,check=True).stdout
H=len(raw)//W
src=[1 if v>=128 else 0 for v in raw]
svg=open(svg_path,encoding="utf-8").read()
vb=[float(x) for x in re.search(r'viewBox="([^"]+)"',svg).group(1).split()]
loops=[]
for sub in re.search(r'd="([^"]+)"',svg).group(1).split("Z"):
    pts=re.findall(r'(-?[\d.]+)\s+(-?[\d.]+)',sub)
    if len(pts)>=3: loops.append([(float(a),float(b)) for a,b in pts])
sx=vb[2]/W
both=union=0
for y in range(H):
    yy=(y+0.5)*sx; xs=[]
    for L in loops:
        n=len(L)
        for i in range(n):
            x1,y1=L[i]; x2,y2=L[(i+1)%n]
            if (y1>yy)!=(y2>yy): xs.append(x1+(yy-y1)*(x2-x1)/(y2-y1))
    xs.sort(); inside=bytearray(W)
    for i in range(0,len(xs)-1,2):
        a=int(max(0,xs[i]/sx)); b=int(min(W,xs[i+1]/sx+1))
        for x in range(a,b): inside[x]=1
    for x in range(W):
        s=src[y*W+x]; t=inside[x]
        if s and t: both+=1
        if s or t: union+=1
print(f"loops={len(loops)}  IoU={100.0*both/union:.2f}%")
