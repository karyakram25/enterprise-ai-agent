from app.rag.rag_chain import answer_question

question = "What is maternity leave policy ?"

answer = answer_question(question)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)