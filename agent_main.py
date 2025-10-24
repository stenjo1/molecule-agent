import os
import json
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from tools import DockingTool, KnowledgeTool

load_dotenv()

@function_tool
def compute_docking_scores(molecules: str, target: str) -> str:
    """Compute docking scores for molecules against a target protein. Input molecules as comma-separated SMILES."""
    docking_tool = DockingTool()
    molecule_list = [mol.strip() for mol in molecules.split(',')]
    scores = docking_tool.compute_scores(molecule_list, target_name=target)
    return json.dumps(scores, indent=2)

@function_tool
def get_knowledge_response(question: str) -> str:
    """Get knowledge-based response about molecular docking, targets, or processes."""
    knowledge_tool = KnowledgeTool()
    return knowledge_tool.answer_general_question(question)

@function_tool
def get_target_info(target_id: str) -> str:
    """Get detailed information about a protein target."""
    knowledge_tool = KnowledgeTool()
    info = knowledge_tool.get_target_info(target_id)
    return json.dumps(info, indent=2)

@function_tool
def analyze_docking_results(scores_json: str, target: str) -> str:
    """Analyze docking results and provide insights. Input scores as JSON string."""
    knowledge_tool = KnowledgeTool()
    try:
        results = json.loads(scores_json)
        insights = knowledge_tool.get_analysis_insights(results, target)
        return "\n".join(insights)
    except json.JSONDecodeError:
        return "Error: Invalid JSON format for scores"

class MolecularAgent:
    """Agent for molecular docking and analysis using OpenAI Agents SDK"""
    
    def __init__(self):
        self.client = OpenAI()
        
        self.agent = Agent(
            name="Molecular Docking Expert",
            instructions="""You are a computational chemistry expert specializing in molecular docking and drug discovery. 

Your capabilities:
- Extract SMILES molecules and protein targets from user queries
- Compute docking scores using AutoDock Vina
- Interpret binding affinities and provide scientific insights
- Explain molecular docking processes and drug discovery concepts
- Rank compounds by binding affinity
- Provide recommendations for drug development

Key knowledge about docking scores:
- Docking scores represent binding free energy in kcal/mol
- More negative scores indicate stronger binding (better affinity)
- Typical range: -2 to -15 kcal/mol (stronger binding = more negative)
- Scores below -6 kcal/mol are generally considered promising hits
- Scores below -8 kcal/mol are considered strong binders
- Differences of 1-2 kcal/mol can be significant (10-fold difference in binding)

When processing queries:
1. Extract molecules (SMILES) and target from the query
2. Check cache for existing scores first
3. Compute missing scores if needed
4. Analyze and interpret results
5. Provide clear, scientific rationale for rankings
6. Suggest next steps for promising compounds

Always provide clear, scientific explanations and practical implications.""",
            tools=[
                compute_docking_scores,
                get_knowledge_response,
                get_target_info,
                analyze_docking_results
            ],
            model="gpt-4.1-nano"
        )
    
    def process_query(self, query: str) -> str:
        """Process user queries through the OpenAI Agents SDK"""
        
        print(f"Processing query: {query}")
        
        try:
            result = Runner.run_sync(self.agent, query)
            return result.final_output
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return f"I encountered an error processing your query: {e}. Please try rephrasing your question."