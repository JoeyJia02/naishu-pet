"""Encode existing RGBA frames as full-canvas APNG; no pixel editing."""
import struct,zlib,io,math
from pathlib import Path
from PIL import Image
SIG=b'\x89PNG\r\n\x1a\n'
def chunks(blob):
 p=8
 while p<len(blob):
  n=int.from_bytes(blob[p:p+4],'big');t=blob[p+4:p+8];d=blob[p+8:p+8+n];yield t,d;p+=12+n

def chunk(t,d):return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
def save_full_apng(frames,durations,path):
 assert len(frames)==len(durations)>0
 encoded=[]
 for f in frames:
  b=io.BytesIO();f.convert('RGBA').save(b,format='PNG');parts=list(chunks(b.getvalue()));ihdr=next(d for t,d in parts if t==b'IHDR');data=b''.join(d for t,d in parts if t==b'IDAT');encoded.append((ihdr,data))
 assert all(h==encoded[0][0] for h,d in encoded)
 w,h=frames[0].size;out=bytearray(SIG);out+=chunk(b'IHDR',encoded[0][0]);out+=chunk(b'acTL',struct.pack('>II',len(frames),0));seq=0
 for i,((header,data),delay) in enumerate(zip(encoded,durations)):
  num=int(round(delay));den=1000;g=math.gcd(num,den);num//=g;den//=g
  out+=chunk(b'fcTL',struct.pack('>IIIIIHHBB',seq,w,h,0,0,num,den,0,0));seq+=1
  if i==0:out+=chunk(b'IDAT',data)
  else:out+=chunk(b'fdAT',struct.pack('>I',seq)+data);seq+=1
 out+=chunk(b'IEND',b'');Path(path).parent.mkdir(parents=True,exist_ok=True);Path(path).write_bytes(out)
 # Exact complete-frame decoding check, not merely dimensions.
 test=Image.open(path);assert test.n_frames==len(frames)
 for i,(f,ms) in enumerate(zip(frames,durations)):
  test.seek(i);assert test.convert('RGBA').tobytes()==f.convert('RGBA').tobytes(),i;assert abs(test.info['duration']-ms)<0.01
 return {'frames':len(frames),'duration_ms':sum(durations),'bytes':len(out),'canvas':[w,h],'dispose':0,'blend':0,'full_frame_rectangles':True,'pillow_exact':True}
if __name__=='__main__':
 import argparse,json
 p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');a=p.parse_args();im=Image.open(a.input);fs=[];ds=[]
 for i in range(im.n_frames):im.seek(i);fs.append(im.convert('RGBA').copy());ds.append(im.info['duration'])
 print(json.dumps(save_full_apng(fs,ds,a.output),indent=2))
