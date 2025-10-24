import json
import os

class KnowledgeTool:
    """Tool for providing domain knowledge and explanations"""
    
    def __init__(self, knowledge_file="data/docking_knowledge.json"):
        self.knowledge_file = knowledge_file
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load knowledge base from JSON file"""
        if not os.path.exists(self.knowledge_file):
            print(f"Warning: Knowledge file {self.knowledge_file} not found, using empty knowledge base")
            return {}
        
        try:
            with open(self.knowledge_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return {}
    
    def get_score_interpretation(self, score):
        """Interpret docking score and provide detailed analysis"""
        if score < -8.0:
            category = "excellent"
        elif score < -6.0:
            category = "good"
        elif score < -4.0:
            category = "moderate"
        else:
            category = "weak"
        
        interpretation = self.knowledge_base.get("docking_scores", {}).get(category, {})
        return {
            "score": score,
            "category": category,
            "range": interpretation.get("range", "Unknown"),
            "description": interpretation.get("description", "No description available"),
            "recommendation": interpretation.get("recommendation", "No specific recommendation available")
        }
    
    def get_target_info(self, target_id):
        """Get comprehensive information about a protein target"""
        targets = self.knowledge_base.get("targets", {})
        target_info = targets.get(target_id, {
            "name": f"Unknown target {target_id}",
            "description": "No information available",
            "drug_examples": [],
            "binding_site": "Unknown",
            "therapeutic_area": "Unknown"
        })
        
        # additional context
        target_info["target_id"] = target_id
        target_info["has_known_drugs"] = len(target_info.get("drug_examples", [])) > 0
        
        return target_info
    
    def explain_process(self, process):
        """Explain a scientific process with detailed information"""
        processes = self.knowledge_base.get("processes", {})
        process_info = processes.get(process.lower())
        
        if not process_info:
            available_processes = list(processes.keys())
            return {
                "error": f"Unknown process: {process}",
                "available_processes": available_processes
            }
        
        return process_info
    
    def get_molecular_property_info(self, property_name):
        """Get information about molecular properties"""
        properties = self.knowledge_base.get("molecular_properties", {})
        return properties.get(property_name.lower(), {
            "error": f"Unknown property: {property_name}",
            "available_properties": list(properties.keys())
        })
    
    def get_analysis_insights(self, results, target=None):
        """Generate comprehensive insights from docking results"""
        insights = []
        
        if not results:
            return ["No results to analyze"]
        
        valid_scores = [score for score in results.values() if score is not None]
        if not valid_scores:
            return ["No valid scores found"]
        
        # basic statistics
        best_score = min(valid_scores)
        worst_score = max(valid_scores)
        avg_score = sum(valid_scores) / len(valid_scores)
        score_range = worst_score - best_score
        
        best_mol = [mol for mol, score in results.items() if score == best_score][0]
        
        insights.append(f"## Analysis Summary")
        insights.append(f"Best binding: {best_mol} ({best_score:.1f} kcal/mol)")
        insights.append(f"Average binding: {avg_score:.1f} kcal/mol")
        insights.append(f"Score range: {score_range:.1f} kcal/mol")
        
        # score distribution analysis
        excellent = [score for score in valid_scores if score < -8.0]
        good = [score for score in valid_scores if -8.0 <= score < -6.0]
        moderate = [score for score in valid_scores if -6.0 <= score < -4.0]
        weak = [score for score in valid_scores if score >= -4.0]
        
        insights.append(f"\n## Binding Affinity Distribution")
        if excellent:
            insights.append(f"• {len(excellent)} compound(s) show excellent binding (< -8.0 kcal/mol)")
        if good:
            insights.append(f"• {len(good)} compound(s) show good binding (-6.0 to -8.0 kcal/mol)")
        if moderate:
            insights.append(f"• {len(moderate)} compound(s) show moderate binding (-4.0 to -6.0 kcal/mol)")
        if weak:
            insights.append(f"• {len(weak)} compound(s) show weak binding (> -4.0 kcal/mol)")
        
        # target-specific insights
        if target:
            target_info = self.get_target_info(target)
            if target_info["has_known_drugs"]:
                insights.append(f"\n## Target Context: {target_info['name']}")
                insights.append(f"Known drugs: {', '.join(target_info['drug_examples'])}")
                insights.append(f"Therapeutic area: {target_info['therapeutic_area']}")
        
        # recommendations
        insights.append(f"\n## Recommendations")
        if excellent:
            insights.append("• High priority: Focus on compounds with excellent binding for lead optimization")
            insights.append("• Consider experimental validation of top compounds")
        elif good:
            insights.append("• Medium priority: Investigate compounds with good binding affinity")
            insights.append("• Consider structural modifications to improve moderate binders")
        else:
            insights.append("• Low priority: All compounds show weak binding")
            insights.append("• Consider different chemical scaffolds or target modifications")
        
        # statistical significance
        if score_range > 2.0:
            insights.append("• Significant differences in binding affinity detected")
            insights.append("• Focus on the best-performing compounds")
        else:
            insights.append("• Similar binding affinities across compounds")
            insights.append("• Consider additional screening criteria")
        
        return insights
    
    def answer_general_question(self, question):
        """Answer general questions about molecular docking and drug discovery"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["docking", "molecular docking"]):
            process_info = self.explain_process("docking")
            if "error" not in process_info:
                return f"**Molecular Docking**\n\n{process_info['description']}\n\n**Steps:**\n" + \
                       "\n".join([f"• {step}" for step in process_info['steps']])
        
        elif any(word in question_lower for word in ["virtual screening", "screening"]):
            process_info = self.explain_process("virtual_screening")
            if "error" not in process_info:
                return f"**Virtual Screening**\n\n{process_info['description']}\n\n**Steps:**\n" + \
                       "\n".join([f"• {step}" for step in process_info['steps']])
        
        elif any(word in question_lower for word in ["drug discovery", "drug development"]):
            process_info = self.explain_process("drug_discovery")
            if "error" not in process_info:
                return f"**Drug Discovery**\n\n{process_info['description']}\n\n**Stages:**\n" + \
                       "\n".join([f"• {stage}" for stage in process_info['stages']]) + \
                       f"\n\n**Timeline:** {process_info['timeline']}"
        
        elif any(word in question_lower for word in ["score", "binding", "affinity"]):
            return """**Docking Score Interpretation:**

• **Excellent binding**: < -8.0 kcal/mol (Very strong binding, potential drug candidate)
• **Good binding**: -6.0 to -8.0 kcal/mol (Good binding affinity, worth further investigation)
• **Moderate binding**: -4.0 to -6.0 kcal/mol (Moderate binding, may need optimization)
• **Weak binding**: > -4.0 kcal/mol (Weak binding, unlikely to be effective)

More negative scores indicate stronger binding affinity. Differences of 1-2 kcal/mol can represent 10-fold differences in binding strength."""
        
        else:
            return """I can help with questions about:

• **Molecular docking** - How docking works and interprets results
• **Virtual screening** - High-throughput compound screening
• **Drug discovery** - The drug development process
• **Binding scores** - Interpreting docking scores and binding affinity
• **Protein targets** - Information about specific targets like F2, 3CLP, etc.
• **Molecular properties** - Drug-likeness and ADMET properties

What would you like to know more about?"""