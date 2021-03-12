def ml(num):
    if num>0:
        return 100/(num+100)
    else:
        return -num/(100-num)
def mlAdj(m1,m2):
    return m1/(m1+m2),m2/(m1+m2)

def mlAdj2(m1,adj1,m2,adj2):
    m1*=adj1
    m2*=adj2
    return m1/(m1+m2),m2/(m1+m2)
def mlOut(ml,bet=1):
    if ml>0:
        return bet*ml/100
    else:
        return bet*(100/-ml)
        

teams=dict()

def prs(line):
    line.replace(' ','')
    line=line.split(',')
    return line[3],int(line[8]),int(line[11])

with open("nba2018.csv") as f:
    lines=f.read().splitlines()
print(lines.pop(0))
for i in range(len(lines)//4):
    t1=prs(lines[2*i])
    t2=prs(lines[2*i+1])
    if t1[0] not in teams:
        teams[t1[0]]={"exp":0,"act":0}
    if t2[0] not in teams:
        teams[t2[0]]={"exp":0,"act":0}
    if t1[1]>t2[1]:
        teams[t1[0]]["act"]+=1
    else:
        teams[t2[0]]["act"]+=1
    ml1=ml(t1[2])
    ml2=ml(t2[2])
    ml1,m2=mlAdj(ml1,ml2)
    teams[t1[0]]["exp"]+=ml1
    teams[t2[0]]["exp"]+=ml2
for team in teams.keys():
    print(team)
    teams[team]['rat']=teams[team]['act']/teams[team]['exp']
    print(teams[team]['rat'])
oldTeams=teams
teams=dict()
for i in range(10):
    for i in range(len(lines)//4):
        t1=prs(lines[2*i])
        t2=prs(lines[2*i+1])
        if t1[0] not in teams:
            teams[t1[0]]={"exp":0,"act":0}
        if t2[0] not in teams:
            teams[t2[0]]={"exp":0,"act":0}
        if t1[1]>t2[1]:
            teams[t1[0]]["act"]+=1
        else:
            teams[t2[0]]["act"]+=1
        ml1=ml(t1[2])
        adj1=oldTeams[t1[0]]["rat"]
        ml2=ml(t2[2])
        adj2=oldTeams[t2[0]]["rat"]
        ml1,m2=mlAdj2(ml1,adj1,ml2,adj2)
        teams[t1[0]]["exp"]+=ml1
        teams[t2[0]]["exp"]+=ml2
    for team in teams.keys():
        teams[team]['rat']=teams[team]['act']/teams[team]['exp']
    oldTeams=teams
for i in range(10):
    print()
for team in teams.keys():
    print(team)
    teams[team]['rat']=teams[team]['act']/teams[team]['exp']
    print(teams[team]['rat'])      


def bet(team1,team2):
    name1=team1[0]
    name2=team2[0]
    ml1=team1[2]
    ml2=team2[2]
    originalOdds1=ml(ml1)
    originalOdds2=ml(ml2)
    newOdds1,newOdds2=mlAdj2(originalOdds1,teams[name1]['rat'],originalOdds2,teams[name2]['rat'])
    if newOdds1>originalOdds1:
        return 1, 10#newOdds1/(newOdds1-originalOdds1)
    if newOdds2>originalOdds2:
        return 2, 10#newOdds2/(newOdds2-originalOdds2)
    return 0,0
def winner(team1,team2):
    if team1[1]>team2[1]:
        return 1
    return 2
def wager(team1,team2, pick,conf):
    if pick!=winner(team1,team2):
        return -conf
    else:
        return mlOut([False,team1,team2][pick][2],conf)




tot=0
count=0
confs=[]
amountb=0
for i in range(len(lines)//4, len(lines)//2-40):
    t1=prs(lines[2*i])
    t2=prs(lines[2*i+1])
    pick,conf=bet(t1,t2)
    confs.append(conf)
    if winner!=0 and 30>conf>5:
        amountb+=conf
        count+=1
        tot+=wager(t1,t2,pick,conf)
        


    t1=prs(lines[2*i])
    t2=prs(lines[2*i+1])
    if t1[1]>t2[1]:
        teams[t1[0]]["act"]+=1
    else:
        teams[t2[0]]["act"]+=1
    ml1=ml(t1[2])
    adj1=teams[t1[0]]["rat"]
    ml2=ml(t2[2])
    adj2=teams[t2[0]]["rat"]
    ml1,m2=mlAdj2(ml1,adj1,ml2,adj2)
    teams[t1[0]]["exp"]+=ml1
    teams[t2[0]]["exp"]+=ml2
    teams[t1[0]]["rat"]+=teams[t1[0]]['act']/teams[t1[0]]['exp']
    teams[t2[0]]["rat"]+=teams[t2[0]]['act']/teams[t2[0]]['exp']
    
