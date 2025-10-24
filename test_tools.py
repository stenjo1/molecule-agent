"""
Test script for individual tools
"""

def test_docking_tool():
    """Test the DockingTool"""
    print("🧬 Testing DockingTool...")
    from tools import DockingTool
    
    docking_tool = DockingTool()
    
    molecules = ["CCO"]
    target = "ACHE"
    
    print(f"Computing scores for {molecules} against {target}")
    scores = docking_tool.compute_scores(molecules, target)
    print(f"Results: {scores}")
    
    print("\nTesting cache hit (should be faster)...")
    scores2 = docking_tool.compute_scores(molecules, target)
    print(f"Cached results: {scores2}")
    
    return scores

def test_knowledge_tool():
    """Test the KnowledgeTool"""
    print("\n📚 Testing KnowledgeTool...")
    from tools import KnowledgeTool
    
    knowledge_tool = KnowledgeTool()
    
    print("Score interpretation for -7.5:")
    interpretation = knowledge_tool.get_score_interpretation(-7.5)
    print(interpretation)
    
    print("\nTarget info for F2:")
    target_info = knowledge_tool.get_target_info("F2")
    print(target_info)
    
    print("\nAnswering general question:")
    answer = knowledge_tool.answer_general_question("What does a docking score of -7.5 mean?")
    print(answer)

def test_agent():
    """Test the full agent"""
    print("\n🤖 Testing MolecularAgent...")
    from agent_main import MolecularAgent
    
    agent = MolecularAgent()
    
    test_queries = [
        'Rank molecules "CCO", "CCN", "CCC" by docking score against target "F2"',
        'What does a docking score of -7.5 mean?',
        'Tell me about target F2'
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test Query {i} ---")
        print(f"Query: {query}")
        try:
            response = agent.process_query(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Run all tests"""
    print("🧪 Molecular Agent System Tests")
    print("=" * 50)
    
    try:
        test_docking_tool()
        test_knowledge_tool()
        
        print("\n" + "=" * 50)
        print("Testing full agent (requires OPENAI_API_KEY)...")
        test_agent()
        
    except Exception as e:
        print(f"Test failed: {e}")
        print("Make sure you have OPENAI_API_KEY set for full agent tests")

if __name__ == "__main__":
    main()
