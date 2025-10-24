# Molecular Docking Agent

A conversational AI agent for molecular docking analysis and virtual screening using OpenAI Agents SDK and Dockstring.

## Overview

This project implements an AI agent that can perform molecular docking calculations, interpret results, and provide scientific insights about drug-target interactions. The agent combines computational chemistry tools with natural language processing to create an interactive interface for virtual screening workflows.

## Setup

### Prerequisites

- Docker and Docker Compose
- OpenAI API key

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd molecule-agent
```

2. Set up environment variables:

```bash
OPENAI_API_KEY="your-openai-api-key"
```

3. Build and run with Docker Compose:

```bash
docker-compose up --build
```

## Running the Demo

### Command Line Demo

```bash
docker-compose run vs-agent-demo
```

This runs a series of predefined queries demonstrating the agent's capabilities:

- Ranking molecules by docking score
- Interpreting binding affinities
- Explaining molecular docking concepts
- Providing target information

### API Server

```bash
docker-compose up vs-agent-api
```

Access the web interface at: http://localhost:5005

### Testing Tools

```bash
docker-compose run vs-agent-test
```

## Tools and Implementation

### Dockstring Integration

The project uses [Dockstring](https://github.com/whitead/dockstring), a Python package that provides standardized molecular docking capabilities. Dockstring offers:

- Pre-configured protein targets (EGFR, HSP90AA1, ACHE, F2, PLK1, ESR1)
- Automated docking workflows using AutoDock Vina
- Consistent scoring and result formats
- Built-in target preparation and binding site definitions

**Current Status**: All scores are cached due to macOS compatibility issues. Real docking can be tested on Linux with the EGFR target which is not cached.

### Knowledge Base

The agent includes a comprehensive knowledge base (`data/docking_knowledge.json`) containing:

- **Docking Score Interpretation**: Ranges and meanings for binding affinities
- **Target Information**: Detailed profiles for each protein target including:
  - Biological function and therapeutic relevance
  - Known drugs and binding sites
  - Therapeutic areas
- **Process Explanations**: Step-by-step descriptions of molecular docking, virtual screening, and drug discovery
- **Molecular Properties**: Drug-likeness criteria and ADMET considerations

### Agent Capabilities

The molecular agent can:

- Extract SMILES molecules and protein targets from natural language queries
- Compute docking scores using Dockstring or fallback to deterministic mock scores
- Interpret binding affinities and provide scientific context
- Rank compounds by binding strength
- Generate comprehensive analysis reports
- Answer questions about drug discovery processes

## Architecture

### Core Components

1. **MolecularAgent** (`agent_main.py`): Main agent class using OpenAI Agents SDK
2. **DockingTool** (`tools/docking_tool.py`): Handles molecular docking calculations
3. **KnowledgeTool** (`tools/knowledge_tool.py`): Provides domain knowledge and analysis
4. **API Server** (`api.py`): Flask-based web interface
5. **Frontend** (`static/index.html`): Web interface for interactive queries

### Data Flow

1. User submits natural language query
2. Agent extracts molecules (SMILES) and target protein
3. DockingTool checks cache for existing scores
4. Missing scores computed using Dockstring (or mock fallback)
5. KnowledgeTool provides interpretation and analysis
6. Agent synthesizes results into comprehensive response

## Trade-offs and Limitations

### Current Limitations

- **Platform Dependency**: Real docking only works on Linux due to macOS compatibility issues
- **Cached Results**: All scores currently cached for consistency
- **Mock Fallback**: Deterministic mock scores used when Dockstring unavailable

### Design Trade-offs

- **Simplicity vs. Accuracy**: Mock scores provide consistent demo experience but lack real docking accuracy
- **Caching vs. Freshness**: Cached results improve response time but may not reflect latest calculations
- **JSON vs. Database**: Simple JSON storage chosen for ease of setup over robust database solution

## Integration with Virtual Screening Pipeline

This agent can fit into a real virtual screening pipeline as follows:

### Hit Identification Phase

- Screen large compound libraries against target proteins
- Rank compounds by binding affinity
- Filter by drug-likeness criteria
- Generate hit lists for experimental validation

### Lead Optimization Phase

- Analyze structure-activity relationships
- Suggest chemical modifications
- Compare binding modes and interactions
- Prioritize compounds for synthesis

### Decision Support

- Provide scientific rationale for compound selection
- Generate reports for project teams
- Answer questions about target biology
- Suggest next steps in drug development

### Conversational Interface Benefits

- Natural language queries reduce technical barriers
- Interactive exploration of results
- Educational tool for non-experts
- Rapid hypothesis testing and validation

## Future Improvements

### Planned Enhancements

1. **Fix Docking Issues**: Resolve macOS compatibility for real-time docking
2. **Enhanced Agent Prompts**: Improve reasoning and analysis capabilities
3. **Additional Tools**: Integrate ADMET prediction, similarity search, and structure optimization
4. **Modular Architecture**: Refactor for better maintainability and extensibility
5. **Vector Store**: Replace JSON files with vector database for better knowledge retrieval
6. **Professional Frontend**: Develop production-ready web interface

### Technical Debt

- Replace mock scoring with real docking calculations
- Implement proper error handling and logging
- Add comprehensive test coverage
- Optimize performance for large-scale screening
- Implement user authentication and project management

## Usage Examples

### Basic Docking Query

```
"Rank molecules CCO, CCN, CCC by docking score against target HSP90AA1"
```

### Score Interpretation

```
"What does a docking score of -7.5 mean?"
```

### Process Explanation

```
"Explain molecular docking"
```

### Target Information

```
"Tell me about target EGFR"
```

## API Endpoints

- `POST /api/query` - Process molecular queries
- `GET /api/health` - Health check
- `GET /` - Web interface

# Linux demo with real docking calculation
[DEMO](https://github.com/user-attachments/assets/8ea399f9-5d9b-4c53-8f94-8c6f263873d2)

# Lucidchart Diagram
<img width="4629" height="1070" alt="Blank diagram" src="https://github.com/user-attachments/assets/2a29b333-fc1f-4bd7-bdd4-ef3193237da0" />



