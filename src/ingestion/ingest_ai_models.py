"""
Modular AI Model & MLflow Registry Ingestion Connector.
Ingests enterprise AI/ML model metadata, training dataset bindings, and serving endpoints
into ea.bronze.ai_models for EU AI Act compliance auditing and risk classification.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
from src.data_backbone.client import get_unity_catalog_client


class AIModelIngestor:
    """Ingests enterprise AI/ML models into ea.bronze.ai_models."""

    def __init__(self):
        self.client = get_unity_catalog_client()

    def generate_models(self) -> List[Dict[str, Any]]:
        """Generate canonical AI/ML model records across all EU AI Act risk tiers."""
        now = datetime.now(timezone.utc).isoformat()
        return [
            {
                "model_id": "MDL-001-BIOMETRIC-EVALUATOR",
                "model_name": "candidate-biometric-evaluator",
                "version": "v1.4.0",
                "framework": "OpenCV / PyTorch",
                "task_type": "Emotion Recognition & Biometric Evaluation",
                "training_dataset_urn": "urn:ea:database:recruitment-video-corpus",
                "serving_endpoint_urn": "urn:ea:microservice:candidate-evaluation-endpoint",
                "owner_team": "People Analytics AI Team",
                "license": "Proprietary",
                "has_human_in_the_loop": False,
                "timestamp": now,
            },
            {
                "model_id": "MDL-002-FRAUD-RISK-SCORER",
                "model_name": "fraud-risk-scorer-v2",
                "version": "v2.1.0",
                "framework": "PyTorch / MLflow",
                "task_type": "Credit & Fraud Risk Assessment",
                "training_dataset_urn": "urn:ea:database:historical-transaction-ledger",
                "serving_endpoint_urn": "urn:ea:microservice:payments-fraud-scoring-endpoint",
                "owner_team": "Risk Intelligence Team",
                "license": "Proprietary",
                "has_human_in_the_loop": False,
                "timestamp": now,
            },
            {
                "model_id": "MDL-003-CUSTOMER-SUPPORT-LLM",
                "model_name": "customer-support-llm-v1",
                "version": "v1.0.2",
                "framework": "Llama 3 / LangChain",
                "task_type": "Customer Support GenAI Chatbot",
                "training_dataset_urn": "urn:ea:database:support-ticket-kb-corpus",
                "serving_endpoint_urn": "urn:ea:microservice:support-chatbot-endpoint",
                "owner_team": "Customer Support AI Team",
                "license": "Meta Llama 3 Community License",
                "has_human_in_the_loop": True,
                "timestamp": now,
            },
            {
                "model_id": "MDL-004-PRODUCT-RECOMMENDER",
                "model_name": "product-recommender-v3",
                "version": "v3.2.0",
                "framework": "Scikit-learn / LightFM",
                "task_type": "E-Commerce Personalization & Recommendations",
                "training_dataset_urn": "urn:ea:database:catalog-clickstream-mart",
                "serving_endpoint_urn": "urn:ea:microservice:storefront-recommendations-endpoint",
                "owner_team": "Merchandising Algorithms Team",
                "license": "Apache 2.0",
                "has_human_in_the_loop": False,
                "timestamp": now,
            },
        ]

    def ingest(self, models: Optional[List[Dict[str, Any]]] = None) -> int:
        """Persist AI/ML models into ea.bronze.ai_models."""
        if models is None:
            models = self.generate_models()
        count = self.client.save_ai_models(models)
        return count


def main():
    parser = argparse.ArgumentParser(description="Ingest AI/ML models into ea.bronze.ai_models")
    parser.add_argument("--input", help="Optional JSON file containing model records")
    args = parser.parse_args()

    ingestor = AIModelIngestor()
    models = None
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            models = json.load(f)

    count = ingestor.ingest(models)
    print(f"✓ Ingested {count} AI/ML model records into ea.bronze.ai_models")


if __name__ == "__main__":
    main()
