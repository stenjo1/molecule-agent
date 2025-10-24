from agent_main import MolecularAgent

def main():    
    print("🧬 Molecular Agent Demo (OpenAI Agents SDK)")
    print("=" * 50)
    
    agent = MolecularAgent()
    
    demo_queries = [
        'Rank molecules "CCO", "CCN", "CCC" by docking score against target "HSP90AA1"',
        'What does a docking score of -7.5 mean?',
        'Explain molecular docking',
        'Tell me about target HSP90AA1',
        'Compare "CCO" and "CCN" against HSP90AA1',
        'What is virtual screening?'
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n🔬 Demo Query {i}: {query}")
        print("-" * 50)
        
        try:
            response = agent.process_query(query)
            print(response)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 50)
    
    print("\n✅ Demo completed!")
    print("\nTo use the API server, run: python api.py")
    print("Then visit: http://localhost:5000/api/health")

if __name__ == "__main__":
    main()
