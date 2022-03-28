import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from collections import deque
import pandas as pd

def atan2(y,x):
    a=np.arctan2(y,x)
    try:
        for i in range(len(a)):
            if a[i] <0:
                a[i]+=(2*np.pi)
            elif x[i]==0 and y[i]==0:
                a[i]=None
    except:
        if a <0:
            a+=(2*np.pi)
        elif x==0 and y==0:
            a=None
    return a

while(True):
    filename=input('Enter Path for the restrictions on the motion\n')
    if filename == 'q':
        quit()
    #Try to read the file
    try:
        res=pd.read_csv(filename)
        break
    except:
        print("The file you specified could not be found, try again")

filename = filename[:-4]+'len.csv'
lens=pd.read_csv(filename)

#convert values to float
for i in range(len(res)):
    res.loc[i,'w']=np.radians(float(res.loc[i,'w']))
    res.loc[i,'TR']=float(res.loc[i,'TR'])
    res.loc[i,'El']=float(res.loc[i,'El'])
    res.loc[i,'Ex']=float(res.loc[i,'Ex'])
    res.loc[i,'Ey']=float(res.loc[i,'Ey'])
    res.loc[i,'Eth']=np.radians(float(res.loc[i,'Eth']))
    #also converts to radians

#same for the second
for i in range(len(lens)):
    lens.loc[i,'a']=float(lens.loc[i,'a'])
    lens.loc[i,'b']=float(lens.loc[i,'b'])
    lens.loc[i,'c']=float(lens.loc[i,'c'])
    lens.loc[i,'d']=float(lens.loc[i,'d'])
    lens.loc[i,'theta1']=np.radians(float(lens.loc[i,'theta1']))

def PosAna(th2,a):
    #range of -pi to pi
    if abs(th2/np.pi) > 1:
        th2-=2*np.pi*(int(th2/(2*np.pi))+(abs(th2)/th2))
#    print(th2/np.pi)
    #a takes the form [a,b,c,d,th1]
    A=a[1]
    B=-a[2]
    C1=-a[3]*np.cos(a[4])+a[0]*np.cos(th2)
    C2=-a[3]*np.sin(a[4])+a[0]*np.sin(th2)
    p=2*B*C2
    q=2*B*C1
    r=B**2+C1**2+C2**2-A**2
    th4 = [0,0]
    th3 = [0,0]
    t=2*p
    s=r-q
    u=r+q
    th4[0]=2*np.arctan2(-t+np.sqrt(t**2-4*s*u),2*s)
    th4[1]=2*np.arctan2(-t-np.sqrt(t**2-4*s*u),2*s)
    th3[0]=np.arctan2(-B*np.sin(th4[0])-C2,-B*np.cos(th4[0])-C1)
    th3[1]=np.arctan2(-B*np.sin(th4[1])-C2,-B*np.cos(th4[1])-C1)
    return th3,th4

t3=deque(maxlen=2)
t3.appendleft(res.loc[0,'Eth'])
t4=deque(maxlen=2)
t4.appendleft(0)

#making figures
fig, ax=plt.subplots()
bar, = ax.plot([],[],'k.-')

minl=-lens.loc[0,'a']
maxl=lens.loc[len(lens)-1,'c']
minh=-lens.loc[0,'a']
maxh=lens.loc[len(lens)-1,'c']
for i in range(len(lens)):
    maxl+=lens.loc[i,'d']*np.cos(lens.loc[i,'theta1'])
    maxh+=lens.loc[i,'d']*np.sin(lens.loc[i,'theta1'])
if True:
    maxh=max(lens.loc[0,'a'],lens.loc[0,'c'])

def init():
    ax.set_xlim(minl,maxl)
    ax.set_ylim(-maxh,maxh)
    ax.set_aspect('equal')
    return bar,

def update(frame):
    spec = lens.iloc[n]
    an3,an4=PosAna(frame,spec)
    if abs(an3[0]-t3[0])<abs(an3[1]-t3[0]):
        t3.appendleft(an3[0])
    else:
        t3.appendleft(an3[1])
    xs=[0,spec.loc['a']*np.cos(frame),
            spec.loc['a']*np.cos(frame)+spec.loc['b']*np.cos(t3[0]),
#            (spec.loc['d']*np.cos(spec.loc['theta1'])
#                +spec.loc['c']*np.cos(t4[0])),
            spec.loc['d']*np.cos(spec.loc['theta1']),0,]
    ys=[0,spec.loc['a']*np.sin(frame),
            spec.loc['a']*np.sin(frame)+spec.loc['b']*np.sin(t3[0]),
#            (spec.loc['d']*np.sin(spec.loc['theta1'])
#                +spec.loc['c']*np.sin(t4[0])),
            spec.loc['d']*np.sin(spec.loc['theta1']),0]
    bar.set_data(xs,ys)
    return bar,

if False:
    spe = lens.iloc[0]
    a3,a4=PosAna(10/20*np.pi,spe)
    print([a3[0]/np.pi,a3[1]/np.pi])
    print([a4[0]/np.pi,a4[1]/np.pi])

if True:
    n=0
    bara = ani.FuncAnimation(fig,update,frames=np.linspace(0,2*np.pi,256),
            init_func=init,blit=False)
    plt.show()

    filename = filename[:-7]+'bar.mp4'
    bara.save(filename)
