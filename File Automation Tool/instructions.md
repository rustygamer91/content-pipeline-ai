Instructions for Claude to Build the File Automation Tool

Objective
Develop a lightweight File Automation Tool to:

Organize and rename files automatically based on user-defined rules.
Leverage Google Gemini APIs for intelligent file content analysis and NLP-based rule interpretation.
Deploy the tool as a web application using Google Cloud Platform (GCP).
Core Functionalities for the MVP
Rule-Based File Organization:
Accept user-defined rules (via a web form or natural language input).
Sort files into folders based on metadata, content, or naming conventions.
Examples:
"Move all PDFs with 'Invoice' in the name to the Finance folder."
"Organize photos by year and month."
Batch Renaming:
Rename files based on patterns (e.g., sequential numbering, adding timestamps).
Example: Report_2024-12-15.pdf or Photo_001.jpg.
Preview and Undo Actions:
Provide a preview of file changes before execution.
Allow users to undo the last performed action.
Step-by-Step Instructions
1. Environment Setup

Configure Google Cloud:
Enable Google Cloud Functions, Firestore, and Google Drive API.
Enable Google Gemini APIs for NLP and multimodal tasks.
Install necessary libraries for development:
Backend: Python (fastapi, google-cloud-storage, google-cloud-firestore) or Node.js (express, googleapis).
Frontend: React.js (use axios for API communication).
2. Backend Development

Build the backend to handle file organization, renaming, and rule processing.

API Endpoints:
POST /upload: Accept file metadata and user-defined rules.
POST /process: Process files according to rules.
POST /undo: Revert the last action.
File Organization Logic:
Use Gemini’s NLP to parse rules into executable logic.
Example Rule:
Input: "Move all files containing 'Invoice' in the name to Finance."
Logic: Apply regex to file names and execute moves via Google Drive API or local file system APIs.
Batch Renaming Logic:
Rename files using patterns like:
Sequential numbering (File_001, File_002).
Adding timestamps (Report_2024-12-15.pdf).
Preview and Undo:
Store a temporary record of actions in Firestore.
Provide a preview table of before/after file changes.
3. Frontend Development

Drag-and-Drop File Upload:
Use react-dropzone to allow users to drag files or folders into the app.
Rule Configuration Interface:
Provide options for users to:
Define file types or keywords for sorting.
Create renaming patterns.
Input natural language rules (processed via Gemini).
Preview Table:
Show a table with:
File names (current and new).
Actions to be performed (move/rename).
Integration with Backend:
Use axios to call backend APIs.
Implement loading indicators and error handling.
4. Google Gemini Integration

NLP for Rule Parsing:
Send user-defined rules to Gemini's NLP API.
Example:
Input: "Move all PDFs to the Reports folder."
Output: { "action": "move", "file_type": "PDF", "destination": "Reports" }.
File Content Analysis:
Use Gemini’s text extraction to identify file content.
Example:
Detect "Invoice" or "Q4 Report" in document text.
5. Deployment

Frontend:
Build the React app: npm run build.
Deploy on Firebase Hosting or Vercel.
Backend:
Deploy on Google Cloud Functions or Cloud Run.
Use a Docker container if needed for scalability.
Firestore Integration:
Store user rules and action logs in Firestore.
Future Features
Once the MVP is live, consider these enhancements:

Cloud Integration:
Add support for cloud storage platforms like Dropbox or OneDrive.
AI-Powered Suggestions:
Use Gemini to suggest sorting rules based on file history.
Cross-Platform Support:
Build a Chrome extension or desktop app for easier access.
Example API Specifications
POST /upload

Description: Upload file metadata and user rules.
Request Body:
{
  "files": [
    { "name": "Invoice_Q4.pdf", "type": "PDF", "path": "/Desktop/Invoices/" }
  ],
  "rules": [
    { "type": "move", "file_type": "PDF", "destination": "/Finance/" }
  ]
}
Response:
{ "status": "success", "message": "Files uploaded successfully" }
POST /process

Description: Process files based on user rules.
Request Body:
{
  "action": "rename",
  "pattern": "Invoice_YYYY-MM-DD.pdf"
}
Response:
{
  "status": "success",
  "preview": [
    { "current_name": "Invoice_Q4.pdf", "new_name": "Invoice_2024-12-15.pdf" }
  ]
}
POST /undo

Description: Revert the last action.
Response:
{ "status": "success", "message": "Last action undone" }
Key Considerations
Performance: Optimize file operations for large batches.
Security: Encrypt data in transit and ensure file access is restricted.
Scalability: Use serverless architecture to handle traffic spikes.
Final Note for Claude
Claude, generate code snippets for:

Parsing natural language rules with Gemini APIs.
Processing file renaming and moving actions.
Frontend drag-and-drop file handling using React.