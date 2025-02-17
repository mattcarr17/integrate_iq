import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify

PROBLEMS_FILE = '../problems.json'

def create_app():

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('pages/index.html')
    
    @app.route('/submit-problem', methods=['POST'])
    def submit_problem():

        try:
            problem_data = request.get_json()

            if not problem_data:
                return jsonify({'error': 'No data provided'}), 400
            
            # Add timestamp to the problem data
            problem_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Initialize problems list
            problems = []
            
            # Try to read existing problems if file exists
            if os.path.exists(PROBLEMS_FILE):
                try:
                    with open(PROBLEMS_FILE, 'r') as f:
                        problems = json.load(f)
                except json.JSONDecodeError:
                    # If file is empty or invalid JSON, start with empty list
                    problems = []
            
            # Add new problem
            problems.append(problem_data)
            
            try:
                # Write back all problems
                with open(PROBLEMS_FILE, 'w') as f:
                    json.dump(problems, f, indent=4)
            except IOError as e:
                return jsonify({'error': f'Failed to write to file: {str(e)}'}), 500
            
            return jsonify({'message': 'Problem saved successfully'}), 200
        
        except:
            print('Error')

        
    return app
