"""
=============================================================
  Plant Disease Detection - Model Training Script
  Uses MobileNetV2 Transfer Learning on PlantVillage Dataset
=============================================================

HOW TO USE:
  1. Download PlantVillage dataset from Kaggle:
     https://www.kaggle.com/datasets/emmarex/plantdisease
  2. Place it in: data/PlantVillage/
  3. Run: python model/train_model.py
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import json

# ─── Configuration ────────────────────────────────────────────────────────────
IMG_SIZE    = 128          # MobileNetV2 expects 224x224
BATCH_SIZE  = 64
EPOCHS      = 5           # Increase for better accuracy (try 30–50)
LEARNING_RATE = 0.001
DATA_DIR    = "data/PlantVillage"
MODEL_SAVE_PATH = "model/plant_disease_model.h5"
LABELS_SAVE_PATH = "model/class_labels.json"

# ─── Image Augmentation ───────────────────────────────────────────────────────
# Augmentation artificially increases dataset diversity to reduce overfitting
train_datagen = ImageDataGenerator(
    rescale=1./255,              # Normalize pixel values to [0, 1]
    rotation_range=40,           # Random rotation up to 40°
    width_shift_range=0.2,       # Horizontal shift
    height_shift_range=0.2,      # Vertical shift
    shear_range=0.2,             # Shearing
    zoom_range=0.2,              # Random zoom
    horizontal_flip=True,        # Mirror images
    fill_mode='nearest',         # Fill empty pixels after transform
    validation_split=0.2         # 20% of data for validation
)

# Validation data: only rescale (no augmentation)
val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

def load_data():
    """Load training and validation datasets from directory."""
    print("📂 Loading dataset...")

    train_generator = train_datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )

    val_generator = val_datagen.flow_from_directory(
        DATA_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    # Save class labels mapping: {0: 'Apple___Apple_scab', 1: ...}
    class_indices = train_generator.class_indices
    labels = {v: k for k, v in class_indices.items()}
    with open(LABELS_SAVE_PATH, 'w') as f:
        json.dump(labels, f, indent=2)
    print(f"✅ Found {len(labels)} classes. Labels saved to {LABELS_SAVE_PATH}")

    return train_generator, val_generator, len(labels)


def build_model(num_classes):
    """
    Build Transfer Learning model using MobileNetV2.

    Architecture:
      MobileNetV2 (pretrained on ImageNet, frozen) →
      GlobalAveragePooling2D →
      Dense(256, ReLU) → Dropout(0.5) →
      Dense(num_classes, Softmax)
    """
    print("🔧 Building MobileNetV2 transfer learning model...")

    # Load MobileNetV2 without top classification layers
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,          # Remove ImageNet classifier
        weights='imagenet'          # Use pretrained weights
    )

    # Phase 1: Freeze base model — only train our new top layers
    base_model.trainable = False

    # Build full model
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),        # Convert feature maps → vector
        layers.Dense(256, activation='relu'),   # Fully connected layer
        layers.Dropout(0.5),                    # Regularization (prevent overfitting)
        layers.Dense(num_classes, activation='softmax')  # Output: probability per class
    ])

    model.compile(
        optimizer=optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    model.summary()
    return model, base_model


def fine_tune_model(model, base_model):
    """
    Phase 2: Unfreeze top layers of base model for fine-tuning.
    This lets the pretrained features adapt to plant disease patterns.
    """
    print("🔓 Fine-tuning top layers of MobileNetV2...")
    base_model.trainable = True

    # Only unfreeze the last 30 layers (keep earlier layers frozen)
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    # Use lower learning rate for fine-tuning
    model.compile(
        optimizer=optimizers.Adam(learning_rate=LEARNING_RATE / 10),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


def train(model, train_gen, val_gen, epochs, phase_name="Phase1"):
    """Train the model with callbacks for best model saving and early stopping."""
    cb = [
        # Save only the best model (by val_accuracy)
        callbacks.ModelCheckpoint(
            MODEL_SAVE_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        # Stop training if no improvement for 5 epochs
        callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        # Reduce LR if stuck
        callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=3,
            verbose=1
        )
    ]

    print(f"\n🚀 Training {phase_name}...")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        callbacks=cb
    )
    return history


def plot_history(history1, history2=None):
    """Plot training accuracy and loss curves."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    acc  = history1.history['accuracy']
    val_acc = history1.history['val_accuracy']
    loss = history1.history['loss']
    val_loss = history1.history['val_loss']

    if history2:
        acc     += history2.history['accuracy']
        val_acc += history2.history['val_accuracy']
        loss    += history2.history['loss']
        val_loss+= history2.history['val_loss']

    epochs_range = range(len(acc))

    axes[0].plot(epochs_range, acc,     label='Train Accuracy')
    axes[0].plot(epochs_range, val_acc, label='Val Accuracy')
    axes[0].set_title('Model Accuracy')
    axes[0].legend()

    axes[1].plot(epochs_range, loss,     label='Train Loss')
    axes[1].plot(epochs_range, val_loss, label='Val Loss')
    axes[1].set_title('Model Loss')
    axes[1].legend()

    plt.savefig('model/training_history.png')
    print("📊 Training plot saved to model/training_history.png")
    plt.show()


if __name__ == "__main__":
    # Step 1: Load data
    train_gen, val_gen, num_classes = load_data()

    # Step 2: Build model
    model, base_model = build_model(num_classes)

    # Step 3: Phase 1 training (frozen base)
    history1 = train(model, train_gen, val_gen, epochs=10, phase_name="Phase 1 (Frozen Base)")

    # Step 4: Phase 2 fine-tuning (unfreeze top layers)
    model = fine_tune_model(model, base_model)
    history2 = train(model, train_gen, val_gen, epochs=EPOCHS, phase_name="Phase 2 (Fine-Tuning)")

    # Step 5: Evaluate
    print("\n📈 Evaluating on validation set...")
    loss, acc = model.evaluate(val_gen)
    print(f"✅ Final Validation Accuracy: {acc*100:.2f}%")
    print(f"✅ Final Validation Loss: {loss:.4f}")

    # Step 6: Plot
    plot_history(history1, history2)

    print(f"\n🎉 Model saved to: {MODEL_SAVE_PATH}")
