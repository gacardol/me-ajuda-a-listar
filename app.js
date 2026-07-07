const SHEETDB='https://sheetdb.io/api/v1/7x95jmwaouxrl';
let F={},H=[];

async function init(){
try{const r=await fetch('flow.json');F=await r.json();pedirContato();}
catch(e){document.getElementById('app').innerHTML='<p>Erro ao carregar. Recarregue a pagina.</p>';}
}

function pedirContato(){
document.getElementById('app').innerHTML=
'<div style="max-width:400px;margin:40px auto;padding:30px;background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.1);text-align:center;">'+
'<h2 style="color:#232F3E;">Ola! Vou te ajudar a listar</h2>'+
'<p style="color:#555;">Primeiro, me deixe um contato pra te ajudarmos se precisar.</p>'+
'<p style="color:#FF9900;font-weight:bold;">100% gratuito!</p>'+
'<input id="zap" type="text" placeholder="WhatsApp com DDD ou Email" style="width:100%;padding:12px;border:2px solid #FF9900;border-radius:8px;font-size:16px;margin:16px 0;box-sizing:border-box;" />'+
'<p id="erro" style="color:red;display:none;">Por favor, digite seu WhatsApp ou Email para continuar</p>'+
'<button onclick="comecar()" style="background:#FF9900;color:#fff;border:none;padding:14px 32px;border-radius:8px;font-size:18px;cursor:pointer;width:100%;">Comecar!</button>'+
'</div>';
}

function comecar(){
var v=document.getElementById('zap').value.trim();
if(!v){document.getElementById('erro').style.display='block';return;}
fetch(SHEETDB,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({data:{whatsapp:v,observacao:'inicio',tela:'inicio'}})}).catch(function(){});
tela('inicio');
}

function tela(id){
var s=F[id];
if(!s){document.getElementById('app').innerHTML='<p>Tela nao encontrada.</p>';return;}
H.push(id);
var h='<div style="max-width:500px;margin:20px auto;padding:24px;background:#fff;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.1);">';
h+='<h2 style="color:#232F3E;">'+s.question+'</h2>';
if(s.info)h+='<p style="color:#555;background:#f0f0f0;padding:12px;border-radius:8px;">'+s.info+'</p>';
if(s.warning)h+='<p style="color:#d32f2f;background:#fde;padding:12px;border-radius:8px;">'+s.warning+'</p>';
if(s.steps){h+='<div style="text-align:left;margin:16px 0;">';for(var i=0;i<s.steps.length;i++){h+='<p style="margin:8px 0;padding:8px;background:#fff3e0;border-radius:6px;"><strong>'+(i+1)+'.</strong> '+s.steps[i]+'</p>';}h+='</div>';}
if(s.options){h+='<div style="margin-top:20px;">';for(var j=0;j<s.options.length;j++){var o=s.options[j];if(o.link){h+='<a href="'+o.link+'" target="_blank" style="display:block;margin:8px 0;padding:14px;background:#146EB4;color:#fff;text-decoration:none;border-radius:8px;text-align:center;">'+o.text+'</a>';}else{h+='<button onclick="tela(\''+o.next+'\')" style="display:block;width:100%;margin:8px 0;padding:14px;background:#FF9900;color:#fff;border:none;border-radius:8px;font-size:16px;cursor:pointer;">'+o.text+'</button>';}}h+='</div>';}
if(H.length>1){h+='<div style="margin-top:20px;padding-top:16px;border-top:1px solid #eee;display:flex;gap:8px;justify-content:center;">';h+='<button onclick="voltar()" style="background:#eee;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;">Voltar</button>';h+='<button onclick="tela(\'inicio\')" style="background:#eee;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;">Inicio</button>';h+='<a href="https://amazonexteu.qualtrics.com/jfe/form/SV_eEhccc2rqm5WURw" target="_blank" style="background:#146EB4;color:#fff;padding:8px 16px;border-radius:6px;text-decoration:none;">Lista pra mim</a>';h+='</div>';}
h+='</div>';
document.getElementById('app').innerHTML=h;
}

function voltar(){H.pop();var p=H.pop();if(p)tela(p);else pedirContato();}

init();
