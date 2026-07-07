
import json, os

os.makedirs('data', exist_ok=True)
os.makedirs('css', exist_ok=True)
os.makedirs('js', exist_ok=True)

# === INDEX.HTML ===
html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Me Ajuda a Listar</title>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div id="app">
<div id="header">
<h1>Me Ajuda a Listar</h1>
<p>Seu guia pra listar na Amazon</p>
</div>
<div id="content"><div id="loading">Carregando...</div></div>
<div id="footer"></div>
</div>
<script src="js/app.js"></script>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html criado')

# === CSS/STYLE.CSS ===
css = """* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:-apple-system,BlinkMacSystemFont,sans-serif; background:#f5f7fa; min-height:100vh; }
#app { max-width:480px; margin:0 auto; min-height:100vh; background:#fff; box-shadow:0 0 20px rgba(0,0,0,0.1); }
#header { background:linear-gradient(135deg,#232F3E,#37475A); padding:24px 20px; text-align:center; }
#header h1 { color:#FF9900; font-size:22px; margin-bottom:4px; }
#header p { color:#ddd; font-size:13px; }
#content { padding:20px; min-height:60vh; }
#footer { padding:12px 20px; border-top:1px solid #eee; display:flex; justify-content:center; gap:12px; }
.question { font-size:18px; font-weight:700; color:#232F3E; margin-bottom:12px; line-height:1.3; }
.info { font-size:14px; color:#555; margin-bottom:16px; line-height:1.5; }
.options { display:flex; flex-direction:column; gap:10px; }
.option-btn { background:#fff; border:2px solid #e8e8e8; border-radius:12px; padding:14px 16px; font-size:15px; cursor:pointer; transition:all 0.2s; display:flex; align-items:center; gap:10px; text-align:left; }
.option-btn:hover { border-color:#FF9900; background:#fff8f0; transform:translateY(-1px); box-shadow:0 4px 12px rgba(255,153,0,0.15); }
.option-btn:active { transform:translateY(0); }
.link-btn { display:flex; align-items:center; gap:10px; background:#fff; border:2px solid #146EB4; border-radius:12px; padding:14px 16px; font-size:15px; color:#146EB4; text-decoration:none; transition:all 0.2s; }
.link-btn:hover { background:#f0f7ff; transform:translateY(-1px); }
.emoji { font-size:18px; flex-shrink:0; width:28px; height:28px; background:#FF9900; color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:13px; }
.warning { background:#fff3cd; border-left:4px solid #ffc107; padding:12px; border-radius:8px; font-size:13px; margin:12px 0; color:#856404; }
.success { background:#d4edda; border-left:4px solid #28a745; padding:12px; border-radius:8px; font-size:13px; margin:12px 0; color:#155724; }
.highlight { background:#e8f4fd; border-left:4px solid #146EB4; padding:12px; border-radius:8px; font-size:13px; margin:12px 0; color:#0c5460; }
.checklist { margin:12px 0; }
.checklist-item { padding:8px 0 8px 28px; position:relative; font-size:14px; color:#333; }
.checklist-item:before { content:'\\2713'; position:absolute; left:4px; color:#28a745; font-weight:700; }
.steps { margin:12px 0; counter-reset:step; }
.step-item { padding:10px 0 10px 36px; position:relative; font-size:14px; color:#333; border-left:2px solid #FF9900; margin-left:10px; counter-increment:step; }
.step-item:before { content:counter(step); position:absolute; left:-12px; top:8px; background:#FF9900; color:#fff; width:22px; height:22px; border-radius:50%; text-align:center; line-height:22px; font-size:12px; font-weight:700; }
.footer-btn { padding:8px 14px; border-radius:20px; font-size:13px; color:#555; cursor:pointer; border:1px solid #ddd; text-decoration:none; transition:all 0.2s; background:#fff; }
.footer-btn:hover { background:#FF9900; color:#fff; border-color:#FF9900; }
#loading { text-align:center; padding:60px 20px; color:#999; font-size:16px; }
@media(max-width:480px){ #app{box-shadow:none;} }"""

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('css/style.css criado')

# === JS/APP.JS ===
appjs = r"""let flowData = {};
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

init();"""

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(appjs)
print('js/app.js criado')

