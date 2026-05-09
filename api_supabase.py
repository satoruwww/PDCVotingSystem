"""
OPTIONAL API WRAPPER: Validates votes before storing in Supabase
This layer is optional but good for understanding request validation.
Deploy to Replit, Render, or local Flask if you want to learn.
For the lab, you can skip this and go directly edge → Supabase.
"""

from flask import Flask, request, jsonify
from supabase import create_client, Client
import os

app = Flask(__name__)

# Initialize Supabase client
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/vote", methods=["POST"])
def receive_vote():
    """
    Validates and stores a vote in Supabase
    """
    try:
        vote = request.get_json()
        
        # Validate required fields
        if not vote or not all(k in vote for k in ["user_id", "poll_id", "choice"]):
            return {"error": "Invalid vote format"}, 400
        
        # Validate choice is valid
        if vote.get("choice") not in ["A", "B", "C"]:
            return {"error": "Invalid choice"}, 400
        
        # Insert into Supabase
        response = supabase.table("votes").insert(vote).execute()
        
        print(f"✓ Vote stored: {vote['user_id'][:8]}...")
        return {"status": "accepted", "id": response.data[0]["id"]}, 201
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return {"error": str(e)}, 500

@app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)