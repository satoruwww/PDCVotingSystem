

import time
from supabase import create_client

SUPABASE_URL = "https://aafcpirqawxeamvadhha.supabase.co"  # From Supabase dashboard
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFhZmNwaXJxYXd4ZWFtdmFkaGhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgyOTE0OTMsImV4cCI6MjA5Mzg2NzQ5M30.4djgLTbidP3NGse2t62whVMTLwCTLhAWJBfStX1B8yk"


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

last_seen_id = 0

print("Listening for new votes...")

while True:
    response = (
        supabase
        .table("votes")
        .select("*")
        .gt("id", last_seen_id)
        .order("id")
        .execute()
    )

    for vote in response.data:
        print("🗳 New vote:", vote)
        last_seen_id = vote["id"]

    time.sleep(2)  # poll every 2 seconds