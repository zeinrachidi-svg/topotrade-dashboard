#!/usr/bin/env python3
"""Regenerates data/team/<token>.json (personal dashboards) from the live index.html.
Usage: TEAM_TOKENS='{"Georges":"...",...}' GH_TOKEN=... python3 build_team_data.py"""
import json,re,os,base64,datetime,urllib.request,urllib.error
from bs4 import BeautifulSoup
REPO="zeinrachidi-svg/topotrade-dashboard"; GH=os.environ["GH_TOKEN"]; tokens=json.loads(os.environ["TEAM_TOKENS"])
def api(method,path,body=None,raw=False):
    req=urllib.request.Request(f"https://api.github.com/repos/{REPO}/contents/{path}",data=json.dumps(body).encode() if body else None,method=method,
      headers={"Authorization":f"Bearer {GH}","Accept":"application/vnd.github+json","User-Agent":"team-build"})
    try: return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e: return {"err":e.code}
def push(path,text):
    cur=api("GET",path); body={"message":"Refresh personal dashboard data","branch":"main","content":base64.b64encode(text.encode()).decode()}
    if cur.get("sha"): body["sha"]=cur["sha"]
    r=api("PUT",path,body); print(path,"ok" if "content" in r else r)
cur=api("GET","index.html"); 
if cur.get("content"): HTML=base64.b64decode(cur["content"]).decode()
else: HTML=urllib.request.urlopen(urllib.request.Request(cur["download_url"],headers={"Authorization":f"Bearer {GH}","User-Agent":"x"})).read().decode()

s=BeautifulSoup(HTML,"html.parser")
def sect(t):
    for h in s.find_all("h2"):
        if h.get_text().strip().startswith(t): return h
def after(h):
    for el in h.next_siblings:
        if getattr(el,"name",None)=="h2": break
        if getattr(el,"name",None): yield el
def tbl(h,i=0):
    ts=[e for e in after(h) if e.name=="table"]
    t=ts[i]
    rows=t.find_all("tr")
    cols=[c.get_text(" ",strip=True) for c in rows[0].find_all(["th","td"])]
    data=[[c.decode_contents().strip() for c in r.find_all("td")] for r in rows[1:]]
    return cols,data
def txt(x): return BeautifulSoup(x,"html.parser").get_text(" ",strip=True)

PEOPLE=[("Georges","Georges Labaky","Sales rep, Americas"),("Claude","Claude Nakhle","Sales rep, Asia / MEA"),
("Mireille","Mireille Baho","Sales rep, Europe / Australia, draft QA, eBay"),("Daniel","Daniel Llorente","Sales rep, France"),
("Zein","Zein Rachidi","CEO"),("Celine","Celine Fleyfel","Marketing"),("Yara","Yara Korh","Team member")]
def mine(first,owner): return first.lower() in txt(owner).lower()



sc=sect("Sales Team Comparison")
ytd_cols,ytd=tbl(sc,0); mtd_cols,mtd=tbl(sc,1)
crm_cols,crm=tbl(sect("CRM Pipeline by Rep"))
def row(rows,full): 
    for r in rows:
        if txt(r[0])==full: return [txt(c) for c in r]
# recs
recs={}
rh=sect("Recommended Actions per Rep")
cur=None;mode=None
for el in after(rh):
    if el.name=="h3": cur=el.get_text(strip=True); recs[cur]={"deal":[],"admin":[]}; continue
    if el.name=="p" and cur:
        t=el.get_text(strip=True)
        mode="deal" if t.startswith("Deal-Closing") else "admin" if t.startswith("Admin") else mode
    if el.name=="ol" and cur and mode: recs[cur][mode]=[li.decode_contents().strip() for li in el.find_all("li",recursive=False)]
# Celine recs
ch=sect("Recommended Actions for Celine")
celine_recs=[li.decode_contents().strip() for li in next(e for e in after(ch) if e.name=="ol").find_all("li",recursive=False)]
# tables
q_cols,q=tbl(sect("Open Offers"))
d_cols,drafts=tbl(sect("Pending Drafts"))
sh_cols,ship=tbl(sect("Ongoing Shipments"))
n_cols,nud=tbl(sect("Self-Serve Nudge"))
f_cols,fol=tbl(sect("Rep Actions Follow-Up"))
admin=[]
for t in ["Topotrade LLC FZ","Digital Realities SASU (France)","9494-1440","Group / cross"]:
    h=sect(t); c,rows=tbl(h)
    for r in rows: admin.append([t.split(" (")[0].replace("9494-1440","9494-1440 Québec")]+r)
a_cols=["Company"]+c
hot=[]
hh=sect("Hot Leads")
for card in hh.find_all_next("div",class_=re.compile("card")):
    if card.find_previous("h2") is not hh: break
    hot.append(card.decode_contents().strip())
# marketing KPIs
m=s.find(id="marketing")
mk=[]
grid=m.find(class_=re.compile("kpi"))
for c in grid.find_all(class_=re.compile("kpi|card"),recursive=False) if grid else []:
    mk.append(c.get_text(" | ",strip=True))
R=(dict(ytd_cols=ytd_cols,ytd=[[txt(c) for c in r] for r in ytd],mtd_cols=mtd_cols,mtd=[[txt(c) for c in r] for r in mtd],
 crm_cols=crm_cols,crm=[[txt(c) for c in r] for r in crm],recs=recs,celine_recs=celine_recs,q_cols=q_cols,q=q,d_cols=d_cols,drafts=drafts,
 sh_cols=sh_cols,ship=ship,n_cols=n_cols,nud=nud,f_cols=f_cols,fol=fol,a_cols=a_cols,admin=admin,hot=hot,mk=mk))

