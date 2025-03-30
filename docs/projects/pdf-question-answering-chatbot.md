# PDF Question Answering Chatbot

**Difficulty**: Intermediate-Advanced  
**Time**: 60-90 minutes  
**Learning Focus**: Document processing, natural language understanding, information retrieval

## Overview

Create a chatbot that can answer questions from a PDF document. This project teaches students how to extract and process text from PDFs and use AI to retrieve relevant information based on user queries.

## Instructions

```python
import os
import sys
import fitz  # PyMuPDF
from ailabkit.chat import get_response

class PDFChatbot:
    """A chatbot that can answer questions about PDF documents."""
    
    def __init__(self):
        self.pdf_file = None
        self.pdf_text = ""
        self.context_size = 5000  # Max context size to send to the AI
    
    def load_pdf(self, file_path):
        """Load and extract text from a PDF file."""
        try:
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' not found.")
                return False
            
            self.pdf_file = file_path
            
            # Open the PDF
            doc = fitz.open(file_path)
            
            # Extract text from all pages
            full_text = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                full_text.append(page.get_text())
            
            self.pdf_text = "\n".join(full_text)
            
            # Print document stats
            print(f"\nDocument loaded: {os.path.basename(file_path)}")
            print(f"Number of pages: {len(doc)}")
            print(f"Total characters: {len(self.pdf_text)}")
            
            # Print a preview
            preview_length = min(200, len(self.pdf_text))
            print(f"\nPreview:\n{self.pdf_text[:preview_length]}...")
            
            return True
            
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def summarize_document(self):
        """Generate a summary of the document."""
        if not self.pdf_text:
            print("Error: No document loaded. Please load a PDF first.")
            return
        
        print("\nGenerating document summary...")
        
        # Create a prompt for the AI
        prompt = f"""
        Please provide a concise summary of the following document:
        
        {self.pdf_text[:5000]}  # Send only the first part if the document is large
        
        Include:
        1. Main topics and themes
        2. Key points or arguments
        3. Important entities mentioned
        4. Document structure overview
        
        Keep the summary under 300 words.
        """
        
        try:
            summary = get_response(prompt)
            print("\n=== Document Summary ===")
            print(summary)
        except Exception as e:
            print(f"Error generating summary: {e}")
    
    def answer_question(self, question):
        """Answer a question about the document."""
        if not self.pdf_text:
            print("Error: No document loaded. Please load a PDF first.")
            return
        
        if not question:
            print("Error: No question provided.")
            return
        
        print(f"\nAnswering: {question}")
        
        # Create a prompt for the AI
        prompt = f"""
        Document text:
        {self.pdf_text[:self.context_size]}
        
        Question: {question}
        
        Please answer the question based only on the information provided in the document.
        If the answer cannot be found in the document, state that clearly.
        Provide page numbers or sections if you can determine them from the context.
        """
        
        try:
            answer = get_response(prompt)
            print("\n=== Answer ===")
            print(answer)
        except Exception as e:
            print(f"Error generating answer: {e}")
    
    def extract_key_information(self):
        """Extract key information from the document."""
        if not self.pdf_text:
            print("Error: No document loaded. Please load a PDF first.")
            return
        
        print("\nExtracting key information...")
        
        # Create a prompt for the AI
        prompt = f"""
        Please extract and organize key information from this document:
        
        {self.pdf_text[:self.context_size]}
        
        Extract the following (if present):
        1. Dates and deadlines
        2. Names and organizations
        3. Numerical data or statistics
        4. Definitions or technical terms
        5. Action items or requirements
        
        Format the information in clear categories with brief explanations.
        """
        
        try:
            key_info = get_response(prompt)
            print("\n=== Key Information ===")
            print(key_info)
        except Exception as e:
            print(f"Error extracting information: {e}")
    
    def find_related_topics(self, topic):
        """Find information related to a specific topic in the document."""
        if not self.pdf_text:
            print("Error: No document loaded. Please load a PDF first.")
            return
        
        if not topic:
            print("Error: No topic provided.")
            return
        
        print(f"\nFinding information related to: {topic}")
        
        # Create a prompt for the AI
        prompt = f"""
        Document text:
        {self.pdf_text[:self.context_size]}
        
        Please find and extract all information related to the topic "{topic}" from the document.
        Include any definitions, explanations, examples, or references related to this topic.
        Organize the information in a structured way and indicate where in the document it appears if possible.
        If the topic is not mentioned in the document, please state that clearly.
        """
        
        try:
            related_info = get_response(prompt)
            print(f"\n=== Information Related to '{topic}' ===")
            print(related_info)
        except Exception as e:
            print(f"Error finding related information: {e}")
    
    def run(self):
        """Run the PDF chatbot interface."""
        print("=== PDF Question Answering Chatbot ===")
        print("This chatbot can answer questions about PDF documents.")
        
        while True:
            print("\nOptions:")
            print("1. Load a PDF document")
            print("2. Get document summary")
            print("3. Ask a question")
            print("4. Extract key information")
            print("5. Find related topics")
            print("6. Exit")
            
            choice = input("\nSelect an option (1-6): ")
            
            if choice == '1':
                # Load PDF
                file_path = input("\nEnter the path to a PDF file: ")
                self.load_pdf(file_path)
                
            elif choice == '2':
                # Summarize document
                self.summarize_document()
                
            elif choice == '3':
                # Ask a question
                if not self.pdf_text:
                    print("Please load a PDF document first (option 1).")
                    continue
                    
                question = input("\nEnter your question about the document: ")
                self.answer_question(question)
                
            elif choice == '4':
                # Extract key information
                self.extract_key_information()
                
            elif choice == '5':
                # Find related topics
                if not self.pdf_text:
                    print("Please load a PDF document first (option 1).")
                    continue
                    
                topic = input("\nEnter a topic to find in the document: ")
                self.find_related_topics(topic)
                
            elif choice == '6':
                # Exit
                print("\nExiting PDF Chatbot. Goodbye!")
                break
                
            else:
                print("Invalid choice. Please select a number between 1 and 6.")

# Run the chatbot
if __name__ == "__main__":
    chatbot = PDFChatbot()
    chatbot.run()
```

## Extension Ideas

- Add support for multiple document formats (DOCX, TXT, etc.)
- Implement semantic search to find specific information more efficiently
- Create a feature to compare information across multiple documents
- Add a citation generator for referencing document content
- Build a web interface using Flask or Streamlit
- Implement document chunking for handling very large documents

---

# Implementation Tips

When using these advanced mini-projects in a classroom setting:

1. **Scaffold appropriately**: Start with simpler projects for beginners, then progress to more complex ones.
2. **Modify complexity**: Adjust project requirements based on student skill level and available time.
3. **Pair programming**: Have students work in pairs to encourage collaboration.
4. **Challenge extensions**: Provide additional challenges for students who finish early.
5. **Focus on concepts**: Emphasize the programming concepts being used rather than just creating a functioning application.
6. **Ethical discussions**: Use these projects as opportunities to discuss AI ethics, bias, and limitations.

# Assessment Ideas

- Have students document their process in a digital portfolio
- Create a "project showcase" where students present their creations
- Ask students to write reflections on what they learned
- Evaluate code structure, comments, and organization
- Have students peer-review each other's projects

---

*These examples are designed to be flexible starting points. Adjust and expand them to suit your specific educational needs and student skill levels.*