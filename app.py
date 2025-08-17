from flask import Flask, request, jsonify, render_template
from transformers import pipeline, set_seed
import torch

app = Flask(__name__)

# Initialize the generator
generator = pipeline('text-generation', 
                    model='gpt2',
                    device=0 if torch.cuda.is_available() else -1,
                    framework='pt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    try:
        data = request.json
        topic = data.get('topic', '').strip()
        genre = data.get('genre', 'Poem')
        max_length = data.get('max_length', 100)
        temperature = data.get('temperature', 0.7)

        if not topic:
            return jsonify({'error': 'Please enter a topic to generate content'}), 400

        set_seed(42)  # For reproducibility

        # Generate two variations
        outputs = generator(
            f"{genre.lower()} about {topic}:",
            max_length=max_length,
            num_return_sequences=2,
            temperature=temperature,
            do_sample=True
        )

        results = [output['generated_text'] for output in outputs]
        
        # Clean up results
        cleaned_results = []
        for result in results:
            # Remove duplicate prompt if exists
            prompt = f"{genre.lower()} about {topic}:"
            if result.startswith(prompt):
                result = result[len(prompt):].strip()
            cleaned_results.append(result)

        return jsonify({'results': cleaned_results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

