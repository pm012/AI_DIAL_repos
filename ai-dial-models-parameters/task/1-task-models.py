from task.app.main import run

# HINT: All available models you can find here: https://ai-proxy.lab.epam.com/openai/models

#  Try different models (`deployment_name`) with such user request:
#  User massage: What LLMs can do?

# Models to try:
# - gpt-4o
# - claude-3-7-sonnet@20250219
# - gemini-2.5-pro
for model in [
    'gpt-4o',
    'claude-3-7-sonnet@20250219',
    'gemini-2.5-pro',
]:
    print(f'\n\n=== Testing model: {model} ===\n')
    run(
        deployment_name=model,
        print_request=True,
        print_only_content=True,
        interactive=False,
        user_input="What LLMs can do?"
    )


# The main goal of this task is to explore the functional capabilities of DIAL to be able to work with different
# LLMs through unified API