import os
from pypdf import PdfReader
from rag.chunk import chunk_text
from rag.search import add_doc

def ingest_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    chunks = chunk_text(text)
    for c in chunks:
        add_doc(c)

def ingest_advpl(path):
    # Regra de Ouro: AdvPL sempre em CP1252
    try:
        with open(path, "r", encoding="cp1252", errors="replace") as f:
            text = f.read()

        filename = os.path.basename(path)
        # Adicionamos metadados ao texto para a IA saber a origem
        context_text = f"FONTE_ADVPL: {filename}\nCONTÉUDO:\n{text}"

        # Chunks ligeiramente maiores para não quebrar funções ao meio
        chunks = chunk_text(context_text, size=1000)
        for c in chunks:
            add_doc(c)
    except Exception as e:
        print(f"Erro ao processar fonte AdvPL {path}: {e}")
