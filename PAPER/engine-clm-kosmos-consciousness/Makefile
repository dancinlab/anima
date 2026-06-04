# engine-clm-kosmos-consciousness monograph build
# Requires a LaTeX toolchain (xelatex preferred for native UTF-8 tier badges).
MAIN = main
ENGINE = xelatex

.PHONY: all clean pages
all:
	$(ENGINE) $(MAIN).tex
	-bibtex $(MAIN)
	$(ENGINE) $(MAIN).tex
	$(ENGINE) $(MAIN).tex

pages:
	@pdfinfo $(MAIN).pdf 2>/dev/null | grep Pages || echo "compile first (make all)"

clean:
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).toc $(MAIN).bbl $(MAIN).blg
