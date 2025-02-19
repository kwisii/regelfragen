import fitz
import os
import re

def extract_text_with_colors(pdf_path):
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
                        
                        if "Regelfragen-Auszug" in text:
                            start_extracting = True
                            continue
                        
                        if start_extracting:
                            extracted_data.append((text, color))
    
    return extracted_data

def parse_questions_and_answers(extracted_data):
    qa_pairs = []
    question = ""
    answer = ""
    black_color = 0 
    green_color = 65280
    
    is_question = False
    
    for text, color in extracted_data:
        if re.match(r"Frage \d+", text):
            if question and answer:
                qa_pairs.append((question.strip(), answer.strip()))
                question = ""
                answer = ""
            is_question = True
            continue

        if color == green_color:
            is_question = False
        
        if is_question and color == black_color:
            question += text + " "
        elif not is_question and color == green_color:
            answer += text + " "
        
    if question and answer:
        qa_pairs.append((question.strip(), answer.strip()))
    
    return qa_pairs

def save_to_file(all_qa_pairs, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#separator:tab\n#html:false\n")
        for question, answer, filename in all_qa_pairs:
            f.write(f"{question}\t{answer}\t{filename}\n")

def process_all_pdfs(directory, output_path):
    all_qa_pairs = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            pdf_filename = os.path.splitext(filename)[0]  # Entfernt die .pdf Endung
            extracted_data = extract_text_with_colors(pdf_path)
            qa_pairs = parse_questions_and_answers(extracted_data)
            for question, answer in qa_pairs:
                all_qa_pairs.append((question, answer, pdf_filename))
    
    save_to_file(all_qa_pairs, output_path)
    print(f"Extraction finished! All questions stored in: {output_path}")

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_directory, "Regelfragen_Anki.txt")
    process_all_pdfs(os.path.join(current_directory, "pdfs_bfv") , output_file)
