"""
Script to ingest manipulation pattern data into the vector database.

This script:
1. Reads data from JSON files (Notion exports)
2. Processes and structures the data for player typologies, abuse flavors, trauma, vulnerabilities
3. Creates embeddings and stores in ChromaDB

Usage:
    python scripts/ingest_data.py --clear  # Ingest all data files, clear existing data first
    python scripts/ingest_data.py          # Ingest all data files, append to existing
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.documents import Document
from app.vector_store import vector_store
from app.config import settings


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON data from file."""
    print(f"Loading data from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def process_player_typologies(data: Dict[str, Any]) -> List[Document]:
    """
    Process player typologies data into LangChain documents.

    Each player type gets embedded with comprehensive information including:
    - Name and summary
    - Motivations, red flags, techniques
    - Vulnerability types they target
    - Abuse flavors they use
    """
    documents = []

    player_types = data.get('player_typologies', [])
    print(f"Processing {len(player_types)} player typologies...")

    for player in player_types:
        name = player.get('name', 'Unknown')

        # Skip if no meaningful data
        if not player.get('summary') and not player.get('main_motivation'):
            print(f"  Skipping '{name}' - no summary or motivation data")
            continue

        # Build comprehensive content for embedding
        content_parts = []

        # Main info
        alias = player.get('alias')
        if alias:
            content_parts.append(f"Player Type: {name} (also known as: {alias})")
        else:
            content_parts.append(f"Player Type: {name}")

        summary = player.get('summary')
        if summary:
            content_parts.append(f"\nDescription: {summary}")

        # Motivations
        motivations = player.get('main_motivation', [])
        if motivations and isinstance(motivations, list) and len(motivations) > 0:
            content_parts.append(f"\nMain Motivations: {', '.join(motivations)}")

        # Red flags
        red_flags = player.get('red_flags', [])
        if red_flags and isinstance(red_flags, list):
            # Take first 10 red flags to avoid too much text
            flags_to_show = red_flags[:10] if len(red_flags) > 10 else red_flags
            content_parts.append(f"\nRed Flags: {', '.join(flags_to_show)}")

        # What they always do
        always_does = player.get('always_does_this', [])
        if always_does and isinstance(always_does, list):
            content_parts.append(f"\nConsistent Behaviors: {', '.join(always_does)}")

        # What they never do (opposites)
        never_does = player.get('he_never_does_this', [])
        if never_does and isinstance(never_does, list):
            content_parts.append(f"\nBehaviors They Avoid: {', '.join(never_does)}")

        # Techniques
        techniques = player.get('techniques_he_might_use', [])
        if techniques and isinstance(techniques, list):
            # Take first 10 techniques
            techs_to_show = techniques[:10] if len(techniques) > 10 else techniques
            content_parts.append(f"\nManipulation Techniques: {', '.join(techs_to_show)}")

        # Trauma signs
        trauma = player.get('trauma_signs', [])
        if trauma and isinstance(trauma, list):
            content_parts.append(f"\nTrauma Signs in Victims: {', '.join(trauma)}")

        # Combine content
        content = "\n".join(content_parts)

        # Create metadata for filtering and display
        metadata = {
            "player_type": name,
            "category": "player_typology",
            "source": "notion_export"
        }

        if alias:
            metadata["alias"] = alias

        if motivations:
            metadata["motivations"] = ", ".join(motivations) if isinstance(motivations, list) else str(motivations)

        if always_does:
            metadata["consistent_behaviors"] = ", ".join(always_does[:5]) if isinstance(always_does, list) else str(always_does)

        # Vulnerability types they target
        vuln_types = player.get('vulnerability_types', [])
        if vuln_types and isinstance(vuln_types, list):
            metadata["targets_vulnerability"] = ", ".join(vuln_types)

        # Abuse flavors
        abuse_flavors = player.get('flavors_of_abuse', [])
        if abuse_flavors and isinstance(abuse_flavors, list):
            metadata["abuse_flavors"] = ", ".join(abuse_flavors[:5])

        # Create document
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)
        print(f"  ✓ Processed: {name}")

    return documents


def process_abuse_flavors(data: Any) -> List[Document]:
    """Process abuse flavors/types data."""
    documents = []

    # Handle both list and dict formats
    if isinstance(data, list):
        flavors = data
    else:
        flavors = data.get('flavours_of_abuse', [])

    print(f"Processing {len(flavors)} abuse flavors...")

    for flavor in flavors:
        # Try different key names
        name = flavor.get('Flavor') or flavor.get('flavor') or flavor.get('name', 'Unknown')
        description = flavor.get('description', flavor.get('Description', ''))

        # If no description, create one from player typologies
        if not description:
            player_types = flavor.get('Player typologies', flavor.get('player_typologies', []))
            if player_types:
                description = f"This manipulation flavor is associated with: {', '.join(player_types)}"
            else:
                continue

        content = f"Abuse Flavor: {name}\n\nDescription: {description}"

        metadata = {
            "abuse_flavor": name,
            "category": "abuse_flavor",
            "source": "notion_export"
        }

        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)
        print(f"  ✓ Processed: {name}")

    return documents


