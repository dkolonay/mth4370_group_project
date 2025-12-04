'''
IDEA:
The model is solving the puzzle of matching text to images

In consequence, it learns concepts like: genre, mood, vibe
as a side effect it learns similarity.

this is kind of a similar idea as to what word2vec does
(next word prediction)
'''

import torch
import torch.nn.functional as F

def contrastive_loss(z_i, z_j, temperature=0.1):
    """
    Computes NT-Xent loss (InfoNCE) for self-supervised learning.

    Args:
        z_i: Embeddings for View 1 (e.g., text+genre) [Batch, Dim]
        z_j: Embeddings for View 2 (e.g., poster+keywords) [Batch, Dim]
        temperature: Scalar scaling factor
    Returns:
        Scalar loss value
    """
    batch_size = z_i.shape[0]

    # Concatenate the two views
    z = torch.cat([z_i, z_j], dim=0)

    # Compute similarity between every movie and every other movie (and view)
    sim_matrix = (z @ z.t()) / temperature
    # the reason this is dot becuase hte length of z

    # targets: [batch_size, 0, 1, ... batch_size-1]
    targets = torch.arange(batch_size, device=z.device)

    # labels: [batch_size... 2*batch-1 | 0 ... batch-1]
    labels = torch.cat([targets + batch_size, targets], dim=0)

    # For a movie at index 'k' (in View 1), the target match is at 'k + batch_size' (View 2)
    # For a movie at index 'k + batch_size' (in View 2), the target match is at 'k' (View 1)

    # The dot product of a vector with itself is always 1
    # We ignore it so the model doesn't cheat by just matching itself.
    mask = torch.eye(2 * batch_size, device=z.device).bool()

    # Set diagonal to negative infinity so Softmax makes it exactly 0
    min_val = torch.finfo(sim_matrix.dtype).min
    sim_matrix.masked_fill_(mask, min_val)

    # Calculate Loss
    return F.cross_entropy(sim_matrix, labels)