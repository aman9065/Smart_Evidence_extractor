# Smart_Evidence_extractor
For example In many software, users often upload evidence in the form of PDFs or images (e.g., screenshots, reports, certificates). This project aims to automatically extract, highlight, and summarize key control evidence from uploaded documents using OCR and keyword-based analysis.

# Introduction

Smart Evidence Extractor is a web-based tool that helps users quickly find information from documents without reading them fully. It supports multiple file types like images, PDFs, and text files. Users can search for keywords, and the system extracts and summarizes related content. The tool saves time and makes document analysis easier and faster using OCR and AI-based summarization.

# Technologies Used

Flask – For building the web application and handling routes, sessions, and user interactions.
OpenCV – For image preprocessing like converting to grayscale and improving text readability.
Tesseract OCR – For extracting text from images and scanned documents.
pdf2image – For converting PDF pages into images so OCR can process them.
OpenAI API (GPT-4o-mini) – For generating summaries based on keywords fom extracted text.
Python-dotenv – For securely storing API keys and sensitive information.
io and os modules – For file management, handling uploads, and storing temporary data.

# How It Works

The user uploads a file in formats like PNG, JPG, PDF, or TXT.
The system processes the file and extracts text using OCR technology.
The user enters one or more keywords to search within the document.
The system scans the text and generates a summary based on the keywords.
The summary is displayed, and the user can download or copy it for further use.
The tool ensures faster and accurate access to important information.

* Below is the user interface of the Smart Evidence Extractor where users can upload files and generate summaries. 

<img width="1918" height="870" alt="image" src="https://github.com/user-attachments/assets/54763b0f-6fd7-4063-b2a4-05b7d640756d" />

# Accuracy of Summary #

<img width="1078" height="611" alt="image" src="https://github.com/user-attachments/assets/9925bfd5-cb74-4d47-8d7c-c6f066f7820b" />


