(function(){
var tok=window.TT, $=function(s){return document.querySelector(s)};
function el(t,c,h){var e=document.createElement(t); if(c)e.className=c; if(h!=null)e.innerHTML=h; return e;}
function tableEl(cols,rows,hl){
  var w=el('div','tw'), t=el('table'), th=el('thead'), tr=el('tr');
  cols.forEach(function(c){tr.appendChild(el('th',null,c));}); th.appendChild(tr); t.appendChild(th);
  var tb=el('tbody');
  rows.forEach(function(r){var tr=el('tr'); if(hl&&String(r[0]).replace(/<[^>]*>/g,'')===hl)tr.className='me';
    r.forEach(function(c){tr.appendChild(el('td',null,c));}); tb.appendChild(tr);});
  t.appendChild(tb); w.appendChild(t); return w;
}
function render(P){
  document.title=P.name+' | Topotrade dashboard';
  $('#who').textContent=P.name; $('#role').textContent=P.role;
  $('#asof').textContent='Data as of '+P.asOf+'. Refreshed by the daily run.';
  var nrec=0; P.recs.forEach(function(r){nrec+=r.items.length;});
  var ntask=0; P.tasks.forEach(function(t){ntask+=t.rows.length;});
  $('#c-rec').textContent=nrec; $('#c-task').textContent=ntask;
  if(P.team){var tm=el('section','teamblk'); tm.appendChild(el('h2',null,P.team.title+' (YTD and MTD)'));
    tm.appendChild(tableEl(P.team.cols,P.team.rows,P.team.hl));
    tm.appendChild(el('p','note','USD, split-credit view from the Cockpit sheet. Tx = transaction count.'));
    $('#kpis').parentNode.insertBefore(tm,$('#kpis'));}
  var kp=$('#kpis'); P.kpis.forEach(function(k){var d=el('div','kpi');
    d.appendChild(el('div','kl',k.label)); d.appendChild(el('div','kv',k.value)); d.appendChild(el('div','ks',k.sub||'')); kp.appendChild(d);});
  if(!P.kpis.length) kp.hidden=true;
  var pf=$('#p-perf'); if(P.note)pf.appendChild(el('p','note',P.note));
  P.tables.forEach(function(t){pf.appendChild(el('h2',null,t.title)); pf.appendChild(tableEl(t.cols,t.rows,t.hl)); if(t.note)pf.appendChild(el('p','note',t.note));});
  if(!P.tables.length&&!P.note) pf.appendChild(el('p','note','No performance data for this view.'));
  var rc=$('#p-rec');
  P.recs.forEach(function(r){rc.appendChild(el('h2',null,r.title+' ('+r.items.length+')'));
    var ol=el('ol','acts'); r.items.forEach(function(i){ol.appendChild(el('li',null,i));}); rc.appendChild(ol);});
  if(!P.recs.length) rc.appendChild(el('p','note','No recommended actions yet.'));
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
fetch('../../data/team/'+tok+'.json?v='+Date.now()).then(function(r){if(!r.ok)throw 0;return r.json();}).then(render)
 .catch(function(){$('#err').hidden=false;});
})();
