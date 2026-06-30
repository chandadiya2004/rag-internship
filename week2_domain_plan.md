# Project Domain Plan: College Admission Assistant

### 1. Project Title
**College Admission Assistant** — A RAG-based document intelligence system for answering student and administrator queries from institutional brochures.

### 2. Target User
* **Prospective Students & Parents:** Looking for quick, precise information regarding admission timelines, eligibility, and fees.
* **College Admission Helpdesk Personnel:** Seeking an efficient tool to look up specific administrative criteria from dense informational brochures.

### 3. Problem Statement
College admission brochures and informational booklets are often massive, multi-page PDFs packed with dense text, tables, and complex guidelines. Prospective candidates find it difficult and time-consuming to manually scan through these booklets to extract atomic answers like exact fee structures, specific course availabilities, or criteria. Furthermore, many official documents are scanned images or un-copyable formats, preventing standard digital searching and creating clear information access bottlenecks.

### 4. Documents to be Used
* **Official Institutional Brochures & Prospectuses:** Main source of data containing intake criteria, course descriptions, and codes.
* **Scanned/Image-Based PDFs & Digital Pamphlets:** Handled through an automated hybrid pipeline consisting of native text parsing (`pdfplumber`) and fallback Optical Character Recognition (`pytesseract`).

### 5. Five Expected Questions (System Should Answer)
1. "What is the total fee structure for the B.Tech Computer Science program?"
2. "What are the core eligibility criteria for international student admissions?"
3. "What is the last date to submit the application form for the upcoming semester?"
4. "Are there any scholarship opportunities available for meritorious students?"
5. "What hostal accommodation facilities are provided, and what are their costs?"

### 6. Questions the System Should Not Answer (Out of Scope)
1. **Subjective Comparisons:** "Is this college better than other top-tier universities?"
2. **Real-time Status Enquiries:** "What is the current status of my individual application form?"
3. **Speculative/Predictive Queries:** "What are my chances of getting selected with an 85% aggregate score?"
4. **General Extraneous Knowledge:** "What are the best tourist spots to visit in this city?"
5. **Direct Financial Negotiations:** "Can I get a discount or extra waiver on the admission fee?"

### 7. Success Criteria
* **Accuracy & Factual Alignment:** The system must answer strictly using facts provided within the uploaded brochure, completely avoiding hallucinations.
* **Robust Multi-Format Parsing:** Successful extraction of clear text from scanned or non-copyable document formats without database uploading crashes.
* **Session Refresh Isolation:** Absolute wipe of the cloud vector database table records and reset of interface session history upon loading a fresh document, ensuring zero cross-contamination of multi-institutional context data.
* **Clean UI Output:** Rapid generation of concise, human-readable answers through the Streamlit interface with hidden internal LLM reasoning lines (`<think>` tags suppressed).