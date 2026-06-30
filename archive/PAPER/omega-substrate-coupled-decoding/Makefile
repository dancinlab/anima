# Compile main.pdf with bibtex (3-pass cross-ref resolution).
#
# Engine: xelatex (UTF-8/emoji native). pdflatex emits a 🔵 fatal on any literal
# emoji in source (encountered on hexa-fusion-7gate); xelatex/lualatex render
# tier emoji 🔵🟢🟡🟠🔴 natively. Override via `make LATEX=pdflatex` only after
# stripping every literal emoji from main.tex (use \tierBlue / \tierGreen / ...
# providecommand macros, redefined to a non-emoji marker).
#
# Targets:
#   make               produce main.pdf
#   make figures       regenerate figures/*.pdf from figures/_scripts/*.{py,tex}
#   make figures-clean remove generated figures/fig*.pdf (keep _scripts/_prompts)
#   make wordcount     report word count (texcount preferred, falls back to wc)
#   make pages         report page count via pdfinfo
#   make lint          run `/paper lint .` (commons @D g51)
#   make arxiv-tar     out/<slug>-arxiv.tar.gz — arxiv-ready source bundle
#   make clean         remove intermediates (PDF preserved)
#   make distclean     also remove the PDF

DOC = main
LATEX = xelatex -interaction=nonstopmode -halt-on-error
BIBTEX = bibtex
PYTHON = python3
SLUG := $(notdir $(CURDIR))

FIG_SCRIPTS_PY  = $(wildcard figures/_scripts/*.py)
FIG_SCRIPTS_TEX = $(wildcard figures/_scripts/*.tex)
FIG_PDFS_PY     = $(patsubst figures/_scripts/%.py,figures/%.pdf,$(FIG_SCRIPTS_PY))
FIG_PDFS_TEX    = $(patsubst figures/_scripts/%.tex,figures/%.pdf,$(FIG_SCRIPTS_TEX))
FIG_PDFS        = $(FIG_PDFS_PY) $(FIG_PDFS_TEX)

# Edit-triggers-rebuild deps (v0.9): the 58p monograph build proved that
# editing an \input'd appendix OR a committed figure PDF did NOT rebuild
# main.pdf — the dep list omitted them, forcing `make distclean && make`.
# APPENDIX = every \input'd chapter; FIG_PDFS_EXISTING = figure PDFs already
# present (dropped in directly, not script-generated). Both now prereqs below.
APPENDIX           = $(wildcard appendix/*.tex)
FIG_PDFS_EXISTING  = $(wildcard figures/*.pdf)

.PHONY: all figures figures-clean wordcount pages lint arxiv-tar clean distclean

all: $(DOC).pdf

$(DOC).pdf: $(DOC).tex references.bib $(FIG_PDFS) $(FIG_PDFS_EXISTING) $(APPENDIX)
	$(LATEX) $(DOC).tex
	$(BIBTEX) $(DOC) || true
	$(LATEX) $(DOC).tex
	$(LATEX) $(DOC).tex
	@echo "[paper] $(DOC).pdf built at $$(date '+%Y-%m-%d %H:%M:%S')"

# Regenerate any figure whose source is newer than its .pdf. Idempotent.
# Add new figs by dropping figures/_scripts/figNN_<name>.{py,tex} — picked up by
# the wildcard above.
figures: $(FIG_PDFS)

figures/%.pdf: figures/_scripts/%.py
	$(PYTHON) $<

# Standalone TikZ/pgfplots figure → PDF via pdflatex on the snippet, then move
# the result alongside its peers. Uses `latexmk -pdf` if present (cleaner
# intermediates), else falls back to pdflatex in a temp dir.
figures/%.pdf: figures/_scripts/%.tex
	@mkdir -p figures/_build
	@cp $< figures/_build/$*.tex
	cd figures/_build && pdflatex -interaction=nonstopmode -halt-on-error $*.tex >/dev/null
	@mv figures/_build/$*.pdf figures/$*.pdf
	@rm -f figures/_build/$*.aux figures/_build/$*.log figures/_build/$*.tex

figures-clean:
	@find figures -maxdepth 1 -name 'fig*.pdf' -delete 2>/dev/null || true
	@rm -rf figures/_build
	@echo "[paper] figures cleaned (sources under _scripts/ preserved)"

wordcount:
	@if command -v texcount >/dev/null 2>&1; then \
	  texcount -1 -sum -merge $(DOC).tex; \
	else \
	  echo "[paper] texcount not on PATH — falling back to wc -w on $(DOC).tex"; \
	  wc -w $(DOC).tex; \
	fi

pages:
	@if [ -f $(DOC).pdf ]; then \
	  if command -v pdfinfo >/dev/null 2>&1; then \
	    pdfinfo $(DOC).pdf | awk '/^Pages:/ {print "[paper] pages: " $$2}'; \
	  else \
	    echo "[paper] pdfinfo not on PATH (install poppler-utils)"; exit 1; \
	  fi; \
	else \
	  echo "[paper] $(DOC).pdf not built — run \`make\` first"; exit 1; \
	fi

lint:
	@/paper lint . 2>/dev/null || hexa run $$CLAUDE_PLUGIN_ROOT/bin/_paper.hexa --root $$CLAUDE_PLUGIN_ROOT lint . 2>/dev/null || { \
	  echo "[paper] /paper lint not reachable — invoke from Claude Code: /paper lint ."; exit 0; \
	}

arxiv-tar: $(DOC).pdf
	@mkdir -p out
	@TMP="$$(mktemp -d)"; \
	cp $(DOC).tex references.bib $$TMP/; \
	[ -f $(DOC).bbl ] && cp $(DOC).bbl $$TMP/ || true; \
	mkdir -p $$TMP/figures; \
	find figures -maxdepth 1 \( -name '*.pdf' -o -name '*.png' -o -name '*.eps' \) \
	  -exec cp {} $$TMP/figures/ \; ; \
	(cd $$TMP && tar -czf $(CURDIR)/out/$(SLUG)-arxiv.tar.gz .); \
	rm -rf $$TMP; \
	echo "[paper] arxiv bundle → out/$(SLUG)-arxiv.tar.gz"

clean:
	rm -f $(DOC).aux $(DOC).bbl $(DOC).blg $(DOC).log $(DOC).out \
	      $(DOC).toc $(DOC).synctex.gz
	@rm -rf figures/_build
	@echo "[paper] intermediates cleaned (PDF preserved)"

distclean: clean
	rm -f $(DOC).pdf
	@rm -rf out
