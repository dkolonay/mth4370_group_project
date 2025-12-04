import os
import torch
import torch.nn.functional as F
from tqdm import tqdm

from ml.src.models.fusion_model import MovieFusionModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../.."))
DIR = os.path.join(PROJECT_ROOT, "data", "processed")

def generate_embeddings_learned(model_path="model/fusion_model.pt", batch_size=256):
    """
    Generate embeddings using trained fusion model

    Args:
        model_path: Path to trained model checkpoint
        batch_size: Number of movies to process at once
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    features = torch.load(os.path.join(DIR, 'features.pt'))
    num_movies = features['text'].shape[0]

    model = MovieFusionModel(output_dim=512).to(device)

    # Load trained weights if available
    if not model_path and (not os.path.exists(model_path)):
        print('provide model')
        return None

    checkpoint = torch.load(os.path.join(DIR, '..' ,model_path), map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])

    model.eval()

    # Generate embedding
    all_embeddings = []
    text_only_embeddings = []

    with torch.no_grad():
        for i in tqdm(range(0, num_movies, batch_size), desc="Processing batches"):
            batch = {k: v[i:i+batch_size].to(device) for k, v in features.items()}

            # Fused embeddings
            fused = model(batch)
            all_embeddings.append(fused.cpu())

            # Text-only embeddings
            text_only = F.normalize(batch['text'], p=2, dim=1)
            text_only_embeddings.append(text_only.cpu())

    fused_embeddings = torch.cat(all_embeddings, dim=0)
    text_embeddings = torch.cat(text_only_embeddings, dim=0)

    # Save embeddings
    embeddings_dict = {
        'fused': fused_embeddings,
        'text_only': text_embeddings
    }

    save_path = os.path.join(DIR, 'embeddings.pt')
    torch.save(embeddings_dict, save_path)

    return embeddings_dict


if __name__ == '__main__':
    generate_embeddings_learned()