const SHEETDB_URL = 'https://sheetdb.io/api/v1/7x95jmwaouxrl';
let flowData = {};
let hist = [];
let userContact = '';

async function init() {
  try {
    const r = await fetch('flow.json');
    flowData = await r.json();
    showContact();
  } catch(e) {
    document.getElementById('app').innerHTML = '<p>Erro ao carregar. Recarregue a pagina.</p>';
  }
}

function showContact() {
  document.getElementById('app').innerHTML = `
    <div class="card">
      <h2>Ola! Vou te ajudar a listar seu produto na Amazon</h2>
      <p class="info">Primeiro, me deixe um contato pra te ajudarmos se precisar. E 100% gratuito!</p>
      <div class="contact-form">
        <label>Seu WhatsApp ou Email:</label>
        <input type="text" id="contactInput" placeholder="(11) 99999-9999 ou email@email.com" />
        <button class="btn" onclick="startFlow()">Comecar!</button>
      </div>
      <p class="skip-link" onclick="startFlow()">Pular e comecar direto</p>
    </div>
  `;
}

function startFlow() {
  const input = document.getElementById('contactInput');
  userContact = input ? input.value.trim() : '';
  if (userContact) {
    sendToSheet(userContact, '', 'inicio');
  }
  showScreen('inicio');
}

function sendToSheet(whatsapp, observacao, tela) {
  fetch(SHEETDB_URL, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({data: {whatsapp: whatsapp, observacao: observacao, tela: tela}})
  }).catch(()=>{});
}

function showScreen(id) {
  const s = flowData[id];
  if (!s) { document.getElementById('app').innerHTML = '<p>Tela nao encontrada.</p>'; return; }
  hist.push(id);
  let h = `<div class="card"><h2>${s.question}</h2>`;
  if (s.success) h += `<div class="success">${s.success}</div>`;
  if (s.info) h += `<p class="info">${s.info}</p>`;
  if (s.warning) h += `<div class="warning">${s.warning}</div>`;
  if (s.highlight) h += `<div class="highlight">${s.highlight}</div>`;
  if (s.steps) { h += '<div class="steps">'; s.steps.forEach((st,i) => { h += `<div class="step"><span class="step-num">${i+1}</span>${st}</div>`; }); h += '</div>'; }
  if (s.checklist) { h += '<div class="checklist">'; s.checklist.forEach(c => { h += `<div class="check-item">&#9745; ${c}</div>`; }); h += '</div>'; }
  if (s.options) { h += '<div class="options">'; s.options.forEach(o => { if (o.link) { h += `<a href="${o.link}" target="_blank" class="btn btn-link">${o.text}</a>`; } else { h += `<button class="btn" onclick="showScreen('${o.next}')">${o.text}</button>`; } }); h += '</div>'; }
  if (hist.length > 1) { h += `<div class="footer"><button class="footer-btn" onclick="goBack()">Voltar</button><button class="footer-btn" onclick="showScreen('inicio')">Inicio</button><button class="footer-btn" onclick="window.open('https://amazonexteu.qualtrics.com/jfe/form/SV_eEhccc2rqm5WURw','_blank')">Lista pra mim</button></div>`; }
  h += '</div>';
  document.getElementById('app').innerHTML = h;
}

function goBack() {
  hist.pop();
  const prev = hist.pop();
  if (prev) showScreen(prev); else showContact();
}

init();
