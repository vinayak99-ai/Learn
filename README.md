# Learn
To keep all learning docs 

## Quiz File Analysis

The repository contains a comprehensive quiz file (`quiz-format.csv`) with 298 questions covering multiple topics and languages.

### 📊 Quiz Statistics

- **Total Questions**: 298
- **Topics**: 12 different categories
- **Languages**: Kannada, Hindi, and English
- **Format**: CSV with 7 fields (question, option_a, option_b, option_c, option_d, correct_answer, topic)

### ⚠️ Important Finding: Answer Distribution Bias

Analysis of the quiz file has revealed a **critical issue** with the distribution of correct answers:

| Correct Answer | Count | Percentage | Status |
|---------------|-------|------------|--------|
| A | 14 | 4.7% | ⚠️ Too Low |
| **B** | **161** | **54.0%** | ❌ Too High |
| C | 110 | 36.9% | ⚠️ High |
| D | 13 | 4.4% | ⚠️ Too Low |

**Problem**: 54% of all questions have "B" as the correct answer, which is more than double the ideal distribution (25% per option). This creates a significant bias where test-takers could achieve better scores by predominantly guessing "B".

### 📝 Topics with Highest Bias

Some topics show particularly severe bias:
- **Hindi Fill Blanks**: 89.7% of answers are B
- **Mahabharata**: 70.0% of answers are B
- **Kannada Fill Blanks**: 65.5% of answers are B
- **English Vocabulary**: 65.0% of answers are C
- **Science Environment**: 65.0% of answers are B

### 🔧 Tools Available

#### 1. Analysis Tool
Run the analysis script to see detailed statistics:
```bash
python3 analyze_quiz.py
```

This tool provides:
- Detailed answer distribution statistics
- Topic-wise bias analysis
- Quality checks (duplicates, short questions)
- Overall health assessment

#### 2. Rebalancing Tool
Automatically fix the answer distribution by shuffling options:
```bash
# Dry run (preview changes without modifying files)
python3 rebalance_quiz.py

# Apply changes (creates quiz-format-balanced.csv)
python3 rebalance_quiz.py --apply
```

This tool:
- Changes 123 questions to achieve balanced distribution
- Creates a new file (doesn't modify original)
- Maintains question quality while fixing statistical bias
- Achieves target: ~25% per option (A, B, C, D)

### 📚 Documentation

- [QUIZ_ANALYSIS.md](QUIZ_ANALYSIS.md) - Comprehensive analysis report
- [QUIZ_IMPROVEMENT_SUGGESTIONS.md](QUIZ_IMPROVEMENT_SUGGESTIONS.md) - Detailed improvement strategies

### 💡 Recommendations

1. **Review and Rebalance**: Questions should be reviewed to distribute correct answers more evenly across all options
2. **Target Distribution**: Aim for ~25% (75 questions) per option for a balanced quiz
3. **Quality Assurance**: Implement automated checks to prevent such biases in future quiz creation

### ✅ Positive Aspects

- All questions have complete data (no missing fields)
- All correct answers are valid (A, B, C, or D)
- Good variety of topics covered
- Multiple languages supported
- Consistent CSV format throughout
- No duplicate questions detected

