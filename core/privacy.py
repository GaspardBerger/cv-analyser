#!/usr/bin/env python3
"""Tijdelijk bestandsbeheer: schrijft geüploade bestanden naar tempfile en verwijdert ze gegarandeerd."""

import os
import tempfile
from contextlib import contextmanager


@contextmanager
def tijdelijk_bestand(uploaded_file, suffix: str):
    """
    Schrijft een Streamlit UploadedFile naar een tijdelijk bestand op schijf,
    geeft het pad terug, en verwijdert het bestand gegarandeerd daarna —
    ook bij uitzonderingen.

    Gebruik:
        with tijdelijk_bestand(uploaded_file, ".pdf") as pad:
            tekst = extraheer_pdf(pad)
        # bestand is hier al verwijderd
    """
    tmp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
        prefix="gluon_cv_",
    )
    try:
        tmp.write(uploaded_file.getbuffer())
        tmp.flush()
        tmp.close()
        yield tmp.name
    finally:
        try:
            if os.path.exists(tmp.name):
                os.unlink(tmp.name)
        except OSError:
            pass
