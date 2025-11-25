"""
Test script with multiple real-world queries to validate RAG system.

This script tests the vector search and RAG analysis with various
manipulation pattern scenarios.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.vector_store import vector_store
from app.rag_chain import rag_chain


# Test cases covering different manipulation patterns
TEST_CASES = [
    {
        "name": "Control and Superiority",
        "query": "My partner always needs to be right about everything. When I share my opinion, he talks over me or dismisses what I say. He uses a patronizing tone and acts like I'm stupid. If I get upset, he says I'm being too sensitive and can't handle his honesty.",
        "expected_patterns": ["Mr. Always Right", "The Critic", "Emotional Invalidator"]
    },
    {
        "name": "Charming Manipulation",
        "query": "He was so charming and sweet at first, made me feel like the most special person. But now he isolates me from my friends, checks my phone constantly, and gets angry when I don't do exactly what he wants. He says he loves me but I feel like I'm walking on eggshells.",
        "expected_patterns": ["Emotional Predator, Puppet Master, The Svengali", "The Charmer", "Dr. Jekyll/Mr. Hyde"]
    },
    {
        "name": "Hot and Cold Behavior",
        "query": "One day he's the most loving partner, the next day he's cold and distant. I never know which version I'm going to get. When he's upset, he completely shuts down and gives me the silent treatment for days.",
        "expected_patterns": ["Dr. Jekyll/Mr. Hyde", "The Water Torturer", "Emotionally Unavailable Man"]
    },
    {
        "name": "Guilt-Tripping",
        "query": "Whenever I try to set boundaries or do something for myself, he makes me feel guilty. He says things like 'after all I've done for you' or 'you're being selfish.' I end up apologizing even when I did nothing wrong.",
        "expected_patterns": ["The Player", "Emotional Predator", "The Demand Man"]
    },
    {
        "name": "Isolation Tactics",
        "query": "He doesn't like my friends and always finds reasons why I shouldn't hang out with them. He says they're a bad influence or that they don't really care about me. Now I barely see anyone except him.",
        "expected_patterns": ["Emotional Predator, Puppet Master, The Svengali", "The Terrorist", "The Rambo, The Iron Fist"]
    },
    {
        "name": "Gaslighting Reality",
        "query": "He constantly denies things he said or did. When I bring up something hurtful, he says it never happened or that I'm remembering it wrong. Now I question my own memory and feel like I'm going crazy.",
        "expected_patterns": ["Emotional Predator, Puppet Master, The Svengali", "Man with a Hidden Life", "The Sensitive Guy"]
    },
    {
        "name": "Love Bombing to Devaluation",
        "query": "At the beginning, he showered me with gifts, attention, and promises of an amazing future together. He talked about marriage and kids after just a few weeks. Now, months later, nothing I do is good enough and he criticizes everything about me.",
        "expected_patterns": ["Emotional Predator, Puppet Master, The Svengali", "The Seducer", "Narcissistic"]
    },
    {
        "name": "Financial Control",
        "query": "He controls all our money and gets angry if I spend anything without asking him first. He says I'm bad with money and can't be trusted. I have to account for every dollar I spend.",
        "expected_patterns": ["The Demand Man", "Mr. Always Right", "The Drill Sergeant"]
    },
    {
        "name": "Commitment Avoidance",
        "query": "We've been together for two years but he still won't commit. He says he loves me but isn't ready for labels. Every time I bring up the future, he changes the subject or gets defensive. Meanwhile, he acts like my boyfriend in private but won't introduce me to anyone.",
        "expected_patterns": ["Mr. Unavailable", "The Freewheeler", "The Player"]
    },
    {
        "name": "Passive Aggressive Behavior",
        "query": "He never directly confronts issues. Instead, he gives me the silent treatment, makes sarcastic comments, or 'forgets' to do things he promised. When I ask what's wrong, he says 'nothing' but clearly something is bothering him.",
        "expected_patterns": ["The Passive Aggressive", "The Water Torturer", "The Sensitive Guy"]
    },
    {
        "name": "Always the Victim",
        "query": "No matter what happens, he's always the victim. If I'm upset about something he did, he turns it around and makes it about how I'm hurting him. He uses his past trauma to excuse his bad behavior and make me feel sorry for him.",
        "expected_patterns": ["The Perpetual Victim", "The Sensitive Guy", "Mommy Seeker"]
    },
    {
        "name": "Constant Criticism",
        "query": "He nitpicks everything - how I dress, how I talk, my weight, my job, my family. Nothing is ever good enough. He says he's just trying to help me be better, but I feel worse about myself every day.",
        "expected_patterns": ["The Nitpicker", "The Critic", "Mr. Always Right"]
    },
    {
        "name": "Jealousy and Possessiveness",
        "query": "He gets jealous if I even talk to another guy. He accuses me of flirting when I'm just being friendly. He wants to know where I am all the time and gets upset if I don't respond to his texts immediately.",
        "expected_patterns": ["The Terrorist", "The Clinger", "Emotional Predator, Puppet Master, The Svengali"]
    },
    {
        "name": "Substance Abuse Issues",
        "query": "When he drinks, he becomes a different person - angry, mean, unpredictable. He promises to stop but keeps drinking. He blames his behavior on the alcohol and says it's not really him.",
        "expected_patterns": ["The Addict", "Dr. Jekyll/Mr. Hyde", "The Rambo, The Iron Fist"]
    },
    {
        "name": "Never Takes Responsibility",
        "query": "He never admits when he's wrong. Everything is always someone else's fault - mine, his boss, his family, the world. He never apologizes genuinely, and if he does say sorry, it's always followed by 'but you...'",
        "expected_patterns": ["Mr. Always Right", "The Perpetual Victim", "Narcissistic"]
    }
]


def test_vector_search_only():
    """Test just the vector search without full RAG."""
    print("=" * 100)
    print(" VECTOR SEARCH TEST - Finding Similar Patterns")
    print("=" * 100)

    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n{'─' * 100}")
        print(f"Test {i}: {test['name']}")
        print(f"{'─' * 100}")
        print(f"Query: {test['query'][:150]}...")

        # Search for top 3 matches
        results = vector_store.similarity_search_with_score(test['query'], k=3)

        print(f"\nTop 3 Matches:")
        for j, (doc, score) in enumerate(results, 1):
            player_type = doc.metadata.get('player_type', 'N/A')
            category = doc.metadata.get('category', 'Unknown')
            similarity = 1 - score  # Convert distance to similarity

            print(f"  {j}. {player_type} (category: {category}, similarity: {similarity:.3f})")

        # Check if expected patterns were found
        found_patterns = [doc.metadata.get('player_type', '') for doc, _ in results]
        expected = test.get('expected_patterns', [])

        matches = [p for p in expected if any(p in fp for fp in found_patterns)]
        if matches:
            print(f"\n✅ Found expected patterns: {', '.join(matches)}")
        else:
            print(f"\n⚠️  Expected: {', '.join(expected)}")
            print(f"   Got: {', '.join(found_patterns)}")


def test_full_rag_analysis(test_case_index: int = 0):
    """Test full RAG analysis with GPT-4 for one test case."""
    if test_case_index >= len(TEST_CASES):
        print(f"Invalid test case index. Max: {len(TEST_CASES) - 1}")
        return

    test = TEST_CASES[test_case_index]

    print("=" * 100)
    print(f" FULL RAG ANALYSIS TEST - {test['name']}")
    print("=" * 100)

    print(f"\nUser Story:")
    print(f"{test['query']}\n")

    print("Analyzing with RAG system (this will call GPT-4)...")
    print("-" * 100)

    try:
        result = rag_chain.get_analysis(test['query'])

        print(f"\n📊 Patterns Detected: {', '.join(result.patterns_detected)}")
        print(f"\n💬 AI Response:")
        print("-" * 100)
        print(result.content)
        print("-" * 100)

        if result.findings:
            print(f"\n🎯 Structured Findings ({len(result.findings)}):")
            for i, finding in enumerate(result.findings, 1):
                icon = "🔴" if finding.type == "danger" else "🟡" if finding.type == "warning" else "🔵"
                print(f"\n{icon} [{finding.type.upper()}] {finding.title}")
                print(f"   {finding.description}")
                if finding.matched_pattern:
                    print(f"   Pattern: {finding.matched_pattern}")

    except Exception as e:
        print(f"\n❌ Error during RAG analysis: {e}")
        import traceback
        traceback.print_exc()


def interactive_menu():
    """Interactive menu for testing."""
    print("\n" + "=" * 100)
    print(" FIA RAG System - Test Menu")
    print("=" * 100)

    while True:
        print("\n\nOptions:")
        print("1. Run all vector search tests (fast, no GPT-4 calls)")
        print("2. Run full RAG analysis on one test case (uses GPT-4)")
        print("3. List all test cases")
        print("4. Custom query (vector search)")
        print("5. Custom query (full RAG analysis)")
        print("6. Exit")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            test_vector_search_only()

        elif choice == "2":
            print("\nAvailable test cases:")
            for i, test in enumerate(TEST_CASES):
                print(f"  {i}. {test['name']}")
            try:
                idx = int(input(f"\nEnter test case number (0-{len(TEST_CASES)-1}): "))
                test_full_rag_analysis(idx)
            except ValueError:
                print("Invalid input")

        elif choice == "3":
            print("\n📋 All Test Cases:")
            for i, test in enumerate(TEST_CASES):
                print(f"\n{i}. {test['name']}")
                print(f"   Query: {test['query'][:100]}...")
                print(f"   Expected: {', '.join(test['expected_patterns'])}")

        elif choice == "4":
            query = input("\nEnter your query: ").strip()
            if query:
                results = vector_store.similarity_search_with_score(query, k=5)
                print(f"\nTop 5 matches:")
                for i, (doc, score) in enumerate(results, 1):
                    player_type = doc.metadata.get('player_type', 'Unknown')
                    print(f"  {i}. {player_type} (similarity: {1-score:.3f})")

        elif choice == "5":
            query = input("\nEnter your query: ").strip()
            if query:
                print("\nAnalyzing with RAG system...")
                try:
                    result = rag_chain.get_analysis(query)
                    print(f"\nPatterns: {', '.join(result.patterns_detected)}")
                    print(f"\n{result.content}")
                except Exception as e:
                    print(f"Error: {e}")

        elif choice == "6":
            print("\nExiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    print("Initializing RAG system...")

    try:
        # Initialize vector store
        vector_store.initialize()
        print("✓ Vector store initialized\n")

        # Check if data exists
        test_results = vector_store.similarity_search("test", k=1)
        if not test_results:
            print("⚠️  WARNING: No data found in vector store!")
            print("Please run the ingestion script first:")
            print("  python scripts/ingest_data.py --clear")
            sys.exit(1)

        print(f"✓ Found data in database ({len(TEST_CASES)} test cases ready)\n")

        # Run interactive menu
        interactive_menu()

    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
