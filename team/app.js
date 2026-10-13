(function(){
var st=document.createElement('style'); st.textContent='.linkrule{border:2px solid #1a73e8;background:rgba(26,115,232,.10);border-radius:10px;padding:12px 16px;margin:0 0 18px} .linkrule h2{margin:0 0 6px} .linkrule p{margin:6px 0} .linkrule .neg{color:#b3261e;font-weight:600} .linkrule .ok{color:#188038;font-weight:600} td.neg{color:#b3261e!important;background:rgba(179,38,30,.12);font-weight:600} .plblk{margin:0 0 18px}'; document.head.appendChild(st);
st.textContent+=' .todo{border:2px solid #c97a2b;border-radius:10px;padding:12px 16px;margin:0 0 14px;background:rgba(201,122,43,.09)} .todo ol{margin:6px 0 0 18px;padding:0} .todo li{margin:6px 0} .todo .why{display:block;font-size:12px;opacity:.75} .chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px} .chip{border:1px solid #c9d3dd;border-radius:10px;padding:6px 10px;font-size:12px;min-width:120px} .chip b{display:block;font-size:18px} .chip.bad{border-color:#b3261e;background:rgba(179,38,30,.10)} .chip.bad b{color:#b3261e} .chip.ok{border-color:#2e8b57} .pace{border:1px solid #c9d3dd;border-radius:10px;padding:10px 14px;margin:0 0 14px} .bar{height:10px;border-radius:5px;background:rgba(128,128,128,.25);position:relative;margin:6px 0} .bar i{display:block;height:100%;border-radius:5px;background:#c97a2b} .bar u{position:absolute;top:-3px;width:2px;height:16px;background:#1f3b57} .dr{border:1px solid #c9d3dd;border-radius:8px;padding:8px 12px;margin:8px 0} .dr pre{white-space:pre-wrap;font:inherit;margin:6px 0} .dr button,.cm button{cursor:pointer;margin-right:6px;font-size:12px;padding:3px 10px;border-radius:12px;border:1px solid #1f3b57;background:transparent;color:inherit} .pb li{list-style:none;margin:4px 0} .yes{color:#2e8b57;font-weight:700} .no{color:#b3261e;font-weight:700} .cm input[type=text]{width:70%;padding:4px 8px;margin:3px 0}';
var tok=window.TT, $=function(s){return document.querySelector(s)};
function el(t,c,h){var e=document.createElement(t); if(c)e.className=c; if(h!=null)e.innerHTML=h; return e;}
function tableEl(cols,rows,hl){
  var w=el('div','tw'), t=el('table'), th=el('thead'), tr=el('tr');
  cols.forEach(function(c){tr.appendChild(el('th',null,c));}); th.appendChild(tr); t.appendChild(th);
  var tb=el('tbody');
  rows.forEach(function(r){var tr=el('tr'); if(hl&&String(r[0]).replace(/<[^>]*>/g,'')===hl)tr.className='me';
    r.forEach(function(c){var td=el('td',null,c); if(/^-\s?(\$|EUR\s?|\u20ac)\s?\d/.test(String(c).replace(/<[^>]*>/g,'').trim()))td.className='neg'; tr.appendChild(td);}); tb.appendChild(tr);});
  t.appendChild(tb); w.appendChild(t); return w;
}
function render(P){
  document.title=P.name+' | Topotrade dashboard';
  $('#who').textContent=P.name; $('#role').textContent=P.role;
  $('#asof').textContent='Data as of '+P.asOf+'. Refreshed by the daily run.';
  var nrec=0; P.recs.forEach(function(r){nrec+=r.items.length;});
  var ntask=0; P.tasks.forEach(function(t){ntask+=t.rows.length;});
  $('#c-rec').textContent=nrec; $('#c-task').textContent=ntask;
  var lr=el('section','linkrule'); lr.innerHTML='<h2>The one rule: share a link, never pictures or text</h2><p><b>Item for sale:</b> create the listing on Topotrade, then share its link. <b>Request (RFP):</b> create the request on Topotrade, then share its link. Never forward photos, specs or a copy of the text.</p><p class="why">Why it works for you: a link sends the prospect to the live page, where they can ask questions, negotiate, buy or make an offer, and where the AI can match your item or request. Pasted pictures and text go stale, leak details, and cannot be matched, so the deal stays in your chat. Every listing and request you create is counted in your performance as traffic and listings you drive.</p>'+(P.linkflags!=null?'<p class="'+(P.linkflags?'neg':'ok')+'">'+(P.linkflags?P.linkflags+' message(s) flagged in the last 7 days: item or request shared without a link.':'No flagged messages in the last 7 days. Keep it up.')+'</p>':''); $('#kpis').parentNode.insertBefore(lr,$('#kpis'));
  var PL=P.tables.filter(function(t){return /P&L/.test(t.title);}); P.tables=P.tables.filter(function(t){return !/P&L/.test(t.title);});
  if(PL.length){var pb=el('section','plblk'); PL.forEach(function(t){pb.appendChild(el('h2',null,t.title)); pb.appendChild(tableEl(t.cols,t.rows,t.hl)); if(t.note)pb.appendChild(el('p','note',t.note));}); $('#kpis').parentNode.insertBefore(pb,$('#kpis'));}
  var anchor=$('#kpis').parentNode;
  if(P.today&&P.today.length){var td=el('section','todo'); td.appendChild(el('h2',null,'Do these '+P.today.length+' today')); var ol=el('ol');
    P.today.forEach(function(x){ol.appendChild(el('li',null,'<b>'+x.text+'</b><span class="why">'+x.why+'</span>'));}); td.appendChild(ol); anchor.insertBefore(td,$('#kpis'));}
  if(P.pace){var pc=P.pace, pw=el('section','pace');
    pw.appendChild(el('h2',null,'Pace to target, '+pc.month));
    pw.appendChild(el('p',null,'<b>'+pc.mtd+'</b> RevRec so far vs <b>'+pc.target+'</b> ('+pc.label+'). Gap <b>'+pc.gap+'</b>, with '+pc.daysLeft+' working days left, so about <b>'+pc.perDay+' per working day</b>.'));
    pw.appendChild(el('div','bar','<i style="width:'+Math.min(pc.pct,100)+'%"></i><u style="left:'+pc.expected+'%" title="Expected by today"></u>'));
    pw.appendChild(el('p','note',pc.pct+'% of target reached; the dark marker is where you should be today ('+pc.expected+'% of the month elapsed).'));
    anchor.insertBefore(pw,$('#kpis'));}
  if(P.attn){var ch=el('div','chips'); P.attn.forEach(function(x){var c=el('div','chip '+(x.n?'bad':'ok'),x.label+'<b>'+x.n+'</b>'+(x.detail?'<span class="why" style="font-size:11px">'+x.detail+'</span>':'')); ch.appendChild(c);}); anchor.insertBefore(ch,$('#kpis'));}
  if(P.team){var tm=el('section','teamblk'); tm.appendChild(el('h2',null,P.team.title+' (YTD and MTD)'));
    tm.appendChild(tableEl(P.team.cols,P.team.rows,P.team.hl));
    tm.appendChild(el('p','note','USD, split-credit view from the Cockpit sheet. Tx = transaction count.'));
    $('#kpis').parentNode.insertBefore(tm,$('#kpis'));}
  var kp=$('#kpis'); P.kpis.forEach(function(k){var d=el('div','kpi');
    d.appendChild(el('div','kl',k.label)); d.appendChild(el('div','kv',k.value)); d.appendChild(el('div','ks',k.sub||'')); kp.appendChild(d);});
  if(!P.kpis.length) kp.hidden=true;
  var pf=$('#p-perf'); if(P.note)pf.appendChild(el('p','note',P.note));
  P.tables.forEach(function(t){pf.appendChild(el('h2',null,t.title)); pf.appendChild(tableEl(t.cols,t.rows,t.hl)); if(t.note)pf.appendChild(el('p','note',t.note));});
  if(P.wins){pf.appendChild(el('h2',null,'Closed in the last 7 days'+(P.wins.total?' ('+P.wins.total+')':'')));
    if(P.wins.rows.length) pf.appendChild(tableEl(['Date','Customer','Product','Billings','Gross profit'],P.wins.rows)); else pf.appendChild(el('p','note','No bookings in the last 7 days yet. Today is a good day to change that.'));}
  if(P.manager){pf.insertBefore(el('h2',null,P.manager.title),pf.firstChild); pf.insertBefore(tableEl(P.manager.cols,P.manager.rows),pf.children[1]);}
  if(P.board){pf.appendChild(el('h2',null,P.board.title)); pf.appendChild(tableEl(P.board.cols,P.board.rows)); if(P.board.note)pf.appendChild(el('p','note',P.board.note));}
  if(!P.tables.length&&!P.note) pf.appendChild(el('p','note','No performance data for this view.'));
  var rc=$('#p-rec');
  P.recs.forEach(function(r){rc.appendChild(el('h2',null,r.title+' ('+r.items.length+')'));
    var ol=el('ol','acts'); r.items.forEach(function(i){ol.appendChild(el('li',null,i));}); rc.appendChild(ol);});
  if(!P.recs.length) rc.appendChild(el('p','note','No recommended actions yet.'));
  function copy(t,b){try{navigator.clipboard.writeText(t).then(function(){b.textContent='Copied';});}catch(e){var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');b.textContent='Copied';}catch(_){}document.body.removeChild(ta);}}
  if(P.drafts&&P.drafts.length){rc.appendChild(el('h2',null,'Ready-to-send follow-ups ('+P.drafts.length+')'));
    P.drafts.forEach(function(d){var w=el('div','dr'); w.appendChild(el('b',null,d.title+(d.to?' &middot; '+d.to:'')));
      var pre=el('pre'); pre.textContent='Subject: '+d.subject+'\n\n'+d.body; w.appendChild(pre);
      var b1=el('button',null,'Copy email'); b1.onclick=function(){copy('Subject: '+d.subject+'\n\n'+d.body,b1);}; var b2=el('button',null,'Copy WhatsApp'); b2.onclick=function(){copy(d.wa,b2);};
      w.appendChild(b1); w.appendChild(b2); rc.appendChild(w);});}
  if(P.playbook){rc.appendChild(el('h2',null,'Your playbook this week')); var ul=el('ul','pb'); ul.style.padding='0';
    P.playbook.forEach(function(r){ul.appendChild(el('li',null,(r.ok===true?'<span class="yes">&#10003;</span>':r.ok===false?'<span class="no">&#10007;</span>':'<span>&#9744;</span>')+' '+r.rule+(r.kind==='self'?' <span class="note">(self-check)</span>':'')));}); rc.appendChild(ul);}
  (function(){var d=new Date(), mon=new Date(d); mon.setDate(d.getDate()-((d.getDay()+6)%7)); var key='cm:'+tok+':'+mon.toISOString().slice(0,10); var st={};
    try{st=JSON.parse(localStorage.getItem(key)||'{}');}catch(e){}
    var w=el('div','cm'); w.appendChild(el('h2',null,'My 3 priorities this week')); w.appendChild(el('p','note','Write your three commitments on Monday and tick them off. Saved in this browser only; tell Zein your list in your reply to the Monday email.'));
    for(var i=0;i<3;i++){(function(i){var row=el('div'); var cb=document.createElement('input'); cb.type='checkbox'; cb.checked=!!st['d'+i]; var tx=document.createElement('input'); tx.type='text'; tx.placeholder='Priority '+(i+1); tx.value=st['t'+i]||'';
      function save(){st['d'+i]=cb.checked; st['t'+i]=tx.value; try{localStorage.setItem(key,JSON.stringify(st));}catch(e){}}
      cb.onchange=save; tx.oninput=save; row.appendChild(cb); row.appendChild(document.createTextNode(' ')); row.appendChild(tx); w.appendChild(row);})(i);}
    rc.appendChild(w);})();
  var tk=$('#p-task');
  var empty=[];
  P.tasks.forEach(function(t){
    if(!t.rows.length){empty.push(t.title.replace(/ \(.*\)$/,''));return;}
    var d=el('details','grp'); d.open=true;
    d.appendChild(el('summary',null,t.title+' <span class="cnt">'+t.rows.length+'</span>'));
    if(t.note)d.appendChild(el('p','note',t.note));
    d.appendChild(tableEl(t.cols,t.rows));
    tk.appendChild(d);
  });
  if(empty.length) tk.appendChild(el('p','note','Nothing open in: '+empty.join(', ')+'.'));
  if(!P.tasks.length||empty.length===P.tasks.length) tk.insertBefore(el('p','note','No open tasks for you right now.'),tk.firstChild);
  $('#q').addEventListener('input',function(e){var v=e.target.value.toLowerCase();
    document.querySelectorAll('#p-task tbody tr').forEach(function(r){r.hidden=v&&r.textContent.toLowerCase().indexOf(v)<0;});
    document.querySelectorAll('#p-task details').forEach(function(g){if(v)g.open=true;});});
}
function tab(n){['perf','rec','task'].forEach(function(k){$('#p-'+k).hidden=k!==n; $('#t-'+k).setAttribute('aria-selected',k===n);});
  $('#qwrap').hidden=n!=='task'; try{history.replaceState(null,'','#'+n);}catch(e){}}
['perf','rec','task'].forEach(function(k){$('#t-'+k).addEventListener('click',function(){tab(k);});});
var h=(location.hash||'').slice(1); tab(['perf','rec','task'].indexOf(h)>=0?h:'rec');
fetch('../../data/team/'+tok+'.json?v='+Date.now()).then(function(r){if(!r.ok)throw 0;return r.json();}).then(function(P){return fetch('../../data/team/linkflags.json?v='+Date.now()).then(function(r){return r.ok?r.json():{};}).catch(function(){return {};}).then(function(F){if(F&&F[tok]!=null)P.linkflags=F[tok];return P;});}).then(render)
 .catch(function(){$('#err').hidden=false;});
})();
