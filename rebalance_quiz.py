#!/usr/bin/env python3
"""
Quiz Rebalancing Tool
Automatically rebalances quiz answer distribution by shuffling options.
"""

import csv
import random
import sys
from collections import defaultdict

def rebalance_quiz(input_file='quiz-format.csv', output_file='quiz-format-balanced.csv', dry_run=True):
    """
    Rebalance the quiz by shuffling options to achieve more even distribution.
    
    Args:
        input_file: Input CSV file
        output_file: Output CSV file (only written if dry_run=False)
        dry_run: If True, only show what would be changed without writing
    """
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            questions = list(reader)
            fieldnames = reader.fieldnames
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    if not questions:
        print("Error: No questions found in file.")
        sys.exit(1)
    
    # Analyze current distribution
    current_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for q in questions:
        current_distribution[q['correct_answer']] += 1
    
    print("=" * 60)
    print("QUIZ REBALANCING TOOL")
    print("=" * 60)
    print(f"\nInput file: {input_file}")
    print(f"Total questions: {len(questions)}")
    print(f"Mode: {'DRY RUN (no changes will be saved)' if dry_run else 'LIVE (changes will be saved)'}")
    
    print("\nCurrent distribution:")
    for ans in ['A', 'B', 'C', 'D']:
        count = current_distribution[ans]
        percentage = (count / len(questions)) * 100
        print(f"  Option {ans}: {count:>3} ({percentage:>5.1f}%)")
    
    # Target distribution
    target_per_option = len(questions) // 4
    remainder = len(questions) % 4
    
    print(f"\nTarget distribution: ~{target_per_option} per option")
    print(f"  (Total: {len(questions)}, {remainder} questions will have uneven distribution)")
    
    # Strategy: Convert excess B and C answers to A and D
    needed = {
        'A': target_per_option - current_distribution['A'],
        'B': target_per_option - current_distribution['B'],
        'C': target_per_option - current_distribution['C'],
        'D': target_per_option - current_distribution['D']
    }
    
    print("\nChanges needed:")
    for ans in ['A', 'B', 'C', 'D']:
        if needed[ans] > 0:
            print(f"  Option {ans}: need +{needed[ans]} more")
        elif needed[ans] < 0:
            print(f"  Option {ans}: need {needed[ans]} fewer (excess: {-needed[ans]})")
        else:
            print(f"  Option {ans}: already at target")
    
    # Find candidates for change
    candidates_B = [q for q in questions if q['correct_answer'] == 'B']
    candidates_C = [q for q in questions if q['correct_answer'] == 'C']
    
    # Shuffle to randomize which questions get changed
    random.shuffle(candidates_B)
    random.shuffle(candidates_C)
    
    # Calculate how many to change
    b_to_change = min(len(candidates_B), -needed['B']) if needed['B'] < 0 else 0
    c_to_change = min(len(candidates_C), -needed['C']) if needed['C'] < 0 else 0
    
    print(f"\nPlanned changes:")
    print(f"  Will change {b_to_change} questions from B to A/D")
    print(f"  Will change {c_to_change} questions from C to A/D")
    
    changes_made = []
    new_questions = []
    
    # Process questions
    for q in questions:
        new_q = q.copy()
        
        # Determine if this question should be changed
        should_change = False
        target_answer = None
        
        if q['correct_answer'] == 'B' and b_to_change > 0:
            should_change = True
            b_to_change -= 1
            # Prefer D if needed, otherwise A
            target_answer = 'D' if needed['D'] > 0 else 'A'
            needed[target_answer] -= 1
            needed['B'] += 1
            
        elif q['correct_answer'] == 'C' and c_to_change > 0:
            should_change = True
            c_to_change -= 1
            # Prefer A if needed, otherwise D
            target_answer = 'A' if needed['A'] > 0 else 'D'
            needed[target_answer] -= 1
            needed['C'] += 1
        
        if should_change and target_answer:
            # Shuffle options to make target_answer correct
            old_correct = q['correct_answer']
            options = ['A', 'B', 'C', 'D']
            
            # Get the content of current correct answer and target
            old_correct_content = q[f'option_{old_correct.lower()}']
            target_content = q[f'option_{target_answer.lower()}']
            
            # Swap them
            new_q[f'option_{old_correct.lower()}'] = target_content
            new_q[f'option_{target_answer.lower()}'] = old_correct_content
            new_q['correct_answer'] = target_answer
            
            changes_made.append({
                'question': q['question'][:50] + '...' if len(q['question']) > 50 else q['question'],
                'old_answer': old_correct,
                'new_answer': target_answer,
                'topic': q['topic']
            })
        
        new_questions.append(new_q)
    
    # Calculate new distribution
    new_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for q in new_questions:
        new_distribution[q['correct_answer']] += 1
    
    print(f"\nTotal changes: {len(changes_made)}")
    
    if changes_made and not dry_run:
        print(f"\nSample changes (showing first 5):")
        for change in changes_made[:5]:
            print(f"  {change['old_answer']} → {change['new_answer']}: {change['question']} [{change['topic']}]")
        if len(changes_made) > 5:
            print(f"  ... and {len(changes_made) - 5} more")
    
    print("\nNew distribution:")
    for ans in ['A', 'B', 'C', 'D']:
        count = new_distribution[ans]
        percentage = (count / len(new_questions)) * 100
        change = count - current_distribution[ans]
        print(f"  Option {ans}: {count:>3} ({percentage:>5.1f}%) [{change:+d}]")
    
    # Write output file if not dry run
    if not dry_run:
        try:
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(new_questions)
            print(f"\n✓ Successfully wrote rebalanced quiz to: {output_file}")
            print(f"\nTo use the rebalanced quiz:")
            print(f"  1. Review the changes in {output_file}")
            print(f"  2. If satisfied, backup original: mv {input_file} {input_file}.backup")
            print(f"  3. Replace original: mv {output_file} {input_file}")
        except Exception as e:
            print(f"\n✗ Error writing output file: {e}")
            sys.exit(1)
    else:
        print(f"\nDRY RUN completed. No files were changed.")
        print(f"To apply changes, run: python3 {sys.argv[0]} --apply")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Check for --apply flag
    dry_run = '--apply' not in sys.argv
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print("Quiz Rebalancing Tool")
        print("\nUsage:")
        print(f"  python3 {sys.argv[0]}           # Dry run (show changes without applying)")
        print(f"  python3 {sys.argv[0]} --apply   # Apply changes and create balanced file")
        print("\nThis tool rebalances quiz answer distribution by shuffling options.")
        print("Original file is never modified directly - a new file is created.")
        sys.exit(0)
    
    rebalance_quiz(dry_run=dry_run)
