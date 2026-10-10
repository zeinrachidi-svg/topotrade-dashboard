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
_a=s.find(class_="asof")
asof=(_a.get_text(strip=True).replace("As of ","") if _a else str(datetime.date.today()))+" (daily run)"
out={}
_m={r[0]:r for r in R["mtd"]}
TEAM_COLS=["Rep","RevRec YTD","GPRec YTD","Tx YTD","RevRec MTD","GPRec MTD","Tx MTD"]
TEAM_ROWS=[[r[0],r[1],r[2],r[3]]+(_m[r[0]][1:4] if r[0] in _m else ["-","-","-"]) for r in R["ytd"]]

# ---------- extra finance tables (billings comparison, personal P&Ls) ----------
import csv as _csv
def _money(v,cur="$"): 
    return "-" if v is None else ("-" if v<0 else "")+cur+f"{abs(v):,.0f}"
def _pct(a,b): return "n/a" if not b else f"{(a-b)/abs(b)*100:+.0f}%"
def _prev(tok):
    cur=api("GET",f"data/team/{tok}.json")
    try: return json.loads(base64.b64decode(cur["content"]).decode())
    except Exception: return {}
def billings_table(path,asof):
    import re as _re
    rows=list(_csv.reader(open(path,encoding="utf-8")))
    h=rows[0]; iD=h.index("Date"); iI=[i for i,x in enumerate(h) if x.replace(" ","")=="Invoicenumber"][0]; iB=h.index("Billings excl Tax")
    mo={m:i+1 for i,m in enumerate(["january","february","march","april","may","june","july","august","september","october","november","december"])}
    def pd(x):
        x=x.strip(); m=_re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})$",x)
        if m: return datetime.date(int(m[3]),int(m[2]),int(m[1]))
        m=_re.match(r"(\d{1,2}) ([A-Za-z]+) (\d{4})$",x)
        if m: return datetime.date(int(m[3]),mo[m[2].lower()],int(m[1]))
    def num(x):
        x=_re.sub(r"[^\d.\-]","",x or ""); return float(x) if x not in("","-",".") else 0.0
    ents=[("FR","Digital Realities SASU (France)"),("AE","Topotrade LLC FZ (UAE)"),("CA","9494-1440 Quebec (Canada)")]
    a={e:dict(y26=0,y25=0,m26=0,m25=0) for e,_ in ents}
    for r in rows[1:]:
        if len(r)<=iB: continue
        d=pd(r[iD])
        if not d: continue
        inv=r[iI].strip(); e="CA" if inv.startswith("CA") else "AE" if inv.startswith("AE") else "FR"
        b=num(r[iB])
        for yr,k in((asof.year,"26"),(asof.year-1,"25")):
            cut=datetime.date(yr,asof.month,min(asof.day,28 if (asof.month==2 and asof.day>28) else asof.day))
            if d.year==yr and d<=cut:
                a[e]["y"+k]+=b
                if d.month==asof.month: a[e]["m"+k]+=b
    tot=dict(y26=0,y25=0,m26=0,m25=0); out=[]
    for e,name in ents:
        v=a[e]; [tot.__setitem__(k,tot[k]+v[k]) for k in v]
        out.append([name,_money(v["y26"],"EUR "),_money(v["y25"],"EUR "),_pct(v["y26"],v["y25"]),_money(v["m26"],"EUR "),_money(v["m25"],"EUR "),_pct(v["m26"],v["m25"])])
    out.append(["<b>Total</b>"]+[f"<b>{x}</b>" for x in [_money(tot["y26"],"EUR "),_money(tot["y25"],"EUR "),_pct(tot["y26"],tot["y25"]),_money(tot["m26"],"EUR "),_money(tot["m25"],"EUR "),_pct(tot["m26"],tot["m25"])]])
    mn=asof.strftime("%b")
    return dict(title="Billings by billing company: YTD and MTD vs last year",
        cols=["Billing company",f"YTD {asof.year}",f"YTD {asof.year-1}","YoY",f"MTD {mn} {asof.year}",f"MTD {mn} {asof.year-1}","YoY"],rows=out,
        note=f"Billings excl. tax in EUR from the Cockpit Sales tab, 1 Jan to {asof.day} {mn} each year. Entity = invoice prefix (CA = Canada, AE = UAE, numbers or blank = France, so not-yet-invoiced Topotrade sales are included). Live sheet, so it can differ slightly from the main dashboard snapshot.")
