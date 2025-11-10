import json
import customtkinter as ctk
import os
from datetime import datetime
import tkinter.messagebox as messagebox

with open('perguntas.json', 'r', encoding='utf-8') as arq:
    vListaPerguntas = json.load(arq)

# customização de tema
corFundo = "#ffffff"  
corBtn = "#2e7d32"    
corFonte = "#ffffff"  
corHover = "#43a047"  
corTexto = "#333333" 
corFrame = "#f8f9fa"  


# adicionar novas cores para a página de cálculo
corCard = "#ffffff"           
corBorda = "#e0e0e0"         
corPergunta = "#1b5e20"      
corContraPergunta = "#666666" 
corResultadoFundo = "#f1f8e9" 

fonteTitulo = ("Helvetica", 22, "bold")
fonteLabel = ("Helvetica", 16)
fonteBtn = ("Helvetica", 16, "bold")
fonteEntry = ("Helvetica", 16)

usuario = None  

ctk.set_appearance_mode("light") # cor
ctk.set_default_color_theme("green")

# criar janela principal e cabeçalho
janela = ctk.CTk()
janela.title("Calculadora de Carbono")
janela.geometry("900x1000")
janela.configure(fg_color=corFundo)

# criar frame do cabeçalho
header_frame = ctk.CTkFrame(janela, height=40, fg_color=corBtn)
header_frame.pack(fill="x", pady=0)
header_frame.pack_propagate(False)

# container do cabeçalho (melhor alinhamento)
header_container = ctk.CTkFrame(header_frame, fg_color="transparent")
header_container.pack(fill="both", expand=True)

# adicionar nome do app ao cabeçalho (em um container para melhor alinhamento)
header_label = ctk.CTkLabel(
    header_container, 
    text="Calculadora de Carbono",
    text_color=corFonte,
    font=ctk.CTkFont("Helvetica", 20, "bold")
)
header_label.pack(side="left", padx=20)

# botão reiniciar
restart_btn = ctk.CTkButton(
    header_container,
    text="↺ Reiniciar",
    width=100,
    height=30,
    font=ctk.CTkFont("Helvetica", 14),
    fg_color=corBtn,
    hover_color=corHover,
    text_color=corFonte,
    corner_radius=8,
    command=lambda: reiniciar_app()
)
restart_btn.pack(side="right", padx=20)

entradas = []
escolhas = []

frame_menu = ctk.CTkFrame(janela, fg_color=corFundo)
frame_perguntas = ctk.CTkFrame(janela, fg_color=corFundo)

HIST_FILE = 'historico.json'

