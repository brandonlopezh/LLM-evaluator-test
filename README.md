# Educational LLM Response Evaluator
A comprehensive tool for evaluating AI-generated educational content quality, designed specifically for conversational educational chatbots.

## What It Does
Evaluates LLM responses for educational prompts based on multiple criteria:
- **Accuracy**: Is the content factually correct and does it answer the prompt?
- **Age-Appropriateness**: Is vocabulary and complexity suitable for the target grade level?
- **Completeness**: Does it provide sufficient detail and fully address the question?
- **Safety**: Is content appropriate and safe for students?
- **Educational Quality**: Overall educational value score (0.0-1.0)

## Features
- ✅ **Auto-incrementing results files** (results_1.csv, results_2.csv, etc.)
- ✅ **Full response evaluation** - Analyzes actual LLM outputs, not just prompts
- ✅ **Educational Quality scoring** - Specialized metric for educational content
- ✅ **Conversational tone support** - Appropriate for chatbots
- ✅ **Comprehensive test data** - 30 test cases with good and poor responses
- ✅ **Evaluator Quality tracking** - Measures how well the evaluator performs
- ✅ **Detailed CSV output** - Includes prompts, responses, and evaluation notes
- ✅ **Visual Dashboard** - Auto-generated charts showing quality metrics and patterns
- ✅ **Pattern Analysis Tool** - Identifies trends, triages issues, and prioritizes action items

## Quick Start

```bash
# Install requirements
pip install -r requirements.txt

# Run the evaluator
python3 evaluate.py

# Analyze patterns and triage issues
python3 analyze_patterns.py
```

The evaluator will generate:
- `results_X.csv` - Detailed evaluation data
- `results_X_dashboard.png` - Visual analysis dashboard

The pattern analyzer provides:
- Quality distribution analysis
- Common issue identification
- Grade-level performance metrics
- Prioritized action items for improvement

## Example Output

```
LLM RESPONSE QUALITY EVALUATOR
========================================================

Evaluating 30 LLM responses...

Test 1: Excellent - Explain photosynthesis to a 5th grader...
Test 2: Excellent - Explain the water cycle...
Test 3: Excellent - Explain gravity simply...
...
Test 16: Poor - Explain photosynthesis to a 5th grader...
Test 17: Poor - Explain the water cycle...

========================================================
EVALUATION SUMMARY
========================================================
Total Responses Evaluated: 30
Excellent: 15
Good: 0
Needs Review: 0
Poor: 15
Safety Issues: 0

Detailed results saved to: results_6.csv

Evaluator Quality: 30/30 (100.0%)

This demonstrates:
  ✓ AI response quality assessment
  ✓ Educational content evaluation with conversational tone
  ✓ Multi-criteria evaluation framework
  ✓ Safety and appropriateness checking
  ✓ Accuracy validation against prompts
  ✓ Educational quality scoring

========================================================
GENERATING EVALUATION DASHBOARD
========================================================
✓ Dashboard saved to: results_6_dashboard.png
========================================================
```

## Dashboard Visualizations

The auto-generated dashboard includes:

1. **Response Quality Distribution** - Bar chart showing Excellent/Good/Poor ratings
2. **Educational Quality Scores** - Histogram with mean line showing score distribution
3. **Evaluator Accuracy** - Pie chart comparing expected vs actual ratings
4. **Quality by Grade Level** - Comparative analysis across different grade levels

![Dashboard Example](results_1_dashboard.png)

## Pattern Analysis & Issue Triage

The `analyze_patterns.py` tool demonstrates systematic feedback management:

### Quality Distribution Analysis
- Categorizes responses by rating (Excellent/Good/Needs Review/Poor)
- Identifies frequency of common issues
- Tracks grade-level performance metrics

### Issue Prioritization
- **HIGH Priority**: Safety issues, evaluator accuracy problems
- **MEDIUM Priority**: Low quality responses requiring prompt review
- **LOW Priority**: Optimization opportunities for good responses

### Executive Summary
- Overall system health metrics
- Evaluator accuracy percentage
- Success rate calculations
- Actionable recommendations

Example output:
```
ISSUE PRIORITIZATION & TRIAGE
========================================================
1. [HIGH] Evaluator Accuracy
   Issue: Evaluator accuracy is 50.0% (15 cases)
   Action: Recalibrate evaluation rubrics and scoring thresholds

2. [MEDIUM] Response Quality
   Issue: Responses with Educational Quality < 0.7 (13 cases)
   Action: Review LLM prompts and fine-tuning needs
```

