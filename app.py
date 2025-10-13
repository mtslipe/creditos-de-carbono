import json
import customtkinter as ctk

with open('perguntas.json', 'r', encoding='utf-8') as arq:
    vListaPerguntas = json.load(arq)

ctk.set_appearance_mode("dark") #cor
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Calculadora de Créditos de Carbono")
janela.geometry("900x800")

entradas = []
escolhas = []

frame_menu = ctk.CTkFrame(janela)
frame_perguntas = ctk.CTkFrame(janela)

#func de navegação
def mostrar_menu():
    frame_perguntas.pack_forget()
    frame_menu.pack(fill="both", expand=True)

def mostrar_perguntas(tipo):
    frame_menu.pack_forget()
    frame_perguntas.pack(fill="both", expand=True)
    carregar_perguntas(tipo)

#func para habilitar/desabilitar campo de escrita
def alternar_campo(valor, entry_widget):
    if valor == "Sim":
        entry_widget.configure(state="normal")
    else:
        entry_widget.delete(0, "end")
        entry_widget.configure(state="disabled")

#func de calcular
def calcular_co2(tipo):
    total_co2 = 0
    perguntas_lista = vListaPerguntas['pergunta_pessoas'] if tipo == 'pessoas' else vListaPerguntas['pergunta_empresas']

    for i, pergunta in enumerate(perguntas_lista):
        escolha = escolhas[i].get()
        entrada_valor = entradas[i]

        if escolha == "Sim":
            try:
                valor = float(entrada_valor.get().strip())
                co2_emitido = valor * pergunta["calculo_co2"]
                total_co2 += co2_emitido
            except ValueError:
                resultado_label.configure(
                    text=f"⚠️ Valor inválido na pergunta {i+1}. Digite um número.",
                    text_color="red"
                )
                return

    #conversão para créditos e valores
    preco_credito = 30  # R$ por crédito | alterar para o mais realista
    co2_em_ton = total_co2 / 1000  # kg -> toneladas
    creditos = co2_em_ton  # 1 crédito = 1 tonelada CO₂
    valor_reais = creditos * preco_credito
    mudas = creditos  # 1 crédito = 1 muda

    resultado_label.configure(
        text=(f"Total de emissões: {total_co2:.2f} kg de CO₂\n"
              f"Equivalente em créditos de carbono: {creditos:.2f} tCO₂\n"
              f"Valor aproximado em dinheiro: R$ {valor_reais:.2f}\n"
              f"Equivalente em mudas: {mudas:.2f} mudas"),
        text_color="lightgreen"
    )


#func para carregar perguntas de forma dinamicamente
def carregar_perguntas(tipo):
    #limpar frame se já tiver conteúdo nele
    for widget in frame_perguntas.winfo_children():
        widget.destroy()

    global entradas, escolhas
    entradas = []
    escolhas = []

    perguntas_lista = vListaPerguntas['pergunta_pessoas'] if tipo == 'pessoas' else vListaPerguntas['pergunta_empresas']

    scroll_frame = ctk.CTkScrollableFrame(frame_perguntas, width=850, height=550)
    scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

    for i, pergunta in enumerate(perguntas_lista):
        frame = ctk.CTkFrame(scroll_frame)
        frame.pack(pady=10, padx=10, fill="x")

        lbl = ctk.CTkLabel(frame, text=pergunta["pergunta"], anchor="w", wraplength=800, font=ctk.CTkFont(size=15))
        lbl.pack(pady=(5, 2), anchor="w")

        escolha_var = ctk.StringVar(value="Não")
        escolhas.append(escolha_var)

        frame_botoes = ctk.CTkFrame(frame)
        frame_botoes.pack(pady=5, anchor="w")

        btn_sim = ctk.CTkRadioButton(frame_botoes, text="Sim", variable=escolha_var, value="Sim",
                                     command=lambda v="Sim", i=i: alternar_campo(v, entradas[i]))
        btn_nao = ctk.CTkRadioButton(frame_botoes, text="Não", variable=escolha_var, value="Não",
                                     command=lambda v="Não", i=i: alternar_campo(v, entradas[i]))
        btn_sim.pack(side="left", padx=10)
        btn_nao.pack(side="left")

        lbl_contra = ctk.CTkLabel(frame, text=pergunta["contra_pergunta"], anchor="w", wraplength=800,
                                  font=ctk.CTkFont(size=13, slant="italic"))
        lbl_contra.pack(pady=(5, 0), anchor="w")

        entrada_valor = ctk.CTkEntry(frame, placeholder_text="Digite aqui...", state="disabled")
        entrada_valor.pack(pady=(2, 5), fill="x")
        entradas.append(entrada_valor)

    #botões calcular e voltar
    btn_calcular = ctk.CTkButton(frame_perguntas, text="Calcular Emissão de CO₂", command=lambda t=tipo: calcular_co2(t))
    btn_calcular.pack(pady=10)

    global resultado_label
    resultado_label = ctk.CTkLabel(frame_perguntas, text="", font=ctk.CTkFont(size=18, weight="bold"))
    resultado_label.pack(pady=10)

    btn_voltar = ctk.CTkButton(frame_perguntas, text="Voltar", command=mostrar_menu)
    btn_voltar.pack(pady=10)

#tela menu
lbl_menu = ctk.CTkLabel(frame_menu, text="Escolha o tipo de perguntas", font=ctk.CTkFont(size=20, weight="bold"))
lbl_menu.pack(pady=50)

btn_pessoas = ctk.CTkButton(frame_menu, text="Perguntas de Pessoas", width=300, height=50, command=lambda: mostrar_perguntas('pessoas'))
btn_pessoas.pack(pady=20)

btn_empresas = ctk.CTkButton(frame_menu, text="Perguntas de Empresas", width=300, height=50, command=lambda: mostrar_perguntas('empresas'))
btn_empresas.pack(pady=20)

#mostrar tela inicial
frame_menu.pack(fill="both", expand=True)

#loop principal
janela.mainloop()
