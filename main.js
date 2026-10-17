'use strict';
const menu=document.querySelector('.menu');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close navigation':'Open navigation');document.querySelector('.navlinks').classList.toggle('open',open)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.getAttribute('aria-expanded')==='true')menu.click()});
const enquiry=document.querySelector('#enquiry-form');
if(enquiry){const service=new URLSearchParams(location.search).get('service');if([...enquiry.elements.service.options].some(o=>o.value===service))enquiry.elements.service.value=service;enquiry.addEventListener('submit',e=>{e.preventDefault();if(!enquiry.reportValidity())return;const d=new FormData(enquiry);const text=`Hello JR Captures! I would like to enquire.\n\nName: ${d.get('name')}\nPhone: ${d.get('phone')}\nService: ${d.get('service')}\nPreferred date: ${d.get('date')||'To discuss'}\nLocation: ${d.get('location')}\nDetails: ${d.get('message')}`;location.href='https://wa.me/919988414176?text='+encodeURIComponent(text)})}
const gift=document.querySelector('#gift-form');
if(gift){document.querySelector('#gift-title').addEventListener('input',e=>document.querySelector('#preview-name').textContent=e.target.value||'A memory to treasure');document.querySelector('#gift-message').addEventListener('input',e=>document.querySelector('#preview-message').textContent=e.target.value||'Made personal. Made for you.');let previewUrl;document.querySelector('#gift-photo').addEventListener('change',e=>{const f=e.target.files[0];if(!f)return;const status=document.querySelector('#gift-status');if(!['image/jpeg','image/png','image/webp'].includes(f.type)||f.size>10*1024*1024){status.textContent='Please choose a JPG, PNG or WebP image under 10 MB.';e.target.value='';return}if(previewUrl)URL.revokeObjectURL(previewUrl);previewUrl=URL.createObjectURL(f);const img=new Image();img.alt='Your selected gift photo preview';img.src=previewUrl;document.querySelector('#preview-image').replaceChildren(img);status.textContent='Preview updated. Attach this photo separately in WhatsApp.'});gift.addEventListener('submit',e=>{e.preventDefault();if(!gift.reportValidity())return;const d=new FormData(gift);const text=`Hello JR Captures! I would like a personalized photo gift.\n\nName: ${d.get('customer')}\nGift idea: ${d.get('idea')}\nTitle: ${d.get('title')||'To discuss'}\nMessage: ${d.get('message')||'To discuss'}\nNeeded by: ${d.get('date')||'To discuss'}\n\nPlease share available options and a quote. I will attach my photo separately.`;location.href='https://wa.me/919988414176?text='+encodeURIComponent(text)})}

/* Shared, progressive motion across every page. Content stays visible without JS. */
(() => {
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!('IntersectionObserver' in window) || !Element.prototype.animate || preference.matches) return;
  const active = new Set();
  const reveal = (el, delay = 0) => {
    const animation = el.animate([
      { opacity: 0, transform: 'translateY(24px)' },
      { opacity: 1, transform: 'translateY(0)' }
    ], { duration: 680, delay, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards' });
    active.add(animation);
    animation.finished.then(() => active.delete(animation)).catch(() => active.delete(animation));
  };
  const hero = document.querySelector('.hero-copy, .pagehead');
  if (hero) [...hero.children].forEach((el, i) => reveal(el, Math.min(i, 4) * 75));
  const heroImage = document.querySelector('.hero-visual');
  if (heroImage) reveal(heroImage, 120);
  const selector = '.heading, .cards > .card, .catalog-card, .steps > article, .split > div, .split > form, .gift-category-card, .product-visual, .product-info, details, .cta, .footgrid > div';
  const targets = [...document.querySelectorAll(selector)];
  const targetSet = new Set(targets);
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      observer.unobserve(entry.target);
      if (preference.matches) continue;
      const siblings = [...entry.target.parentElement.children];
      const index = siblings.indexOf(entry.target);
      const stagger = entry.target.matches('.catalog-card, .card, .steps > article, .footgrid > div') ? (index % 3) * 75 : 0;
      reveal(entry.target, stagger);
    }
  }, { threshold: 0.08, rootMargin: '0px 0px -20px 0px' });
  targets.forEach(el => {
    let parent = el.parentElement;
    while (parent && !targetSet.has(parent)) parent = parent.parentElement;
    if (!parent) observer.observe(el);
  });
  preference.addEventListener('change', event => {
    if (!event.matches) return;
    observer.disconnect();
    active.forEach(animation => animation.cancel());
    active.clear();
  });
})();
