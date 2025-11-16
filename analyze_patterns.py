"""
Pattern Analysis Tool - Simulates Feedback Triage and Issue Identification
Demonstrates ability to identify patterns in LLM quality issues and prioritize them
"""

import pandas as pd
import os
from collections import Counter

def find_latest_results():
    """Find the most recent results file"""
    results_files = [f for f in os.listdir('.') if f.startswith('results_') and f.endswith('.csv')]
    if not results_files:
        return None
    # Sort by number in filename
    results_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]), reverse=True)
    return results_files[0]

def analyze_quality_patterns(df):
    """Identify common quality issues and patterns"""
    
    print("=" * 70)
    print("PATTERN ANALYSIS: QUALITY ISSUES")
    print("=" * 70)
    
    # Identify issues by rating
    issues = {
        'Poor': df[df['Overall_Rating'] == 'Poor'],
        'Needs Review': df[df['Overall_Rating'] == 'Needs Review'],
        'Good': df[df['Overall_Rating'] == 'Good'],
        'Excellent': df[df['Overall_Rating'] == 'Excellent']
    }
    
    print(f"\n📊 Quality Distribution:")
    for rating, data in issues.items():
        count = len(data)
        percentage = (count / len(df)) * 100
        print(f"  {rating}: {count} ({percentage:.1f}%)")
    
    # Analyze notes for common issues
    all_notes = []
    for notes in df['Notes']:
        if isinstance(notes, str) and notes:
            all_notes.extend([n.strip() for n in notes.split(';')])
    
    note_counts = Counter(all_notes)
    
    if note_counts:
        print(f"\n🔍 Common Issues Identified:")
        for note, count in note_counts.most_common(5):
            print(f"  • {note}: {count} occurrences")
    
    # Grade level analysis
    print(f"\n📚 Grade Level Performance:")
    grade_performance = df.groupby('Grade_Level').agg({
        'Educational_Quality': ['mean', 'min', 'max', 'count']
    }).round(2)
    
    for grade in grade_performance.index:
        stats = grade_performance.loc[grade]['Educational_Quality']
        print(f"  {grade}: Avg={stats['mean']:.2f}, Min={stats['min']:.2f}, Max={stats['max']:.2f} (n={int(stats['count'])})")
    
    # Low performers (Educational Quality < 0.7)
    low_performers = df[df['Educational_Quality'] < 0.7]
    if len(low_performers) > 0:
        print(f"\n⚠️  Low Quality Responses ({len(low_performers)} found):")
        for idx, row in low_performers.head(5).iterrows():
            print(f"  Test #{row['Test_ID']}: {row['Prompt'][:50]}... (Score: {row['Educational_Quality']:.2f})")
    
    # Mismatches between expected and actual
    mismatches = df[~df['Matches_Expected']]
    if len(mismatches) > 0:
        print(f"\n🎯 Evaluator Mismatches ({len(mismatches)} found):")
        for idx, row in mismatches.head(5).iterrows():
            print(f"  Test #{row['Test_ID']}: Expected '{row['Expected_Quality']}' but got '{row['Overall_Rating']}'")
            print(f"    Prompt: {row['Prompt'][:60]}...")
    
    return issues, low_performers, mismatches

