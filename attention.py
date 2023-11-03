import sys
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel

def get_mask_token_index(tokenizer_output):
    for i, token in enumerate(tokenizer_output["input_ids"][0]):
        if token == tokenizer.mask_token_id:
            return i
    return None

def get_color_for_attention_score(score):
    # Scale attention score to grayscale color (0=black, 1=white)
    color_value = int(255 * (1 - score))
    return (color_value, color_value, color_value)

def visualize_attentions(tokens, attentions):
    for layer in range(attentions.shape[1]):
        for head in range(attentions.shape[2]):
            attention_matrix = attentions[0, layer, head].cpu().detach().numpy()
            plt.figure(figsize=(10, 8))
            plt.imshow(attention_matrix, cmap="gray")
            plt.title(f"Attention Layer {layer + 1}, Head {head + 1}")
            plt.xticks(np.arange(len(tokens)), tokens, rotation=45)
            plt.yticks(np.arange(len(tokens)), tokens)
            plt.colorbar()
            plt.tight_layout()
            plt.show()

def main():
    text = input("Text: ")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModel.from_pretrained("bert-base-uncased")

    inputs = tokenizer(text, return_tensors="pt")
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
    
    predicted_token_ids = torch.argmax(outputs.logits, dim=2)
    predicted_tokens = tokenizer.batch_decode(predicted_token_ids)

    mask_index = get_mask_token_index(inputs)
    if mask_index is not None:
        tokens = text.split()
        tokens[mask_index] = predicted_tokens[0][mask_index]

        attentions = outputs.attentions
        visualize_attentions(tokens, attentions)

if __name__ == "__main__":
    main()
