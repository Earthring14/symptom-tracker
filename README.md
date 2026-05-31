1. Create new virtual environment
python3.12 -m venv venv

2. Activate the virtual environment
macOS/Linux: source venv/bin/activate
Windows: venv\Scripts\activate

3. Install the requirements 
pip install -r requirements.txt

4. Run the application 
uvicorn api.index:app --reload

5. Navigate to the following url
http://127.0.0.1:8000

http://127.0.0.1:8000/docs



