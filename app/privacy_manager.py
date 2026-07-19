import re
import logging

logger = logging.getLogger(__name__)

class PrivacyManager:
    """
    Zero-Trust Security Component: Masks Protected Health Information (PHI)
    before sending data to external LLMs.
    """
    
    # Common PII Regex Patterns
    PATTERNS = {
        "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "PHONE": r'\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
        "SSN": r'\b\d{3}[-]?\d{2}[-]?\d{4}\b',
        "DATE_OF_BIRTH": r'\b(0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])[-/](19|20)\d{2}\b',
    }

    @staticmethod
    def mask_phi(text: str) -> str:
        if not text:
            return text
            
        masked_text = text
        
        # Mask Standard PII
        for entity_type, pattern in PrivacyManager.PATTERNS.items():
            masked_text = re.sub(pattern, f"[PHI_MASKED_{entity_type}]", masked_text)
            
        # Basic Name Masking (Very simplified heuristic for demonstration)
        # In a production environment, you would use a robust NER model like SpaCy en_core_web_trf
        # Here we look for titles followed by capitalized words as a simple heuristic
        name_pattern = r'\b(Mr\.|Mrs\.|Ms\.|Dr\.)\s+[A-Z][a-z]+(\s+[A-Z][a-z]+)?\b'
        masked_text = re.sub(name_pattern, r'\1 [PHI_MASKED_NAME]', masked_text)
        
        if masked_text != text:
            logger.info("PrivacyManager: PHI detected and masked before LLM transmission.")
            
        return masked_text
