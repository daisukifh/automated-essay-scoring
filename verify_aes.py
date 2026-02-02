import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aes_project.settings')
django.setup()

from scoring.models import Question, Essay
from scoring.logic import calculate_score

def test_workflow():
    print("--- Starting Verification ---")
    
    # Clean up previous test data if any
    Question.objects.filter(title="Test Question 101").delete()

    print("1. Creating Test Question...")
    q = Question.objects.create(
        title="Test Question 101",
        prompt_text="Explain the importance of water.",
        reference_answer="Water is essential for all known forms of life. It covers 71% of Earth's surface.",
        min_score=0,
        max_score=100
    )
    print(f"   Created Question: {q.title} (ID: {q.id})")

    print("\n2. Testing Scoring Logic...")
    # Good Answer
    ans_good = "Water is crucial for life and covers most of the Earth."
    score_good = calculate_score(ans_good, q.reference_answer, 0, 100)
    print(f"   Good Answer Score: {score_good:.2f} (Expected > 50)")

    # Bad Answer
    ans_bad = "Computers are made of silicon."
    score_bad = calculate_score(ans_bad, q.reference_answer, 0, 100)
    print(f"   Bad Answer Score: {score_bad:.2f} (Expected Low)")

    if score_good > score_bad:
        print("   [SUCCESS] Scoring logic correctly identifies relevance.")
    else:
        print("   [FAILURE] Scoring logic failed to distinguish answers.")

    print("\n3. Simulating Essay Submission...")
    e = Essay.objects.create(
        question=q,
        student_name="Verification Bot",
        content=ans_good,
        score=score_good
    )
    print(f"   Saved Essay ID: {e.id}, Score: {e.score}")

    if Essay.objects.filter(id=e.id).exists():
        print("   [SUCCESS] Essay successfully saved to database.")
    else:
        print("   [FAILURE] Essay not found in database.")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    test_workflow()
