# Compile main.pdf with bibtex (3-pass cross-ref resolution).
# `make`           — produce main.pdf
# `make clean`     — remove intermediates (PDF preserved)
# `make distclean` — also remove the PDF
#
# NOTE: this scaffold has no python figure pipeline (commons: hexa-only
# authoring — no .py/.sh). The headline schematic (Fig. 1) is inline TikZ.
# A fal.ai cover (figures/_prompts/cover.txt) is staged but DEFERRED per
# g51 (see README "Honest stance"); generate it with `/paper fig` when the
# paper is promoted past scaffold, then \includegraphics it in main.tex.

DOC = main
LATEX = pdflatex -interaction=nonstopmode -halt-on-error
BIBTEX = bibtex

.PHONY: all clean distclean

all: $(DOC).pdf

$(DOC).pdf: $(DOC).tex references.bib
	$(LATEX) $(DOC).tex
	$(BIBTEX) $(DOC) || true
	$(LATEX) $(DOC).tex
	$(LATEX) $(DOC).tex
	@echo "[paper] $(DOC).pdf built at $$(date '+%Y-%m-%d %H:%M:%S')"

clean:
	rm -f $(DOC).aux $(DOC).bbl $(DOC).blg $(DOC).log $(DOC).out \
	      $(DOC).toc $(DOC).synctex.gz
	@echo "[paper] intermediates cleaned (PDF preserved)"

distclean: clean
	rm -f $(DOC).pdf
