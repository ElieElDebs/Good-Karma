import numpy as np


class DynamicGESCalculator:
    """
    Calcule le Score d'Engagement Global (GES) d'un brouillon en utilisant des cibles
    dynamiques (TARGET_*) extraites des 'successful_posts' pertinents pour ce brouillon.

    Cette approche garantit que le GES est spécifique au contexte sémantique.
    """

    def __init__(self, full_kpi_data: dict):
        """
        Initialise le calculateur en extrayant les KPI du brouillon (draft) et les cibles (targets)
        à partir du dictionnaire de données complet.
        :param full_kpi_data: Le dictionnaire JSON contenant 'draft_post' et 'successful_posts'.
        """

        try:
            data = full_kpi_data["data"]
            self.original_draft_text = data["orignal_draft_text"]
            self.draft_kpi = data["draft_post"]
            successful_posts_kpi = data["successful_posts"]
        except KeyError:
            raise ValueError(
                "La structure de données JSON est incorrecte. Les clés 'data', 'draft_post' ou 'successful_posts' sont manquantes."
            )

        # CONSTANT
        self.S_MIN = 0.7  # Seuil minimal de similarité pour F_Sémantique.
        self.LENGTH_MIN_THRESHOLD = (
            100  # Mots minimum pour commencer à avoir un score > 0.
        )
        self.LENGTH_MIN_SCORE = 3  # Score de base à 3 mots.

        # Poids Statégiques (w_i) - Les pondérations restent fixes
        self.W_TITLE = 3.0
        self.W_READABILITY = 2.0
        self.W_LENGTH = 1
        self.W_SEMANTIC = 3.0
        # Ajoute un poids pour le facteur lexical
        self.W_LEXICAL = 1.5
        self.W_TOTAL = (
            self.W_TITLE + self.W_READABILITY + self.W_LENGTH + self.W_SEMANTIC
        )
        self.W_TOTAL_STRUCT = (
            self.W_TITLE + self.W_READABILITY + self.W_LENGTH + self.W_LEXICAL
        )
        self.CRITICAL_ADVICE_THRESHOLD = (
            5.0  # Seuil pour générer des conseils stratégiques.
        )

        # --- Extraction des Cibles Dynamiques (TARGET_*) ---
        # TARGET_POLARITY (global_title_kpi > average_title_polarity)
        self.TARGET_POLARITY = self._get_target_kpi_value(
            successful_posts_kpi, ["global_title_kpi", "average_title_polarity"]
        )
        # TARGET_READABILITY (global_body_kpi > readability)
        # NOTE: Le chemin pour body_kpi est ajusté pour un scénario réaliste (même si non visible entièrement dans le snippet).
        self.TARGET_READABILITY = self._get_target_kpi_value(
            successful_posts_kpi,
            [
                "global_body_kpi",
                "polarity_and_readability_subjectivity",
                "average_readability_score",
            ],
            default_value=71.52,
        )
        # TARGET_WORD_COUNT (global_body_kpi > word_count)
        self.TARGET_WORD_COUNT = self._get_target_kpi_value(
            successful_posts_kpi,
            ["global_body_kpi", "words_and_sentences", "average_word_count"],
            default_value=323.7,
        )

        # Calcul du Diviseur de Pente (LENGTH_SLOPE_DIVISOR)
        # Calibré pour atteindre le score max (10) au TARGET_WORD_COUNT
        length_range = self.TARGET_WORD_COUNT - self.LENGTH_MIN_THRESHOLD
        score_range = 10 - self.LENGTH_MIN_SCORE
        self.LENGTH_SLOPE_DIVISOR = (
            length_range / score_range if score_range != 0 else 1.0
        )

        # Pour la logique logarithmique, on fixe une base pour la croissance
        self.LENGTH_LOG_BASE = 1.7  # Ajustable pour tuning de la courbe

        # Récupère les mots les plus utilisés (top 20 par exemple)
        self.MOST_USED_WORDS = []
        try:
            self.MOST_USED_WORDS = [
                w
                for w, _ in successful_posts_kpi.get("global_body_kpi", {})
                .get("words_and_sentences", {})
                .get("most_used_words", [])[:20]
            ]
        except Exception:
            pass

    def _get_target_kpi_value(self, kpi_dict: dict, keys: list, default_value=0.0):
        """
        Récupère une valeur KPI imbriquée du dictionnaire en gérant les KeyError.
        """
        current = kpi_dict
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default_value
        return current

    def _get_draft_kpi_value(self, keys: list, default_value=0.0):
        """
        Récupère une valeur KPI imbriquée du dictionnaire du brouillon.
        """
        current = self.draft_kpi
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default_value
        return current

    def _calculate_lexical_factor(self, text: str) -> float:
        """
        Calcule la proportion de mots fréquents présents dans le texte.

        :param text: Le texte du brouillon.
        :return: Le facteur lexical F_Lexical [0 à 10].
        """
        text_words = set(w.lower() for w in text.split())

        if not self.MOST_USED_WORDS:
            return 5.0

        count = sum(1 for w in self.MOST_USED_WORDS if w in text_words)

        return round(10 * count / len(self.MOST_USED_WORDS), 2)

    def _calculate_factors(self, semantic_similarity_avg: float) -> dict:
        """
        Calcule les quatre facteurs normalisés (F_i) [0 à 10] en utilisant les cibles dynamiques.
        """
        # --- Extraction des Valeurs Brutes du Brouillon ---
        draft_polarity = self._get_draft_kpi_value(
            ["title_kpi", "average_title_polarity"], default_value=0.0
        )
        draft_readability = self._get_draft_kpi_value(
            [
                "body_kpi",
                "polarity_and_readability_subjectivity",
                "average_readability_score",
            ],
            default_value=self.TARGET_READABILITY,
        )
        draft_word_count = self._get_draft_kpi_value(
            ["body_kpi", "words_and_sentences", "average_word_count"], default_value=0
        )

        factors = {}

        # 1. Facteur du Titre (F_Titre)
        denom = self.TARGET_POLARITY + 0.1
        if denom == 0:
            F_Titre = 0.0
        else:
            F_Titre = 10 * np.clip((draft_polarity - (-0.1)) / denom, 0, 1)
        factors["F_Titre"] = round(float(F_Titre), 2)

        # 2. Facteur de Lisibilité (F_Lisibilité) - asymétrique
        # Si le texte est plus simple (score > cible), pas de pénalité
        if draft_readability >= self.TARGET_READABILITY:
            F_Lisibilité = 10.0
        else:
            F_Lisibilité = np.clip(
                10 - np.abs(draft_readability - self.TARGET_READABILITY) / 2.5, 0, 10
            )
        factors["F_Lisibilité"] = round(float(F_Lisibilité), 2)

        # 3. Facteur de Longueur du Corps (F_Longueur) - progression logarithmique
        if draft_word_count < self.LENGTH_MIN_THRESHOLD:
            F_Longueur = 0.0
        else:
            # Logarithmic scaling: fast gain up to target, diminishing returns after
            max_wc = max(self.TARGET_WORD_COUNT, self.LENGTH_MIN_THRESHOLD + 1)
            # Normalized log: log(1 + (words - min) / (target - min))
            norm = (draft_word_count - self.LENGTH_MIN_THRESHOLD) / (
                max_wc - self.LENGTH_MIN_THRESHOLD
            )
            norm = max(0, norm)
            # log_base(1 + norm * (base-1)) to get 0 at min, 1 at target
            log_score = np.log1p(norm * (self.LENGTH_LOG_BASE - 1)) / np.log(
                self.LENGTH_LOG_BASE
            )
            F_Longueur = np.clip(
                self.LENGTH_MIN_SCORE + (10 - self.LENGTH_MIN_SCORE) * log_score, 0, 10
            )
        factors["F_Longueur"] = round(float(F_Longueur), 2)

        # 4. Facteur Sémantique (F_Sémantique) - gatekeeper
        if semantic_similarity_avg < self.S_MIN:
            F_Sémantique = 0.0
        else:
            normalized_slope = (semantic_similarity_avg - self.S_MIN) / (1 - self.S_MIN)
            F_Sémantique = 10 * np.clip(normalized_slope, 0, 1)
        factors["F_Sémantique"] = round(float(F_Sémantique), 2)

        # Ajoute le facteur lexical
        draft_text = self._get_draft_kpi_value(["body_kpi", "text"], default_value="")
        F_Lexical = self._calculate_lexical_factor(self.original_draft_text)
        factors["F_Lexical"] = F_Lexical

        return factors

    def generate_advice_list(self, results: dict) -> list[str]:
        """
        Génère une liste de conseils stratégiques reflétant la nouvelle logique.
        """
        advice_list = []
        factors = results["factors"]
        targets = results["targets_used"]

        # Score de confiance (multiplicateur)
        semantic_similarity_avg = results.get("semantic_similarity_avg", None)
        if semantic_similarity_avg is None:
            # fallback : approx via F_Sémantique
            semantic_similarity_avg = factors["F_Sémantique"] / 10.0

        confidence_multiplier = (
            semantic_similarity_avg**1.5 if semantic_similarity_avg > 0 else 0.0
        )

        # Conseil prioritaire si la confiance est basse
        if confidence_multiplier < 0.5:
            advice_list.append(
                "Your topic is not semantically aligned with successful posts in this community. Even with a well-structured post, chances of high engagement are low unless you adapt your subject to match what works here."
            )

        # --- 1. Semantic Alignment Advice ---
        score = factors["F_Sémantique"]
        if score < self.CRITICAL_ADVICE_THRESHOLD:
            if score <= 5.0:
                advice_list.append(
                    f"Semantic alignment ({score:.2f}/10): Your topic is poorly aligned with successful posts. Consider changing the angle or focus to better match the community's core interests."
                )
            else:
                advice_list.append(
                    f"Semantic alignment ({score:.2f}/10): The semantic link is moderate. Explicitly integrate keywords and vocabulary used by the successful posts in this category."
                )

        # --- 2. Title Advice ---
        score = factors["F_Titre"]
        if score < self.CRITICAL_ADVICE_THRESHOLD:
            draft_polarity = self._get_draft_kpi_value(
                ["title_kpi", "average_title_polarity"]
            )
            advice_list.append(
                f"Title hook ({score:.2f}/10): Your title's polarity ({draft_polarity:.2f}) is far from the target ({targets['polarity']:.2f}). Use strong, positive emotional language or utility (e.g., 'How to', numbers, 'I Learned') to capture initial clicks."
            )

        # --- 3. Length Advice ---
        score = factors["F_Longueur"]
        if score < self.CRITICAL_ADVICE_THRESHOLD:
            draft_word_count = self._get_draft_kpi_value(
                ["body_kpi", "words_and_sentences", "average_word_count"]
            )
            words_needed = targets["word_count"] - draft_word_count
            advice_list.append(
                f"Substance/Length ({score:.2f}/10): Aim for approximately {targets['word_count']:.0f} words. You need about {max(0, words_needed):.0f} more words. Longer posts are often perceived as more detailed and authoritative in this context."
            )

        # --- 4. Readability Advice ---
        score = factors["F_Lisibilité"]
        draft_readability = self._get_draft_kpi_value(
            [
                "body_kpi",
                "polarity_and_readability_subjectivity",
                "average_readability_score",
            ]
        )
        if draft_readability < targets["readability"]:
            if score < 8.5:
                advice_list.append(
                    f"Readability ({score:.2f}/10): Your Flesch readability score ({draft_readability:.2f}) is below the target ({targets['readability']:.2f}). Try to simplify your sentences, use shorter words, and avoid complex structures to make your text easier to read."
                )

        if not advice_list:
            advice_list.append(
                "The core of your post is strong. Focus only on minor improvements."
            )

        return advice_list

    def calculate_ges(self, semantic_similarity_avg: float) -> dict:
        """
        Calcule le Score d'Engagement Global (GES) avec gatekeeper logic.

        :param semantic_similarity_avg: La similarité sémantique moyenne entre le brouillon et les posts réussis.
        :return: Un dictionnaire contenant le score GES, le label, les facteurs,
        """
        factors = self._calculate_factors(semantic_similarity_avg)

        # --- Calcul du Score Structurel (hors sémantique) ---
        numerator = (
            self.W_TITLE * factors["F_Titre"]
            + self.W_READABILITY * factors["F_Lisibilité"]
            + self.W_LENGTH * factors["F_Longueur"]
            + self.W_LEXICAL * factors["F_Lexical"]
        )
        w_struct = self.W_TOTAL_STRUCT
        score_struct = (numerator / w_struct) * 10  # sur 10

        # --- Multiplicateur de confiance (semantic gatekeeper) ---
        confidence_multiplier = (
            semantic_similarity_avg**1.5 if semantic_similarity_avg > 0 else 0.0
        )
        score_ges = score_struct * confidence_multiplier
        score_ges = np.clip(score_ges, 0, 100)

        # --- Attribution du Label ---
        if score_ges <= 45:
            label = "Bad"
        elif score_ges <= 65:
            label = "Medium"
        elif score_ges <= 85:
            label = "Good"
        else:
            label = "Really Good"

        return {
            "score_ges": float(score_ges),
            "label": label,
            "factors": factors,
            "targets_used": {
                "readability": self.TARGET_READABILITY,
                "polarity": self.TARGET_POLARITY,
                "word_count": self.TARGET_WORD_COUNT,
            },
            "semantic_similarity_avg": semantic_similarity_avg,  # pour advice
        }
