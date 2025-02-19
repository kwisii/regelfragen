import fitz
import re
import os

def extract_text_with_colors(pdf_path):
    """Extracts text and color information from a PDF file."""
    doc = fitz.open(pdf_path)
    extracted_data = []
    
    start_extracting = False
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        color = span["color"]
                        
                        if "R E G E L-T E S T" in text:
                            start_extracting = True

                        if start_extracting:
                            extracted_data.append((text, color))

    return extracted_data

def parse_situations_and_answers(extracted_data):
    """Parses situations and answers based on color and structure."""
    qa_pairs = []
    current_situation = ""
    current_question = ""
    answers = {}
    black_color = [1578774, 2301728]
    green_color = [1947530, 2403968]
    parsing_answers = False
    found_first_separator = False
    current_answer = ""
    current_situation_number = None

    for text, color in extracted_data:
        if "So werden die 15" in text:
            found_first_separator = True
            continue

        if found_first_separator and "richtig gelöst:" in text:
            parsing_answers = True
            qa_pairs.append((current_question.strip(), "", current_situation))
            continue

        if not parsing_answers:
            situation_match = re.match(r"S\s*I\s*T\s*U\s*A\s*T\s*I\s*O\s*N\s*(1[0-5]|[1-9])", text)
            if situation_match:
                if current_question:
                    qa_pairs.append((current_question.strip(), "", current_situation))
                current_situation = text.replace(" ", "")
                current_question = ""
                continue

            if black_color[0] <= color <= black_color[1] and current_situation:
                current_question += " " + text
        else:
            match = re.match(r"(\d+):", text)
            if match:
                if current_situation_number is not None and current_answer:
                    for idx, (question, answer, situation) in enumerate(qa_pairs):
                        situation_number_match = re.search(r"\d+", situation)
                        if situation_number_match and situation_number_match.group() == current_situation_number:
                            qa_pairs[idx] = (question, current_answer.strip(), situation)
                current_situation_number = match.group(1)
                current_answer = text[len(match.group(0)):].strip()
            elif green_color[0] <= color <= green_color[1]:
                current_answer += " " + text.strip()

    if current_situation_number and current_answer:
        for idx, (question, answer, situation) in enumerate(qa_pairs):
            if situation.endswith(current_situation_number):
                qa_pairs[idx] = (question, current_answer.strip(), situation)

    return qa_pairs

def save_to_file(qa_pairs, output_path):
    """Saves all question-answer pairs to a single tab-separated file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#separator:tab\n#html:false\n")
        for question, answer, filename in qa_pairs:
            f.write(f"{question}\t{answer}\t{filename}\n")

def process_pdf(directory, output_path):
    """Processes the PDF and extracts all relevant data."""
    all_qa_pairs = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            pdf_filename = os.path.splitext(filename)[0]
            extracted_data = extract_text_with_colors(pdf_path)
            qa_pairs = parse_situations_and_answers(extracted_data)
            for question, answer, situation in qa_pairs:
                all_qa_pairs.append((question, answer, pdf_filename))

    save_to_file(all_qa_pairs, output_path)
    print(f"Extraction complete! Data saved to: {output_path}")

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_directory, "DFB_Fragen_Anki.txt")
    process_pdf(os.path.join(current_directory, "pdfs_dfb"), output_file)