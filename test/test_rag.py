from utils.rag_chain import generate_response

result = generate_response(
    "Best places to visit in Kerala"
)

print(result["answer"])

print("\n" + "=" * 60)
print("Sources:")

for source in result["sources"]:
    print(f"- {source}")
