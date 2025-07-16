"""
Conversor de Moedas com Interface Gráfica (Tkinter) 💰
------------------------------------------------------
Este programa permite ao usuário:
- Selecionar uma moeda de origem e uma de destino
- Digitar um valor a ser convertido
- Obter a conversão em tempo real com base na cotação do Yahoo Finance

Usa as bibliotecas:
- tkinter: para interface gráfica
- yfinance: para acessar cotações reais do mercado financeiro

Funcionalidades:
- Interface amigável e intuitiva
- Conversão automática com base no valor atual
- Tratamento de erros e mensagens educativas
"""

# Importa as bibliotecas necessárias
import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf  # Biblioteca para obter cotações do Yahoo Finance

# Dicionário com os nomes amigáveis das moedas e seus respectivos códigos
moedas = {
    "Real Brasileiro (BRL)": "BRL",
    "Dólar Americano (USD)": "USD",
    "Euro (EUR)": "EUR",
    "Libra Esterlina (GBP)": "GBP",
    "Peso Argentino (ARS)": "ARS",
    "Iene Japonês (JPY)": "JPY"
}


# Função para buscar a taxa de câmbio entre duas moedas usando o Yahoo Finance
def obter_taxa_yahoo(moeda_origem, moeda_destino):
    # Monta o símbolo do par de moedas no formato usado pelo Yahoo (ex: USDBRL=X)
    par = f"{moeda_origem}{moeda_destino}=X"
    ticker = yf.Ticker(par)
    dados = ticker.history(period="1d")  # Pega os dados do dia atual

    if dados.empty:
        raise ValueError("Não foi possível obter a cotação atual.")

    # Retorna o último preço de fechamento
    return dados['Close'].iloc[-1]


# Função principal chamada ao clicar no botão "Converter"
def converter():
    nome_origem = combo_origem.get()
    nome_destino = combo_destino.get()
    valor_str = entrada_valor.get()

    # Verifica se as moedas foram selecionadas
    if not nome_origem or not nome_destino:
        messagebox.showwarning("Atenção", "Selecione ambas as moedas.")
        return

    # Converte o valor digitado em número (aceita , ou .)
    try:
        valor = float(valor_str.replace(",", "."))
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor numérico válido.")
        return

    # Obtém os códigos das moedas selecionadas
    codigo_origem = moedas[nome_origem]
    codigo_destino = moedas[nome_destino]

    try:
        # Se a moeda de origem for igual à de destino, taxa é 1
        if codigo_origem == codigo_destino:
            taxa = 1.0
        else:
            # Mostra mensagem temporária enquanto busca cotação
            resultado_label.config(text="🔄 Consultando cotação em tempo real...")
            janela.update()  # Atualiza a interface
            taxa = obter_taxa_yahoo(codigo_origem, codigo_destino)

        # Realiza o cálculo da conversão
        convertido = valor * taxa

        # Exibe o resultado final
        resultado_label.config(
            text=f"{valor:.2f} {codigo_origem} = {convertido:.2f} {codigo_destino} 💱"
        )
    except Exception as e:
        # Em caso de erro (como sem internet, símbolo incorreto, etc.)
        resultado_label.config(text=f"Erro: {e}")


# ------------------ INTERFACE GRÁFICA ------------------

# Cria a janela principal
janela = tk.Tk()
janela.title("Conversor de Moedas 💰")
janela.geometry("400x350")  # Tamanho da janela
janela.resizable(False, False)  # Impede redimensionamento

# Título principal
tk.Label(janela, text="Bem-vindo ao Conversor de Moedas!", font=("Arial", 14, "bold")).pack(pady=10)

# Seletor da moeda de origem
tk.Label(janela, text="Selecione a moeda que você possui:", font=("Arial", 10)).pack()
combo_origem = ttk.Combobox(janela, values=list(moedas.keys()), state="readonly")
combo_origem.pack(pady=5)

# Seletor da moeda de destino
tk.Label(janela, text="Selecione a moeda que deseja obter:", font=("Arial", 10)).pack()
combo_destino = ttk.Combobox(janela, values=list(moedas.keys()), state="readonly")
combo_destino.pack(pady=5)

# Campo para digitar o valor
tk.Label(janela, text="Digite o valor a ser convertido:", font=("Arial", 10)).pack()
entrada_valor = tk.Entry(janela, justify="center", font=("Arial", 12))
entrada_valor.pack(pady=5)

# Botão que chama a função de conversão
btn_converter = tk.Button(
    janela,
    text="Converter",
    font=("Arial", 11),
    bg="#4CAF50", fg="white",
    command=converter
)
btn_converter.pack(pady=10)

# Área onde o resultado da conversão será exibido
resultado_label = tk.Label(janela, text="", font=("Arial", 12), fg="#333")
resultado_label.pack(pady=10)

# Rodapé com aviso da fonte da cotação
tk.Label(janela, text="Cotação fornecida por Yahoo Finance", font=("Arial", 8), fg="gray").pack(side="bottom", pady=5)

# Inicia o loop da interface gráfica
janela.mainloop()
