#!/bin/bash
set -e # script stops if  command fails

OUTPUT_DIR="ml/data/raw"

DATASET_URL="https://www.kaggle.com/api/v1/datasets/download/asaniczka/tmdb-movies-dataset-2023-930k-movies"

DOWNLOADED_FILENAME="tmdb-movies-dataset-2023-930k-movies.zip"
DOWNLOADED_FILE_PATH="$OUTPUT_DIR/$DOWNLOADED_FILENAME"

log() {
    echo "$1"
}

download_file() {
    log "Starting download"
    log "Source URL: $DATASET_URL"

    curl -L -C - -o "$DOWNLOADED_FILE_PATH" "$DATASET_URL"

    log "Download complete."
    log "Saving to: $DOWNLOADED_FILE_PATH"
}

decompress_file() {
	log "Starting decompression of $DOWNLOADED_FILENAME (ZIP file)..."

    (cd "$OUTPUT_DIR" && unzip -o "$DOWNLOADED_FILENAME")

    log "Decompression successful"
    log "Contents extracted to $OUTPUT_DIR"
}

log "--- TMDB Dataset Downloader Started ---"

download_file
decompress_file

log "--- TMDB Dataset Downloader Finished ---"
