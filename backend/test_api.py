"""
Quick script to test the RAG API endpoints.
Make sure the server is running first: uvicorn app.main:app --reload
"""

import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("=" * 80)
    print("Testing Health Endpoint")
    print("=" * 80)
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_patterns():
    """Test patterns listing endpoint."""
    print("=" * 80)
    print("Testing Patterns Endpoint")
    print("=" * 80)
    response = requests.get(f"{API_URL}/patterns")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total Patterns: {data.get('count', 0)}")
    print(f"Patterns: {', '.join(data.get('patterns', [])[:5])}...\n")

def test_analyze(story: str):
    """Test the analyze endpoint with RAG."""
    print("=" * 80)
    print("Testing RAG Analysis Endpoint")
    print("=" * 80)
    print(f"User Story:\n{story}\n")

    response = requests.post(
        f"{API_URL}/analyze",
        json={"content": story},
        headers={"Content-Type": "application/json"}
    )

    print(f"Status: {response.status_code}\n")

    if response.status_code == 200:
        result = response.json()

        print("📊 Patterns Detected:")
        print(f"   {', '.join(result.get('patterns_detected', []))}\n")

        print("💬 AI Response:")
        print("-" * 80)
        print(result.get('content', 'No content'))
        print("-" * 80)

        findings = result.get('findings', [])
        if findings:
            print(f"\n🎯 Findings ({len(findings)}):")
            for i, finding in enumerate(findings, 1):
                icon = "🔴" if finding['type'] == "danger" else "🟡" if finding['type'] == "warning" else "🔵"
                print(f"\n{icon} [{finding['type'].upper()}] {finding['title']}")
                print(f"   {finding['description']}")
                if finding.get('matched_pattern'):
                    print(f"   Pattern: {finding['matched_pattern']}")
    else:
        print(f"Error: {response.text}")

# Test cases
TEST_STORIES = [
    {
        "name": "Control and Superiority",
        "story": "My partner always needs to be right about everything. When I share my opinion, he talks over me or dismisses what I say. He uses a patronizing tone and acts like I'm stupid. If I get upset, he says I'm being too sensitive and can't handle his honesty. Nothing I do is ever good enough."
    },
    {
        "name": "Charming to Controlling",
        "story": "He was so charming at first and made me feel special. But now he isolates me from my friends, checks my phone constantly, and gets angry when I don't do exactly what he wants. He says he loves me but I feel like I'm walking on eggshells."
    },
    {
        "name": "Gaslighting",
        "story": "He constantly denies things he said or did. When I bring up something hurtful, he says it never happened or that I'm remembering it wrong. Now I question my own memory and feel like I'm going crazy."
    }
]

if __name__ == "__main__":
    print("\n🚀 FIA RAG API Test Suite\n")

    try:
        # Test 1: Health check
        test_health()

        # Test 2: List patterns
        test_patterns()

        # Test 3: Analyze stories
        for i, test in enumerate(TEST_STORIES, 1):
            print(f"\n{'='*80}")
            print(f"Test Case {i}: {test['name']}")
            print(f"{'='*80}\n")
            test_analyze(test['story'])

            if i < len(TEST_STORIES):
                input("\nPress Enter to continue to next test case...")

        print("\n" + "=" * 80)
        print("✅ All tests completed!")
        print("=" * 80)

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Make sure the server is running:")
        print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
