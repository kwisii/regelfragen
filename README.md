# RefereeRuleScanner

This Python tool is helpful for football referees preparing for rule tests.
The Bavarian Football Association (BFV) continuously provides rule-related questions in its blue book.
This tool extracts these questions from the PDF files and converts them into a readable format for the flashcard tool Anki.
Additionally the questions from the dfb referee magazine will be extracted as well.

## Features

- Extracts rule-related questions and answers from PDFs ([BFV blue book](https://www.bfv.de/spielbetrieb-verbandsleben/schiedsrichter/schiedsrichter-regelwerk), [DFB referee magazine](https://www.dfb.de/training-service/schiedsrichterin/aktiver-schiedsrichter/schiedsrichter-zeitung))
- Stores the data in a text file
- Compatible with Anki for targeted learning using keywords

## Use learning cards

- Use the [GitHub Actions artefacts](https://github.com/kwisii/regelfragen/actions) to download the current rule set (.txt files) and import it into Anki!

## Installation

1. Clone this repository:
```
git clone https://github.com/your-repo/pdf-rule-extractor.git
cd pdf-rule-extractor
```

2. Install the required dependencies:
```
pip install pymupdf
```

## Usage

Simply place the script in the folder where your PDF files are stored and run it:
```
python create_anki_set_bfv.py
python create_anki_set_dfb.py
```

This will generate ```Regelfragen_Anki.txt``` and ```DFB_Fragen_Anki.txt``` files containing all extracted questions and answers in a format ready for import into Anki.

## Output Format

The extracted text file follows this structure:
```
#separator:tab
#html:false
<Question>\t<Answer>\t<PDF Filename>
```

Each question-answer pair is stored in a single line, separated by tabs.

## Future Features

- Additional export formats (e.g., GoodNotes)
- Direct Upload to Anki

Contributions and feature requests are welcome!