def pl_canada(path):
    import openpyxl
    ws=openpyxl.load_workbook(path,data_only=True)["P&L Canada"]
    rows=[list(r) for r in ws.iter_rows(values_only=True)]
    st=next(i for i,r in enumerate(rows) if r[1] and "Revenue & GP recognition" in str(r[1]))
    out=[];T=dict(rev=0,gp=0,fc=0,np=0,tr=0,tg=0)
    for r in rows[st+2:]:
        if r[1]=="Total" or not hasattr(r[1],"year"): break
        if r[2] is None: continue
        out.append([r[1].strftime("%b %Y"),_money(r[2]),_money(r[6]),_money(r[7]),_money(r[8]),_money(r[9]),_money(r[10]),_money(r[11])])
        T["rev"]+=r[2];T["gp"]+=r[6];T["fc"]+=r[7];T["np"]+=r[8];T["tr"]+=r[10] or 0;T["tg"]+=r[11] or 0
    out.append(["<b>YTD</b>"]+[f"<b>{x}</b>" for x in [_money(T["rev"]),_money(T["gp"]),_money(T["fc"]),_money(T["np"]),"",_money(T["tr"]),_money(T["tg"])]])
    out.append(["<b>% of YTD target</b>",f"<b>{T['rev']/T['tr']*100:.0f}%</b>" if T["tr"] else "",f"<b>{T['gp']/T['tg']*100:.0f}%</b>" if T["tg"] else "","","","","",""])
    return dict(title="Topotrade Canada: YTD P&L (USD, revenue and GP recognition)",cols=["Month","RevRec","GPRec","Fixed cost","Net profit","Cumulated profit","RevRec target","GPRec target"],rows=out,
        note="From the 'Cockpit Report Canada' workbook, P&L Canada tab. YTD = months with actuals; later months only carry budgeted fixed costs.")
def pl_france(path):
    import openpyxl
    ws=openpyxl.load_workbook(path,data_only=True)["P&L"]
    rows=[list(r) for r in ws.iter_rows(values_only=True)]
    g=[];cur=None
    for c in rows[2]:
        cur=c or cur; g.append(cur)
    names=rows[3]; out=[];T=dict(rev=0,gp=0,fr=0,pl=0); grp={}
    for r in rows[4:]:
        if not hasattr(r[1],"year") : break
        if r[2] is None or r[1].month>_asof_d.month: continue
        out.append([r[1].strftime("%b %Y")+(" (month to date)" if False else ""),_money(r[2],"EUR "),_money(r[3],"EUR "),_money(r[5],"EUR "),_money(r[4],"EUR ")])
        T["rev"]+=r[2];T["gp"]+=r[3];T["fr"]+=r[5] or 0;T["pl"]+=r[4] or 0
        for i in range(6,len(r)):
            if isinstance(r[i],(int,float)) and g[i]: grp[g[i]]=grp.get(g[i],0)+r[i]
    out.append(["<b>YTD</b>"]+[f"<b>{x}</b>" for x in [_money(T["rev"],"EUR "),_money(T["gp"],"EUR "),_money(T["fr"],"EUR "),_money(T["pl"],"EUR ")]])
    t1=dict(title="Digital Realities France: YTD P&L (EUR)",cols=["Month","RevRec","GPRec","Total costs","P&L"],rows=out,
        note="From the 'Cockpit Report France DR' workbook, P&L tab. The latest month is month-to-date. Nov and Dec only hold budgeted costs and are not in YTD.")
    t2=dict(title="Costs YTD by category (EUR)",cols=["Category","YTD"],rows=[[k,_money(v,"EUR ")] for k,v in sorted(grp.items(),key=lambda x:-x[1])])
    return [t1,t2]
_asof_d=datetime.date.today()
if os.environ.get("ASOF"): _asof_d=datetime.date.fromisoformat(os.environ["ASOF"])
EXTRA={}
if os.path.exists(os.environ.get("SALES_CSV","/nonexistent")):
    _b=billings_table(os.environ["SALES_CSV"],_asof_d); EXTRA["Georges"]=[_b]; EXTRA["Mireille"]=[_b]
if os.path.exists(os.environ.get("CANADA_XLSX","/nonexistent")): EXTRA.setdefault("Georges",[]).append(pl_canada(os.environ["CANADA_XLSX"]))
if os.path.exists(os.environ.get("FRANCE_XLSX","/nonexistent")): EXTRA["Daniel"]=pl_france(os.environ["FRANCE_XLSX"])
KEEP_TITLES=("Billings by billing company","Topotrade Canada: YTD P&L","Digital Realities France: YTD P&L","Costs YTD by category")

for first,full,role in PEOPLE:
    P=dict(team=dict(title="Team comparison",cols=TEAM_COLS,rows=TEAM_ROWS,hl=full),name=full,first=first,role=role,asOf=asof,updatedAt=datetime.datetime.utcnow().isoformat()+"Z",kpis=[],tables=[],recs=[],tasks=[],note="")
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
            P["tasks"][2]=dict(title="Self-serve nudges (all reps, company-wide)",cols=R["n_cols"],rows=R["nud"])
            P["tasks"][5]=dict(title="Drafts pending review (company-wide)",cols=R["d_cols"],rows=R["drafts"])
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
    _need={"Georges":["Billings by billing company","Topotrade Canada: YTD P&L"],"Mireille":["Billings by billing company"],"Daniel":["Digital Realities France: YTD P&L","Costs YTD by category"]}.get(first,[])
    P["tables"]+=EXTRA.get(first,[])
    _have=[t["title"] for t in P["tables"]]
    if any(not any(h.startswith(n) for h in _have) for n in _need):
        for t in _prev(tokens[first]).get("tables",[]):
            if t["title"].startswith(KEEP_TITLES) and not any(h==t["title"] for h in _have): P["tables"].append(t); print("kept previous table for",first,":",t["title"])
    push(f"data/team/{tokens[first]}.json",json.dumps(P,ensure_ascii=False))
    out[first]=sum(len(t["rows"]) for t in P["tasks"])
print(out)
