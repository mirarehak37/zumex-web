const toggle=document.querySelector('.menu-toggle');
const menu=document.querySelector('#site-menu');
if(toggle&&menu){
 const mobile=matchMedia('(max-width:767px)');
 const closeMenu=(focus=false)=>{menu.hidden=mobile.matches;toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Otevřít menu');if(focus)toggle.focus()};
 mobile.addEventListener('change',()=>closeMenu());closeMenu();
 toggle.addEventListener('click',()=>{if(!mobile.matches)return;const open=menu.hidden;menu.hidden=!open;toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Zavřít menu':'Otevřít menu')});
 menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>closeMenu()));
 document.addEventListener('click',e=>{if(mobile.matches&&!menu.hidden&&!menu.contains(e.target)&&!toggle.contains(e.target))closeMenu()});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&mobile.matches&&!menu.hidden)closeMenu(true)});
 document.addEventListener('focusin',e=>{if(mobile.matches&&!menu.hidden&&!menu.contains(e.target)&&!toggle.contains(e.target))closeMenu()});
}

const catalogForm=document.querySelector('#catalog-filters');
if(catalogForm){
 const cards=[...document.querySelectorAll('.catalog-results .product-card')];
 const count=document.querySelector('#catalog-count'),empty=document.querySelector('.catalog-empty');
 const search=catalogForm.querySelector('[type=search]');
 const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const groups=['category','demand','business'];
 const update=()=>{
  const selected=Object.fromEntries(groups.map(g=>[g,[...catalogForm.querySelectorAll(`input[name="${g}"]:checked`)].map(e=>e.value)]));
  const words=normalize(search.value.trim()).split(/\s+/).filter(Boolean);let visible=0;
  cards.forEach(card=>{
   const matches=groups.every(g=>!selected[g].length||selected[g].some(v=>card.dataset[g].split(' ').includes(v)))&&words.every(w=>normalize(card.dataset.search+' '+card.textContent).includes(w));
   card.hidden=!matches;if(matches)visible++;
  });
  count.textContent=`Zobrazeno ${visible} z ${cards.length} produktových řad`;empty.hidden=visible!==0;
 };
 catalogForm.addEventListener('input',update);catalogForm.addEventListener('change',update);
 catalogForm.addEventListener('reset',()=>{setTimeout(update,0)});
 document.querySelector('.empty-reset').addEventListener('click',()=>{catalogForm.reset();search.focus()});
 const hashCategories={citrusy:['citrusy'],samocistici:['samocistici'],multifruit:['odstavnovace','ananas'],'cold-press':['cold-press'],prumyslove:['prumyslove']};
 const applyHash=()=>{const chosen=hashCategories[location.hash.slice(1)];if(chosen){catalogForm.querySelectorAll('[name=category]').forEach(e=>e.checked=chosen.includes(e.value));update()}};
 window.addEventListener('hashchange',applyHash);applyHash();update();
 const panel=document.querySelector('.filter-panel');const mobileFilters=matchMedia('(max-width:767px)');panel.open=!mobileFilters.matches;mobileFilters.addEventListener('change',()=>panel.open=!mobileFilters.matches);
}
