# qmirror arXiv preprint build helpers.
# Date: 2026-05-04
# Status: v0.1 LaTeX skeleton; figures = text-flowchart placeholders.

JOB    := qmirror_arxiv
BUILD  := build
LATEX  := pdflatex -interaction=nonstopmode -output-directory=$(BUILD)
BIBTEX := bibtex

.PHONY: all pdf clean veryclean smoke

all: pdf

pdf: $(BUILD)/$(JOB).pdf

$(BUILD)/$(JOB).pdf: $(JOB).tex sections/*.tex bibliography.bib | $(BUILD)
	cp bibliography.bib $(BUILD)/bibliography.bib
	$(LATEX) $(JOB).tex
	cd $(BUILD) && $(BIBTEX) $(JOB)
	$(LATEX) $(JOB).tex
	$(LATEX) $(JOB).tex

$(BUILD):
	mkdir -p $(BUILD)

# Smoke test: 1 pass only, ignores undefined refs.
smoke: | $(BUILD)
	$(LATEX) $(JOB).tex || true
	@echo "--- smoke pass complete; check $(BUILD)/$(JOB).pdf"

clean:
	rm -f $(BUILD)/*.aux $(BUILD)/*.log $(BUILD)/*.out $(BUILD)/*.toc \
	      $(BUILD)/*.bbl $(BUILD)/*.blg $(BUILD)/*Notes.bib

veryclean: clean
	rm -rf $(BUILD)
