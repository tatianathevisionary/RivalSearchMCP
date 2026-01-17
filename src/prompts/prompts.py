"""
MCP Prompts for RivalSearchMCP server.
Provides 4 essential prompt templates for LLMs to use our research capabilities effectively.
"""

from fastmcp import FastMCP
from typing import Literal


def register_prompts(mcp: FastMCP):
    """Register 4 core prompt templates for LLM interactions."""

    @mcp.prompt
    def research_question_generator(
        topic: str, depth: Literal["basic", "intermediate", "advanced"] = "intermediate"
    ) -> str:
        """
        Generates targeted research questions for systematic investigation.
        Returns a prompt that helps LLMs formulate specific, actionable research questions.
        """
        depth_guidance = {
            "basic": "fundamental questions about what, who, and where",
            "intermediate": "questions about how, why, and comparative analysis",
            "advanced": "questions about causality, implications, and future trends",
        }

        return f"""
        You are conducting research on: {topic}

        Generate 5-7 specific, researchable questions that will guide a comprehensive investigation using multiple data sources and analytical methods.

        Focus on {depth_guidance[depth]}.

        Your questions should:
        1. Be specific and measurable
        2. Address different aspects of the topic
        3. Enable systematic data collection and analysis
        4. Lead to actionable insights or conclusions
        5. Consider both current state and future implications

        Structure your response as a numbered list of questions, followed by a brief explanation of why each question is important for understanding the topic.
        """

    @mcp.prompt
    def evidence_synthesis_analyzer(
        sources: str,
        analysis_type: Literal[
            "consensus", "conflicts", "gaps", "trends"
        ] = "consensus",
    ) -> str:
        """
        Synthesizes evidence from multiple sources to identify patterns and insights.
        Returns a prompt for LLMs to analyze and synthesize findings across different data sources.
        """
        synthesis_focus = {
            "consensus": "areas of agreement and established knowledge",
            "conflicts": "contradictions and alternative viewpoints",
            "gaps": "missing information and unanswered questions",
            "trends": "patterns, changes, and emerging developments",
        }

        return f"""
        Analyze and synthesize evidence from these sources: {sources}

        Focus on identifying {synthesis_focus[analysis_type]} across all available information.

        Your analysis should:

        1. **Summarize Key Findings**: Extract the most important insights from each source
        2. **Identify Patterns**: Look for recurring themes, data points, or conclusions
        3. **Assess Credibility**: Evaluate the reliability and quality of each source
        4. **Highlight Significance**: Explain why certain findings are particularly important
        5. **Note Implications**: Discuss what the synthesized evidence means for understanding the topic

        Structure your response with:
        - Executive summary of the most important synthesis points
        - Detailed analysis organized by theme or finding
        - Assessment of evidence strength and confidence levels
        - Recommendations for further investigation if needed
        """

    @mcp.prompt
    def data_quality_evaluator(
        dataset_description: str,
        evaluation_criteria: Literal[
            "reliability", "completeness", "relevance", "usability"
        ] = "reliability",
    ) -> str:
        """
        Evaluates data quality and suitability for research purposes.
        Returns a prompt for LLMs to assess datasets and data sources critically.
        """
        criteria_focus = {
            "reliability": "accuracy, consistency, and trustworthiness of the data",
            "completeness": "coverage, missing values, and data comprehensiveness",
            "relevance": "alignment with research questions and analytical needs",
            "usability": "accessibility, format, and ease of analysis",
        }

        return f"""
        Evaluate the quality and suitability of this dataset: {dataset_description}

        Focus your evaluation on {criteria_focus[evaluation_criteria]}.

        Assessment Framework:

        1. **Data Source Credibility**:
           - Who collected/maintains this data?
           - What is their reputation and expertise?
           - Are there any potential biases or conflicts of interest?

        2. **Data Collection Methodology**:
           - How was the data gathered?
           - What quality controls were in place?
           - Are the methods appropriate for the intended use?

        3. **Data Characteristics**:
           - Size, scope, and time period covered
           - Update frequency and currency
           - Format and accessibility

        4. **Analytical Suitability**:
           - Does it answer the research questions?
           - Are there limitations or constraints?
           - What additional data might be needed?

        5. **Recommendations**:
           - Is this dataset suitable for the intended analysis?
           - What precautions should be taken when using it?
           - Are there alternative or complementary datasets to consider?

        Provide a structured evaluation with scores (1-5) for each criterion and clear recommendations for use.
        """

    @mcp.prompt
    def insight_extraction_specialist(
        content_summary: str,
        insight_type: Literal[
            "strategic", "operational", "tactical", "predictive"
        ] = "strategic",
    ) -> str:
        """
        Extracts actionable insights from research findings.
        Returns a prompt for LLMs to identify and articulate key insights from analyzed content.
        """
        insight_focus = {
            "strategic": "high-level implications and long-term strategic value",
            "operational": "practical applications and immediate implementation",
            "tactical": "specific actions and short-term opportunities",
            "predictive": "future trends and forward-looking implications",
        }

        return f"""
        Extract and articulate key insights from this research content: {content_summary}

        Focus on {insight_focus[insight_type]}.

        Insight Extraction Process:

        1. **Identify Key Findings**: What are the most important discoveries or conclusions?

        2. **Contextualize Significance**: Why do these findings matter? What makes them noteworthy?

        3. **Extract Implications**: What do these findings mean for stakeholders, decision-makers, or practitioners?

        4. **Generate Applications**: How can these insights be applied in real-world scenarios?

        5. **Assess Impact**: What is the potential value or consequence of acting on these insights?

        Structure your response as:
        - **Primary Insights**: 3-5 most important findings (numbered)
        - **Key Implications**: What these insights mean in broader context
        - **Actionable Applications**: Specific ways to use these insights
        - **Confidence Assessment**: How certain are we about these insights?
        - **Next Steps**: What additional research or validation would be valuable

        Focus on insights that are specific, actionable, and supported by evidence from the research.
        """
