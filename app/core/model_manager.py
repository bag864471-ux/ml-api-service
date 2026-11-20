import os
import pickle
import tensorflow as tf
from typing import Dict, Optional
import structlog

logger = structlog.get_logger()

class ModelManager:
    """Manages ML model loading, versioning, and caching"""

    def __init__(self):
        self.models: Dict = {}
        self.model_versions: Dict = {}
        self.active_versions: Dict = {}

    async def load_models(self):
        """Load all models from storage"""
        model_dir = os.getenv("MODEL_STORAGE_PATH", "./models")

        if not os.path.exists(model_dir):
            logger.warning("model_directory_not_found", path=model_dir)
            return

        for model_name in os.listdir(model_dir):
            model_path = os.path.join(model_dir, model_name)
            if os.path.isdir(model_path):
                await self.load_model(model_name, model_path)

    async def load_model(self, model_name: str, model_path: str):
        """Load a specific model"""
        try:
            # Load TensorFlow model
            if os.path.exists(os.path.join(model_path, "model.h5")):
                model = tf.keras.models.load_model(os.path.join(model_path, "model.h5"))
                self.models[model_name] = model
                logger.info("model_loaded", model=model_name, type="tensorflow")

            # Load scikit-learn model
            elif os.path.exists(os.path.join(model_path, "model.pkl")):
                with open(os.path.join(model_path, "model.pkl"), "rb") as f:
                    model = pickle.load(f)
                self.models[model_name] = model
                logger.info("model_loaded", model=model_name, type="sklearn")

            # Set active version
            self.active_versions[model_name] = "v1.0.0"

        except Exception as e:
            logger.error("model_load_failed", model=model_name, error=str(e))

    def get_model(self, model_name: str, version: Optional[str] = None):
        """Get a loaded model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")

        return self.models[model_name]

    def list_models(self) -> Dict:
        """List all loaded models"""
        return {
            name: {
                "active_version": self.active_versions.get(name),
                "loaded": True
            }
            for name in self.models.keys()
        }

    async def reload_model(self, model_name: str):
        """Reload a model"""
        if model_name in self.models:
            del self.models[model_name]

        model_path = os.path.join(
            os.getenv("MODEL_STORAGE_PATH", "./models"),
            model_name
        )
        await self.load_model(model_name, model_path)