def carregar_historico():
    if os.path.exists(HIST_FILE):
        try:
            with open(HIST_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def salvar_historico(entrada):
    historico = carregar_historico()
    historico.append(entrada)
    with open(HIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

# tipos de projetos com preço e descrição
project_types = {
    "Reflorestamento": {"price": 90.0, "desc": "Plantar árvores para sequestrar CO₂ e restaurar ecossistemas."},
    "Energias Renováveis": {"price": 85.0, "desc": "Investimento em parques eólicos/solar para reduzir emissões."},
    "Captura de Metano": {"price": 110.0, "desc": "Captura de metano em aterros e fazendas para reduzir GEE."},
    "Conservação Florestal": {"price": 75.0, "desc": "Proteção de florestas existentes para manter estoques de carbono."}
}

# variáveis para ui/estado do cálculo
selected_project_var = None
project_desc_label = None
compensation_cost_label = None
ultimo_calculo = None

def mostrar_historico(tipo=None):
    # usa frame_perguntas para mostrar histórico (sem criar nova janela)
    for widget in frame_perguntas.winfo_children():
        widget.destroy()

    # container principal do histórico
    container = ctk.CTkFrame(frame_perguntas, fg_color=corFrame, corner_radius=15)
    container.pack(pady=30, padx=50, fill="both", expand=True)

    # título do histórico
    title_label = ctk.CTkLabel(
        container,
        text="Histórico de Cálculos",
        font=ctk.CTkFont("Helvetica", 24, "bold"),
        text_color=corPergunta
    )
    title_label.pack(pady=20)

    # área rolável para os registros
    scroll = ctk.CTkScrollableFrame(container, width=750, height=520, fg_color="transparent")
    scroll.pack(pady=10, padx=20, fill="both", expand=True)

    hist = carregar_historico()
    if not hist:
        ctk.CTkLabel(scroll, text="Nenhum cálculo registrado.", text_color=corTexto).pack(pady=20)
    else:
        for entry in reversed(hist):
            card = ctk.CTkFrame(scroll, fg_color=corCard, corner_radius=8, border_width=1, border_color=corBorda)
            card.pack(pady=8, padx=8, fill="x")
            ts = entry.get('timestamp', '')
            tipo_e = entry.get('tipo', '')
            usuario_entry = entry.get('usuario', '—')
            total_co2 = entry.get('total_co2', 0.0)
            creditos = entry.get('creditos', 0.0)
            valor_reais = entry.get('valor_reais', 0.0)
            mudas = entry.get('mudas', 0.0)
            compensado = entry.get('compensado', False)
            projeto = entry.get('projeto', None)
            preco_projeto = entry.get('preco_projeto', None)
            custo_comp = entry.get('custo_compensacao', None)

            texto = (f"{ts}  •  {tipo_e.capitalize()}  •  Usuário: {usuario_entry}\n"
                     f"Total de emissões: {total_co2:.2f} kg CO₂\n"
                     f"Créditos: {creditos:.2f} tCO₂  •  Valor: R$ {valor_reais:.2f}  •  Mudas: {mudas:.2f}")
            if compensado:
                texto += f"\nCompensado com: {projeto} — R$ {custo_comp:.2f} (R$ {preco_projeto:.2f}/t)"
            ctk.CTkLabel(card, text=texto, anchor="w", wraplength=680, text_color=corTexto).pack(pady=10, padx=12, anchor="w")

    # ações: voltar e limpar histórico
    actions = ctk.CTkFrame(container, fg_color="transparent")
    actions.pack(pady=12)

    def limpar():
        # confirmação antes de apagar
        confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar todo o histórico?")
        if not confirm:
            return
        # apagar arquivo e atualizar view
        if os.path.exists(HIST_FILE):
            try:
                os.remove(HIST_FILE)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível apagar o histórico:\n{e}")
                return
        for w in scroll.winfo_children():
            w.destroy()
        ctk.CTkLabel(scroll, text="Histórico limpo.", text_color=corTexto).pack(pady=20)
        messagebox.showinfo("Histórico", "Histórico apagado com sucesso.")

    clear_btn = ctk.CTkButton(actions, text="Limpar Histórico", width=160, height=36, fg_color=corBtn, hover_color=corHover, text_color=corFonte, command=limpar)
    clear_btn.pack(side="left", padx=8)

    # voltar: se chamado a partir de carregar_perguntas passa tipo para retornar à página; senão vai ao menu
    def voltar():
        for w in frame_perguntas.winfo_children():
            w.destroy()
        if tipo:
            carregar_perguntas(tipo)
        else:
            mostrar_menu()

    back_btn = ctk.CTkButton(actions, text="Voltar", width=120, height=36, fg_color=corBtn, hover_color=corHover, text_color=corFonte, command=voltar)
    back_btn.pack(side="left", padx=8)

# func de navegação
def mostrar_menu():
    frame_perguntas.pack_forget()
    
    # limpar frame_menu antes de recriar elementos
    for widget in frame_menu.winfo_children():
        widget.destroy()
    
    # container central
    container = ctk.CTkFrame(frame_menu, fg_color=corFrame, corner_radius=20)
    container.pack(pady=100, padx=50)
    
    # logo ou ícone
    logo_label = ctk.CTkLabel(
        container,
        text="🌱",
        font=ctk.CTkFont(size=50)
    )
    logo_label.pack(pady=(30, 0))
    
    # boas vindas
    lbl_menu = ctk.CTkLabel(
        container, 
        text=f"Seja Bem-Vindo, {usuario}!", 
        font=ctk.CTkFont("Helvetica", 28, "bold"),
        text_color=corTexto
    )
    lbl_menu.pack(pady=(10, 5))

    lbl_menu2 = ctk.CTkLabel(
        container, 
        text="Escolha o tipo de Pergunta:", 
        font=ctk.CTkFont("Helvetica", 22),
        text_color=corTexto
    )
    lbl_menu2.pack(pady=(0, 30))

    # botões em um frame transparente
    buttons_frame = ctk.CTkFrame(container, fg_color="transparent")
    buttons_frame.pack(pady=20, padx=50)

    btn_pessoas = ctk.CTkButton(
        buttons_frame, 
        text="Perguntas para Pessoas", 
        width=400, 
        height=60,
        font=fonteBtn,
        fg_color=corBtn,
        hover_color=corHover,
        text_color=corFonte,
        corner_radius=10,
        command=lambda: mostrar_perguntas('pessoas')
    )
    btn_pessoas.pack(pady=15)

    btn_empresas = ctk.CTkButton(
        buttons_frame, 
        text="Perguntas para Empresas", 
        width=400, 
        height=60,
        font=fonteBtn,
        fg_color=corBtn,
        hover_color=corHover,
        text_color=corFonte,
        corner_radius=10,
        command=lambda: mostrar_perguntas('empresas')
    )
    btn_empresas.pack(pady=(0, 30))
    
    frame_menu.pack(fill="both", expand=True)

def mostrar_perguntas(tipo):
    frame_menu.pack_forget()
    frame_perguntas.pack(fill="both", expand=True)
    carregar_perguntas(tipo)

# func para habilitar/desabilitar campo de escrita
def alternar_campo(valor, entry_widget):
    if valor == "Sim":
        entry_widget.configure(state="normal")
    else:
        entry_widget.delete(0, "end")
        entry_widget.configure(state="disabled")

# func de calcular
def calcular_co2(tipo):
    global ultimo_calculo
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

    # conversão para créditos e valores
    preco_credito = 78.46  # r$ por crédito | alterar para o mais realista
    co2_em_ton = total_co2 / 1000  # kg -> toneladas
    creditos = co2_em_ton  # 1 crédito = 1 tonelada co₂
    valor_reais = creditos * preco_credito
    mudas = creditos  # 1 crédito = 1 muda

    # salvar no histórico (agora inclui o usuário - registro base do cálculo)
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo,
        "usuario": usuario if usuario else "—",
        "total_co2": total_co2,
        "creditos": creditos,
        "valor_reais": valor_reais,
        "mudas": mudas,
        "compensado": False,
        "projeto": None,
        "preco_projeto": None,
        "custo_compensacao": None
    }
    salvar_historico(entry)

    # guardar ultimo calculo para possível compensação na sessão atual
    ultimo_calculo = {
        "tipo": tipo,
        "total_co2": total_co2,
        "creditos": creditos,
        "valor_reais": valor_reais,
        "mudas": mudas
    }

    resultado_label.configure(
        text=(f"Total de emissões: {total_co2:.2f} kg de CO₂\n"
              f"Equivalente em créditos de carbono: {creditos:.2f} tCO₂\n"
              f"Valor aproximado em dinheiro: R$ {valor_reais:.2f}\n"
              f"Equivalente em mudas: {mudas:.2f} mudas"),
        text_color="green"
    )

    # atualizar custo de compensação exibido (se ui presente)
    try:
        if selected_project_var and compensation_cost_label:
            proj = selected_project_var.get()
            price = project_types.get(proj, {}).get("price", 0.0)
            cost = creditos * price
            compensation_cost_label.configure(text=f"Custo para compensar com '{proj}': R$ {cost:.2f} (R$ {price:.2f}/t)")
            if project_desc_label:
                project_desc_label.configure(text=project_types[proj]["desc"])
    except Exception:
        pass

# função para executar compensação (marca histórico)
def compensar_emissao():
    global ultimo_calculo
    if not ultimo_calculo:
        messagebox.showwarning("Aviso", "Calcule as emissões antes de compensar.")
        return
    proj = selected_project_var.get() if selected_project_var else None
    if not proj:
        messagebox.showwarning("Aviso", "Escolha um projeto para compensar.")
        return
    price = project_types.get(proj, {}).get("price", 0.0)
    cost = ultimo_calculo["creditos"] * price

    # confirmação final
    confirm = messagebox.askyesno("Confirmar compensação",
                                  f"Compensar {ultimo_calculo['creditos']:.2f} tCO₂ com '{proj}' por R$ {cost:.2f}?")
    if not confirm:
        return

    # adicionar entrada de compensação ao histórico (registro separado)
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": ultimo_calculo.get("tipo", ""),
        "usuario": usuario if usuario else "—",
        "total_co2": ultimo_calculo["total_co2"],
        "creditos": ultimo_calculo["creditos"],
        "valor_reais": ultimo_calculo["valor_reais"],
        "mudas": ultimo_calculo["mudas"],
        "compensado": True,
        "projeto": proj,
        "preco_projeto": price,
        "custo_compensacao": cost
    }
    salvar_historico(entry)
    messagebox.showinfo("Sucesso", f"Compensação registrada: {proj} — R$ {cost:.2f}")

    # opcional: atualizar label de resultado indicando compensação
    if resultado_label:
        resultado_label.configure(text=resultado_label.cget("text") + f"\n\nCompensado com: {proj} (R$ {cost:.2f})")

