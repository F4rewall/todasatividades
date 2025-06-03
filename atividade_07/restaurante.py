import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
import json
import os
import datetime


# Paleta de cores e fontes
COR_FUNDO = "#f4f4f4"
COR_PRIMARIA = "#2d8cf0"
COR_SECUNDARIA = "#ffffff"
COR_TEXTO = "#333333"
COR_ERRO = "#ff4d4d"
COR_SUCESSO = "#4CAF50"

FONTE_PADRAO = ("Segoe UI", 12)
FONTE_TITULO = ("Segoe UI", 16, "bold")


class Produto:
    def __init__(self, nome, preco, codigo):
        self.nome = nome
        self.preco = float(preco)
        self.codigo = codigo

    def __str__(self):
        return f"{self.nome} - R$ {self.preco:.2f} (Código: {self.codigo})"

    def to_dict(self):
        return {"nome": self.nome, "preco": self.preco, "codigo": self.codigo}

    @classmethod
    def from_dict(cls, data):
        return cls(data["nome"], data["preco"], data["codigo"])


class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurante - Sistema de Gerenciamento")
        self.root.geometry("900x600")

        # Dados persistentes
        self.produtos = []
        self.carregar_produtos()

        # Pedidos e vendas rápidas
        self.pedidos = {}  # Armazena pedidos por número de mesa
        self.itens_caixa_rapido = []  # Itens do caixa rápido
        self.total_caixo_rapido = 0.0

        # Frames para navegação
        self.frame_principal = tk.Frame(root, bg=COR_FUNDO)
        self.frame_produtos = tk.Frame(root, bg=COR_FUNDO)
        self.frame_mesas = tk.Frame(root, bg=COR_FUNDO)
        self.frame_pedidos = tk.Frame(root, bg=COR_FUNDO)
        self.frame_caixa_rapido = tk.Frame(root, bg=COR_FUNDO)
        self.frame_historico = tk.Frame(root, bg=COR_FUNDO)
        self.frame_relatorios = tk.Frame(root, bg=COR_FUNDO)

        # Criação das telas
        self.criar_menu_principal()
        self.criar_tela_produtos()
        self.criar_tela_mesas()
        self.criar_tela_pedidos()
        self.criar_tela_caixa_rapido()
        self.criar_tela_historico()
        self.criar_tela_relatorios()

        # Mostrar tela inicial
        self.mostrar_frame(self.frame_principal)

    def mostrar_frame(self, frame):
        """Mostra apenas o frame desejado"""
        for f in [self.frame_principal, self.frame_produtos, self.frame_mesas,
                  self.frame_pedidos, self.frame_caixa_rapido, self.frame_historico, self.frame_relatorios]:
            f.grid_forget()
        frame.grid(row=0, column=0, sticky="nsew")

    def criar_menu_principal(self):
        frame = self.frame_principal

        tk.Label(frame, text="Sistema de Gerenciamento", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=30)

        tk.Button(frame, text="Gerenciamento de Produtos", width=30,
                  bg=COR_PRIMARIA, fg="white", font=FONTE_PADRAO,
                  command=lambda: self.mostrar_frame(self.frame_produtos)).pack(pady=15)

        tk.Button(frame, text="Gerenciamento de Mesas", width=30,
                  bg="#57606f", fg="white", font=FONTE_PADRAO,
                  command=lambda: self.mostrar_frame(self.frame_mesas)).pack(pady=15)

        tk.Button(frame, text="Gerenciamento de Pedidos", width=30,
                  bg="#57606f", fg="white", font=FONTE_PADRAO,
                  command=lambda: self.mostrar_frame(self.frame_pedidos)).pack(pady=15)

        tk.Button(frame, text="Caixa Rápido", width=30,
                  bg=COR_PRIMARIA, fg="white", font=FONTE_PADRAO,
                  command=lambda: self.mostrar_frame(self.frame_caixa_rapido)).pack(pady=15)

        tk.Button(frame, text="Ver Histórico de Vendas", width=30,
                  bg="#999999", fg="white", font=FONTE_PADRAO,
                  command=lambda: self.mostrar_frame(self.frame_historico)).pack(pady=15)

        tk.Button(frame, text="Relatórios de Vendas", width=30,
                  bg="#4caf50", fg="white", font=FONTE_PADRAO,
                  command=lambda: self.mostrar_frame(self.frame_relatorios)).pack(pady=15)

    def criar_tela_produtos(self):
        frame = self.frame_produtos

        tk.Label(frame, text="Gerenciar Produtos", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=15)

        self.entry_pesquisa_produto = tk.Entry(frame, width=40, font=FONTE_PADRAO)
        self.entry_pesquisa_produto.pack(padx=10, pady=5)
        self.entry_pesquisa_produto.bind("<KeyRelease>", self.filtrar_produtos)

        tk.Label(frame, text="Nome do Produto", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_PADRAO).pack()
        self.entry_nome = tk.Entry(frame, width=40, font=FONTE_PADRAO)
        self.entry_nome.pack(padx=10, pady=5)

        tk.Label(frame, text="Preço (R$)", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_PADRAO).pack()
        self.entry_preco = tk.Entry(frame, width=40, font=FONTE_PADRAO)
        self.entry_preco.pack(padx=10, pady=5)

        tk.Label(frame, text="Código do Produto", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_PADRAO).pack()
        self.entry_codigo = tk.Entry(frame, width=40, font=FONTE_PADRAO)
        self.entry_codigo.pack(padx=10, pady=5)

        tk.Button(frame, text="Adicionar Produto", width=30,
                  bg=COR_SUCESSO, fg="white", font=FONTE_PADRAO,
                  command=self.adicionar_produto).pack(pady=10)

        scroll_frame = tk.Frame(frame, bg=COR_FUNDO)
        scroll_frame.pack(padx=10, pady=10)

        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lista_produtos = tk.Listbox(scroll_frame, width=60, height=10,
                                        font=FONTE_PADRAO, yscrollcommand=scrollbar.set)
        self.lista_produtos.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.lista_produtos.yview)

        btn_frame = tk.Frame(frame, bg=COR_FUNDO)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Editar Produto", width=15, bg="#57606f", fg="white",
                  font=FONTE_PADRAO, command=self.editar_produto).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Remover Produto", width=15, bg=COR_ERRO, fg="white",
                  font=FONTE_PADRAO, command=self.remover_produto).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Voltar", width=15, bg=COR_ERRO, fg="white",
                  font=FONTE_PADRAO, command=lambda: self.mostrar_frame(self.frame_principal)).grid(row=0, column=2, padx=5)

        self.atualizar_lista_produtos()

    def filtrar_produtos(self, event=None):
        termo = self.entry_pesquisa_produto.get().lower()
        self.lista_produtos.delete(0, tk.END)
        for produto in self.produtos:
            if termo in produto.nome.lower() or termo in produto.codigo.lower():
                self.lista_produtos.insert(tk.END, str(produto))

    def adicionar_produto(self):
        nome = self.entry_nome.get().strip()
        preco_str = self.entry_preco.get().strip()
        codigo = self.entry_codigo.get().strip()

        if not nome or not codigo:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        try:
            preco = float(preco_str)
        except ValueError:
            messagebox.showerror("Erro", "O preço deve ser um número.")
            return

        produto = Produto(nome, preco, codigo)
        self.produtos.append(produto)
        self.atualizar_lista_produtos()
        self.salvar_produtos()
        messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado!")

    def atualizar_lista_produtos(self):
        self.lista_produtos.delete(0, tk.END)
        for p in self.produtos:
            self.lista_produtos.insert(tk.END, f"{p}")

    def salvar_produtos(self):
        with open("produtos.json", "w") as f:
            json.dump([p.to_dict() for p in self.produtos], f, indent=2)

    def carregar_produtos(self):
        if os.path.exists("produtos.json"):
            with open("produtos.json", "r") as f:
                try:
                    dados = json.load(f)
                    self.produtos = [Produto.from_dict(d) for d in dados]
                except json.JSONDecodeError:
                    self.produtos = []
        else:
            self.produtos = []

    def editar_produto(self):
        try:
            indice = self.lista_produtos.curselection()[0]
            produto = self.produtos[indice]

            janela = tk.Toplevel(self.root)
            janela.title("Editar Produto")
            janela.configure(bg=COR_FUNDO)

            tk.Label(janela, text="Nome", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_PADRAO).pack()
            entry_nome = tk.Entry(janela, width=40, font=FONTE_PADRAO)
            entry_nome.insert(0, produto.nome)
            entry_nome.pack(padx=10, pady=5)

            tk.Label(janela, text="Preço", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_PADRAO).pack()
            entry_preco = tk.Entry(janela, width=40, font=FONTE_PADRAO)
            entry_preco.insert(0, str(produto.preco))
            entry_preco.pack(padx=10, pady=5)

            tk.Label(janela, text="Código", bg=COR_FUNDO, fg=COR_TEXTO, font=FONTE_PADRAO).pack()
            entry_codigo = tk.Entry(janela, width=40, font=FONTE_PADRAO)
            entry_codigo.insert(0, produto.codigo)
            entry_codigo.pack(padx=10, pady=5)

            def salvar():
                novo_nome = entry_nome.get().strip()
                novo_preco = entry_preco.get().strip()
                novo_codigo = entry_codigo.get().strip()

                if not novo_nome or not novo_codigo:
                    messagebox.showwarning("Erro", "Preencha todos os campos.")
                    return

                try:
                    novo_preco_float = float(novo_preco)
                except ValueError:
                    messagebox.showerror("Erro", "O preço deve ser um número.")
                    return

                produto.nome = novo_nome
                produto.preco = novo_preco_float
                produto.codigo = novo_codigo

                self.atualizar_lista_produtos()
                self.salvar_produtos()
                janela.destroy()
                messagebox.showinfo("Sucesso", "Produto editado.")

            tk.Button(janela, text="Salvar", width=20, bg=COR_SUCESSO, fg="white",
                      font=FONTE_PADRAO, command=salvar).pack(pady=10)

        except IndexError:
            messagebox.showwarning("Erro", "Selecione um produto para editar.")

    def remover_produto(self):
        try:
            indice = self.lista_produtos.curselection()[0]
            produto = self.produtos[indice]
            resposta = messagebox.askyesno("Confirmar", f"Remover '{produto.nome}'?")
            if resposta:
                del self.produtos[indice]
                self.atualizar_lista_produtos()
                self.salvar_produtos()
                messagebox.showinfo("Sucesso", "Produto removido.")
        except IndexError:
            messagebox.showwarning("Erro", "Selecione um produto para remover.")

    def criar_tela_mesas(self):
        frame = self.frame_mesas

        tk.Label(frame, text="Gerenciar Mesas", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=15)

        scroll_frame = tk.Frame(frame, bg=COR_FUNDO)
        scroll_frame.pack(padx=10, pady=10)

        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lista_mesas = tk.Listbox(scroll_frame, width=60, height=15,
                                      font=FONTE_PADRAO, yscrollcommand=scrollbar.set)
        self.lista_mesas.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.lista_mesas.yview)

        tk.Button(frame, text="Voltar", width=20,
                  bg=COR_ERRO, fg="white", font=FONTE_PADRAO,
                  command=lambda: self.mostrar_frame(self.frame_principal)).pack(pady=10)

        self.atualizar_lista_mesas()
        self.lista_mesas.bind("<<ListboxSelect>>", self.mostrar_pedidos_da_mesa)

    def atualizar_lista_mesas(self):
        self.lista_mesas.delete(0, tk.END)
        for i in range(1, 41):  # De 1 a 40 mesas
            status = "Ocupada" if i in self.pedidos else "Livre"
            self.lista_mesas.insert(tk.END, f"Mesa {i} - {status}")

    def mostrar_pedidos_da_mesa(self, event):
        try:
            selecionado = self.lista_mesas.get(self.lista_mesas.curselection())
            mesa_numero = int(selecionado.split(" ")[1].split("-")[0])

            if mesa_numero in self.pedidos:
                itens = self.pedidos[mesa_numero]
                texto = f"Pedidos da Mesa {mesa_numero}:\n\n"
                total = 0.0
                for item in itens:
                    subtotal = item['produto'].preco * item['quantidade']
                    texto += f"- {item['produto'].nome} x{item['quantidade']} - R$ {subtotal:.2f}\n"
                    total += subtotal
                texto += f"\nTotal: R$ {total:.2f}"
                messagebox.showinfo("Pedidos da Mesa", texto)
            else:
                messagebox.showinfo("Pedidos da Mesa", f"Nenhum pedido registrado para a Mesa {mesa_numero}.")
        except Exception as e:
            messagebox.showwarning("Erro", "Selecione uma mesa válida.")

    def criar_tela_pedidos(self):
        frame = self.frame_pedidos

        tk.Label(frame, text="Gerenciar Pedidos", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=15)

        self.lista_pedidos = tk.Listbox(frame, width=70, height=15, font=FONTE_PADRAO)
        self.lista_pedidos.pack(padx=10, pady=10)

        btn_frame = tk.Frame(frame, bg=COR_FUNDO)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Adicionar Pedido", width=20, bg=COR_SUCESSO, fg="white",
                  font=FONTE_PADRAO, command=self.adicionar_pedido).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Marcar como Entregue", width=20, bg=COR_ERRO, fg="white",
                  font=FONTE_PADRAO, command=self.marcar_pedido_entregue).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Finalizar Venda", width=20, bg="#2d8cf0", fg="white",
                  font=FONTE_PADRAO, command=self.finalizar_pedido).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Voltar", width=20, bg=COR_ERRO, fg="white",
                  font=FONTE_PADRAO, command=lambda: self.mostrar_frame(self.frame_principal)).pack(side=tk.RIGHT, padx=5)

        self.atualizar_lista_pedidos()

    def adicionar_pedido(self):
        try:
            mesa_numero = simpledialog.askinteger("Mesa", "Digite o número da mesa (1 a 40):", minvalue=1, maxvalue=40)
            if not mesa_numero or not (1 <= mesa_numero <= 40):
                messagebox.showwarning("Erro", "Número da mesa inválido ou cancelado.")
                return

            codigo = simpledialog.askstring("Produto", "Digite o código do produto:")
            if not codigo:
                messagebox.showwarning("Erro", "Código do produto inválido.")
                return

            produto = next((p for p in self.produtos if p.codigo == codigo), None)
            if not produto:
                messagebox.showwarning("Erro", "Produto não encontrado.")
                return

            quantidade = simpledialog.askinteger("Quantidade", "Digite a quantidade:", minvalue=1)
            if not quantidade:
                messagebox.showwarning("Erro", "Quantidade inválida.")
                return

            if mesa_numero not in self.pedidos:
                self.pedidos[mesa_numero] = []

            self.pedidos[mesa_numero].append({"produto": produto, "quantidade": quantidade})
            self.atualizar_lista_pedidos()
            self.atualizar_lista_mesas()
            messagebox.showinfo("Sucesso", f"Pedido adicionado à Mesa {mesa_numero}: {produto.nome} x{quantidade}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def marcar_pedido_entregue(self):
        try:
            selecionado = self.lista_pedidos.get(self.lista_pedidos.curselection())
            mesa_numero = int(selecionado.split(":")[0].split(" ")[1])

            if mesa_numero in self.pedidos:
                resposta = messagebox.askyesno("Confirmar", f"Marcar Mesa {mesa_numero} como entregue?")
                if resposta:
                    del self.pedidos[mesa_numero]
                    self.atualizar_lista_pedidos()
                    self.atualizar_lista_mesas()
                    messagebox.showinfo("Sucesso", f"Pedido da Mesa {mesa_numero} marcado como entregue.")
        except Exception as e:
            messagebox.showwarning("Erro", "Selecione um pedido válido.")

    def finalizar_pedido(self):
        try:
            selecionado = self.lista_pedidos.get(self.lista_pedidos.curselection())
            mesa_numero = int(selecionado.split(":")[0].split(" ")[1])

            if mesa_numero in self.pedidos:
                itens = self.pedidos[mesa_numero]
                total = sum(item['produto'].preco * item['quantidade'] for item in itens)

                texto_pedido = f"Pedido da Mesa {mesa_numero}:\n\n"
                for item in itens:
                    texto_pedido += f"{item['produto'].nome} x{item['quantidade']} - R$ {item['produto'].preco * item['quantidade']:.2f}\n"
                texto_pedido += f"\nTotal: R$ {total:.2f}"

                resposta = messagebox.askyesno("Finalizar Pedido", texto_pedido + "\n\nDeseja realmente finalizar?")
                if resposta:
                    self.salvar_venda(mesa_numero, total)
                    del self.pedidos[mesa_numero]
                    self.atualizar_lista_pedidos()
                    self.atualizar_lista_mesas()
                    messagebox.showinfo("Sucesso", f"Pedido da Mesa {mesa_numero} finalizado!\nTotal: R$ {total:.2f}")
        except Exception as e:
            messagebox.showerror("Erro", f"Selecione um pedido válido ou ocorreu um erro: {e}")

    def salvar_venda(self, mesa_numero, total):
        venda_registro = {
            "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "mesa": mesa_numero,
            "itens": [
                {"nome": item['produto'].nome, "quantidade": item['quantidade'],
                 "subtotal": item['produto'].preco * item['quantidade']}
                for item in self.pedidos.get(mesa_numero, [])
            ],
            "total": total
        }

        if os.path.exists("vendas.json"):
            with open("vendas.json", "r") as f:
                historico = json.load(f)
        else:
            historico = []

        historico.append(venda_registro)
        with open("vendas.json", "w") as f:
            json.dump(historico, f, indent=2)

    def atualizar_lista_pedidos(self):
        self.lista_pedidos.delete(0, tk.END)
        for mesa, itens in self.pedidos.items():
            texto = f"Mesa {mesa}: "
            for item in itens:
                texto += f"{item['produto'].nome} x{item['quantidade']}, "
            texto = texto.rstrip(", ")
            self.lista_pedidos.insert(tk.END, texto)

    def criar_tela_caixa_rapido(self):
        frame = self.frame_caixa_rapido

        tk.Label(frame, text="Caixa Rápido - Venda Direta", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=15)

        self.lista_caixa_rapido = tk.Listbox(frame, width=70, height=15, font=FONTE_PADRAO)
        self.lista_caixa_rapido.pack(padx=10, pady=10)

        btn_frame = tk.Frame(frame, bg=COR_FUNDO)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Adicionar Produto", width=20, bg=COR_SUCESSO, fg="white",
                  font=FONTE_PADRAO, command=self.adicionar_produto_caixa).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Finalizar Venda", width=20, bg="#2d8cf0", fg="white",
                  font=FONTE_PADRAO, command=self.finalizar_venda_rapida).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpar Venda", width=20, bg="#999999", fg="white",
                  font=FONTE_PADRAO, command=self.limpar_venda_rapida).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Voltar", width=20, bg=COR_ERRO, fg="white",
                  font=FONTE_PADRAO, command=lambda: self.mostrar_frame(self.frame_principal)).pack(side=tk.RIGHT, padx=5)

        self.atualizar_lista_caixa_rapido()

    def adicionar_produto_caixa(self):
        try:
            codigo = simpledialog.askstring("Produto", "Digite o código do produto:")
            if not codigo:
                messagebox.showwarning("Erro", "Código do produto inválido.")
                return

            quantidade = simpledialog.askinteger("Quantidade", "Digite a quantidade:", minvalue=1)
            if not quantidade:
                messagebox.showwarning("Erro", "Quantidade inválida.")
                return

            produto = next((p for p in self.produtos if p.codigo == codigo), None)
            if not produto:
                messagebox.showwarning("Erro", "Produto não encontrado.")
                return

            subtotal = produto.preco * quantidade
            self.itens_caixa_rapido.append({"produto": produto, "quantidade": quantidade, "subtotal": subtotal})
            self.atualizar_lista_caixa_rapido()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def atualizar_lista_caixa_rapido(self):
        self.lista_caixa_rapido.delete(0, tk.END)
        self.total_caixo_rapido = sum(item["subtotal"] for item in self.itens_caixa_rapido)

        for item in self.itens_caixa_rapido:
            self.lista_caixa_rapido.insert(tk.END,
                                          f"{item['produto'].nome} x{item['quantidade']} - R$ {item['subtotal']:.2f}")

        self.lista_caixa_rapido.insert(tk.END, "")
        self.lista_caixa_rapido.insert(tk.END, "=" * 40)
        self.lista_caixa_rapido.insert(tk.END, f"Total: R$ {self.total_caixo_rapido:.2f}")

    def finalizar_venda_rapida(self):
        if not self.itens_caixa_rapido:
            messagebox.showwarning("Erro", "Nenhum produto adicionado.")
            return

        texto_pedido = "Venda Rápida:\n\n"
        for item in self.itens_caixa_rapido:
            texto_pedido += f"{item['produto'].nome} x{item['quantidade']} - R$ {item['subtotal']:.2f}\n"
        texto_pedido += f"\nTotal: R$ {self.total_caixo_rapido:.2f}"

        resposta = messagebox.askyesno("Confirmar Venda", texto_pedido + "\n\nFinalizar venda?")
        if resposta:
            self.salvar_historico_caixa({
                "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                "itens": [{"nome": item['produto'].nome, "quantidade": item['quantidade'], "total": item['subtotal']}
                          for item in self.itens_caixa_rapido],
                "total_venda": self.total_caixo_rapido
            })
            self.limpar_venda_rapida()
            messagebox.showinfo("Sucesso", f"Venda finalizada!\nTotal: R$ {self.total_caixo_rapido:.2f}")

    def limpar_venda_rapida(self):
        self.itens_caixa_rapido.clear()
        self.total_caixo_rapido = 0.0
        self.atualizar_lista_caixa_rapido()

    def salvar_historico_caixa(self, venda):
        if os.path.exists("vendas_rapidas.json"):
            with open("vendas_rapidas.json", "r") as f:
                historico = json.load(f)
        else:
            historico = []

        historico.append(venda)
        with open("vendas_rapidas.json", "w") as f:
            json.dump(historico, f, indent=2)

    def criar_tela_historico(self):
        frame = self.frame_historico

        tk.Label(frame, text="Histórico de Vendas", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=15)

        scroll_frame = tk.Frame(frame, bg=COR_FUNDO)
        scroll_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lista_historico = tk.Listbox(scroll_frame, width=80, height=20,
                                         font=FONTE_PADRAO, yscrollcommand=scrollbar.set)
        self.lista_historico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.lista_historico.yview)

        btn_frame = tk.Frame(frame, bg=COR_FUNDO)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Carregar Todas", width=20, bg="#57606f", fg="white",
                  font=FONTE_PADRAO, command=self.carregar_historico_completo).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Por Mesa", width=20, bg="#57606f", fg="white",
                  font=FONTE_PADRAO, command=self.filtrar_por_mesa).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Por Data", width=20, bg="#57606f", fg="white",
                  font=FONTE_PADRAO, command=self.filtrar_por_data).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Voltar", width=20, bg=COR_ERRO, fg="white",
                  font=FONTE_PADRAO, command=lambda: self.mostrar_frame(self.frame_principal)).pack(side=tk.RIGHT, padx=5)

        self.carregar_historico_completo()

    def carregar_historico_completo(self):
        self.lista_historico.delete(0, tk.END)

        try:
            vendas = []

            if os.path.exists("vendas.json"):
                with open("vendas.json", "r") as f:
                    vendas += json.load(f)
            if os.path.exists("vendas_rapidas.json"):
                with open("vendas_rapidas.json", "r") as f:
                    vendas += json.load(f)

            if not vendas:
                self.lista_historico.insert(tk.END, "Nenhuma venda registrada ainda.")
                return

            for venda in vendas:
                if "mesa" in venda:
                    linha = f"[MESA {venda['mesa']} - {venda['data']}]\n"
                    for item in venda["itens"]:
                        linha += f"   {item['nome']} x{item['quantidade']} - R$ {item['subtotal']:.2f}\n"
                    linha += f"   Total: R$ {venda['total']:.2f}"
                else:
                    linha = f"[CAIXA RÁPIDO - {venda['data']}]\n"
                    for item in venda["itens"]:
                        linha += f"   {item['nome']} x{item['quantidade']} - R$ {item['total']:.2f}\n"
                    linha += f"   Total: R$ {venda['total_venda']:.2f}"

                self.lista_historico.insert(tk.END, linha + "\n" + "-" * 60 + "\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar histórico: {e}")

    def filtrar_por_mesa(self):
        try:
            mesa = simpledialog.askinteger("Filtrar", "Digite o número da mesa (1 a 40):", minvalue=1, maxvalue=40)
            if not mesa:
                return

            self.lista_historico.delete(0, tk.END)
            encontradas = []

            if os.path.exists("vendas.json"):
                with open("vendas.json", "r") as f:
                    vendas = json.load(f)
                    encontradas += [v for v in vendas if v.get("mesa") == mesa]

            if os.path.exists("vendas_rapidas.json"):
                with open("vendas_rapidas.json", "r") as f:
                    vendas = json.load(f)
                    for v in vendas:
                        if any(i.get('mesa') == mesa for i in v.get('itens', [])):
                            encontradas.append(v)

            if not encontradas:
                self.lista_historico.insert(tk.END, f"Nenhuma venda encontrada para a Mesa {mesa}.")
                return

            for venda in encontradas:
                if "mesa" in venda:
                    linha = f"[MESA {venda['mesa']} - {venda['data']}]\n"
                    for item in venda["itens"]:
                        linha += f"   {item['nome']} x{item['quantidade']} - R$ {item['subtotal']:.2f}\n"
                    linha += f"   Total: R$ {venda['total']:.2f}"
                else:
                    linha = f"[CAIXA RÁPIDO - {venda['data']}]\n"
                    for item in venda["itens"]:
                        linha += f"   {item['nome']} x{item['quantidade']} - R$ {item['total']:.2f}\n"
                    linha += f"   Total: R$ {venda['total_venda']:.2f}"

                self.lista_historico.insert(tk.END, linha + "\n" + "-" * 60 + "\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao filtrar: {e}")

    def filtrar_por_data(self):
        try:
            data_inicio = simpledialog.askstring("Data", "Digite a data inicial (dd/mm/aaaa):")
            data_fim = simpledialog.askstring("Data", "Digite a data final (dd/mm/aaaa):")

            if not data_inicio or not data_fim:
                return

            data_inicio = datetime.datetime.strptime(data_inicio, "%d/%m/%Y")
            data_fim = datetime.datetime.strptime(data_fim, "%d/%m/%Y")

            self.lista_historico.delete(0, tk.END)
            vendas_encontradas = []

            if os.path.exists("vendas.json"):
                with open("vendas.json", "r") as f:
                    for venda in json.load(f):
                        data_venda = datetime.datetime.strptime(venda["data"], "%d/%m/%Y %H:%M")
                        if data_inicio <= data_venda <= data_fim:
                            vendas_encontradas.append(venda)

            if os.path.exists("vendas_rapidas.json"):
                with open("vendas_rapidas.json", "r") as f:
                    for venda in json.load(f):
                        data_venda = datetime.datetime.strptime(venda["data"], "%d/%m/%Y %H:%M")
                        if data_inicio <= data_venda <= data_fim:
                            vendas_encontradas.append(venda)

            if not vendas_encontradas:
                self.lista_historico.insert(tk.END, "Nenhuma venda encontrada nesse período.")
                return

            for venda in vendas_encontradas:
                if "mesa" in venda:
                    linha = f"[MESA {venda['mesa']} - {venda['data']}]\n"
                    for item in venda["itens"]:
                        linha += f"   {item['nome']} x{item['quantidade']} - R$ {item['subtotal']:.2f}\n"
                    linha += f"   Total: R$ {venda['total']:.2f}"
                else:
                    linha = f"[CAIXA RÁPIDO - {venda['data']}]\n"
                    for item in venda["itens"]:
                        linha += f"   {item['nome']} x{item['quantidade']} - R$ {item['total']:.2f}\n"
                    linha += f"   Total: R$ {venda['total_venda']:.2f}"

                self.lista_historico.insert(tk.END, linha + "\n" + "-" * 60 + "\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Formato de data inválido ou erro ao carregar: {e}")

    def criar_tela_historico(self):
        frame = self.frame_historico

        tk.Label(frame, text="Histórico de Vendas", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=15)

        scroll_frame = tk.Frame(frame, bg=COR_FUNDO)
        scroll_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lista_historico = tk.Listbox(scroll_frame, width=80, height=20,
                                       font=FONTE_PADRAO, yscrollcommand=scrollbar.set)
        self.lista_historico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.lista_historico.yview)

        btn_frame = tk.Frame(frame, bg=COR_FUNDO)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Carregar Todas", width=20, bg="#57606f", fg="white",
                  font=FONTE_PADRAO, command=self.carregar_historico_completo).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Por Mesa", width=20, bg="#57606f", fg="white",
                  font=FONTE_PADRAO, command=self.filtrar_por_mesa).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Por Data", width=20, bg="#57606f", fg="white",
                  font=FONTE_PADRAO, command=self.filtrar_por_data).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Voltar", width=20, bg=COR_ERRO, fg="white",
                  font=FONTE_PADRAO, command=lambda: self.mostrar_frame(self.frame_principal)).pack(side=tk.RIGHT, padx=5)

        self.carregar_historico_completo()

    def criar_tela_relatorios(self):
        frame = self.frame_relatorios

        tk.Label(frame, text="Relatórios de Vendas", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=15)

        btn_topo = tk.Frame(frame, bg=COR_FUNDO)
        btn_topo.pack(pady=10)

        tk.Button(btn_topo, text="Relatório Diário", width=30, bg=COR_SUCESSO, fg="white",
                  font=FONTE_PADRAO, command=self.carregar_relatorio_diario).pack(pady=5)

        tk.Button(btn_topo, text="Relatório Mensal", width=30, bg="#57606f", fg="white",
                  font=FONTE_PADRAO, command=self.carregar_relatorio_mensal).pack(pady=5)

        tk.Button(btn_topo, text="Relatório Geral", width=30, bg="#999999", fg="white",
                  font=FONTE_PADRAO, command=self.carregar_relatorio_completo).pack(pady=5)

        self.lista_relatorios = tk.Listbox(frame, width=80, height=15, font=FONTE_PADRAO)
        self.lista_relatorios.pack(padx=10, pady=10)

        tk.Button(frame, text="Voltar", width=20, bg=COR_ERRO, fg="white",
                  font=FONTE_PADRAO, command=lambda: self.mostrar_frame(self.frame_principal)).pack(pady=10)

    def carregar_relatorio_diario(self):
        self.lista_relatorios.delete(0, tk.END)
        hoje = datetime.datetime.now().strftime("%d/%m/%Y")
        vendas_do_dia = []

        if os.path.exists("vendas.json"):
            with open("vendas.json", "r") as f:
                vendas_do_dia += [v for v in json.load(f) if v["data"].startswith(hoje)]

        if os.path.exists("vendas_rapidas.json"):
            with open("vendas_rapidas.json", "r") as f:
                vendas_do_dia += [v for v in json.load(f) if v["data"].startswith(hoje)]

        if not vendas_do_dia:
            self.lista_relatorios.insert(tk.END, "Nenhuma venda registrada hoje.")
            return

        self.lista_relatorios.insert(tk.END, f"=== Relatório Diário - {hoje} ===\n")
        total_geral = 0.0
        produtos_vendidos = {}

        for venda in vendas_do_dia:
            if "mesa" in venda:
                for item in venda["itens"]:
                    chave = item["nome"]
                    qtd = item["quantidade"]
                    produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd
            else:
                for item in venda["itens"]:
                    chave = item["nome"]
                    qtd = item["quantidade"]
                    produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd

            total_geral += venda.get("total", venda.get("total_venda", 0))

        for produto, qtd in produtos_vendidos.items():
            self.lista_relatorios.insert(tk.END, f"- {produto}: {qtd} unidades")

        self.lista_relatorios.insert(tk.END, f"\nTotal do Dia: R$ {total_geral:.2f}")
        self.lista_relatorios.insert(tk.END, "-" * 60)

    def carregar_relatorio_mensal(self):
        try:
            data_input = simpledialog.askstring("Data", "Digite qualquer data do mês (dd/mm/aaaa):")
            if not data_input:
                return

            data_selecionada = datetime.datetime.strptime(data_input, "%d/%m/%Y").strftime("%m/%Y")
            self.lista_relatorios.delete(0, tk.END)

            vendas_do_mes = []

            if os.path.exists("vendas.json"):
                with open("vendas.json", "r") as f:
                    for v in json.load(f):
                        data_venda = datetime.datetime.strptime(v["data"], "%d/%m/%Y %H:%M").strftime("%m/%Y")
                        if data_venda == data_selecionada:
                            vendas_do_mes.append(v)

            if os.path.exists("vendas_rapidas.json"):
                with open("vendas_rapidas.json", "r") as f:
                    for v in json.load(f):
                        data_venda = datetime.datetime.strptime(v["data"], "%d/%m/%Y %H:%M").strftime("%m/%Y")
                        if data_venda == data_selecionada:
                            vendas_do_mes.append(v)

            if not vendas_do_mes:
                self.lista_relatorios.insert(tk.END, f"Nenhuma venda registrada para {data_selecionada}.")
                return

            self.lista_relatorios.insert(tk.END, f"=== Relatório Mensal - {data_selecionada} ===\n")
            total_geral = 0.0
            produtos_vendidos = {}

            for venda in vendas_do_mes:
                if "mesa" in venda:
                    for item in venda["itens"]:
                        chave = item["nome"]
                        qtd = item["quantidade"]
                        produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd
                else:
                    for item in venda["itens"]:
                        chave = item["nome"]
                        qtd = item["quantidade"]
                        produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd

                total_geral += venda.get("total", venda.get("total_venda", 0))

            for produto, qtd in produtos_vendidos.items():
                self.lista_relatorios.insert(tk.END, f"- {produto}: {qtd} unidades")

            self.lista_relatorios.insert(tk.END, f"\nTotal do Mês: R$ {total_geral:.2f}")
            self.lista_relatorios.insert(tk.END, "-" * 60)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar relatório mensal: {e}")

    def carregar_relatorio_completo(self):
        self.lista_relatorios.delete(0, tk.END)

        try:
            vendas = []
            if os.path.exists("vendas.json"):
                with open("vendas.json", "r") as f:
                    vendas += json.load(f)
            if os.path.exists("vendas_rapidas.json"):
                with open("vendas_rapidas.json", "r") as f:
                    vendas += json.load(f)

            if not vendas:
                self.lista_relatorios.insert(tk.END, "Nenhuma venda registrada ainda.")
                return

            self.lista_relatorios.insert(tk.END, "=== Relatório Completo ===\n")
            total_geral = 0.0
            produtos_vendidos = {}

            for venda in vendas:
                if "mesa" in venda:
                    for item in venda["itens"]:
                        chave = item["nome"]
                        qtd = item["quantidade"]
                        produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd
                else:
                    for item in venda["itens"]:
                        chave = item["nome"]
                        qtd = item["quantidade"]
                        produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd

                total_geral += venda.get("total", venda.get("total_venda", 0))

            for produto, qtd in produtos_vendidos.items():
                self.lista_relatorios.insert(tk.END, f"- {produto}: {qtd} unidades")

            self.lista_relatorios.insert(tk.END, f"\nTotal Acumulado: R$ {total_geral:.2f}")
            self.lista_relatorios.insert(tk.END, "-" * 60)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar relatório completo: {e}")

    def criar_tela_relatorios(self):
        frame = self.frame_relatorios
        frame.configure(bg=COR_FUNDO)

        tk.Label(frame, text="Relatórios de Vendas", font=FONTE_TITULO, bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=15)

        btn_topo = tk.Frame(frame, bg=COR_FUNDO)
        btn_topo.pack(pady=10)

        tk.Button(btn_topo, text="Relatório Diário", width=30, bg=COR_SUCESSO, fg="white",
                  font=FONTE_PADRAO, command=self.carregar_relatorio_diario).pack(pady=5)

        tk.Button(btn_topo, text="Relatório Mensal", width=30, bg="#57606f", fg="white",
                  font=FONTE_PADRAO, command=self.carregar_relatorio_mensal).pack(pady=5)

        tk.Button(btn_topo, text="Relatório Geral", width=30, bg="#999999", fg="white",
                  font=FONTE_PADRAO, command=self.carregar_relatorio_completo).pack(pady=5)

        self.lista_relatorios = tk.Listbox(frame, width=80, height=15, font=FONTE_PADRAO)
        self.lista_relatorios.pack(padx=10, pady=10)

        tk.Button(frame, text="Voltar", width=20, bg=COR_ERRO, fg="white",
                  font=FONTE_PADRAO, command=lambda: self.mostrar_frame(self.frame_principal)).pack(pady=10)

    def carregar_relatorio_diario(self):
        self.lista_relatorios.delete(0, tk.END)
        hoje = datetime.datetime.now().strftime("%d/%m/%Y")
        vendas_do_dia = []

        if os.path.exists("vendas.json"):
            with open("vendas.json", "r") as f:
                for venda in json.load(f):
                    if venda["data"].startswith(hoje):
                        vendas_do_dia.append(venda)

        if os.path.exists("vendas_rapidas.json"):
            with open("vendas_rapidas.json", "r") as f:
                for venda in json.load(f):
                    if venda["data"].startswith(hoje):
                        vendas_do_dia.append(venda)

        if not vendas_do_dia:
            self.lista_relatorios.insert(tk.END, "Nenhuma venda registrada hoje.")
            return

        self.lista_relatorios.insert(tk.END, f"=== Relatório Diário - {hoje} ===\n")
        total_geral = 0.0
        produtos_vendidos = {}

        for venda in vendas_do_dia:
            if "mesa" in venda:
                for item in venda["itens"]:
                    chave = item["nome"]
                    qtd = item["quantidade"]
                    produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd
            else:
                for item in venda["itens"]:
                    chave = item["nome"]
                    qtd = item["quantidade"]
                    produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd

            total_geral += venda.get("total", venda.get("total_venda", 0))

        for produto, qtd in produtos_vendidos.items():
            self.lista_relatorios.insert(tk.END, f"- {produto}: {qtd} unidades")

        self.lista_relatorios.insert(tk.END, f"\nTotal do Dia: R$ {total_geral:.2f}")
        self.lista_relatorios.insert(tk.END, "-" * 60)

    def carregar_relatorio_mensal(self):
        try:
            data_input = simpledialog.askstring("Data", "Digite qualquer data do mês (dd/mm/aaaa):")
            if not data_input:
                return

            data_selecionada = datetime.datetime.strptime(data_input, "%d/%m/%Y").strftime("%m/%Y")
            self.lista_relatorios.delete(0, tk.END)

            vendas_do_mes = []

            if os.path.exists("vendas.json"):
                with open("vendas.json", "r") as f:
                    for venda in json.load(f):
                        data_venda = datetime.datetime.strptime(venda["data"], "%d/%m/%Y %H:%M").strftime("%m/%Y")
                        if data_venda == data_selecionada:
                            vendas_do_mes.append(venda)

            if os.path.exists("vendas_rapidas.json"):
                with open("vendas_rapidas.json", "r") as f:
                    for venda in json.load(f):
                        data_venda = datetime.datetime.strptime(venda["data"], "%d/%m/%Y %H:%M").strftime("%m/%Y")
                        if data_venda == data_selecionada:
                            vendas_do_mes.append(venda)

            if not vendas_do_mes:
                self.lista_relatorios.insert(tk.END, f"Nenhuma venda registrada para {data_selecionada}.")
                return

            self.lista_relatorios.insert(tk.END, f"=== Relatório Mensal - {data_selecionada} ===\n")
            total_geral = 0.0
            produtos_vendidos = {}

            for venda in vendas_do_mes:
                if "mesa" in venda:
                    for item in venda["itens"]:
                        chave = item["nome"]
                        qtd = item["quantidade"]
                        produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd
                else:
                    for item in venda["itens"]:
                        chave = item["nome"]
                        qtd = item["quantidade"]
                        produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd

                total_geral += venda.get("total", venda.get("total_venda", 0))

            for produto, qtd in produtos_vendidos.items():
                self.lista_relatorios.insert(tk.END, f"- {produto}: {qtd} unidades")

            self.lista_relatorios.insert(tk.END, f"\nTotal do Mês: R$ {total_geral:.2f}")
            self.lista_relatorios.insert(tk.END, "-" * 60)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar relatório mensal: {e}")

    def carregar_relatorio_completo(self):
        self.lista_relatorios.delete(0, tk.END)

        try:
            vendas = []
            if os.path.exists("vendas.json"):
                with open("vendas.json", "r") as f:
                    vendas += json.load(f)
            if os.path.exists("vendas_rapidas.json"):
                with open("vendas_rapidas.json", "r") as f:
                    vendas += json.load(f)

            if not vendas:
                self.lista_relatorios.insert(tk.END, "Nenhuma venda registrada ainda.")
                return

            self.lista_relatorios.insert(tk.END, "=== Relatório Completo ===\n")
            total_geral = 0.0
            produtos_vendidos = {}

            for venda in vendas:
                if "mesa" in venda:
                    for item in venda["itens"]:
                        chave = item["nome"]
                        qtd = item["quantidade"]
                        produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd
                else:
                    for item in venda["itens"]:
                        chave = item["nome"]
                        qtd = item["quantidade"]
                        produtos_vendidos[chave] = produtos_vendidos.get(chave, 0) + qtd

                total_geral += venda.get("total", venda.get("total_venda", 0))

            for produto, qtd in produtos_vendidos.items():
                self.lista_relatorios.insert(tk.END, f"- {produto}: {qtd} unidades")

            self.lista_relatorios.insert(tk.END, f"\nTotal Acumulado: R$ {total_geral:.2f}")
            self.lista_relatorios.insert(tk.END, "-" * 60)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar relatório completo: {e}")

    def carregar_produtos(self):
        if os.path.exists("produtos.json"):
            with open("produtos.json", "r") as f:
                try:
                    dados = json.load(f)
                    self.produtos = [Produto.from_dict(d) for d in dados]
                except json.JSONDecodeError:
                    self.produtos = []
        else:
            self.produtos = []

    def salvar_produtos(self):
        with open("produtos.json", "w") as f:
            json.dump([p.to_dict() for p in self.produtos], f, indent=2)

    def atualizar_lista_mesas(self):
        self.lista_mesas.delete(0, tk.END)
        for i in range(1, 41):  # 40 mesas
            status = "Ocupada" if i in self.pedidos else "Livre"
            self.lista_mesas.insert(tk.END, f"Mesa {i} - {status}")

    def atualizar_lista_pedidos(self):
        self.lista_pedidos.delete(0, tk.END)
        for mesa, itens in self.pedidos.items():
            texto = f"Mesa {mesa}: "
            for item in itens:
                texto += f"{item['produto'].nome} x{item['quantidade']}, "
            texto = texto.rstrip(", ")
            self.lista_pedidos.insert(tk.END, texto)

    def atualizar_lista_caixa_rapido(self):
        self.lista_caixa_rapido.delete(0, tk.END)
        self.total_caixo_rapido = sum(item["subtotal"] for item in self.itens_caixa_rapido)

        for item in self.itens_caixa_rapido:
            self.lista_caixa_rapido.insert(tk.END,
                                          f"{item['produto'].nome} x{item['quantidade']} - R$ {item['subtotal']:.2f}")

        self.lista_caixa_rapido.insert(tk.END, "")
        self.lista_caixa_rapido.insert(tk.END, "=" * 40)
        self.lista_caixa_rapido.insert(tk.END, f"Total: R$ {self.total_caixo_rapido:.2f}")

    def salvar_historico_caixa(self, venda):
        if os.path.exists("vendas_rapidas.json"):
            with open("vendas_rapidas.json", "r") as f:
                historico = json.load(f)
        else:
            historico = []

        historico.append(venda)
        with open("vendas_rapidas.json", "w") as f:
            json.dump(historico, f, indent=2)

    def adicionar_produto(self):
        nome = self.entry_nome.get().strip()
        preco_str = self.entry_preco.get().strip()
        codigo = self.entry_codigo.get().strip()

        if not nome or not codigo:
            messagebox.showwarning("Erro", "Preencha todos os campos.")
            return

        try:
            preco = float(preco_str)
        except ValueError:
            messagebox.showerror("Erro", "O preço deve ser um número.")
            return

        produto = Produto(nome, preco, codigo)
        self.produtos.append(produto)
        self.atualizar_lista_produtos()
        self.salvar_produtos()
        messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado!")

    def atualizar_lista_produtos(self):
        self.lista_produtos.delete(0, tk.END)
        for p in self.produtos:
            self.lista_produtos.insert(tk.END, str(p))

    def adicionar_produto_caixa(self):
        try:
            codigo = simpledialog.askstring("Produto", "Digite o código do produto:")
            if not codigo:
                messagebox.showwarning("Erro", "Código do produto inválido.")
                return

            quantidade = simpledialog.askinteger("Quantidade", "Digite a quantidade:", minvalue=1)
            if not quantidade:
                messagebox.showwarning("Erro", "Quantidade inválida.")
                return

            produto = next((p for p in self.produtos if p.codigo == codigo), None)
            if not produto:
                messagebox.showwarning("Erro", "Produto não encontrado.")
                return

            subtotal = produto.preco * quantidade
            self.itens_caixa_rapido.append({"produto": produto, "quantidade": quantidade, "subtotal": subtotal})
            self.atualizar_lista_caixa_rapido()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def limpar_venda_rapida(self):
        self.itens_caixa_rapido.clear()
        self.total_caixo_rapido = 0.0
        self.atualizar_lista_caixa_rapido()


# Iniciar aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = RestauranteApp(root)
    root.mainloop()