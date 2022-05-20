from kerdezo import Kerdezo

# Create interactive suite
suite = Kerdezo()

# Add questions
suite.addQuestion("How do you feel today?", dest="feel", default="happy")

# Start asking questions
suite.ask()

# Do something with the answers
print(f"You are feeling {suite.getAnswer('feel')}")