def process_trauma_types(data: Any) -> List[Document]:
    """Process trauma types data."""
    documents = []

    # Handle both list and dict formats
    if isinstance(data, list):
        trauma_types = data
    else:
        trauma_types = data.get('trauma', [])

    print(f"Processing {len(trauma_types)} trauma types...")

    for trauma in trauma_types:
        # Try different key names
        name = trauma.get('Name') or trauma.get('name', 'Unknown')
        description = trauma.get('description', trauma.get('Description', ''))

        # If no description, create one from player typologies
        if not description:
            player_types = trauma.get('Player Typologies', trauma.get('player_typologies', []))
            if player_types:
                description = f"This trauma sign is commonly seen with: {', '.join(player_types)}"
            else:
                continue

        content = f"Trauma Sign: {name}\n\nDescription: {description}"

        metadata = {
            "trauma_type": name,
            "category": "trauma",
            "source": "notion_export"
        }

        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)
        print(f"  ✓ Processed: {name}")

    return documents


def process_vulnerability_types(data: Any) -> List[Document]:
    """Process vulnerability types data."""
    documents = []

    # Handle both list and dict formats
    if isinstance(data, list):
        vulnerabilities = data
    else:
        vulnerabilities = data.get('vulnerability_types', [])

    print(f"Processing {len(vulnerabilities)} vulnerability types...")

    for vuln in vulnerabilities:
        name = vuln.get('name', vuln.get('Name', 'Unknown'))
        description = vuln.get('description', vuln.get('Description', ''))

        # Create description from traits if not available
        if not description:
            traits = vuln.get('vulnerability_traits', vuln.get('traits', []))
            if traits and isinstance(traits, list):
                description = f"Common traits: {', '.join(traits[:10])}"  # Limit to 10 traits
            else:
                continue

        content = f"Vulnerability Type: {name}\n\nDescription: {description}"

        # Add traits if available
        traits = vuln.get('vulnerability_traits', vuln.get('traits', []))
        if traits and isinstance(traits, list) and not description.startswith('Common traits'):
            content += f"\n\nCommon Traits: {', '.join(traits[:10])}"

        metadata = {
            "vulnerability_type": name,
            "category": "vulnerability",
            "source": "notion_export"
        }

        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)
        print(f"  ✓ Processed: {name}")

    return documents


def ingest_all_data(data_dir: str, clear_existing: bool = False):
    """Main ingestion function for all data files."""
    print("=" * 80)
    print("FIA Data Ingestion Script - Manipulation Pattern Database")
    print("=" * 80)

    # Initialize vector store
    print("\n[1/4] Initializing vector store...")
    vector_store.initialize()

    # Clear existing data if requested
    if clear_existing:
        print("\n[2/4] Clearing existing data...")
        vector_store.clear()  # clear() now reinitializes automatically
    else:
        print("\n[2/4] Appending to existing data...")

    all_documents = []

    # Process each data file
    print("\n[3/4] Processing data files...")
    data_path = Path(data_dir)

    # Player typologies (main data)
    player_file = data_path / "player_typologies.json"
    if player_file.exists():
        print(f"\n→ Player Typologies ({player_file.name}):")
        data = load_json_file(str(player_file))
        docs = process_player_typologies(data)
        all_documents.extend(docs)
        print(f"  Added {len(docs)} player typology documents")

    # Abuse flavors
    abuse_file = data_path / "flavours_of_abuse.json"
    if abuse_file.exists():
        print(f"\n→ Abuse Flavors ({abuse_file.name}):")
        data = load_json_file(str(abuse_file))
        docs = process_abuse_flavors(data)
        all_documents.extend(docs)
        print(f"  Added {len(docs)} abuse flavor documents")

    # Trauma types
    trauma_file = data_path / "trauma.json"
    if trauma_file.exists():
        print(f"\n→ Trauma Types ({trauma_file.name}):")
        data = load_json_file(str(trauma_file))
        docs = process_trauma_types(data)
        all_documents.extend(docs)
        print(f"  Added {len(docs)} trauma documents")

    # Vulnerability types
    vuln_file = data_path / "vulnerability_types.json"
    if vuln_file.exists():
        print(f"\n→ Vulnerability Types ({vuln_file.name}):")
        data = load_json_file(str(vuln_file))
        docs = process_vulnerability_types(data)
        all_documents.extend(docs)
        print(f"  Added {len(docs)} vulnerability documents")

    # Add all documents to vector store
    print(f"\n[4/4] Adding {len(all_documents)} total documents to vector store...")
    if all_documents:
        vector_store.add_documents(all_documents)
        print("✓ All documents added successfully!")
    else:
        print("⚠ No documents to add!")
        return

    print("\n" + "=" * 80)
    print("Ingestion Complete!")
    print("=" * 80)

    # Test search
    print("\n🔍 Testing search with query: 'My partner says that he is always there for me but then everytime I call him he says he is busy'")
    print("-" * 80)
    results = vector_store.similarity_search("My partner always needs to be right", k=3)
    for i, doc in enumerate(results, 1):
        print(f"\n[Result {i}]")
        print(f"Category: {doc.metadata.get('category', 'Unknown')}")
        print(f"Name: {doc.metadata.get('player_type', doc.metadata.get('abuse_flavor', 'Unknown'))}")
        print(f"Content preview: {doc.page_content[:250]}...")
        print("-" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ingest manipulation pattern data into vector database"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="./data",
        help="Directory containing JSON data files (default: ./data)"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing data before ingesting"
    )

    args = parser.parse_args()

    try:
        ingest_all_data(args.data_dir, clear_existing=args.clear)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
