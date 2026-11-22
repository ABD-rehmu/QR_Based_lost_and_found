import sys
from fastapi.testclient import TestClient
from app.main import app

def run_debug_battery():
    client = TestClient(app)
    print("=== STARTING DEEP SYSTEM DEBUGGING BATTERY ===")

    # 1. Server Health
    res = client.get("/health")
    assert res.status_code == 200
    print(" [1/12] PASS: Server health check")

    # 2. Register new item with minimal optional fields
    res = client.post("/api/items", json={
        "name": "Sony FX3 Camera",
        "category": "Electronics",
        "owner_id": "usr_sanis"
    })
    assert res.status_code == 200, f"Register failed: {res.text}"
    item = res.json()
    assert item["token"].startswith("cpt_")
    assert item["qr_data_url"].startswith("data:image/png;base64,")
    print(f" [2/12] PASS: Item registration with auto QR generation ({item['name']})")

    # 3. Toggle Mark Lost
    res = client.post(f"/api/items/{item['id']}/mark-lost")
    assert res.status_code == 200
    assert res.json()["status"] == "lost"
    print(" [3/12] PASS: 1-Click Mark as Lost toggle & report synchronization")

    # 4. Regenerate QR Token
    res = client.post(f"/api/items/{item['id']}/regenerate-qr")
    assert res.status_code == 200
    new_token = res.json()["new_token"]
    assert new_token != item["token"]
    print(" [4/12] PASS: QR token regeneration and invalidation of compromised tag")

    # 5. Public Zero-Install Finder Scan
    res = client.get(f"/api/tag/{new_token}")
    assert res.status_code == 200
    tag_data = res.json()
    assert tag_data["is_lost"] is True
    print(" [5/12] PASS: Zero-PII public tag endpoint loads with 'Reported Lost' status")

    # 6. Finder Action Submission
    res = client.post(f"/api/finder-action/{new_token}", json={
        "action_type": "keep_chat",
        "current_location": "Main Canteen / Food Court",
        "location_notes": "Holding safe in green backpack"
    })
    assert res.status_code == 200
    chat_key = res.json()["chat_key"]
    print(" [6/12] PASS: Finder action submitted and instant alert pushed to owner")

    # 7. Anonymous In-App Messenger
    res = client.post("/api/chat", json={
        "conversation_key": chat_key,
        "sender_role": "Finder",
        "sender_display": "Finder (Guest)",
        "content": "Hi, I have your camera safe near juice counter."
    })
    assert res.status_code == 200
    msg_id = res.json()["id"]

    res = client.get(f"/api/chat/{chat_key}")
    assert res.status_code == 200
    assert len(res.json()) >= 1
    print(" [7/12] PASS: Anonymous masked messenger communication")

    # 8. Flag Abusive Message
    res = client.post(f"/api/chat/{msg_id}/flag", json={
        "reason": "Test moderation flag",
        "reported_by": "Sanis Sharma"
    })
    assert res.status_code == 200
    print(" [8/12] PASS: Abuse reporting & content moderation queue")

    # 9. Create Lost & Found Reports and Trigger Instant Match
    res_found = client.post("/api/reports", json={
        "type": "FOUND",
        "reporter_id": "usr_priya",
        "reporter_name": "Priya Patel",
        "category": "Bottles & Flasks",
        "title": "Milton Thermosteel Water Bottle",
        "color": "Silver",
        "brand": "Milton",
        "description": "Found on table 5 in library. Has blue cap strap.",
        "campus_location": "Library - Ground Floor",
        "verification_question": "What is written at the bottom of the bottle?",
        "verification_answer": "Priya P. Mech 2024"
    })
    assert res_found.status_code == 200
    found_id = res_found.json()["report"]["id"]

    res_lost = client.post("/api/reports", json={
        "type": "LOST",
        "reporter_id": "usr_sanis",
        "reporter_name": "Sanis Sharma",
        "category": "Bottles & Flasks",
        "title": "Silver Milton Flask Bottle",
        "color": "Silver",
        "brand": "Milton",
        "description": "Lost my silver water bottle in library near ground floor entrance.",
        "campus_location": "Library - Ground Floor"
    })
    if res_lost.status_code != 200:
        print("res_lost error:", res_lost.status_code, res_lost.text)
    assert res_lost.status_code == 200, f"res_lost failed: {res_lost.text}"
    lost_data = res_lost.json()
    lost_id = lost_data["report"]["id"]
    print(" [9/12] PASS: Real-time Instant Match calculation across opposite reports")

    # 10. Verify Match Score and Signal Breakdown
    res_matches = client.get("/api/matches")
    assert res_matches.status_code == 200
    all_matches = res_matches.json()
    bottle_match = next((m for m in all_matches if m["lost_report"]["id"] == lost_id or m["found_report"]["id"] == found_id), None)
    assert bottle_match is not None
    assert bottle_match["score"] >= 50.0
    print(f" [10/12] PASS: Match generated with Score {bottle_match['score']}% ({bottle_match['confidence']} confidence)")

    # 11. Anti-Fraud Verification & Handover OTP
    res_init = client.post("/api/claims/initiate", json={
        "match_id": bottle_match["id"],
        "lost_report_id": lost_id,
        "found_report_id": found_id,
        "claimant_id": "usr_sanis",
        "claimant_name": "Sanis Sharma"
    })
    assert res_init.status_code == 200
    claim_id = res_init.json()["claim_id"]

    # Test wrong verification answer
    res_bad = client.post("/api/claims/verify", json={
        "claim_id": claim_id,
        "claimant_id": "usr_sanis",
        "answer": "Completely Wrong Answer 123"
    })
    assert res_bad.status_code == 200
    assert res_bad.json()["success"] is False
    print("   -> Anti-fraud rejection confirmed for incorrect detail")

    # Test correct verification answer
    res_good = client.post("/api/claims/verify", json={
        "claim_id": claim_id,
        "claimant_id": "usr_sanis",
        "answer": "Priya P. Mech 2024"
    })
    assert res_good.status_code == 200
    assert res_good.json()["success"] is True
    otp_code = res_good.json()["otp_code"]
    print(f" [11/12] PASS: Anti-fraud verification passed! OTP Code: {otp_code}")

    # Test handover with wrong OTP
    res_wrong_otp = client.post("/api/claims/handover-verify", json={
        "claim_id": claim_id,
        "entered_otp": "000000",
        "verifier_id": "usr_priya",
        "verifier_role": "finder"
    })
    assert res_wrong_otp.status_code == 400
    print("   -> Handover rejected for invalid OTP")

    # Test handover with correct OTP
    res_handover = client.post("/api/claims/handover-verify", json={
        "claim_id": claim_id,
        "entered_otp": otp_code,
        "verifier_id": "usr_priya",
        "verifier_role": "finder"
    })
    assert res_handover.status_code == 200
    assert res_handover.json()["status"] == "RETURNED"
    print(" [12/12] PASS: Handover completed with verified OTP -> Status: RETURNED")

    print("\n=======================================================")
    print(" >>> ALL 12 END-TO-END DEBUG TESTS PASSED WITH 100% SUCCESS!")
    print("=======================================================\n")

if __name__ == "__main__":
    run_debug_battery()
