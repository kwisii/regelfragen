# PDF Rule Questions Extractor

This Python script is a helpful tool for football referees preparing for rule tests.
The Bavarian Football Association (BFV) continuously provides rule-related questions in its blue book.
This script extracts these questions from PDF files and converts them into a readable format for the flashcard tool Anki.

## Features

- Extracts rule-related questions and answers from PDFs
- Saves the data in a tab-separated text file
- Compatible with Anki for targeted learning using keywords
- Processes all PDFs in the same directory automatically

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
python extract_questions.py
```

This will generate a ```gesamt_extrahiert.txt``` file containing all extracted questions and answers in a format ready for import into Anki.

## Output Format

The extracted text file follows this structure:
```
#separator:tab
#html:false
<Question>\t<Answer>\t<PDF Filename>
```

Each question-answer pair is stored in a single line, separated by tabs.

## Future Features

- Support for DFB referee magazine
- Additional export formats (e.g., GoodNotes)

Contributions and feature requests are welcome!