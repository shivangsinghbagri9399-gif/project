from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

CURRENT_DOC = None

# Real project metadata
PROJECT_TITLE = 'LSB Steganography Mini-App'
STUDENT_NAME = '[STUDENT NAME]'
STUDENT_CODE = '[STUDENT CODE]'
SESSION = '[SESSION]'
GUIDE_NAME = '[GUIDE NAME]'
HOD_NAME = '[HOD NAME]'


def set_doc_style(doc):
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    style.paragraph_format.space_before = Pt(6)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.5


def add_centered(doc, text, bold=False, size=12):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = bold
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    return p


def add_section_title(doc, title, level=1):
    doc.add_heading(title, level=level)


def add_paragraphs(*texts, doc=None):
    target_doc = doc if doc is not None else CURRENT_DOC
    if target_doc is None:
        raise ValueError('No document is active for add_paragraphs().')
    for text in texts:
        p = target_doc.add_paragraph(text)
        p.style = 'Normal'
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.5


def build_report():
    global CURRENT_DOC
    doc = Document()
    CURRENT_DOC = doc
    set_doc_style(doc)

    # Front Matter: Title Page
    add_centered(doc, 'A PROJECT REPORT', True, 18)
    add_centered(doc, 'ON', False, 14)
    add_centered(doc, '“LSB STEGANOGRAPHY MINI-APP”', True, 18)
    add_centered(doc, 'Submitted in partial fulfillment of the requirements for the award of the degree of', False, 12)
    add_centered(doc, 'Bachelor of Technology', True, 14)
    add_centered(doc, 'in', False, 12)
    add_centered(doc, 'Computer Science and Engineering', True, 14)
    add_centered(doc, 'B.Tech. (CSE) AI/DS', True, 14)
    add_centered(doc, '5th Semester', True, 12)
    add_centered(doc, 'Submitted By:', True, 12)
    add_centered(doc, STUDENT_NAME, False, 12)
    add_centered(doc, STUDENT_CODE, False, 12)
    add_centered(doc, SESSION, False, 12)
    add_centered(doc, 'Under the Guidance of:', True, 12)
    add_centered(doc, GUIDE_NAME, False, 12)
    add_centered(doc, 'Department of Computer Science & Engineering', False, 12)
    add_centered(doc, 'Faculty of Engineering and Technology', False, 12)
    add_centered(doc, 'AKS University, Satna (M.P.)', False, 12)
    doc.add_page_break()

    # Certificate page
    add_section_title(doc, 'CERTIFICATE', 1)
    add_paragraphs(
        'This is to certify that the project report entitled "LSB Steganography Mini-App" submitted by ' + STUDENT_NAME + ' (' + STUDENT_CODE + ') in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering is a bonafide record of work carried out under the supervision of ' + GUIDE_NAME + '.',
        'The project is based on the actual implementation of LSB steganography using Python, Tkinter, Pillow, and PNG images for educational demonstration and analysis.',
        'Guide / Supervisor: ' + GUIDE_NAME,
        'Head of Department: ' + HOD_NAME,
        'External Examiner: [EXTERNAL EXAMINER NAME]',
        'Signature of Guide: ____________________________',
        'Signature of HOD: ____________________________',
        'Signature of External Examiner: ____________________________'
    )
    doc.add_page_break()

    # Declaration
    add_section_title(doc, 'SELF DECLARATION', 1)
    add_paragraphs(
        'I, ' + STUDENT_NAME + ', student of B.Tech. Computer Science and Engineering, AKS University, Satna (M.P.), hereby declare that the project report entitled "LSB Steganography Mini-App" is my own academic work carried out under the guidance of ' + GUIDE_NAME + ' during the academic session ' + SESSION + '.',
        'I further declare that this report is my original contribution and has not been submitted for any other degree or diploma elsewhere.',
        'Student Name: ' + STUDENT_NAME,
        'Student Code: ' + STUDENT_CODE,
        'Signature: ____________________________',
        'Date: ____________________________'
    )
    doc.add_page_break()

    # Acknowledgement
    add_section_title(doc, 'ACKNOWLEDGEMENT', 1)
    add_paragraphs(
        'I express my sincere gratitude to my project guide, ' + GUIDE_NAME + ', for the valuable guidance, support, and constructive feedback throughout the development of this project.',
        'I am also thankful to the Head of the Department, ' + HOD_NAME + ', and the faculty members of the Department of Computer Science and Engineering for enabling an academic environment that encouraged learning, discussion, and project work.',
        'I extend my gratitude to AKS University for providing the infrastructure, resources, and support required for the completion of the project.',
        'I thank my parents, family members, friends, and classmates for their continuous encouragement, patience, and understanding during the course of this work.',
        'This project helped me understand the practical implementation of information security concepts, digital image processing, and desktop application development using Python and Tkinter.'
    )
    doc.add_page_break()

    # Abstract
    add_section_title(doc, 'ABSTRACT', 1)
    add_paragraphs(
        'The LSB Steganography Mini-App is a desktop graphical application developed using Python 3.x, Tkinter, and Pillow to demonstrate the embedding and extraction of text messages inside digital images using Least Significant Bit (LSB) steganography. The project focuses on concealing the existence of a message by modifying the least significant bits of the RGB channels in a PNG image while keeping the visual appearance of the image nearly unchanged.',
        'Steganography differs from cryptography in that it is designed to hide the fact that communication is taking place rather than to make the content unreadable. The application uses the LSB technique to embed a UTF-8 encoded message along with a 32-bit message-length prefix. During extraction, the first 32 bits are read to determine the total message size in bits, after which the remaining bits are reconstructed into bytes and decoded to display the original text.',
        'The system is implemented as a small local desktop application with an Encode tab and a Decode tab. The GUI allows the user to browse an image, enter a secret message, save an encoded image, and later recover the hidden data from the encoded image. The application performs validation for empty messages, invalid image selection, image capacity, and extraction errors. This makes the project appropriate for educational demonstration in information security, image handling, data hiding, and GUI development.',
        'The project is intended for academic learning rather than secure communication in production systems. It does not implement encryption, authentication, or database features. Instead, it demonstrates the principles of bit-level data insertion, pixel processing, PNG usage, and message recovery. The project is also supported by a testing file that checks the encode/decode round trip, capacity limits, UTF-8 support, and multiple image sizes.',
        'Keywords: image steganography, LSB, PNG, UTF-8, information security, Python, Tkinter, Pillow.'
    )
    doc.add_page_break()

    # Table of Contents
    add_section_title(doc, 'TABLE OF CONTENTS', 1)
    contents = [
        '1. Introduction',
        '2. Objectives of the Project',
        '3. Scope of the Project',
        '4. Definition of the Problem',
        '5. Benefits of the Project',
        '6. Main Modules of the Project',
        '7. Technical Overview',
        '8. System Configuration',
        '9. Block Diagram',
        '10. Data Flow Diagram',
        '11. ER Diagram',
        '12. Project Explanation',
        '13. Coding with Detailed Explanation',
        '14. Results and Analysis',
        '15. Software Testing',
        '16. Conclusion',
        '17. Bibliography / References',
        '18. Appendix: Student Profile',
        '19. Appendix: Published Paper List',
        '20. Appendix: Plagiarism Report',
        '21. Appendix: PPT Handouts'
    ]
    for line in contents:
        doc.add_paragraph(line)
    doc.add_page_break()

    # Chapter 1
    add_section_title(doc, 'CHAPTER 1 — INTRODUCTION', 1)
    add_section_title(doc, '1.1 Introduction to Information Security', 2)
    add_paragraphs(
        'Information security relates to protecting digital information from unauthorized access, alteration, or destruction. One of the major goals is confidentiality, which ensures that information is accessible only to authorized users. In many communication systems, cryptography is used to protect message content, while steganography focuses on hiding the existence of the communication itself.'
    )
    add_section_title(doc, '1.2 Confidentiality and Data Protection', 2)
    add_paragraphs(
        'Confidentiality ensures that sensitive information remains inaccessible to unauthorized persons. In this project, the secret message is not stored in an obvious form; instead, it is hidden in the image pixel data. This demonstrates a basic concept of data protection without the use of encryption.'
    )
    add_section_title(doc, '1.3 Introduction to Steganography', 2)
    add_paragraphs(
        'Steganography is the method of concealing information within a carrier such as an image, audio, video, or text. The word literally means covered writing. In digital media, the carrier must appear ordinary so that the hidden message is not visually evident.'
    )
    add_section_title(doc, '1.4 Steganography vs Cryptography', 2)
    add_paragraphs(
        'Cryptography protects the content by making it unreadable, while steganography hides the fact that a message exists. This project demonstrates the latter by embedding a message into image pixels. It does not claim to provide cryptographic security.'
    )
    add_section_title(doc, '1.5 Digital Image Steganography', 2)
    add_paragraphs(
        'Image steganography hides information in digital images by modifying particular image components. The LSB technique is the simplest form and is suitable for educational work. Because digital images contain many pixels and color channels, they provide a practical carrier for hidden data.'
    )
    add_section_title(doc, '1.6 Image as a Cover Medium', 2)
    add_paragraphs(
        'The image acts as a cover medium. The project uses PNG, because PNG is lossless and preserves the original pixel values while the message bits are inserted. Lossy formats such as JPEG may alter the image data and destroy the embedded payload.'
    )
    add_section_title(doc, '1.7 Least Significant Bit Technique', 2)
    add_paragraphs(
        'The LSB technique changes the least significant bit of selected pixel channels to store message data. Since the change is usually limited to one unit of intensity value, it is nearly invisible to the eye. In an RGB image, each pixel has three channels and therefore has three available bit positions for LSB embedding.'
    )
    add_section_title(doc, '1.8 RGB Image Representation', 2)
    add_paragraphs(
        'An RGB color image stores red, green, and blue values for each pixel. Each channel typically uses 8 bits, giving 24 bits per pixel. The project converts the image to RGB before embedding so that the LSB values can be processed consistently.'
    )
    add_section_title(doc, '1.9 PNG Image Format', 2)
    add_paragraphs(
        'PNG is a lossless format designed for portable raster graphics. This makes it suitable for steganography because the encoded bits remain stable when the image is saved and reopened. The project specifically recommends PNG for this purpose.'
    )
    add_section_title(doc, '1.10 Need for LSB Steganography', 2)
    add_paragraphs(
        'There are situations where the existence of communication itself must remain hidden. LSB steganography offers a simple demonstration of data hiding in which the medium remains visually ordinary. This makes it a valuable teaching example in image processing and information security.'
    )
    add_section_title(doc, '1.11 Motivation of the Project', 2)
    add_paragraphs(
        'The project is motivated by the need to connect real-world digital image processing with theoretical concepts like binary data, bitwise operations, and information security. It demonstrates how a message can be hidden in an image without requiring complex analysis or large infrastructure.'
    )
    add_section_title(doc, '1.12 Project Background', 2)
    add_paragraphs(
        'The project originated as a B.Tech mini-project aimed at providing a simple, understandable example of steganography. It uses standard Python libraries and a small GUI so that students can easily comprehend and test the idea.'
    )
    add_section_title(doc, '1.13 Overview of Proposed System', 2)
    add_paragraphs(
        'The proposed system includes a GUI with Encode and Decode tabs. Users can select a cover image, type a message, encode it into the image, save the stego image, and later recover the hidden text by selecting the encoded image. The source code implements the core LSB algorithm and validation checks.'
    )
    add_section_title(doc, '1.14 Educational Importance', 2)
    add_paragraphs(
        'The project has strong educational value because it combines several topics in one practical application, including digital images, binary representation, text encoding, and software testing. It is a useful teaching aid in information security laboratories and computer science classrooms.'
    )
    add_section_title(doc, '1.15 Advantages of the Proposed Application', 2)
    add_paragraphs(
        'The application is lightweight, easy to run, and suitable for beginner use. It requires only Python, Tkinter, and Pillow. It encourages experimentation with image data and exposes students to the concept of hidden message embedding without requiring a large codebase.'
    )
    add_section_title(doc, '1.16 Limitations of Basic LSB Steganography', 2)
    add_paragraphs(
        'LSB steganography is simple and educational, but it has limitations: it is vulnerable to compression, image processing operations, and statistical analysis. It does not provide cryptographic security or message authentication. The project therefore clearly describes its educational scope.'
    )
    add_section_title(doc, '1.17 Chapter Summary', 2)
    add_paragraphs(
        'This chapter introduced the concepts of information security, steganography, digital image representation, LSB embedding, and the utility of PNG files for lossless embedding. The project is best understood as an educational steganography demonstration rather than a production-grade secure communication system.'
    )
    doc.add_page_break()

    # Chapter 2
    add_section_title(doc, 'CHAPTER 2 — OBJECTIVES OF THE PROJECT', 1)
    out = [
        'The primary objective of the project is to design and implement a desktop application for hiding messages inside PNG images and retrieving them later.',
        'The technical objectives include using Python, Tkinter, and Pillow for image loading, pixel processing, validation, and GUI operation.',
        'Functional objectives include image selection, message entry, capacity check, and encode/decode functions.',
        'The GUI objective is to present a clean Encode tab and Decode tab for beginners and students.',
        'The project also aims to support UTF-8 text and a 32-bit message-length header so that the decoder can reconstruct the correct payload.',
        'Finally, the project provides testing and educational demonstration value without claiming advanced security features beyond what is actually implemented.'
    ]
    for text in out:
        doc.add_paragraph(text)
    doc.add_page_break()

    # Chapter 3
    add_section_title(doc, 'CHAPTER 3 — SCOPE OF THE PROJECT', 1)
    add_paragraphs(
        'The current scope of the project is a local desktop application that hides UTF-8 text in PNG images using the LSB principle. It includes GUI-based image selection, message entry, encoding, decoding, validation, and testing.',
        'The functional scope does not include databases, encryption, cloud deployment, or network communication. The project is intentionally limited to educational local use and practical demonstration.',
        'The technical scope is based on Python, Tkinter, Pillow, PNG, and the RGB channel representation of digital images. It is designed to teach and demonstrate a simple steganographic algorithm in an undergraduate environment.',
        'Future scope may include stronger data security, better integration, and support for more image types or advanced steganography techniques, but these remain future work and are not part of the current implementation.'
    )
    doc.add_page_break()

    # Chapter 4
    add_section_title(doc, 'CHAPTER 4 — DEFINITION OF PROBLEM', 1)
    add_paragraphs(
        'The problem is to conceal the existence of sensitive information in a digital image while keeping the image visually ordinary. Traditional encrypted messages may still reveal that communication exists, whereas steganography attempts to hide the communication itself.',
        'Manual steganography is difficult and error-prone. This project automates the process with a software application that hides secret text in image pixels and later extracts it without manual computation.',
        'The project also addresses the challenge of incorrect extraction by using a message length prefix and capacity checks. This ensures the decoder knows how many bits to read and prevents invalid or oversized data.'
    )
    doc.add_page_break()

    # Chapter 5
    add_section_title(doc, 'CHAPTER 5 — BENEFITS OF THE PROJECT', 1)
    add_paragraphs(
        'The project offers educational value because it links theory and practice in information security, digital image processing, and software testing.',
        'It is useful for students because it demonstrates binary representation, bit operations, and the idea of hidden communication.',
        'It is cost effective because it uses open-source Python libraries and a standard desktop environment.',
        'It is also maintainable because the code structure is modular and easy to follow.'
    )
    doc.add_page_break()

    # Chapter 6 main modules
    add_section_title(doc, 'CHAPTER 6 — MAIN MODULES OF THE PROJECT', 1)
    module_list = [
        'Graphical User Interface Module: Creates the desktop interface with Encode and Decode tabs.',
        'Image Selection Module: Selects a file using Tkinter file dialogs and validates it.',
        'Message Input Module: Accepts the secret message and validates that it is not empty.',
        'UTF-8 Encoding Module: Converts the message to bytes before embedding.',
        'Message Length Header Module: Stores a 32-bit value representing the hidden message length in bits.',
        'LSB Encoding Module: Replaces the LSB of RGB channels with the message bits.',
        'Image Generation and Saving Module: Builds a new image and saves it as a PNG output file.',
        'LSB Extraction Module: Reads the least significant bits back from the stego image.',
        'Message Reconstruction Module: Rebuilds bytes and then the text message.',
        'Error Handling Module: Provides user feedback and validation for invalid inputs.',
        'Testing Module: Verifies encode/decode behavior, capacity validation, UTF-8 support, and different image sizes.'
    ]
    for item in module_list:
        doc.add_paragraph(item)
    doc.add_page_break()

    # Chapter 7 technical overview
    add_section_title(doc, 'CHAPTER 7 — TECHNICAL OVERVIEW', 1)
    add_paragraphs(
        'Python 3.x provides the base implementation environment. Tkinter provides the GUI required for file selection and message handling. Pillow supports image loading and pixel operations. PNG is the preferred cover medium because it is lossless, and RGB pixel channels allow the hidden message to be written into bit positions with little visible distortion.',
        'The core capacity formula for this project is based on RGB image pixels: total bits = width × height × 3. A 32-bit message-length header reduces the usable payload, so the effective capacity is (width × height × 3) − 32 bits.'
    )
    doc.add_page_break()

    # Chapter 8 system config
    add_section_title(doc, 'CHAPTER 8 — SYSTEM CONFIGURATION', 1)
    add_paragraphs(
        'The project requires Python 3.x, Tkinter, and Pillow. The dependencies are listed in requirements.txt and the actual requirement is pillow>=10.0.0. The project is intended for a standard desktop computer with local storage access and a local PNG image file.',
        'The workflow is simple: install Python, install Pillow, run the application using python steg_app.py, select an image, enter the secret message, and either encode or decode the hidden text.'
    )
    doc.add_page_break()

    # Chapter 9 block diagram
    add_section_title(doc, 'CHAPTER 9 — BLOCK DIAGRAM', 1)
    add_paragraphs(
        'The block diagram of the project shows the flow from input image and user text into the encoding logic, where the message bits are embedded into the image. The stego image is then used as input to the decoding logic, which extracts the length header and reconstructs the original message text.',
        'This model reflects the actual implementation of hide_message() and extract_message() in the project source code.'
    )
    doc.add_page_break()

    # Chapter 10 DFD
    add_section_title(doc, 'CHAPTER 10 — DATA FLOW DIAGRAM', 1)
    add_paragraphs(
        'The system data flow includes user input, image validation, LSB embedding, stego image creation, and message recovery. No relational database is used because the application is a local file-based desktop tool rather than a database-driven application.',
        'The context-level DFD shows the user as the external entity, while the level-0 DFD shows encoding and decoding processes. The data travels in local file and memory form only.'
    )
    doc.add_page_break()

    # Chapter 11 ER diagram
    add_section_title(doc, 'CHAPTER 11 — ER DIAGRAM', 1)
    add_paragraphs(
        'No database is implemented in the actual project. Therefore, a traditional ER diagram is not appropriate. The conceptual data model instead represents the input image, secret message, encoded image, and recovered message as local artifacts of the application workflow.'
    )
    doc.add_page_break()

    # Chapter 12 project explanation
    add_section_title(doc, 'CHAPTER 12 — PROJECT EXPLANATION', 1)
    add_paragraphs(
        'The complete workflow starts when the user opens the Tkinter-based GUI. The user selects a cover image, enters the secret message, and clicks the Encode button. The hide_message() function converts the message to UTF-8 bytes, computes the length in bits, builds a 32-bit header, and then replaces the LSB of each RGB channel with the next bit in the payload.',
        'The output is a new PNG image. Later, the user selects the encoded image in the Decode tab; the extract_message() function reads the first 32 bits as the length header, reconstructs the payload, and decodes the bytes to text. The result is shown in the GUI output area.'
    )
    doc.add_page_break()

    # Chapter 13 code explanation
    add_section_title(doc, 'CHAPTER 13 — CODING WITH DETAILED EXPLANATION', 1)
    add_paragraphs(
        'The actual source code is organized into helper functions such as rgb_to_bytes(), int_to_rgb(), extract_bits_from_image(), embed_bits_into_image(), hide_message(), and extract_message(). These functions implement the actual LSB embedding and extraction logic of the project.',
        'The StegApp class creates the Tkinter interface using a Notebook with separate Encode and Decode tabs. It validates the image path and message, then triggers the correct processing function in response to user clicks.'
    )
    doc.add_page_break()

    # Chapter 14 results and analysis
    add_section_title(doc, 'CHAPTER 14 — RESULT AND ANALYSIS', 1)
    add_paragraphs(
        'The project is expected to produce a stego image that remains visually similar to the original image while carrying a hidden UTF-8 message. The result is qualitatively judged by correctness of the round trip, clarity of the GUI, capacity limits, and suitability of PNG as a cover format.',
        'The project does not provide numerical performance benchmarks, so the analysis remains qualitative and implementation-based. The important result is that the application works as a conceptual and educational image steganography demonstration.'
    )
    doc.add_page_break()

    # Chapter 15 testing
    add_section_title(doc, 'CHAPTER 15 — SOFTWARE TESTING', 1)
    add_paragraphs(
        'The test_steg.py file implements functional tests for the encode/decode cycle, capacity limits, UTF-8 support, and multiple image sizes. The tests create temporary images and check whether the algorithm correctly round-trips messages without fabricating results.',
        'The test suite is appropriate for this project because it validates the real functions implemented in the source code and highlights the limitations of the algorithm when the image is too small or when invalid conditions are encountered.'
    )
    doc.add_page_break()

    # Chapter 16 conclusion
    add_section_title(doc, 'CHAPTER 16 — CONCLUSION', 1)
    add_paragraphs(
        'In conclusion, the LSB Steganography Mini-App is a simple, educational, and technically valid Python application for hiding text in PNG images. It demonstrates the use of least significant bits, UTF-8 encoding, bitwise operations, and GUI-driven local image processing. It should be read as a teaching project and not as a fully secure communication system.'
    )
    doc.add_page_break()

    # Chapter 17 references
    add_section_title(doc, 'CHAPTER 17 — BIBLIOGRAPHY / REFERENCES', 1)
    add_paragraphs(
        'Python Software Foundation. Python Documentation.',
        'Tkinter Documentation. Python standard library GUI toolkit.',
        'Pillow Documentation. Python Imaging Library (PIL) official reference.',
        'PNG specification and reference documentation.',
        'Unicode Consortium Documentation for UTF-8 and Unicode encoding.',
        'Academic references on steganography, information security, and image processing.'
    )
    doc.add_page_break()

    # Appendices
    add_section_title(doc, 'CHAPTER 18 — APPENDIX: STUDENT PROFILE', 1)
    add_paragraphs(
        'Student Name: ' + STUDENT_NAME,
        'Student Code: ' + STUDENT_CODE,
        'Degree: Bachelor of Technology',
        'Department: Computer Science & Engineering',
        'University: AKS University, Satna (M.P.)',
        'Semester: 5th Semester',
        'Academic Session: ' + SESSION,
        'Technical Skills: Python, Tkinter, Pillow, image processing, testing',
        'Project Role: Student Developer and Researcher',
        '[INSERT PROFESSIONAL PHOTOGRAPH HERE]'
    )
    doc.add_page_break()

    add_section_title(doc, 'CHAPTER 19 — APPENDIX: PUBLISHED PAPER LIST', 1)
    add_paragraphs(
        'No published paper information was provided in the project source materials.',
        'A placeholder table can be inserted here if required by the university format.'
    )
    doc.add_page_break()

    add_section_title(doc, 'CHAPTER 20 — APPENDIX: PLAGIARISM REPORT', 1)
    add_paragraphs(
        '[INSERT OFFICIAL PLAGIARISM CHECK REPORT HERE]',
        'This placeholder should be replaced by the official plagiarism report before final submission.'
    )
    doc.add_page_break()

    add_section_title(doc, 'CHAPTER 21 — APPENDIX: PPT HANDOUTS', 1)
    add_paragraphs(
        'Slide 1 — Project Title',
        'Slide 2 — Problem and Objectives',
        'Slide 3 — Technology and Architecture',
        'Slide 4 — LSB Encoding/Decoding Workflow',
        'Slide 5 — Results and Testing',
        'Slide 6 — Conclusion and Future Scope'
    )

    # Save
    output_path = 'project_report.docx'
    doc.save(output_path)
    print(f'Generated {output_path}')


if __name__ == '__main__':
    build_report()
