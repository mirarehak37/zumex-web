/* Zumex Česko, interakce webu. Efekty inspirované knihovnou React Bits, přepsané do čistého JS bez závislostí. */
(()=>{
 document.documentElement.classList.add('js');
 const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
 // Mobilní menu
 const toggle=document.querySelector('.nav-toggle'),menu=document.querySelector('#menu');
 if(toggle&&menu){
  const set=open=>{menu.classList.toggle('is-open',open);toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Zavřít menu':'Otevřít menu');toggle.innerHTML=open?'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>':'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'};
  toggle.addEventListener('click',()=>set(!menu.classList.contains('is-open')));
  menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>set(false)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.classList.contains('is-open')){set(false);toggle.focus()}});
  document.addEventListener('click',e=>{if(menu.classList.contains('is-open')&&!menu.contains(e.target)&&!toggle.contains(e.target))set(false)});
 }
 // Odhalování při scrollu
 const els=document.querySelectorAll('.reveal');
 if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
  const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add('is-visible');io.unobserve(en.target)}}),{rootMargin:'0px 0px -8% 0px'});
  els.forEach(el=>io.observe(el));
 }else els.forEach(el=>el.classList.add('is-visible'));
 // Záložky na detailu produktu
 const tabs=[...document.querySelectorAll('.tabs a')];
 if(tabs.length&&'IntersectionObserver' in window){
  const map=new Map(tabs.map(a=>[a.getAttribute('href').slice(1),a]));
  const so=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){tabs.forEach(t=>t.classList.remove('is-active'));const a=map.get(en.target.id);if(a){a.classList.add('is-active');a.scrollIntoView({block:'nearest',inline:'center'})}}}),{rootMargin:'-45% 0px -50% 0px'});
  map.forEach((a,id)=>{const s=document.getElementById(id);if(s)so.observe(s)});
 }
 // Galerie se šipkami
 document.querySelectorAll('[data-gallery]').forEach(wrap=>{
  const track=wrap.querySelector('.gallery');
  wrap.querySelectorAll('[data-dir]').forEach(b=>b.addEventListener('click',()=>track.scrollBy({left:track.clientWidth*0.8*+b.dataset.dir,behavior:'smooth'})));
 });
 // Katalog: vyhledávání a filtry
 const form=document.querySelector('#catalog-filters');
 if(form){
  const cards=[...document.querySelectorAll('.catalog-grid .card-product')];
  const count=document.querySelector('#catalog-count'),empty=document.querySelector('.catalog-empty');
  const search=document.querySelector('#product-search');
  const norm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
  const groups=['category','demand','business'];
  const update=()=>{
   const sel=Object.fromEntries(groups.map(g=>[g,[...form.querySelectorAll(`input[name="${g}"]:checked`)].map(i=>i.value)]));
   const words=norm(search.value.trim()).split(/\s+/).filter(Boolean);let n=0;
   cards.forEach(c=>{const ok=groups.every(g=>!sel[g].length||sel[g].some(v=>c.dataset[g].split(' ').includes(v)))&&words.every(w=>norm(c.dataset.search+' '+c.textContent).includes(w));c.hidden=!ok;if(ok)n++});
   count.textContent=`Zobrazeno ${n} z ${cards.length} produktových řad`;empty.hidden=n!==0;
  };
  form.addEventListener('input',update);form.addEventListener('change',update);search.addEventListener('input',update);
  form.addEventListener('reset',()=>setTimeout(update,0));
  document.querySelectorAll('[data-reset]').forEach(b=>b.addEventListener('click',()=>{form.reset();search.value='';update();search.focus()}));
  const ft=document.querySelector('.filter-toggle');if(ft)ft.addEventListener('click',()=>{const o=form.classList.toggle('is-open');ft.setAttribute('aria-expanded',String(o))});
  const hashes={citrusy:['citrusy'],samocistici:['samocistici'],multifruit:['odstavnovace','ananas'],'cold-press':['cold-press'],prumyslove:['prumyslove']};
  const applyHash=()=>{const h=location.hash.slice(1);if(h==='hledat'){search.focus();return}const ch=hashes[h];if(ch){form.querySelectorAll('[name=category]').forEach(i=>i.checked=ch.includes(i.value));update()}};
  window.addEventListener('hashchange',applyHash);applyHash();update();
 }
 // Split / Blur Text: nadpis se skládá po slovech
 document.querySelectorAll('.split-text').forEach(el=>{
  const words=el.textContent.trim().split(/\s+/);el.setAttribute('aria-label',el.textContent.trim());
  el.innerHTML=words.map((w,i)=>`<span class="split-word" aria-hidden="true" style="--i:${i}">${w}</span>`).join(' ');
  requestAnimationFrame(()=>requestAnimationFrame(()=>el.classList.add('is-in')));
 });
 // Count Up: čísla doběhnou při zobrazení
 const counters=document.querySelectorAll('[data-count]');
 const runCount=el=>{const to=+el.dataset.count,dur=1400,t0=performance.now();const step=t=>{const k=Math.min(1,(t-t0)/dur),v=Math.round(to*(1-Math.pow(1-k,3)));el.textContent=v+(el.dataset.suffix||'');if(k<1)requestAnimationFrame(step)};requestAnimationFrame(step)};
 if(reduce||!('IntersectionObserver' in window))counters.forEach(el=>el.textContent=el.dataset.count+(el.dataset.suffix||''));
 else{const co=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){runCount(en.target);co.unobserve(en.target)}}),{threshold:.6});counters.forEach(el=>{el.textContent='0'+(el.dataset.suffix||'');co.observe(el)})}
 // Scroll Reveal: věta se rozsvěcuje po slovech podle scrollu
 document.querySelectorAll('.statement').forEach(el=>{
  const parts=[];el.childNodes.forEach(n=>{if(n.nodeType===3)n.textContent.split(/(\s+)/).forEach(t=>parts.push(t.trim()?`<span class="sr-word">${t}</span>`:t));else{n.classList.add('sr-word');parts.push(n.outerHTML)}});
  el.innerHTML=parts.join('');const ws=[...el.querySelectorAll('.sr-word')];
  if(reduce){ws.forEach(w=>w.classList.add('on'));return}
  ws.forEach((w,i)=>w.style.transitionDelay=(i*45)+'ms');
  const io2=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){ws.forEach(w=>w.classList.add('on'));io2.disconnect()}}),{threshold:.35});io2.observe(el);
 });
 // Logo Loop: zdvojení obsahu pásu pro plynulou smyčku
 document.querySelectorAll('.marquee-track').forEach(t=>{t.innerHTML+=t.innerHTML;[...t.children].slice(t.children.length/2).forEach(c=>c.setAttribute('aria-hidden','true'))});
 // Spotlight karta
 if(fine)document.querySelectorAll('.spotlight').forEach(c=>c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-r.left)+'px');c.style.setProperty('--my',(e.clientY-r.top)+'px')}));
 // Magnet tlačítka
 if(fine&&!reduce)document.querySelectorAll('.magnet').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.18}px,${(e.clientY-r.top-r.height/2)*.28}px)`});b.addEventListener('pointerleave',()=>b.style.transform='')});
 // Přepínač kategorií
 document.querySelectorAll('[data-showcase]').forEach(w=>{
  const tabs=[...w.querySelectorAll('[role=tab]')],panels=[...w.querySelectorAll('[role=tabpanel]')];
  const sel=i=>{tabs.forEach((t,j)=>{t.setAttribute('aria-selected',String(i===j));t.tabIndex=i===j?0:-1});panels.forEach((p,j)=>p.hidden=i!==j)};
  tabs.forEach((t,i)=>{t.addEventListener('click',()=>sel(i));t.addEventListener('keydown',e=>{const k={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1}[e.key];if(k){e.preventDefault();const n=(i+k+tabs.length)%tabs.length;sel(n);tabs[n].focus()}})});
 });
 // Video s vlastním tlačítkem přehrát
 document.querySelectorAll('[data-video]').forEach(f=>{const v=f.querySelector('video'),b=f.querySelector('.play-btn');b.addEventListener('click',()=>{f.classList.add('is-playing');v.controls=true;v.play()})});
})();