def prioritize_issues(df, low_performers, mismatches):
    """Create a prioritized list of issues to address"""
    
    print("\n" + "=" * 70)
    print("ISSUE PRIORITIZATION & TRIAGE")
    print("=" * 70)
    
    priority_queue = []
    
    # High Priority: Safety issues
    safety_issues = df[df['Notes'].str.contains('inappropriate language', case=False, na=False)]
    if len(safety_issues) > 0:
        priority_queue.append({
            'priority': 'HIGH',
            'category': 'Safety',
            'count': len(safety_issues),
            'description': 'Inappropriate language detected',
            'action': 'Immediate review and content filter adjustment needed'
        })
    
    # High Priority: Large evaluator mismatches
    if len(mismatches) > 5:
        priority_queue.append({
            'priority': 'HIGH',
            'category': 'Evaluator Accuracy',
            'count': len(mismatches),
            'description': f'Evaluator accuracy is {(1 - len(mismatches)/len(df))*100:.1f}%',
            'action': 'Recalibrate evaluation rubrics and scoring thresholds'
        })
    
    # Medium Priority: Low quality responses
    if len(low_performers) > 0:
        priority_queue.append({
            'priority': 'MEDIUM',
            'category': 'Response Quality',
            'count': len(low_performers),
            'description': 'Responses with Educational Quality < 0.7',
            'action': 'Review LLM prompts and fine-tuning needs'
        })
    
    # Low Priority: Minor improvements
    good_responses = df[df['Overall_Rating'] == 'Good']
    if len(good_responses) > 0:
        priority_queue.append({
            'priority': 'LOW',
            'category': 'Optimization',
            'count': len(good_responses),
            'description': 'Good responses that could be elevated to Excellent',
            'action': 'Analyze for enhancement opportunities'
        })
    
    if priority_queue:
        print("\n📋 Prioritized Action Items:\n")
        for i, item in enumerate(priority_queue, 1):
            print(f"{i}. [{item['priority']}] {item['category']}")
            print(f"   Issue: {item['description']} ({item['count']} cases)")
            print(f"   Action: {item['action']}\n")
    else:
        print("\n✅ No critical issues identified! System performing well.")
    
    return priority_queue

def generate_summary_report(df, filename):
    """Generate executive summary"""
    
    print("=" * 70)
    print("EXECUTIVE SUMMARY")
    print("=" * 70)
    
    total = len(df)
    excellent = len(df[df['Overall_Rating'] == 'Excellent'])
    good = len(df[df['Overall_Rating'] == 'Good'])
    needs_review = len(df[df['Overall_Rating'] == 'Needs Review'])
    poor = len(df[df['Overall_Rating'] == 'Poor'])
    
    avg_quality = df['Educational_Quality'].mean()
    evaluator_accuracy = (df['Matches_Expected'].sum() / total) * 100
    
    print(f"\n📄 Analysis of: {filename}")
    print(f"📊 Total Responses: {total}")
    print(f"📈 Average Educational Quality: {avg_quality:.2f}/1.0")
    print(f"🎯 Evaluator Accuracy: {evaluator_accuracy:.1f}%")
    print(f"\n🏆 Success Rate: {((excellent + good) / total * 100):.1f}% (Excellent + Good)")
    print(f"⚠️  Attention Needed: {((needs_review + poor) / total * 100):.1f}% (Needs Review + Poor)")
    
    # Recommendation
    print("\n💡 Recommendation:")
    if avg_quality >= 0.8 and evaluator_accuracy >= 90:
        print("   ✓ System is performing well. Continue monitoring.")
    elif avg_quality >= 0.7 and evaluator_accuracy >= 80:
        print("   → Good performance with room for optimization.")
    else:
        print("   ⚠ System needs attention. Review low-performing cases and recalibrate evaluators.")
    
    print("=" * 70)

def main():
    # Find the latest results file
    results_file = find_latest_results()
    
    if not results_file:
        print("❌ No results files found. Run evaluate.py first.")
        return
    
    print(f"\n🔍 Analyzing: {results_file}\n")
    
    # Load data
    df = pd.read_csv(results_file)
    
    # Run analyses
    issues, low_performers, mismatches = analyze_quality_patterns(df)
    priority_queue = prioritize_issues(df, low_performers, mismatches)
    generate_summary_report(df, results_file)
    
    print("\n✅ Pattern analysis complete!")
    print("\nThis demonstrates:")
    print("  ✓ Feedback intake and triage capabilities")
    print("  ✓ Pattern recognition in quality issues")
    print("  ✓ Issue prioritization and escalation")
    print("  ✓ Data-driven decision making")
    print("  ✓ Executive-level reporting")

if __name__ == "__main__":
    main()
