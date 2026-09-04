# ==============================================================================
# ALUNOS: Leonardo Hermann e Maria Clara Corrêa 
# CURSO: Técnico em Informática - CEFET-MG
# ATIVIDADE: Atividade Avaliativa 2 - Bimestre 3
# ==============================================================================

import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class EditorAnotacoes:
    def __init__(self, glade_file="interface.glade"):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)

        self.jan_principal = self.builder.get_object("jan_principal")
        self.entry_titulo = self.builder.get_object("entry_titulo")
        self.txt_anotacao = self.builder.get_object("txt_anotacao")
        self.lbl_contador = self.builder.get_object("lbl_contador")
        self.lbl_status = self.builder.get_object("lbl_status")
        self.btn_limpar = self.builder.get_object("btn_limpar")
        self.btn_salvar = self.builder.get_object("btn_salvar")

        self.buffer_anotacao = self.txt_anotacao.get_buffer()

        self._conectar_sinais()

        self.jan_principal.show_all()

    def _conectar_sinais(self):
        self.jan_principal.connect("destroy", self.on_jan_principal_destroy)
        self.buffer_anotacao.connect("changed", self.on_texto_changed)
        self.entry_titulo.connect("changed", self.on_titulo_changed)
        self.btn_limpar.connect("clicked", self.on_btn_limpar_clicked)
        self.btn_salvar.connect("clicked", self.on_btn_salvar_clicked)

    def on_jan_principal_destroy(self, widget):
        Gtk.main_quit()

    def on_texto_changed(self, buffer):
        inicio = buffer.get_start_iter()
        fim = buffer.get_end_iter()
        texto = buffer.get_text(inicio, fim, True)

        num_caracteres = len(texto)
        num_palavras = len(texto.split()) if texto.strip() else 0

        self.lbl_contador.set_text(f"{num_caracteres} caracteres - {num_palavras} palavras")
        self.lbl_status.set_text("Alterações não salvas")

    def on_titulo_changed(self, entry):
        self.lbl_status.set_text("Alterações não salvas")

    def on_btn_limpar_clicked(self, button):
        self.entry_titulo.set_text("")
        self.buffer_anotacao.set_text("")
        self.lbl_status.set_text("Alterações não salvas")
        self.lbl_contador.set_text("0 caracteres - 0 palavras")

    def on_btn_salvar_clicked(self, button):
        titulo = self.entry_titulo.get_text().strip()
        if not titulo:
            titulo = "anotacao_sem_titulo"

        nome_arquivo = f"{titulo}.txt"
        inicio = self.buffer_anotacao.get_start_iter()
        fim = self.buffer_anotacao.get_end_iter()
        conteudo = self.buffer_anotacao.get_text(inicio, fim, True)

        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(f"TÍTULO: {titulo}\n")
                f.write("=" * 40 + "\n")
                f.write(conteudo)

            self.lbl_status.set_text(f"Salvo em '{nome_arquivo}'")
        except Exception as e:
            self.lbl_status.set_text("Erro ao salvar arquivo!")


if __name__ == "__main__":
    app = EditorAnotacoes("interface.glade")
    Gtk.main()