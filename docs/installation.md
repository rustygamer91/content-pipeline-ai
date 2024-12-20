# Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Google Cloud account with Gemini API access
- Git (for cloning the repository)

## Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/content-pipeline-ai
   cd content-pipeline-ai
   ```

2. **Create a Virtual Environment**
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Key**
   ```bash
   # On macOS/Linux
   export GOOGLE_API_KEY='your_api_key_here'

   # On Windows (Command Prompt)
   set GOOGLE_API_KEY=your_api_key_here

   # On Windows (PowerShell)
   $env:GOOGLE_API_KEY='your_api_key_here'
   ```

5. **Verify Installation**
   ```bash
   python content_agent.py
   ```
   You should see the welcome message and menu options.

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```
   Error: GOOGLE_API_KEY environment variable not set
   ```
   Solution: Make sure you've set the environment variable correctly.

2. **Module Not Found**
   ```
   ModuleNotFoundError: No module named 'google.generativeai'
   ```
   Solution: Ensure you're in the virtual environment and have run `pip install -r requirements.txt`

3. **Python Version Error**
   ```
   SyntaxError: invalid syntax
   ```
   Solution: Verify you're using Python 3.7 or higher with `python --version`

### Getting Help

If you encounter any issues:
1. Check the [GitHub Issues](https://github.com/yourusername/content-pipeline-ai/issues)
2. Review the [API Documentation](api.md)
3. Contact the maintainers 