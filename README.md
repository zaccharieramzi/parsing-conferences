# Parsing conferences

![GitHub Workflow Build Status](https://github.com/zaccharieramzi/parsing-conferences/workflows/Continuous%20testing/badge.svg)

Trying to automatically parse conference papers, in order to perform meta-analysis.
This util focuses on the institutions that publish in ML conference and is based on the tool CERMINE.

I clearly don't know if this is the best tool to parse a scientific PDF to get the institutions, but I know that it's definitely not bullet-proof.
Also, since I want to make this relatively fast (still 5-10s/paper) I needed to rely on programmatically splitting PDFs, which I found is very error-prone using PyPDF2, an unmaintained library.

I also dabbled a bit with async programming but the neurips server didn't like that too much.

## Local institution extraction

Download [this jar](http://maven.ceon.pl/artifactory/webapp/#/artifacts/browse/simple/General/kdd-releases/pl/edu/icm/cermine/cermine-impl/1.13/cermine-impl-1.13-jar-with-dependencies.jar).
