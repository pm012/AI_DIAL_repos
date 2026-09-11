from task.app.main import run

# TODO:
#  Try the `temperature` parameter that controls the randomness of the output. It's a parameter for balancing creativity
#        and determinism. Range: 0.0 to 2.0, Default: 1.0
#  User massage: Describe the sound that the color purple makes when it's angry
models = [
    'gpt-4o',
    'claude-3-7-sonnet@20250219',
    'gemini-2.5-pro',
]
temperatures = [0.0,  1.0,  2.0]
for model in models:
    for temp in temperatures:
    
        print(f"\n=== Testing model: {model} with temperature={temp} ===\n")
        run(
            deployment_name=model,
            print_only_content=True,
            user_input="Describe the sound that the color purple makes when it's angry",
            temperature=temp,
            interactive=False,
        #  (Optional) Use `temperature` parameter with value 2.1 and check what happens
    )