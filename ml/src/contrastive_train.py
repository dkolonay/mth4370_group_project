'''
Indicies are based off:

features = {
    "text": text_features,
    "keywords": keywords_features,
    "genres": genre_features,
    "year": year_features,
    "month_sin": month_sin_features,
    "month_cos": month_cos_features,
    "vote_average": vote_average_features,
    "vote_count": vote_count_features,
    "popularity": popularity_features,
    "runtime": runtime_features,
    "poster_file": poster_file_features,
    "backdrop_file": backdrop_file_features,
    "mask": mask_features
}

because mask uses:

FEATURE_IDX = {
    "text": 0,
    "keywords": 1,
    "genres": 2,
    "year": 3,
    "month_sin": 4,
    "month_cos": 5,
    "vote_average": 6,
    "vote_count": 7,
    "popularity": 8,
    "runtime": 9,
    "poster": 10,
    "backdrop": 11
}
'''
import os
import torch
import torch.optim as optim
from torch.optim.lr_scheduler import LinearLR, CosineAnnealingLR, SequentialLR
from tqdm import tqdm

from models.fusion_model import MovieFusionModel
from utils.dataset import get_dataloader
from utils.losses import contrastive_loss

# --- Config ---
BATCH_SIZE = 256
LEARNING_RATE = 1e-4
EPOCHS = 100
WARMUP_EPOCHS = 10
TEMPERATURE = 0.1
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SAVE_DIR = "checkpoints"
DATA_PATH = "features.pt"

os.makedirs(SAVE_DIR, exist_ok=True)

# --- TRAINING LOOP ---
def train():
    dataloader = get_dataloader(
        features_file=DATA_PATH,
        batch_size=BATCH_SIZE,
    )

    # Calculate Total Steps for Scheduler
    total_steps = len(dataloader) * EPOCHS
    warmup_steps = len(dataloader) * WARMUP_EPOCHS
    decay_steps = total_steps - warmup_steps

    # 2. Initialize Model
    model = MovieFusionModel(output_dim=512).to(DEVICE)
    print("Compiling model...")
    model = torch.compile(model)

    optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-5)

    warmup_scheduler = LinearLR(
        optimizer, start_factor=0.01, end_factor=1.0, total_iters=warmup_steps
    )

    decay_scheduler = CosineAnnealingLR(
        optimizer, T_max=decay_steps, eta_min=1e-6
    )

    scheduler = SequentialLR(
        optimizer,
        schedulers=[warmup_scheduler, decay_scheduler],
        milestones=[warmup_steps]
    )

    scaler = torch.cuda.amp.GradScaler()

    # 3. Resume Logic
    start_epoch = 0
    checkpoint_path = os.path.join(SAVE_DIR, "latest_checkpoint.pt")

    if os.path.exists(checkpoint_path):
        print(f"Resuming from {checkpoint_path}")
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint['model_state_dict'], strict=False)
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        scaler.load_state_dict(checkpoint['scaler_state_dict'])
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        start_epoch = checkpoint['epoch'] + 1

    model.train()

    print(f"Starting training on {DEVICE}...")

    for epoch in range(start_epoch, EPOCHS):
        total_loss = 0
        progress_bar = tqdm(dataloader, desc=f"Epoch {epoch + 1}/{EPOCHS}")

        for batch in progress_bar:
            batch = {k: v.to(DEVICE, non_blocking=True) for k, v in batch.items()}

            optimizer.zero_grad(set_to_none=True)

            # Create Views
            mask_v1 = batch['mask'].clone()
            mask_v1[:, 10:12] = 0 # zero out indicies 10-11 (in mask)
            view1 = {**batch, 'mask': mask_v1}

            mask_v2 = batch['mask'].clone()
            mask_v2[:, 0:2] = 0 # zero out indicies 0-1 (in mask)
            view2 = {**batch, 'mask': mask_v2}

            with torch.cuda.amp.autocast():
                z1 = model(view1)
                z2 = model(view2)
                loss = contrastive_loss(z1, z2, temperature=TEMPERATURE)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            # STEP SCHEDULER PER BATCH (Not per epoch)
            scheduler.step()

            total_loss += loss.item()

            # Get current LR for display
            current_lr = optimizer.param_groups[0]['lr']
            progress_bar.set_postfix({'loss': loss.item(), 'lr': f"{current_lr:.2e}"})

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch + 1} Done. Loss: {avg_loss:.4f}")

        # Save Checkpoint
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'scaler_state_dict': scaler.state_dict(),
            'scheduler_state_dict': scheduler.state_dict(),  # Save scheduler
            'loss': avg_loss,
        }
        torch.save(checkpoint, os.path.join(SAVE_DIR, "latest_checkpoint.pt"))

        if (epoch + 1) % 10 == 0:
            torch.save(checkpoint, os.path.join(SAVE_DIR, f"model_epoch_{epoch + 1}.pt"))

    torch.save(model.state_dict(), "model/fusion_model.pt")
    print("Training Complete.")


if __name__ == "__main__":
    train()