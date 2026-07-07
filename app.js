let flowData = {};
let hist = [];

async function init() {
  try {
    const res = await fetch('data/flow.json');
    flowData = await res.json();
    render('inicio');
  } catch(e) {
    document.getElementById('content').innerHTML = '<div class="warning">Erro ao carregar. Recarregue a pagina.</div>';
  }
}

function render(id) {
  const s = flowData[id];
  if (!s) return;
  let h = '';
  if (s.question) h += '<h2 class="question">' + s.question + '</h2>';
  if (s.info) h += '<div class="info">' + fmt(s.info) + '</div>';
  if (s.success) h += '<div class="success">' + fmt(s.success) + '</div>';
  if (s.highlight) h += '<div class="highlight">' + fmt(s.highlight) + '</div>';
  if (s.warning) h += '<div class="warning">' + fmt(s.warning) + '</div>';
  if (s.checklist) {
    h += '<div class="checklist">';
    s.checklist.forEach(function(i){ h += '<div class="checklist-item">' + i + '</div>'; });
    h += '</div>';
  }
  if (s.steps) {
    h += '<div class="steps">';
    s.steps.forEach(function(i){ h += '<div class="step-item">' + i + '</div>'; });
    h += '</div>';
  }
  if (s.options) {
    h += '<div class="options">';
    s.options.forEach(function(o, idx){
      if (o.link) {
        h += '<a href="' + o.link + '" target="_blank" class="link-btn"><span class="emoji">&#128279;</span>' + o.text + '</a>';
      } else if (o.next) {
        var num = idx + 1;
        h += '<div class="option-btn" onclick="goTo(\'' + o.next + '\')"><span class="emoji">' + num + '</span>' + o.text + '</div>';
      }
    });
    h += '</div>';
  }
  document.getElementById('content').innerHTML = h;
  document.getElementById('content').dataset.current = id;
  renderFooter(id);
  window.scrollTo(0,0);
}

function renderFooter(id) {
  const f = document.getElementById('footer');
  if (id === 'inicio') { f.innerHTML = ''; return; }
  f.innerHTML = '<div class="footer-btn" onclick="goBack()">Voltar</div><div class="footer-btn" onclick="goHome()">Inicio</div><a class="footer-btn" href="https://amazonexteu.qualtrics.com/jfe/form/SV_eEhccc2rqm5WURw" target="_blank">Lista pra mim</a>';
}

function goTo(id) {
  var cur = document.getElementById('content').dataset.current || 'inicio';
  hist.push(cur);
  render(id);
}

function goBack() { if (hist.length > 0) render(hist.pop()); }
function goHome() { hist = []; render('inicio'); }
function fmt(t) { return t ? t.replace(/\n/g,'<br>').replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>') : ''; }

init();