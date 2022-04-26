# PlagChecker - Plagiarism Checker for Assignments

* With the recent surge of pandemic, online classrooms have become inevitable. Be it lectures, exams, submissions everything has shifted to the online mode. But along with online exams and assignments submissions, the increasing rate of students 
accessing to unfair medium to complete them has increased 10x folds. 
* Therefore, an application which would check the percentage of plagiarized content in a document and thus encourage students to take genuine efforts to complete their coursework.

## Functionality

**1.** The system will take the input assignments in image (.jpg, .png) or document (.pdf) form.

**2.** If it is a .pdf file, then the document is first converted into .png format for application of image pre-processing techniques.

**3.** Image pre-processing techniques, like scaling, binarization and noise removal are performed.

**4.** Use Optical Character Recognition and extract the text.

**5.** Tokenize the text using NLP word tokenization method.

**6.** Then automate a search query for the tokenized text and perform web-scraping. 

**7.** Perform semantic analysis on the extracted text and web-scraped text and give out the plagiarisation percentage and the links of website from where the content is copied as output.