PEOPLE=[("Georges","Georges Labaky","Sales rep, Americas"),("Claude","Claude Nakhle","Sales rep, Asia / MEA"),
("Mireille","Mireille Baho","Sales rep, Europe / Australia, draft QA, eBay"),("Daniel","Daniel Llorente","Sales rep, France"),
("Zein","Zein Rachidi","CEO"),("Celine","Celine Fleyfel","Marketing"),("Yara","Yara Korh","Team member")]
def mine(first,x): return first.lower() in txt(x).lower()
def find(rows,full): 
    for r in rows:
        if r[0]==full: return r
m_asof=re.search(r"As of ([0-9A-Za-z ,]{4,30})",s.get_text())
asof=(m_asof.group(1).strip() if m_asof else str(datetime.date.today()))+" (from the daily run)"
out={}
for first,full,role in PEOPLE:
    P=dict(name=full,first=first,role=role,asOf=asof,updatedAt=datetime.datetime.utcnow().isoformat()+"Z",kpis=[],tables=[],recs=[],tasks=[],note="")
    if first in("Georges","Claude","Mireille","Daniel","Zein"):
        y=find(R["ytd"],full); mt=find(R["mtd"],full); team=find(R["ytd"],"Team"); tmt=find(R["mtd"],"Team"); c=find(R["crm"],full)
        P["kpis"]=[dict(label="Revenue YTD",value=y[1],sub=f"{y[6]} vs same period 2025"),dict(label="Gross profit YTD",value=y[2],sub=f"GM {y[4]}"),
          dict(label="Transactions YTD",value=y[3],sub=f"team total {team[3]}"),dict(label="Revenue MTD (Oct)",value=mt[1],sub=f"{mt[3]} tx, GP {mt[2]}"),
          dict(label="Open opportunities",value=c[1],sub=f"expected {c[2]}")]
        P["tables"]=[dict(title="Year to date vs last year",cols=R["ytd_cols"],rows=R["ytd"],hl=full),
                     dict(title="Month to date",cols=R["mtd_cols"],rows=R["mtd"],hl=full),
                     dict(title="Your biggest open deals",cols=["Deal"],rows=[[d.strip()] for d in c[3].split("; ")])]
        P["recs"]=[dict(title="Deal-closing actions",items=R["recs"][full]["deal"]),dict(title="Admin & housekeeping",items=R["recs"][full]["admin"])]
        q=[r for r in R["q"] if txt(r[2])==full]
        if first=="Zein": q+= [r for r in R["q"] if txt(r[2]) in("Contact","(none)")]
        P["tasks"].append(dict(title="Open quotations to follow up"+(" (incl. unassigned)" if first=="Zein" else ""),cols=R["q_cols"],rows=q,
            note="All are 5+ business days old with no confirmation. Pick the recent, real-customer ones first (see your deal-closing list)."))
        pk=[r for r in R["ship"] if mine(first,r[4])]
        P["tasks"].append(dict(title="Shipments you own",cols=R["sh_cols"],rows=pk))
        P["tasks"].append(dict(title="Self-serve nudges you own",cols=R["n_cols"],rows=[r for r in R["nud"] if mine(first,r[3])]))
        P["tasks"].append(dict(title="Admin tasks you own",cols=R["a_cols"],rows=[r for r in R["admin"] if mine(first,r[5])]))
        P["tasks"].append(dict(title="Yesterday's actions, follow-up",cols=R["f_cols"],rows=[r for r in R["fol"] if mine(first,r[0])]))
        dr=R["drafts"] if first=="Mireille" else []
        P["tasks"].append(dict(title="Drafts waiting for review"+("" if first=="Mireille" else " (Mireille reviews all drafts)"),cols=R["d_cols"],rows=dr))
        hl=[h for h in R["hot"] if first.lower() in txt(h).lower()]
        P["tasks"].append(dict(title="Hot leads naming you",cols=["Lead"],rows=[[h] for h in hl]))
        if first=="Zein":
            P["tables"].insert(0,dict(title="Pipeline by rep (company)",cols=R["crm_cols"],rows=R["crm"]))
            P["tasks"][3]["title"]="Admin tasks you own (all companies)"
    elif first=="Celine":
        P["kpis"]=[dict(label=k.split(" | ")[0],value=k.split(" | ")[1].replace("●","").strip() or "n/a",sub=" ".join(k.split(" | ")[2:])) for k in R["mk"]]
        P["recs"]=[dict(title="Your 10 recommended actions",items=R["celine_recs"])]
        P["tasks"].append(dict(title="Drafts waiting for your approval",cols=R["d_cols"],rows=[r for r in R["drafts"] if re.search("campaign|social|LinkedIn|Facebook|post",txt(r[0]),re.I)]))
        P["tasks"].append(dict(title="Admin tasks you own",cols=R["a_cols"],rows=[r for r in R["admin"] if mine(first,r[5])]))
        P["note"]="Ready-to-use suggested posts (sold items, latest listings, wanted items) are on the main dashboard's Marketing tab."
    else:
        P["note"]="Your page is ready, but no daily data feeds it yet (no Odoo salesperson record or Cockpit sales rows under your name). Tell Zein if you should get a rep-style or marketing-style view."
    push(f"data/team/{tokens[first]}.json",json.dumps(P,ensure_ascii=False))
    out[first]=sum(len(t["rows"]) for t in P["tasks"])
print(out)
