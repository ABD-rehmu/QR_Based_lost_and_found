from fastapi.testclient import TestClient
from app.main import app

def run_tests():
    client = TestClient(app)

    # 1. Health check
    res = client.get('/health')
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("PASS: Health check (/health)")

    # 2. Get items
    res = client.get('/api/items')
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 5
    print(f"PASS: Loaded {len(items)} registered items with active QR tags")

    # 3. Test Public Finder scan endpoint (/t/{token}) and API (/api/tag/{token})
    client.post('/api/items/item_01/mark-lost')
    html_res = client.get('/t/cpt_macbook88a')
    assert html_res.status_code == 200
    assert 'CampusTag Return' in html_res.text

    api_res = client.get('/api/tag/cpt_macbook88a')
    assert api_res.status_code == 200
    tag_data = api_res.json()
    assert tag_data['is_lost'] is True
    print(f"PASS: Public QR Scan -> Item '{tag_data['name']}' (Reported Lost: {tag_data['is_lost']})")

    # 4. Test Finder Action Submission
    res = client.post('/api/finder-action/cpt_macbook88a', json={
        "action_type": "drop_desk",
        "current_location": "Main Security Gate",
        "location_notes": "Handed to Guard on Duty"
    })
    assert res.status_code == 200
    print(f"PASS: Finder Action Submission -> {res.json()['message']}")

    # 5. Test Instant Match Engine
    res = client.get('/api/matches')
    assert res.status_code == 200
    matches = res.json()
    assert len(matches) >= 1
    top_match = matches[0]
    print(f"PASS: Instant Match Engine -> Score: {top_match['score']}% ({top_match['confidence']} confidence)")

    # 6. Test Anti-Fraud Claim Verification & OTP Generation
    res = client.post('/api/claims/initiate', json={
        "match_id": top_match['id'],
        "lost_report_id": top_match['lost_report']['id'],
        "found_report_id": top_match['found_report']['id'],
        "claimant_id": "usr_sanis",
        "claimant_name": "Sanis Sharma"
    })
    assert res.status_code == 200
    claim_init = res.json()
    claim_id = claim_init['claim_id']
    print(f"PASS: Claim Initiated -> ID: {claim_id}, Question: '{claim_init['verification_question']}'")

    # Submit verification answer
    res = client.post('/api/claims/verify', json={
        "claim_id": claim_id,
        "claimant_id": "usr_sanis",
        "answer": "GitHub Octocat"
    })
    assert res.status_code == 200
    claim_verif = res.json()
    assert claim_verif['success'] is True
    otp = claim_verif['otp_code']
    print(f"PASS: Verification Passed -> Issued Handover OTP: {otp}")

    # Complete handover at security desk with OTP
    res = client.post('/api/claims/handover-verify', json={
        "claim_id": claim_id,
        "entered_otp": otp,
        "verifier_id": "usr_security",
        "verifier_role": "security",
        "staff_id_confirmed": "SEC-DESK-01",
        "notes": "Verified student ID card. Handed over."
    })
    assert res.status_code == 200
    assert res.json()['success'] is True
    print(f"PASS: Handover Complete with OTP -> Status: {res.json()['status']}")

    # 7. Test Admin Analytics
    res = client.get('/api/admin/analytics')
    assert res.status_code == 200
    analytics = res.json()
    print(f"PASS: Admin Analytics -> Recovery Rate: {analytics['kpis']['recovery_rate_pct']}%, Returned count: {analytics['kpis']['successfully_returned']}")

    # 8. Test Web Pages & Manifest
    assert client.get('/').status_code == 200
    assert client.get('/print-sheet').status_code == 200
    assert client.get('/manifest.json').status_code == 200
    assert client.get('/sw.js').status_code == 200
    print("PASS: PWA shell, Print Sheet, Manifest, and Service Worker loaded")

    print("\n" + "="*50)
    print(" [SUCCESS] 100% OF END-TO-END PRD ACCEPTANCE TESTS PASSED!")
    print("="*50 + "\n")

if __name__ == '__main__':
    run_tests()
