Aqui está um relatório pronto e organizado com base no **Algoritmo de Bresenham** 👇

---

# 📝 Relatório – Algoritmo de Rasterização de Linha

## 📌 Nome do Algoritmo

O algoritmo escolhido é o **Algoritmo de Bresenham**.

---

## ⚡ Principal Vantagem em relação ao DDA

A principal vantagem do Algoritmo de Bresenham em relação ao **DDA (Digital Differential Analyzer)** é:

* ✅ **Não utiliza números decimais (ponto flutuante)**
* ✅ Usa apenas **operações inteiras (soma e subtração)**
* ✅ **Mais rápido e eficiente**, especialmente em sistemas com menos poder computacional

👉 Enquanto o DDA realiza cálculos com valores reais e arredondamentos, o Bresenham evita isso completamente, tornando o processamento mais leve.

---

## 🧠 Como ele decide o próximo pixel?

O algoritmo utiliza um **parâmetro de decisão (erro)** para determinar qual será o próximo pixel.

### Funcionamento:

* A cada passo no eixo principal (geralmente X), ele avalia um valor chamado **erro (d)**.
* Esse valor indica se a linha "ideal" está mais próxima de:

  * Um pixel na horizontal (→)
  * Ou um pixel na diagonal (↗)

### Regra de decisão:

* Se **d ≤ 0** → escolhe o próximo pixel na horizontal
* Se **d > 0** → escolhe o pixel na diagonal (incrementa Y também)

👉 Após cada decisão, o erro é atualizado para o próximo passo.

---

## 💻 Algoritmo (Exemplo)

```python
def bresenham(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    y = y1

    pontos = []

    for x in range(x1, x2 + 1):
        pontos.append((x, y))

        if d > 0:
            y += 1
            d -= 2*dx

        d += 2*dy

    return pontos
```

---

## 📊 Conclusão

O **Algoritmo de Bresenham** é uma das formas mais eficientes de desenhar linhas em computação gráfica, sendo amplamente utilizado devido à sua:

* Alta performance
* Simplicidade
* Uso exclusivo de inteiros

Apesar de não suavizar a linha (efeito de “escada”), ele é ideal para aplicações onde desempenho é prioridade.

---

Se quiser, posso adaptar esse relatório pro formato **ABNT**, PDF ou deixar mais "acadêmico" ainda 👍