# === DATA/FLOW.JSON ===
flow = {
    "inicio": {
        "question": "Como posso te ajudar a listar?",
        "info": "Escolha uma opcao abaixo:",
        "options": [
            {"text": "Listar 1 produto (manual)", "next": "manual_novo_usado"},
            {"text": "Listar muitos produtos (massivo)", "next": "massivo_inicio"},
            {"text": "Quero que listem pra mim", "link": "https://amazonexteu.qualtrics.com/jfe/form/SV_eEhccc2rqm5WURw"}
        ]
    },
    "manual_novo_usado": {
        "question": "Seu produto e novo ou usado?",
        "options": [
            {"text": "Novo", "next": "novo_ean"},
            {"text": "Usado / Seminovo", "next": "usado"}
        ]
    },
    "novo_ean": {
        "question": "Seu produto tem codigo de barras (EAN)?",
        "info": "EAN = codigo de barras na embalagem (numeros embaixo das barrinhas).",
        "options": [
            {"text": "Sim, tenho EAN", "next": "gs1_valida"},
            {"text": "Nao tenho EAN", "next": "sem_ean_marca"}
        ]
    },
    "gs1_valida": {
        "question": "Valide seu EAN antes de listar!",
        "info": "Confirme que seu EAN esta ativo e correto no site do GS1:",
        "steps": ["Clique no link abaixo", "Digite o numero do EAN", "Confira se aparece como valido"],
        "options": [
            {"text": "Validar EAN no GS1", "link": "https://www.gs1.org/services/verified-by-gs1/results"},
            {"text": "EAN validado! Proximo passo", "next": "com_ean_marca"},
            {"text": "Meu EAN deu invalido", "next": "ean_invalido"}
        ]
    },
    "ean_invalido": {
        "question": "EAN invalido - O que fazer:",
        "info": "Se o EAN nao apareceu como valido, pode ser que:",
        "checklist": ["O fabricante ainda nao ativou no GS1", "O numero foi digitado errado", "O EAN e falsificado"],
        "highlight": "Se o EAN e do seu produto e voce comprou do GS1 Brasil, entre em contato com o GS1 pra ativar. Se nao, liste sem EAN (como generico).",
        "options": [
            {"text": "Listar sem EAN (generico)", "next": "sem_ean_marca"},
            {"text": "Voltar", "next": "novo_ean"}
        ]
    },
    "com_ean_marca": {
        "question": "Seu produto tem marca na embalagem?",
        "info": "A marca precisa estar impressa, gravada ou estampada no produto ou embalagem. Adesivo ou costurado NAO conta.",
        "options": [
            {"text": "Sim, tem marca", "next": "com_ean_tipo_marca"},
            {"text": "Nao tem marca (generico)", "next": "listar_generico_com_ean"}
        ]
    },
    "com_ean_tipo_marca": {
        "question": "A marca e sua ou voce revende?",
        "options": [
            {"text": "Marca propria (sou dono)", "next": "marca_propria_inpi"},
            {"text": "Revendo (marca de terceiro)", "next": "revendedor_nf"}
        ]
    },
    "marca_propria_inpi": {
        "question": "Voce tem registro no INPI?",
        "info": "INPI = Instituto Nacional de Propriedade Industrial. E o registro oficial da sua marca no Brasil.",
        "options": [
            {"text": "Sim, tenho INPI (aprovado ou em processo)", "next": "marca_propria_brand_registry"},
            {"text": "Nao tenho INPI", "next": "marca_propria_sem_inpi"}
        ]
    },
    "marca_propria_brand_registry": {
        "question": "Registre sua marca no Brand Registry!",
        "info": "Com INPI voce pode registrar no Brand Registry da Amazon e ter beneficios exclusivos:",
        "checklist": ["Protecao contra copias", "A+ Content (pagina premium)", "Sponsored Brands (ads avancado)", "Loja propria na Amazon"],
        "steps": ["Acesse o Brand Registry (link abaixo)", "Cadastre sua marca com numero INPI", "Aguarde aprovacao (3-10 dias)", "Depois volte e liste normalmente!"],
        "options": [
            {"text": "Ir para Brand Registry", "link": "https://brandservices.amazon.com.br"},
            {"text": "Ja tenho Brand Registry, quero listar", "next": "listar_com_marca"},
            {"text": "Voltar", "next": "marca_propria_inpi"}
        ]
    },
    "marca_propria_sem_inpi": {
        "question": "Sem INPI - Seu produto tem a logo/nome da marca VISIVEL no produto?",
        "info": "Precisa estar impresso, gravado ou moldado. NAO pode ser adesivo ou costurado.",
        "options": [
            {"text": "Sim, nome/logo aparece no produto", "next": "marca_sem_inpi_fotos"},
            {"text": "Nao aparece no produto", "next": "listar_generico_sem_ean"}
        ]
    },
    "marca_sem_inpi_fotos": {
        "question": "Voce consegue listar com marca mesmo sem INPI!",
        "info": "A Amazon aceita se voce comprovar com fotos que a marca aparece no produto.",
        "steps": ["Tire fotos claras mostrando o nome/logo no produto", "Na hora de listar, selecione sua marca", "O sistema vai pedir comprovacao - envie as fotos", "Aguarde aprovacao"],
        "highlight": "Dica: Ter embalagem propria com a marca impressa ajuda muito na aprovacao!",
        "options": [
            {"text": "Entendi! Ir para listar", "next": "listar_com_marca"},
            {"text": "Voltar", "next": "marca_propria_sem_inpi"}
        ]
    },
    "revendedor_nf": {
        "question": "Voce tem Nota Fiscal com minimo de 10 produtos dessa marca na MESMA NF?",
        "warning": "Precisa ser 10 ou mais unidades na MESMA nota fiscal. Nao pode juntar notas diferentes.",
        "options": [
            {"text": "Sim, tenho NF com 10+ produtos", "next": "revendedor_listar"},
            {"text": "Nao tenho NF ou tem menos de 10", "next": "revendedor_sem_nf"}
        ]
    },
    "revendedor_listar": {
        "question": "Otimo! Vamos listar como revendedor:",
        "steps": ["Va em Seller Central - Catalogo - Adicionar produto", "Busque pelo nome ou EAN do produto", "Clique em 'Vender este produto' se ja existir", "Se nao existir, clique em 'Criar nova oferta'", "Complete os dados e salve"],
        "info": "Se o sistema pedir autorizacao de marca, ele vai solicitar sua NF automaticamente.",
        "options": [
            {"text": "Deu certo! Listei", "next": "sucesso"},
            {"text": "Deu erro ou pediu autorizacao", "next": "erro_autorizacao"},
            {"text": "Voltar", "next": "revendedor_nf"}
        ]
    },
    "revendedor_sem_nf": {
        "question": "Sem NF com 10+ produtos, suas opcoes sao:",
        "info": "A Amazon exige NF com minimo de 10 produtos da mesma marca para autorizar revendedores.",
        "options": [
            {"text": "Vou conseguir a NF e voltar depois", "next": "inicio"},
            {"text": "Quero listar como generico (sem marca)", "next": "listar_generico_sem_ean"},
            {"text": "Voltar", "next": "revendedor_nf"}
        ]
    },
    "sem_ean_marca": {
        "question": "Seu produto tem marca ou logo na embalagem/produto?",
        "info": "Impresso, gravado ou estampado. Adesivo ou costurado NAO conta.",
        "options": [
            {"text": "Sim, tem marca", "next": "sem_ean_tipo_marca"},
            {"text": "Nao tem marca", "next": "listar_generico_sem_ean"}
        ]
    },
    "sem_ean_tipo_marca": {
        "question": "A marca e sua ou voce revende?",
        "options": [
            {"text": "Marca propria", "next": "marca_propria_inpi"},
            {"text": "Revendo (marca de terceiro)", "next": "revendedor_nf"}
        ]
    },
    "listar_generico_com_ean": {
        "question": "Listar produto generico COM EAN:",
        "steps": ["Va em Seller Central - Catalogo - Adicionar produto", "Busque pelo EAN", "Se ja existir, clique em 'Vender este produto'", "Se nao existir, clique em 'Criar nova oferta'", "No campo Marca coloque: Generico", "No campo ID coloque o EAN", "Complete titulo, descricao, imagens e preco", "Salve!"],
        "options": [
            {"text": "Deu certo!", "next": "sucesso"},
            {"text": "Deu erro", "next": "erros_inicio"},
            {"text": "Voltar", "next": "com_ean_marca"}
        ]
    },
    "listar_generico_sem_ean": {
        "question": "Listar produto generico SEM EAN:",
        "steps": ["Va em Seller Central - Catalogo - Adicionar produto", "Clique em 'Criar nova oferta'", "Selecione a categoria do produto", "No campo Marca coloque: Generico", "No campo ID do produto: clique em 'Nao tenho ID'", "O sistema vai pedir isencao de EAN", "Complete titulo, descricao, imagens e preco", "Salve!"],
        "warning": "Sem EAN seu produto entra como generico e NAO disputa Buy Box. Mas funciona!",
        "options": [
            {"text": "Deu certo!", "next": "sucesso"},
            {"text": "Deu erro", "next": "erros_inicio"},
            {"text": "Voltar", "next": "sem_ean_marca"}
        ]
    },
    "listar_com_marca": {
        "question": "Listar produto com marca registrada:",
        "steps": ["Va em Seller Central - Catalogo - Adicionar produto", "Busque pelo nome ou EAN", "Se ja existir, clique em 'Vender este produto'", "Se nao existir, clique em 'Criar nova oferta'", "Selecione SUA MARCA no campo de marca", "Complete todos os campos", "Salve!"],
        "highlight": "Com Brand Registry ativo, voce tem mais controle sobre a pagina do produto!",
        "options": [
            {"text": "Deu certo!", "next": "sucesso"},
            {"text": "Deu erro", "next": "erros_inicio"},
            {"text": "Voltar", "next": "marca_propria_inpi"}
        ]
    },
    "erro_autorizacao": {
        "question": "O sistema pediu autorizacao de marca:",
        "info": "Isso e normal! A Amazon precisa verificar que voce pode vender essa marca.",
        "steps": ["O sistema abre um chamado automaticamente", "Envie a NF com 10+ produtos da marca (mesma NF)", "Aguarde a analise (3-5 dias uteis)", "Voce recebe o resultado por email e no Seller Central"],
        "options": [
            {"text": "Aprovaram! Listei", "next": "sucesso"},
            {"text": "Recusaram minha NF", "next": "nf_recusada"},
            {"text": "Voltar", "next": "revendedor_listar"}
        ]
    },
    "nf_recusada": {
        "question": "NF recusada - Confira esses pontos:",
        "checklist": ["NF emitida nos ultimos 365 dias?", "NF tem 10+ unidades da MESMA marca?", "Nome da marca na NF bate com a marca do produto?", "NF esta legivel (nao cortada/borrada)?", "NF em nome da sua empresa (mesmo CNPJ)?"],
        "options": [
            {"text": "Corrigi e reenviei", "next": "erro_autorizacao"},
            {"text": "Ta tudo certo mas recusou mesmo assim", "next": "nf_recusada_ajuda"},
            {"text": "Voltar", "next": "erro_autorizacao"}
        ]
    },
    "nf_recusada_ajuda": {
        "question": "NF correta mas recusou? Abra um chamado:",
        "steps": ["Va em Seller Central - Ajuda (canto superior)", "Clique em Obter Ajuda", "Busque por 'autorizacao de marca'", "Localize o chamado e clique em Responder", "Explique que a NF atende os requisitos", "Peca revisao humana"],
        "info": "Se nao conseguir resolver, entre em contato com seu Account Manager (AM).",
        "options": [
            {"text": "Resolveu!", "next": "sucesso"},
            {"text": "Nao resolveu", "next": "inicio"},
            {"text": "Voltar", "next": "nf_recusada"}
        ]
    },
    "erros_inicio": {
        "question": "Qual erro apareceu?",
        "options": [
            {"text": "Erro no EAN (invalido ou duplicado)", "next": "erro_ean"},
            {"text": "Pediu autorizacao de marca", "next": "erro_autorizacao"},
            {"text": "Categoria restrita (precisa aprovacao)", "next": "erro_categoria"},
            {"text": "Erro de atributo obrigatorio", "next": "erro_atributo"},
            {"text": "Imagem rejeitada", "next": "erro_imagem"},
            {"text": "Outro erro", "next": "erro_outro"}
        ]
    },
    "erro_ean": {
        "question": "Erro no EAN:",
        "info": "Possiveis causas e solucoes:",
        "checklist": ["EAN ja existe com outra marca: voce foi redirecionado pra 'Vender este produto' (e correto!)", "EAN invalido: valide no GS1 e tente novamente", "EAN duplicado no seu catalogo: verifique se ja listou esse produto"],
        "options": [
            {"text": "Validar EAN no GS1", "link": "https://www.gs1.org/services/verified-by-gs1/results"},
            {"text": "Listar sem EAN", "next": "listar_generico_sem_ean"},
            {"text": "Voltar", "next": "erros_inicio"}
        ]
    },
    "erro_categoria": {
        "question": "Categoria restrita!",
        "info": "Algumas categorias precisam de aprovacao antes de vender. Geralmente pedem documentos como NF, certificados ANVISA, INMETRO ou ANATEL.",
        "steps": ["Clique em 'Solicitar aprovacao' quando aparecer", "Prepare os documentos solicitados", "Envie e aguarde 5-10 dias uteis"],
        "options": [
            {"text": "Ver categorias restritas", "link": "https://sellercentral.amazon.com.br/help/hub/reference/external/G200164330?locale=pt-BR"},
            {"text": "Voltar", "next": "erros_inicio"}
        ]
    },
    "erro_atributo": {
        "question": "Erro de atributo obrigatorio:",
        "info": "O sistema esta pedindo um campo que voce nao preencheu. Campos obrigatorios mais comuns:",
        "checklist": ["Titulo do produto", "Marca", "Imagem principal (fundo branco)", "Preco", "Quantidade em estoque", "Condicao (novo/usado)", "Categoria"],
        "highlight": "Volte na pagina do produto e preencha o campo que esta em vermelho/destaque.",
        "options": [
            {"text": "Corrigi! Deu certo", "next": "sucesso"},
            {"text": "Voltar", "next": "erros_inicio"}
        ]
    },
    "erro_imagem": {
        "question": "Imagem rejeitada:",
        "info": "A Amazon tem regras para imagens. Confira:",
        "checklist": ["Fundo BRANCO puro (RGB 255,255,255)", "Minimo 1000x1000 pixels", "Produto ocupa 85% do espaco", "Sem textos, logos ou marcas d'agua", "Sem embalagem transparente na frente", "Formato JPG, PNG ou GIF"],
        "highlight": "App gratuito pra remover fundo: remove.bg ou PhotoRoom",
        "options": [
            {"text": "Corrigi a imagem! Deu certo", "next": "sucesso"},
            {"text": "Voltar", "next": "erros_inicio"}
        ]
    },
    "erro_outro": {
        "question": "Outro erro?",
        "info": "Se o erro nao esta listado aqui, tente:",
        "steps": ["Copie a mensagem de erro exata", "Va em Seller Central - Ajuda - Obter Ajuda", "Cole a mensagem e abra um chamado", "Ou entre em contato com seu Account Manager"],
        "options": [
            {"text": "Resolveu!", "next": "sucesso"},
            {"text": "Voltar ao inicio", "next": "inicio"}
        ]
    },
    "usado": {
        "question": "Produto Usado / Seminovo",
        "info": "Para vender produtos usados, a Amazon tem o programa Amazon Seminovos:",
        "steps": ["Acesse o link abaixo", "Cadastre-se no programa Seminovos", "Siga as instrucoes de listagem especificas"],
        "options": [
            {"text": "Ir para Amazon Seminovos", "link": "https://venda.amazon.com.br/seminovos"},
            {"text": "Voltar", "next": "manual_novo_usado"}
        ]
    },
    "massivo_inicio": {
        "question": "Listagem Massiva (muitos produtos)",
        "info": "Para listar muitos produtos de uma vez, a melhor opcao depende do seu caso:",
        "options": [
            {"text": "Tenho integrador (Bling, Tiny, etc)", "next": "massivo_integrador"},
            {"text": "Ja vendo em outro marketplace e tenho planilha", "next": "massivo_planilha"},
            {"text": "Nunca vendi online (so tenho fotos/anotacoes)", "next": "massivo_zero"},
            {"text": "Quero que listem pra mim", "link": "https://amazonexteu.qualtrics.com/jfe/form/SV_eEhccc2rqm5WURw"}
        ]
    },
    "massivo_integrador": {
        "question": "Voce tem integrador!",
        "info": "Se voce usa Bling, Tiny, Ideris, Anymarket ou outro integrador, ele ja faz a listagem massiva pra voce!",
        "steps": ["Acesse seu integrador", "Conecte com a Amazon (se ainda nao fez)", "Sincronize seus produtos", "O integrador envia tudo pra Amazon automaticamente"],
        "highlight": "Se deu erro de integracao, entre em contato com o suporte do seu integrador. Eles conhecem os erros mais comuns!",
        "options": [
            {"text": "Deu certo!", "next": "sucesso"},
            {"text": "Erros na integracao - quero listar manual", "next": "massivo_planilha"},
            {"text": "Voltar", "next": "massivo_inicio"}
        ]
    },
    "massivo_planilha": {
        "question": "Listagem por planilha:",
        "info": "A Amazon aceita upload de planilha Excel (.xlsx) com todos os seus produtos de uma vez.",
        "steps": ["Seller Central - Catalogo - Adicionar produtos via upload", "Baixe o modelo de planilha da sua categoria", "Preencha os dados dos produtos (1 linha por SKU)", "Para variacoes: 1 linha SKU pai + 1 linha por variacao", "Faca upload da planilha preenchida", "Aguarde o processamento (pode levar algumas horas)"],
        "highlight": "Dica: Se voce ja tem planilha de outro marketplace (Mercado Livre, Shopee), use ela como base! Ajuste os campos pro formato Amazon.",
        "options": [
            {"text": "Tutorial: como preencher a planilha", "next": "massivo_tutorial_planilha"},
            {"text": "Como colocar imagens na planilha", "next": "massivo_imagens"},
            {"text": "Deu certo!", "next": "sucesso"},
            {"text": "Voltar", "next": "massivo_inicio"}
        ]
    },
    "massivo_tutorial_planilha": {
        "question": "Como preencher a planilha Amazon:",
        "info": "Campos essenciais em cada linha:",
        "checklist": ["SKU (codigo interno seu - invente um)", "Titulo do produto", "Marca (ou Generico)", "Preco", "Quantidade em estoque", "EAN (se tiver)", "Link da imagem principal", "Descricao", "Bullet points (pontos-chave)"],
        "warning": "Para variacoes (tamanho, cor): crie 1 linha 'pai' + 1 linha para cada variacao (filho). Cada filho tem seu proprio SKU, EAN e preco.",
        "options": [
            {"text": "Como colocar imagens", "next": "massivo_imagens"},
            {"text": "Voltar", "next": "massivo_planilha"}
        ]
    },
    "massivo_imagens": {
        "question": "Como colocar imagens na planilha:",
        "info": "A planilha pede um LINK publico da imagem (URL). Voce precisa hospedar a imagem online primeiro.",
        "steps": ["Suba a imagem no Google Drive", "Clique com botao direito - Compartilhar - Qualquer pessoa com link", "Copie o link", "Cole na coluna de imagem da planilha"],
        "highlight": "Importante: O link precisa ser PUBLICO! Se for privado, a Amazon nao consegue acessar.",
        "options": [
            {"text": "Entendi! Vou fazer", "next": "massivo_planilha"},
            {"text": "Voltar", "next": "massivo_planilha"}
        ]
    },
    "massivo_zero": {
        "question": "Primeira vez vendendo online:",
        "info": "Se voce nunca vendeu online e so tem fotos ou anotacoes, o melhor caminho e:",
        "options": [
            {"text": "Aprender a usar a planilha", "next": "massivo_tutorial_planilha"},
            {"text": "Listar 1 a 1 primeiro (mais facil)", "next": "manual_novo_usado"},
            {"text": "Quero que listem pra mim", "link": "https://amazonexteu.qualtrics.com/jfe/form/SV_eEhccc2rqm5WURw"}
        ]
    },
    "sucesso": {
        "question": "Parabens! Produto listado com sucesso!",
        "success": "Seu produto ja esta na Amazon. Agora e so aguardar as vendas!",
        "info": "Proximos passos para vender mais:",
        "options": [
            {"text": "Listar outro produto", "next": "inicio"},
            {"text": "Dicas para vender mais", "link": "https://venda.amazon.com.br"}
        ]
    }
}

with open('data/flow.json', 'w', encoding='utf-8') as f:
    json.dump(flow, f, ensure_ascii=False, indent=2)

print(f'\ndata/flow.json criado com {len(flow)} telas!')
print(f'\nSUCESSO! Todos os arquivos criados!')
print('Agora suba a pasta inteira pro GitHub e Netlify!')