## Files
- `evaluate.py` - Main evaluation script with advanced scoring logic and dashboard generation
- `analyze_patterns.py` - Pattern analysis tool for feedback triage and issue prioritization
- `test_prompts.csv` - 30 educational prompts with both good and poor responses
- `results_X.csv` - Auto-numbered evaluation results with comprehensive metrics
- `results_X_dashboard.png` - Auto-generated visualization dashboard

## Sample Results CSV

| Test_ID | Prompt | Response | Grade_Level | Expected_Quality | Educational_Quality | Overall_Rating | Matches_Expected | Notes |
|---------|--------|----------|-------------|-----------------|-------------------|----------------|------------------|-------|
| 1 | Explain photosynthesis... | Photosynthesis is how plants make... | 5th | Excellent | 0.95 | Excellent | True | Response meets quality standards |
| 16 | Explain photosynthesis... | Plants just eat sunlight and make stuff... | 5th | Poor | 0.1 | Poor | True | Response contains inappropriate language |

## Test Case Coverage

### Good Responses (Tests 1-15)
- Photosynthesis explanation with scientific accuracy
- Water cycle with proper terminology
- Gravity explained simply but correctly
- Fractions using relatable pizza analogy
- Comprehensive coverage of key educational topics

### Poor Responses (Tests 16-30)
- Vague or incomplete explanations
- Casual language inappropriate for education ("idk", "lol", "ngl")
- Missing key scientific concepts
- Factually incomplete or unclear information

## Evaluation Logic

The evaluator checks for:
1. **Content accuracy** - Does the response contain correct information?
2. **Key concept coverage** - Are essential terms and ideas included?
3. **Language appropriateness** - Flags severely inappropriate language while allowing conversational tone
4. **Response completeness** - Evaluates length and depth of explanation
5. **Grade-level vocabulary** - Ensures complexity matches target audience

## Updates Made
- **v1.0**: Initial prompt evaluation system
- **v2.0**: Switched to response evaluation (analyzing LLM outputs)
- **v3.0**: Added auto-incrementing file names
- **v4.0**: Added Educational Quality scoring metric
- **v5.0**: Included full responses in results CSV
- **v6.0**: Optimized for conversational chatbots (removed overly strict language filters)
- **v7.0**: Expanded test dataset to 30 cases with good/poor response pairs
- **v8.0**: Added visual dashboard with 4 key metrics charts for pattern analysis
- **v9.0**: Built pattern analysis tool for feedback triage and issue prioritization

## Skills Demonstrated
✓ **LLM output evaluation and quality assessment**  
✓ **Educational content analysis and scoring**  
✓ **Multi-criteria evaluation framework design**  
✓ **Data visualization and dashboard creation**  
✓ **Pattern recognition in AI outputs**  
✓ **Feedback intake, triage, and prioritization**  
✓ **Issue escalation and stakeholder reporting**  
✓ **CSV data processing and automated reporting**  
✓ **Educational technology understanding**  
✓ **Python programming and data analysis**  
✓ **Quality assurance for AI systems**  
✓ **Understanding of conversational AI requirements**

## Relevance to LLM Quality Analyst Roles

This project demonstrates core competencies for Associate LLM Quality Analyst positions:

### Direct Skill Alignment
- **Feedback Management**: `analyze_patterns.py` shows systematic intake and triage of quality issues
- **Ground Truthing**: Evaluation logic compares actual responses against expected quality benchmarks
- **Test Suite Development**: 30 test cases with diverse scenarios and edge cases
- **Pattern Recognition**: Automated identification of common issues across responses
- **Dashboard Creation**: Visual metrics for monitoring evaluator outputs and consistency
- **Quality Assessment**: Multi-dimensional rubrics for scoring LLM responses

### Technical Capabilities
- Working with LLM outputs programmatically
- Building evaluation frameworks from scratch
- Data analysis and reporting workflows
- Systematic documentation and clear communication

### Collaboration with AI
Built collaboratively with AI assistance, demonstrating:
- Effective prompting and iteration
- Understanding of AI capabilities and limitations
- Practical experience working alongside LLMs
- Ability to validate and refine AI-generated solutions

---

*Built to showcase advanced LLM evaluation capabilities for AI applications