# func para carregar perguntas de forma dinamicamente
def carregar_perguntas(tipo):
    # Limpa toda a área de perguntas
    for widget in frame_perguntas.winfo_children():
        widget.destroy()

    # Wrapper da página para centralização via grid
    page = ctk.CTkFrame(frame_perguntas, fg_color=corFundo)
    page.pack(fill="both", expand=True)
    page.grid_columnconfigure(0, weight=1)
    page.grid_rowconfigure(0, weight=1)

    # Content central (não expande em largura total)
    content = ctk.CTkFrame(page, fg_color="transparent")
    content.grid(row=0, column=0, sticky="n", padx=24, pady=(24, 12))

    # Container com largura máxima e cantos arredondados
    container = ctk.CTkFrame(content, fg_color=corFrame, corner_radius=15, width=900)
    container.pack(anchor="n", pady=6, padx=6, fill="both", expand=True)
    # Define layout em duas colunas: esquerda perguntas, direita resumo/compensação/ações
    container.grid_columnconfigure(0, weight=3)  # coluna perguntas
    container.grid_columnconfigure(1, weight=2)  # coluna lateral
    container.grid_rowconfigure(1, weight=1)     # área de perguntas com scroll ocupa o restante

    # Título (linha 0, ocupa as duas colunas)
    titulo = "Cálculo de Emissão de Carbono para " + ("Pessoas" if tipo == "pessoas" else "Empresas")
    title_label = ctk.CTkLabel(
        container,
        text=titulo,
        font=ctk.CTkFont("Helvetica", 24, "bold"),
        text_color=corPergunta
    )
    title_label.grid(row=0, column=0, columnspan=2, pady=(18, 6), padx=18, sticky="n")

    # Coluna esquerda: perguntas com scroll
    perguntas_col = ctk.CTkScrollableFrame(
        container,
        fg_color=corCard,
        width=560,
        height=560,
        corner_radius=12
    )
    perguntas_col.grid(row=1, column=0, sticky="nsew", padx=(18, 9), pady=(6, 18))

    # Coluna direita: sidebar fixa com Resultado + Compensação + Ações
    sidebar = ctk.CTkFrame(container, fg_color=corCard, corner_radius=12)
    sidebar.grid(row=1, column=1, sticky="nsew", padx=(9, 18), pady=(6, 18))
    sidebar.grid_columnconfigure(0, weight=1)

    # Estado local das listas
    global entradas, escolhas
    entradas = []
    escolhas = []

    perguntas_lista = vListaPerguntas['pergunta_pessoas'] if tipo == 'pessoas' else vListaPerguntas['pergunta_empresas']

    # Cards de perguntas na coluna esquerda
    for i, pergunta in enumerate(perguntas_lista):
        card = ctk.CTkFrame(
            perguntas_col,
            fg_color=corCard,
            corner_radius=10,
            border_width=1,
            border_color=corBorda
        )
        card.pack(pady=10, padx=12, fill="x")

        num_pergunta = ctk.CTkLabel(
            card,
            text=f"Pergunta {i+1}",
            font=ctk.CTkFont("Helvetica", 12, "bold"),
            text_color=corPergunta
        )
        num_pergunta.pack(pady=(12, 4), padx=16, anchor="w")

        lbl = ctk.CTkLabel(
            card,
            text=pergunta["pergunta"],
            anchor="w",
            wraplength=520,
            font=ctk.CTkFont(size=14),
            text_color=corTexto
        )
        lbl.pack(pady=(0, 8), padx=16, anchor="w")

        botoes = ctk.CTkFrame(card, fg_color="transparent")
        botoes.pack(pady=4, padx=16, anchor="w")

        escolha_var = ctk.StringVar(value="Não")
        escolhas.append(escolha_var)

        btn_sim = ctk.CTkRadioButton(
            botoes, text="Sim", variable=escolha_var, value="Sim",
            command=lambda v="Sim", idx=i: alternar_campo(v, entradas[idx])
        )
        btn_nao = ctk.CTkRadioButton(
            botoes, text="Não", variable=escolha_var, value="Não",
            command=lambda v="Não", idx=i: alternar_campo(v, entradas[idx])
        )
        btn_sim.pack(side="left", padx=(0, 20))
        btn_nao.pack(side="left")

        if pergunta["contra_pergunta"]:
            lbl_contra = ctk.CTkLabel(
                card,
                text=pergunta["contra_pergunta"],
                anchor="w",
                wraplength=520,
                font=ctk.CTkFont(size=13, slant="italic"),
                text_color=corContraPergunta
            )
            lbl_contra.pack(pady=(4, 10), padx=16, anchor="w")

        entrada_valor = ctk.CTkEntry(
            card,
            placeholder_text="Digite o valor aqui...",
            state="disabled",
            height=36,
            font=ctk.CTkFont(size=13),
            corner_radius=8
        )
        entrada_valor.pack(pady=(0, 14), padx=16, fill="x")
        entradas.append(entrada_valor)

    # Sidebar: Resultado
    result_frame = ctk.CTkFrame(sidebar, fg_color=corResultadoFundo, corner_radius=10)
    result_frame.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 10))
    global resultado_label
    resultado_label = ctk.CTkLabel(
        result_frame,
        text="",
        font=ctk.CTkFont(size=16, weight="bold"),
        wraplength=360,
        justify="left"
    )
    resultado_label.pack(padx=12, pady=10, anchor="w")

    # Sidebar: Compensação
    global selected_project_var, project_desc_label, compensation_cost_label
    comp_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
    comp_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(4, 10))

    ctk.CTkLabel(
        comp_frame,
        text="Opções de compensação:",
        font=ctk.CTkFont("Helvetica", 14, "bold"),
        text_color=corTexto
    ).pack(anchor="w", padx=6, pady=(2, 6))

    selected_project_var = ctk.StringVar(value=list(project_types.keys())[0])
    option = ctk.CTkOptionMenu(
        comp_frame,
        values=list(project_types.keys()),
        variable=selected_project_var,
        width=320,
        command=lambda v: update_project_info(v)
    )
    option.pack(anchor="w", padx=6, pady=(0, 8))

    project_desc_label = ctk.CTkLabel(
        comp_frame,
        text=project_types[selected_project_var.get()]["desc"],
        wraplength=360,
        text_color=corTexto,
        justify="left"
    )
    project_desc_label.pack(anchor="w", padx=6, pady=(0, 8))

    compensation_cost_label = ctk.CTkLabel(
        comp_frame,
        text="Custo para compensação: —",
        font=ctk.CTkFont("Helvetica", 13, "bold"),
        text_color=corTexto
    )
    compensation_cost_label.pack(anchor="w", padx=6, pady=(0, 8))

    # Atualizador da seleção de projeto
    def update_project_info(proj_name):
        if project_desc_label:
            project_desc_label.configure(text=project_types[proj_name]["desc"])
        try:
            if ultimo_calculo:
                price = project_types[proj_name]["price"]
                cost = ultimo_calculo["creditos"] * price
                compensation_cost_label.configure(
                    text=f"Custo para compensar com '{proj_name}': R$ {cost:.2f} (R$ {price:.2f}/t)"
                )
        except Exception:
            pass

    # Sidebar: Ações (Calcular, Histórico, Voltar, Compensar)
    actions = ctk.CTkFrame(sidebar, fg_color="transparent")
    actions.grid(row=2, column=0, sticky="ew", padx=16, pady=(6, 16))
    actions.grid_columnconfigure(0, weight=1)

    btn_calcular = ctk.CTkButton(
        actions,
        text="Calcular Emissão de CO₂",
        height=44,
        font=fonteBtn,
        fg_color=corBtn,
        hover_color=corHover,
        text_color=corFonte,
        corner_radius=10,
        command=lambda t=tipo: calcular_co2(t)
    )
    btn_calcular.grid(row=0, column=0, sticky="ew", pady=(0, 8))

    btn_historico = ctk.CTkButton(
        actions,
        text="Ver Histórico",
        height=40,
        fg_color="#6aa84f",
        hover_color="#7fc77a",
        text_color=corFonte,
        corner_radius=10,
        command=lambda: mostrar_historico(tipo)
    )
    btn_historico.grid(row=1, column=0, sticky="ew", pady=(0, 8))

    btn_voltar = ctk.CTkButton(
        actions,
        text="Voltar",
        height=40,
        fg_color=corBtn,
        hover_color=corHover,
        text_color=corFonte,
        corner_radius=10,
        command=mostrar_menu
    )
    btn_voltar.grid(row=2, column=0, sticky="ew", pady=(0, 8))

    compensar_btn = ctk.CTkButton(
        actions,
        text="Compensar Emissões",
        height=44,
        fg_color="#6aa84f",
        hover_color="#7fc77a",
        text_color=corFonte,
        corner_radius=10,
        command=compensar_emissao
    )
    compensar_btn.grid(row=3, column=0, sticky="ew")

