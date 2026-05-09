"""
EDGE NODE: Generates votes and sends to Supabase
Much simpler than GCP version!
"""

import requests
import uuid
import random
import time
import json

# ===== CHANGE THESE =====
SUPABASE_URL = "https://aafcpirqawxeamvadhha.supabase.co"  # From Supabase dashboard
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFhZmNwaXJxYXd4ZWFtdmFkaGhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyOTE0OTMsImV4cCI6MjA5Mzg2NzQ5M30.4djgLTbidP3NGse2t62whVMTLwCTLhAWJBfStX1B8yk"  # From Supabase dashboard
EDGE_ID = "node-1"  # Change to node-2, node-3, etc for each group member
# ========================

class VotingClient:
    def __init__(self, url, key, edge_id):
        self.url = url
        self.key = key
        self.edge_id = edge_id
        self.api_url = f"{url}/rest/v1/votes"
        self.headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "apikey": key
        }
        self.vote_count = 0
    
    def generate_vote(self):
        """Create a fake vote"""
        return {
            "user_id": str(uuid.uuid4()),
            "poll_id": "poll_1",
            "choice": random.choice(["A", "B", "C"]),
            "timestamp": int(time.time() * 1000),  # Milliseconds
            "edge_id": self.edge_id
        }
    
    def send_vote(self, vote):
        """Send vote to Supabase (with retry)"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    json=vote,
                    headers=self.headers,
                    timeout=5
                )
                
                if response.status_code in [200, 201]:
                    self.vote_count += 1
                    print(f"✓ Vote #{self.vote_count} | {self.edge_id} | Choice: {vote['choice']}")
                    return True
                else:
                    print(f"⚠️  Attempt {attempt+1}: Status {response.status_code}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Attempt {attempt+1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        
        print(f"✗ Failed to send vote after {max_retries} attempts")
        return False
    
    def run(self):
        """Continuously generate and send votes"""
        print(f"🚀 Edge Node {self.edge_id} starting...")
        print(f"   Supabase: {self.url}\n")
        
        try:
            while True:
                vote = self.generate_vote()
                self.send_vote(vote)
                
                # Random delay between votes (1-3 seconds)
                delay = random.uniform(1, 3)
                time.sleep(delay)
        
        except KeyboardInterrupt:
            print(f"\n\n📊 Edge node stopped.")
            print(f"   Total votes sent: {self.vote_count}")

if __name__ == "__main__":
    if SUPABASE_URL == "https://xxxxx.supabase.co":
        print("❌ ERROR: Replace SUPABASE_URL and SUPABASE_ANON_KEY!")
        print("   Get them from: Supabase Dashboard → Settings → API")
    else:
        client = VotingClient(SUPABASE_URL, SUPABASE_ANON_KEY, EDGE_ID)
        client.run()