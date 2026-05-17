## 📌 Quando faz sentido usar ReAct (Reason + Act)

O padrão ReAct foi uma das primeiras abordagens para permitir que LLMs “pensem em voz alta”
(Thought) e decidam quando e como chamar ferramentas (Action), com base em um prompt
estritamente textual.

Esse padrão faz sentido principalmente em:
- Estudos conceituais sobre agentes e raciocínio passo a passo
- Demonstrações didáticas do funcionamento interno de agentes baseados em LLM
- Casos experimentais ou protótipos onde a interpretação do raciocínio do modelo é mais
  importante do que a robustez da execução
- Ambientes controlados, com poucas ferramentas e baixo risco de erro

## ⚠️ Limitações importantes:
O ReAct textual depende de o modelo obedecer rigorosamente a um formato de texto.
Na prática, o LLM pode misturar etapas, pular observações ou “inventar” resultados,
causando falhas de parsing e execução incorreta das tools.

## 🔍 Sobre este exemplo específico:
Neste exemplo, o uso de ReAct NÃO é o mais adequado, pois:
- As ferramentas são simples e determinísticas
- Não há necessidade de raciocínio complexo ou multi-etapas
- Erros de parsing podem fazer com que a tool não seja executada de fato
- O LLM pode responder sem respeitar a saída real da ferramenta

👉 Para este caso, o método recomendado é Tool Calling estruturado,
que garante que as ferramentas sejam executadas programaticamente,
sem depender de parsing de texto livre.
