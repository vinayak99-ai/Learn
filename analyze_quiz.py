#!/usr/bin/env python3
"""
Quiz Analysis Tool
Analyzes the quiz-format.csv file and provides detailed statistics.
"""

import csv
import sys
from collections import defaultdict

# Constants
CSV_HEADER_LINE = 1
CSV_DATA_START_LINE = 2  # First line of actual data (after header)

def analyze_quiz(filename='quiz-format.csv'):
    """Analyze the quiz file and print detailed statistics."""
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            questions = list(reader)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    if not questions:
        print("Error: No questions found in file.")
        sys.exit(1)
    
    # Basic statistics
    print("=" * 60)
    print("QUIZ FILE ANALYSIS")
    print("=" * 60)
    print(f"\nTotal Questions: {len(questions)}")
    
    # Topic distribution
    print("\n" + "-" * 60)
    print("TOPIC DISTRIBUTION")
    print("-" * 60)
    topics = defaultdict(int)
    for q in questions:
        topics[q['topic']] += 1
    
    for topic in sorted(topics.keys()):
        count = topics[topic]
        percentage = (count / len(questions)) * 100
        print(f"  {topic:<30} {count:>3} ({percentage:>5.1f}%)")
    
    # Answer distribution
    print("\n" + "-" * 60)
    print("CORRECT ANSWER DISTRIBUTION")
    print("-" * 60)
    answers = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    answer_by_topic = defaultdict(lambda: {'A': 0, 'B': 0, 'C': 0, 'D': 0})
    
    for q in questions:
        ans = q['correct_answer']
        if ans in answers:
            answers[ans] += 1
            answer_by_topic[q['topic']][ans] += 1
    
    print("\nOverall Distribution:")
    ideal_count = len(questions) / 4
    for ans in ['A', 'B', 'C', 'D']:
        count = answers[ans]
        percentage = (count / len(questions)) * 100
        deviation = count - ideal_count
        status = "⚠️ HIGH" if percentage > 35 else ("⚠️ LOW" if percentage < 15 else "✓ OK")
        print(f"  Option {ans}: {count:>3} ({percentage:>5.1f}%) [{status:>8}] Deviation: {deviation:+.1f}")
    
    # Find topics with most bias
    print("\n" + "-" * 60)
    print("TOPICS WITH HIGHEST BIAS")
    print("-" * 60)
    
    biased_topics = []
    for topic, ans_dist in answer_by_topic.items():
        total = sum(ans_dist.values())
        if total > 0:
            max_ans = max(ans_dist.items(), key=lambda x: x[1])
            max_percentage = (max_ans[1] / total) * 100
            if max_percentage > 50:  # More than 50% is one answer
                biased_topics.append((topic, max_ans[0], max_ans[1], total, max_percentage))
    
    biased_topics.sort(key=lambda x: x[4], reverse=True)
    
    if biased_topics:
        print("\nTopics where one answer appears >50% of the time:")
        for topic, ans, count, total, percentage in biased_topics:
            print(f"  {topic:<30} Option {ans}: {count}/{total} ({percentage:.1f}%)")
    else:
        print("\n✓ No topics with severe bias detected.")
    
    # Quality checks
    print("\n" + "-" * 60)
    print("QUALITY CHECKS")
    print("-" * 60)
    
    issues = []
    
    # Check for very short questions
    short_questions = []
    for i, q in enumerate(questions, CSV_DATA_START_LINE):
        if len(q['question']) < 10:
            short_questions.append((i, q['question']))
    
    if short_questions:
        print(f"\n⚠️  Found {len(short_questions)} question(s) that are very short (<10 characters):")
        for line_num, question in short_questions[:5]:
            print(f"    CSV Line {line_num}: {question}")
        if len(short_questions) > 5:
            print(f"    ... and {len(short_questions) - 5} more")
    else:
        print("\n✓ All questions have adequate length")
    
    # Check for duplicate questions
    question_texts = {}
    duplicates = []
    for i, q in enumerate(questions, CSV_DATA_START_LINE):
        q_text = q['question'].lower().strip()
        if q_text in question_texts:
            duplicates.append((i, question_texts[q_text], q['question']))
        else:
            question_texts[q_text] = i
    
    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} duplicate question(s):")
        for curr_line, orig_line, question in duplicates[:5]:
            print(f"    CSV Line {curr_line} duplicates CSV Line {orig_line}: {question[:50]}...")
        if len(duplicates) > 5:
            print(f"    ... and {len(duplicates) - 5} more")
    else:
        print("✓ No duplicate questions found")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    max_ans_pct = max((v / len(questions)) * 100 for v in answers.values())
    min_ans_pct = min((v / len(questions)) * 100 for v in answers.values())
    
    if max_ans_pct > 35 or min_ans_pct < 15:
        print("\n❌ CRITICAL: Answer distribution is significantly imbalanced!")
        print("   This may compromise the validity of assessments using this quiz.")
        print("   Recommendation: Review and rebalance the correct answers.")
    else:
        print("\n✓ Answer distribution is reasonably balanced.")
    
    print("\n" + "=" * 60)
    print()

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 'quiz-format.csv'
    analyze_quiz(filename)
