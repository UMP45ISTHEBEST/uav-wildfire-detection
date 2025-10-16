from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
import random

def save(arr,p): Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).save(p)
def fire(h=256,w=256):
    img=np.random.normal(30,8,(h,w))
    for _ in range(np.random.randint(1,4)):
        cx,cy=np.random.randint(w//5,4*w//5),np.random.randint(h//5,4*h//5); r=np.random.randint(15,45)
        y,x=np.ogrid[:h,:w]; img+=np.exp(-((x-cx)**2+(y-cy)**2)/(2*r*r))*np.random.uniform(120,200)
    return img
def nofire(h=256,w=256):
    img=np.random.normal(45,12,(h,w))
    return np.array(Image.fromarray(np.clip(img,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))) if random.random()<0.5 else img
def gen(root,split,nf,nn):
    for cls,n,fn in [('fire',nf,fire),('no_fire',nn,nofire)]:
        d=Path(root)/split/cls; d.mkdir(parents=True,exist_ok=True)
        for i in range(n): save(fn(), d/f"{cls}_{i:04d}.png")

for s in ["train","val","test"]:
    (Path("data")/s/"fire").mkdir(parents=True,exist_ok=True)
    (Path("data")/s/"no_fire").mkdir(parents=True,exist_ok=True)
gen("data","train",200,200); gen("data","val",40,40); gen("data","test",40,40)
print("✅ Dummy dataset ready under data/ …")
