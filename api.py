from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import asyncio
import threading
import os
from agent_main import MolecularAgent

app = Flask(__name__, static_folder='static')
CORS(app)  

agent = MolecularAgent()

def run_in_thread(query):
    """Run the agent query in a separate thread with its own event loop"""
    def run_query():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return agent.process_query(query)
        finally:
            loop.close()
    
    # Run in thread
    result = [None]
    thread = threading.Thread(target=lambda: result.__setitem__(0, run_query()))
    thread.start()
    thread.join()
    return result[0]

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process user queries through the molecular agent"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        response = run_in_thread(query)
        
        return jsonify({
            'response': response,
            'query': query,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Molecular Agent API is running'})

@app.route('/')
def serve_frontend():
    """Serve the main frontend page"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    print("Starting Molecular Agent API...")
    print("Available endpoints:")
    print("  GET  / - Frontend interface")
    print("  POST /api/query - Process molecular queries")
    print("  GET  /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5005)