def mostrar_login():
    frame_menu.pack_forget()
    
    login_frame = ctk.CTkFrame(janela, fg_color=corFundo)
    login_frame.pack(fill="both", expand=True)
    
    # container central
    container = ctk.CTkFrame(login_frame, fg_color=corFrame, corner_radius=20)
    container.pack(pady=100, padx=50)
    
    # logo ou ícone
    logo_label = ctk.CTkLabel(
        container,
        text="🌱",  # emoji como logo
        font=ctk.CTkFont(size=50)
    )
    logo_label.pack(pady=(30, 0))
    
    # título de boas-vindas
    title_label = ctk.CTkLabel(
        container,
        text="Calculadora de Carbono",
        font=ctk.CTkFont("Helvetica", 28, "bold"),
        text_color=corBtn
    )
    title_label.pack(pady=(10, 5))
    
    subtitle_label = ctk.CTkLabel(
        container,
        text="Sua ferramenta para um futuro sustentável",
        font=ctk.CTkFont("Helvetica", 14),
        text_color=corTexto
    )
    subtitle_label.pack(pady=(0, 20))
    
    # frame para entrada do nome
    entry_frame = ctk.CTkFrame(container, fg_color="transparent")
    entry_frame.pack(pady=20, padx=50)
    
    name_entry = ctk.CTkEntry(
        entry_frame,
        width=300,
        height=45,
        font=ctk.CTkFont("Helvetica", 16),
        placeholder_text="Digite seu nome...",
        border_width=2,
        corner_radius=10
    )
    name_entry.pack()
    
    # label para mensagem de erro
    error_label = ctk.CTkLabel(
        container,
        text="",
        text_color="red",
        font=ctk.CTkFont("Helvetica", 12)
    )
    error_label.pack()
    
    def validar_e_continuar():
        global usuario
        nome = name_entry.get().strip()
        if len(nome) < 2:
            error_label.configure(text="Por favor, digite um nome válido")
            name_entry.configure(border_color="red")
            return
        if any(char.isdigit() for char in nome):
            error_label.configure(text="O nome não deve conter números")
            name_entry.configure(border_color="red")
            return
            
        usuario = nome
        login_frame.destroy()
        mostrar_menu()
    
    # botão de continuar
    continue_btn = ctk.CTkButton(
        container,
        text="Começar",
        width=200,
        height=45,
        font=fonteBtn,
        fg_color=corBtn,
        hover_color=corHover,
        text_color=corFonte,
        corner_radius=10,
        command=validar_e_continuar
    )
    continue_btn.pack(pady=30)
    
    # vincular a tecla enter ao botão de continuar
    name_entry.bind("<Return>", lambda event: validar_e_continuar())
    
    # dar foco ao campo de entrada
    name_entry.focus()

# função para reiniciar o aplicativo
def reiniciar_app():
    if messagebox.askyesno("Reiniciar", "Deseja realmente reiniciar o aplicativo?"):
        global usuario, entradas, escolhas, selected_project_var, project_desc_label
        global compensation_cost_label, ultimo_calculo, frame_menu, frame_perguntas
        
        # resetar variáveis globais
        usuario = None
        entradas = []
        escolhas = []
        selected_project_var = None
        project_desc_label = None
        compensation_cost_label = None 
        ultimo_calculo = None

        # destruir todos os widgets exceto o cabeçalho
        for widget in janela.winfo_children():
            if widget != header_frame:
                widget.destroy()
                
        # recriar frames principais
        frame_menu = ctk.CTkFrame(janela, fg_color=corFundo)
        frame_perguntas = ctk.CTkFrame(janela, fg_color=corFundo)
        
        # reiniciar no login
        mostrar_login()

# criar frames principais (garantia de existência)
frame_menu = ctk.CTkFrame(janela, fg_color=corFundo)
frame_perguntas = ctk.CTkFrame(janela, fg_color=corFundo)

# mostrar a tela de login inicial
mostrar_login()

# loop principal
janela.mainloop()
