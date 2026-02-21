---
name: academic-research
description: Academic paper search and dataset discovery workflow. Finds relevant papers across arXiv and Semantic Scholar, discovers datasets on Kaggle and HuggingFace, and retrieves key documents for analysis.
---

# Academic Research

Conduct academic research on: **$ARGUMENTS**

Follow these steps for a structured literature review and dataset discovery.

## Step 1: Academic Paper Search

Use `scientific_research`:
- operation: "academic_search"
- query: "$ARGUMENTS"
- max_results: 15
- sources: ["semantic_scholar", "arxiv"]

Identify the most cited papers, recent publications, key authors, and methodologies.

## Step 2: Refined Paper Search

Based on Step 1 findings, search with more specific terminology:
- operation: "academic_search", query: <refined_query>, max_results: 10

Also search for surveys:
- operation: "academic_search", query: "$ARGUMENTS survey OR review OR overview", max_results: 5

## Step 3: Dataset Discovery

Use `scientific_research`:
- operation: "dataset_discovery"
- query: "$ARGUMENTS"
- max_results: 10

Also search with specific terms from Step 1.

## Step 4: Retrieve Key Papers

For top 2-3 papers with accessible PDFs, use `document_analysis`:
- url: <paper_pdf_url>
- max_pages: 10
- extract_metadata: true
- summary_length: 1000

## Step 5: Supplementary Context

Use `web_search` for accessible explanations:
- query: "$ARGUMENTS research paper summary explanation", num_results: 10

Use `social_search` for community discussion:
- query: "$ARGUMENTS paper research", platforms: ["reddit", "hackernews"], max_results_per_platform: 5

## Step 6: Open Source Implementations

Use `github_search`:
- query: "$ARGUMENTS"
- sort: "stars"
- max_results: 10
- include_readme: true

## Step 7: Compile Literature Review

1. **Research Overview** -- Introduction to the area and why it matters
2. **Key Papers** -- Summaries of important papers (title, authors, year, contribution, findings)
3. **Literature Landscape** -- How papers relate; major research threads
4. **Methodologies** -- Common approaches and frameworks
5. **Available Datasets** -- Datasets with descriptions, sizes, access info
6. **Open Source Implementations** -- GitHub repos implementing the research
7. **Research Gaps** -- Areas with limited research or open questions
8. **Suggested Reading Order** -- Recommended sequence for newcomers
9. **References** -- Complete bibliography with links

Use proper academic citation style where possible.
