from task.app.main import run

#  Try the `n` parameter with different models (`deployment_name`). With the parameter `n`, we can configure how many
#       chat completion choices to generate for each input message
#  User massage: Why is the snow white?

# Models to try:
# - gpt-4o
# - claude-3-7-sonnet@20250219
# - gemini-2.5-pro

models = [
    'gpt-4o',
    'claude-3-7-sonnet@20250219',
    'gemini-2.5-pro',
]

for model in models:
    for n_value in range(1, 6):  # n from 1 to 5
        print(f"\n=== Testing model: {model} with n={n_value} ===\n")
        run(
            deployment_name=model,
            print_request=True,         # See full request/response
            print_only_content=False,   # See all choices in the response
            interactive=False,          # Non-interactive mode
            user_input="Why is the snow white?",
            n=n_value                   # Number of choices
        )

# Pay attention to the number of choices in the response!
# If you have worked with ChatGPT, you have probably seen responses where ChatGPT offers you a choice between two
# responses to select which one you prefer. This is done with the `n` parameter.
