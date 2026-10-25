
<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Simulador Psicotécnico Angola</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#f1f5f9;color:#172033;font-family:Arial,sans-serif}
header{background:#102a43;color:white;padding:22px 15px;text-align:center}
header h1{font-size:22px;margin:0 0 8px}
main{max-width:650px;margin:20px auto;padding:0 14px}
.card{background:white;border-radius:14px;padding:20px;margin-bottom:16px}
button{border:0;border-radius:9px;padding:14px;font-size:15px;font-weight:bold;cursor:pointer}
.primary{background:#1769aa;color:white;width:100%}
.secondary{background:#e2e8f0;color:#172033}
.hidden{display:none}
.topline{display:flex;justify-content:space-between;gap:10px;font-weight:bold}
#timer{color:#b42318;font-variant-numeric:tabular-nums}
.progress{height:8px;background:#e2e8f0;border-radius:10px;overflow:hidden;margin:15px 0}
#bar{height:100%;width:0;background:#16845b}
#question{font-size:19px;line-height:1.5;font-weight:bold;margin:20px 0}
.option{display:block;width:100%;text-align:left;background:#f8fafc;border:2px solid #e2e8f0;margin:9px 0;line-height:1.4}
.option.selected{border-color:#1769aa;background:#eaf4ff}
.nav{display:flex;gap:10px;margin-top:18px}
.nav button{flex:1}
.small{font-size:13px;color:#64748b;line-height:1.5}
#result{text-align:center}
.score{font-size:42px;font-weight:bold;color:#1769aa;margin:15px}
</style>
</head>
<body>
<header>
<h1>Assistente Psicotécnico Angola</h1>
<p>20 perguntas • 1 minuto por pergunta</p>
</header>
<main>
<section class="card" id="intro">
<h2>Simulador psicotécnico</h2>
<p>Responde a 20 perguntas de treino. Tens 60 segundos para cada pergunta.</p>
<p class="small">Quando o tempo terminar, o sistema passa automaticamente à pergunta seguinte. O tempo não é acumulado.</p>
<p class="small">Simulação para treino, não representa necessariamente as perguntas oficiais do concurso.</p>
<button class="primary" onclick="startTest()">Iniciar teste</button>
</section>

<section class="card hidden" id="quiz">
<div class="topline"><span id="counter"></span><span id="timer">01:00</span></div>
<div class="progress"><div id="bar"></div></div>
<div id="question"></div>
<div id="options"></div>
<p class="small" id="notice">Escolhe uma alternativa antes de o tempo terminar.</p>
<div class="nav">
<button class="secondary" id="prev" onclick="move(-1)">Anterior</button>
<button class="primary" id="next" onclick="move(1)">Seguinte</button>
</div>
<button class="secondary" style="width:100%;margin-top:12px" onclick="finishTest(false)">Terminar teste</button>
</section>

<section class="card hidden" id="result">
<h2>Resultado do teste</h2>
<div class="score" id="score"></div>
<p id="details"></p>
<div id="review"></div>
<button class="primary" onclick="location.reload()">Repetir teste</button>
</section>
</main>
<script>
const questions=[
{q:"Qual é o próximo número: 2, 4, 8, 16, ...?",o:["18","24","32","36"],a:2,e:"Cada número é o dobro do anterior."},
{q:"Qual é o próximo número: 5, 10, 15, 20, ...?",o:["22","25","30","35"],a:1,e:"A sequência aumenta de 5 em 5."},
{q:"Qual elemento é diferente dos outros?",o:["Círculo","Triângulo","Quadrado","Maçã"],a:3,e:"Maçã é um fruto; os restantes são figuras geométricas."},
{q:"Todos os agentes são trabalhadores. Paulo é agente. Logo:",o:["Paulo não trabalha","Paulo é trabalhador","Todos os trabalhadores são agentes","Não se pode concluir"],a:1,e:"Paulo pertence ao grupo dos agentes, que são trabalhadores."},
{q:"Qual é o próximo número: 1, 4, 9, 16, ...?",o:["20","24","25","36"],a:2,e:"São quadrados perfeitos: 1, 4, 9, 16, 25."},
{q:"Se hoje é segunda-feira, que dia será daqui a 3 dias?",o:["Terça-feira","Quarta-feira","Quinta-feira","Sexta-feira"],a:2,e:"Três dias depois de segunda-feira é quinta-feira."},
{q:"Qual palavra não pertence ao grupo?",o:["Cão","Gato","Cavalo","Mesa"],a:3,e:"Mesa não é um animal."},
{q:"Completa: 20, 18, 16, 14, ...",o:["13","12","11","10"],a:1,e:"A sequência diminui de 2 em 2."},
{q:"3 cadernos custam 600 Kz. Quanto custam 5?",o:["800 Kz","900 Kz","1.000 Kz","1.200 Kz"],a:2,e:"Cada caderno custa 200 Kz; cinco custam 1.000 Kz."},
{q:"Qual letra vem a seguir: A, C, E, G, ...?",o:["H","I","J","K"],a:1,e:"Avança uma letra, deixando uma letra de intervalo."},
{q:"Qual é o próximo número: 3, 6, 12, 24, ...?",o:["30","36","48","54"],a:2,e:"Cada número é multiplicado por 2."},
{q:"Qual número é o menor?",o:["0,8","0,08","0,88","0,18"],a:1,e:"0,08 é menor do que as outras opções."},
{q:"Se 10 pessoas fazem um trabalho em 2 dias, ao mesmo ritmo, quantas pessoas-dia são necessárias?",o:["5","10","20","30"],a:2,e:"10 pessoas durante 2 dias equivalem a 20 pessoas-dia."},
{q:"Qual é o próximo número: 100, 90, 80, 70, ...?",o:["65","60","55","50"],a:1,e:"A sequência diminui de 10 em 10."},
{q:"Livro está para ler assim como comida está para:",o:["Dormir","Comer","Escrever","Correr"],a:1,e:"A relação é objecto e acção correspondente."},
{q:"Se ontem foi domingo, que dia é hoje?",o:["Sábado","Segunda-feira","Terça-feira","Quarta-feira"],a:1,e:"O dia depois de domingo é segunda-feira."},
{q:"Qual é o próximo número: 2, 5, 8, 11, ...?",o:["12","13","14","15"],a:1,e:"A sequência aumenta de 3 em 3."},
{q:"Qual figura tem quatro lados iguais?",o:["Triângulo","Círculo","Quadrado","Pentágono"],a:2,e:"Um quadrado tem quatro lados iguais."},
{q:"Uma viatura percorre 60 km em 1 hora. Quantos km percorre em 3 horas à mesma velocidade?",o:["120 km","150 km","180 km","240 km"],a:2,e:"60 × 3 = 180 km."},
{q:"Qual é o próximo número: 1, 1, 2, 3, 5, 8, ...?",o:["11","12","13","15"],a:2,e:"Cada número é a soma dos dois anteriores: 5 + 8 = 13."}
];
let index=0,answers=Array(questions.length).fill(null),remaining=60,interval=null,finished=false,visited=Array(questions.length).fill(false);
function formatTime(){return "00:"+String(remaining).padStart(2,"0")}
function startTest(){
document.getElementById("intro").classList.add("hidden");
document.getElementById("quiz").classList.remove("hidden");
beginQuestion();
}
function beginQuestion(){
if(finished)return;
clearInterval(interval);
remaining=60;
visited[index]=true;
render();
interval=setInterval(()=>{
remaining--;
document.getElementById("timer").textContent=formatTime();
if(remaining<=0){
clearInterval(interval);
if(index===questions.length-1)finishTest(true);
else{index++;beginQuestion()}
}
},1000);
}
function render(){
const q=questions[index];
document.getElementById("counter").textContent="Pergunta "+(index+1)+" de "+questions.length;
document.getElementById("timer").textContent=formatTime();
document.getElementById("bar").style.width=((index+1)/questions.length*100)+"%";
document.getElementById("question").textContent=q.q;
const box=document.getElementById("options");box.innerHTML="";
q.o.forEach((option,i)=>{
const b=document.createElement("button");
b.className="option"+(answers[index]===i?" selected":"");
b.textContent=String.fromCharCode(65+i)+") "+option;
b.onclick=()=>{answers[index]=i;render()};
box.appendChild(b);
});
document.getElementById("prev").disabled=index===0;
document.getElementById("next").textContent=index===questions.length-1?"Terminar":"Seguinte";
}
function move(delta){
if(index===questions.length-1&&delta>0){finishTest(false);return}
const target=index+delta;
if(target<0||target>=questions.length)return;
index=target;
beginQuestion();
}
function finishTest(timeUp){
if(finished)return;
if(!timeUp&&!confirm("Queres terminar e ver a pontuação?"))return;
finished=true;clearInterval(interval);
document.getElementById("quiz").classList.add("hidden");
document.getElementById("result").classList.remove("hidden");
let correct=0;
questions.forEach((q,i)=>{if(answers[i]===q.a)correct++});
document.getElementById("score").textContent=correct+"/"+questions.length;
document.getElementById("details").textContent="Correctas: "+correct+" • Erradas ou sem resposta: "+(questions.length-correct)+" • Resultado: "+(correct*5)+"%"+(timeUp?" • O tempo terminou.":"");
const review=document.getElementById("review");
review.style.textAlign="left";
questions.forEach((q,i)=>{
const p=document.createElement("p");
p.textContent=(i+1)+". "+(answers[i]===q.a?"✓ Correcta":"✗ Incorrecta ou sem resposta")+". Resposta: "+String.fromCharCode(65+q.a)+") "+q.o[q.a]+". "+q.e;
review.appendChild(p);
});
}
</script>
</body>
</html>
