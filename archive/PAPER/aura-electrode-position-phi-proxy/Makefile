# PAPER/aura-electrode-position-phi-proxy — build targets
# Default: xelatex (engine-agnostic; falls back to pdflatex if xelatex missing).
#
# Usage:
#   make            # build main.pdf (xelatex -> bibtex -> xelatex x2)
#   make figure     # build standalone figures/fig01_invasiveness_reach.pdf
#   make clean      # remove aux/log/bbl/blg/etc
#   make distclean  # also remove main.pdf and figure pdf

ENGINE ?= xelatex
BIB    ?= bibtex

TEX    := main.tex
PDF    := main.pdf
FIG_SRC := figures/_scripts/fig01_invasiveness_reach.tex
FIG_PDF := figures/fig01_invasiveness_reach.pdf

.PHONY: all figure clean distclean

all: $(PDF)

$(PDF): $(TEX) references.bib figures/fig01_body.tex
	@echo "==> Running $(ENGINE) pass 1"
	$(ENGINE) -interaction=nonstopmode $(TEX) || true
	@echo "==> Running $(BIB)"
	$(BIB) main || true
	@echo "==> Running $(ENGINE) pass 2"
	$(ENGINE) -interaction=nonstopmode $(TEX) || true
	@echo "==> Running $(ENGINE) pass 3"
	$(ENGINE) -interaction=nonstopmode $(TEX)

figure: $(FIG_PDF)

$(FIG_PDF): $(FIG_SRC) figures/fig01_body.tex
	@echo "==> Building standalone figure"
	cd figures/_scripts && pdflatex -interaction=nonstopmode fig01_invasiveness_reach.tex
	@mv -f figures/_scripts/fig01_invasiveness_reach.pdf $(FIG_PDF) 2>/dev/null || true

clean:
	rm -f main.aux main.bbl main.blg main.log main.out main.toc main.run.xml \
	      main.fdb_latexmk main.fls
	rm -f figures/_scripts/*.aux figures/_scripts/*.log

distclean: clean
	rm -f $(PDF) $(FIG_PDF)
