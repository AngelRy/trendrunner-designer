# prompts.py

def generate_slogan_prompt(keywords, style):
    prompt = f"""
You are a fashion designer creating simple slogans for running apparel.
Use the following keywords: {', '.join(keywords)}
Style: {style} (minimalist, motivational, or funny)
Generate a short, catchy slogan suitable for printing on a T-shirt or hoodie.
"""
    return prompt
