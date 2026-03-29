"""
This class contains all the new logics to calculate de Global Engagement Score
based on the new criteria established in 2026.
"""
import numpy as np

class GlobalEngagementScoreNew:

    def __init__ (self, kpi_data: dict, seuil_minimal: float = 0.50) :
        """
        Constructor for the GlobalEngagementScoreNew class.

        Args:
            kpi_data (dict): A dictionary containing all the necessary KPI data for calculations.
            seuil_minimal (float): Minimal threshold for semantic score adjustment. Default is 0.
        """
        self.__s_min:float = seuil_minimal
        self._average_semantic_score:float = kpi_data["data"]["successful_posts"]["global_body_kpi"]["scores"]["average_score"]

        self._draft_kpi:dict = kpi_data['data']['draft_post']
        self._target_kpi:dict = kpi_data['data']['successful_posts']
        self._original_text: str = kpi_data["data"]["orignal_draft_text"]


    def proximity_score(self, draft: float, target: float, max_range: float) -> float:
        """
        Calculate a proximity score between 0 and 1 based on the distance
        between the draft and target values, normalized by the maximum range.

        Args:
            draft (float): The draft value.
            target (float): The target value.
            max_range (float): The maximum range for normalization.
        Returns:
            float: Proximity score between 0 and 1.
        """
        return 1.0 - min(abs(draft - target) / max_range, 1.0)


    def log_length_score(
            self, 
            draft_wc: float, 
            target_wc: float, 
            min_wc: float = 100, 
            min_score: float = 3,
            log_base: float = 1.7
        ) -> float :
        """
        Calculate a logarithmic length score for word count.
        Args:
            draft_wc (float): Word count of the draft.
            target_wc (float): Target word count.
            min_wc (float): Minimum word count threshold.
            min_score (float): Minimum score to return.
            log_base (float): Base of the logarithm for scaling.

        Returns:
            float: Length score between 0 and 1.
        """
        if draft_wc < min_wc:
            return 0.0
        max_wc = max(target_wc, min_wc + 1)
        norm = (draft_wc - min_wc) / (max_wc - min_wc)
        norm = max(0, norm)
        log_score = np.log1p(norm * (log_base - 1)) / np.log(log_base)

        return np.clip(min_score + (10 - min_score) * log_score, 0, 1)
    

    def log_readability_score(
            self,
            draft_read: float, 
            target_read: float, 
            min_score: float = 3, 
            log_base: float = 1.7
        ) -> float :
        """
        Calculate a logarithmic readability score.
        Args:
            draft_read (float): Readability score of the draft.
            target_read (float): Target readability score.
            min_score (float): Minimum score to return.
            log_base (float): Base of the logarithm for scaling.
        Returns:
            float: Readability score between 0 and 1.
        """
        # Score max si le draft est plus lisible que la cible
        if draft_read >= target_read:
            return 1.0
        
        max_read = max(target_read, draft_read + 1)
        norm = (draft_read) / (max_read)
        log_score = np.log1p(norm * (log_base - 1)) / np.log(log_base)
        return np.clip(min_score + (10 - min_score) * log_score, 0, 1)

    # --------------------------------- PRIVATE INTERNAL METHODS --------------------------------- #

    def __calculate_title_features_scores(
            self,
            title_length_weight: float = 0.6,
            subjectivity_weight: float = 0.2,
            polarity_weight: float = 0.2
        ) -> tuple [float, list[str]]:
        """
        STEP 1: Retrieve target and draft values for title features.
        STEP 2: Calculate proximity scores for each feature using realistic ranges.
        STEP 3: Weighted combination and normalization.
        STEP 4: Return score between 0 and 10.
        STEP 5: Generate advice based on title features.

        Returns:
            tuple[float, list[str]]: Title score between 0 and 10 and list of advice strings.
        """

        # STEP 1: Retrieve target and draft values
        target_length = self._target_kpi['global_title_kpi']["average_title_length"]
        target_polarity = self._target_kpi['global_title_kpi']["average_title_polarity"]
        target_subjectivity = self._target_kpi['global_title_kpi']["average_title_subjectivity"]

        draft_length = self._draft_kpi["title_kpi"]["average_title_length"]
        draft_polarity = self._draft_kpi["title_kpi"]["average_title_polarity"]
        draft_subjectivity = self._draft_kpi["title_kpi"]["average_title_subjectivity"]

        # STEP 2: Proximity score with realistic ranges
        max_length_range = max(target_length, draft_length, 10)
        max_polarity_range = 2.0  # polarité entre -1 et 1
        max_subjectivity_range = 1.0  # subjectivité entre 0 et 1

        length_score = self.proximity_score(draft_length, target_length, max_length_range)
        polarity_score = self.proximity_score(draft_polarity, target_polarity, max_polarity_range)
        subjectivity_score = self.proximity_score(draft_subjectivity, target_subjectivity, max_subjectivity_range)

        # STEP 3: Weighted combination and normalization
        denominator = title_length_weight + polarity_weight + subjectivity_weight
        if denominator == 0:
            denominator = 0.1  # Avoid division by zero

        combined_score = (
            (length_score * title_length_weight) +
            (polarity_score * polarity_weight) +
            (subjectivity_score * subjectivity_weight)
        ) / denominator

        # STEP 4: Scale to 0-10 and return
        title_score: float = np.clip(combined_score * 10, 0, 10)

        # STEP 5: Generate advice
        advice_list = self.generate_title_advice(
            target_length,
            draft_length,
            target_polarity,
            draft_polarity,
            target_subjectivity,
            draft_subjectivity
        )

        return round(title_score, 2) , advice_list


    def __calculate_body_features_scores(
            self,
            body_length_weight: float = 0.5,
            subjectivity_weight: float = 0.2,
            polarity_weight: float = 0.2,
            readability_weight: float = 0.1
        ) -> float:
        """
        STEP 1: Retrieve target and draft values for body features.
        STEP 2: Calculate proximity scores for each feature using realistic ranges and logarithmic scaling for length and readability.
        STEP 3: Weighted combination and normalization.
        STEP 4: Return score between 0 and 10.
        """

        # STEP 1: Retrieve target and draft values
        target_length = self._target_kpi['global_body_kpi']["words_and_sentences"]["average_word_count"]
        target_polarity = self._target_kpi['global_body_kpi']["polarity_and_readability_subjectivity"]["average_polarity"]
        target_subjectivity = self._target_kpi['global_body_kpi']["polarity_and_readability_subjectivity"]["average_subjectivity"]
        target_readability = self._target_kpi['global_body_kpi']["polarity_and_readability_subjectivity"]["average_readability_score"]

        draft_length = self._draft_kpi["body_kpi"]["words_and_sentences"]["average_word_count"]
        draft_polarity = self._draft_kpi["body_kpi"]["polarity_and_readability_subjectivity"]["average_polarity"]
        draft_subjectivity = self._draft_kpi["body_kpi"]["polarity_and_readability_subjectivity"]["average_subjectivity"]
        draft_readability = self._draft_kpi["body_kpi"]["polarity_and_readability_subjectivity"]["average_readability_score"]

        # STEP 2: Calculate individual feature scores
        length_score = self.log_length_score(draft_length, target_length)
        polarity_score = self.proximity_score(draft_polarity, target_polarity, 2.0)  # polarité entre -1 et 1
        subjectivity_score = self.proximity_score(draft_subjectivity, target_subjectivity, 1.0)  # subjectivité entre 0 et 1
        readability_score = self.log_readability_score(draft_readability, target_readability)

        # STEP 3: Weighted combination and normalization
        denominator = body_length_weight + polarity_weight + subjectivity_weight + readability_weight
        
        if denominator > 1 :
            body_length_weight /= denominator
            polarity_weight /= denominator
            subjectivity_weight /= denominator
            readability_weight /= denominator

        combined_score = (
            (length_score * body_length_weight) +
            (polarity_score * polarity_weight) +
            (subjectivity_score * subjectivity_weight) +
            (readability_score * readability_weight)
        )
        # STEP 4: Scale to 0-10 and return
        body_score = np.clip(combined_score * 10, 0, 10)


        # Step 5: Generate advice
        advice_list = self.generate_body_advice(
            target_length,
            draft_length,
            target_polarity,
            draft_polarity,
            target_subjectivity,
            draft_subjectivity,
            target_readability,
            draft_readability
        )


        return round(body_score, 2), advice_list


    def __calculate_substance_features_scores(self) -> float:
        """
        This method calculates the scores for all substance features.
        These features include the number of most used words used in the body.

        Returns:
            float: Combined substance score between 0 and 10.
        """

        # STEP 1 : EXTRACT MOST USED WORDS FROM TARGET KPI (list of tuples)
        target_most_used_words = self._target_kpi['global_body_kpi']["words_and_sentences"]["most_used_words"]
        # Convert to set of words
        target_words_set = set(word for word, count in target_most_used_words)
        number_of_target_words = len(target_words_set)

        # STEP 2 : EXTRACT WORDS FROM DRAFT (assuming self._original_text is a string)
        # Tokenize the draft text into words (simple split, can be improved)
        draft_words = set(self._original_text.lower().split())

        # STEP 3 : CALCULATE THE OVERLAP BETWEEN THE TWO SETS OF WORDS
        common_words = target_words_set.intersection(draft_words)
        number_of_common_words = len(common_words)

        # STEP 4 : CALCULATE THE SUBSTANCE SCORE BASED ON THE OVERLAP
        if number_of_target_words > 0:


            substance_score = np.log1p(number_of_common_words) / np.log1p(number_of_target_words) * 10

            # STEP 5 : Generate advice based on substance features
            if substance_score < 6:
                advice = ["Substance: Consider incorporating more relevant keywords and phrases that are commonly used in successful posts to enhance the substance of your content."]
                return float(np.clip(substance_score, 0, 10)), advice
            
            return float(np.clip(substance_score, 0, 10)) , []
        
        return 0.0 , ["Substance: Consider incorporating more relevant keywords and phrases that are commonly used in successful posts to enhance the substance of your content."]


    def __calculate_semantic_features_scores (self) -> float:
        """
        This method retrieves the precomputed average semantic similarity score
        between the draft and the set of successful posts.
        This score is used as a confidence multiplier for the final score.

        Returns:
            float: Semantic similarity score between 0 and 1.
        """
        
        # STEP 1 : RETRIEVE THE AVERAGE SEMANTIC SIMILARITY SCORE
        s_avg:float = self._average_semantic_score

        # STEP 2 : RETURN THE SEMANTIC SIMILARITY SCORE
        normalized_score = np.clip(s_avg, 0, 1)

        # STEP 3 : generate advice based on semantic score
        advice_list = self.generate_semantic_advice(normalized_score)

        return normalized_score, advice_list


    def generate_title_advice(
            self,
            target_length: int,
            draft_length: int,
            target_polarity: float,
            draft_polarity: float,
            target_subjectivity: float,
            draft_subjectivity: float
        ) -> list[str]:
        """
        This method generates advice for improving the title based on its features.

        Args:
            target_length (int): Target title length.
            draft_length (int): Draft title length.
            target_polarity (float): Target title polarity.
            draft_polarity (float): Draft title polarity.
            target_subjectivity (float): Target title subjectivity.
            draft_subjectivity (float): Draft title subjectivity.

        Returns:
            list[str]: A list of advice strings.
        """

        advice_list: list[str] = []

        # Advice on length
        if draft_length < target_length * 0.8:
            advice_list.append("Title (Length): Consider increasing the title length to better capture attention.")
        elif draft_length > target_length * 1.2:
            advice_list.append("Title (Length): Consider shortening the title to make it more concise and impactful.")

        # Advice on polarity
        if draft_polarity < target_polarity - 0.2:
            advice_list.append("Title (Polarity): Try to make the title more positive to engage readers for example by highlighting benefits or solutions.")
        elif draft_polarity > target_polarity + 0.2:
            advice_list.append("Title (Polarity): Try to make the title more neutral or balanced to avoid alienating readers.")

        # Advice on subjectivity
        if draft_subjectivity < target_subjectivity - 0.2:
            advice_list.append("Title (Subjectivity): Consider adding more personal or emotional elements to the title to connect with readers.")
        elif draft_subjectivity > target_subjectivity + 0.2:
            advice_list.append("Title (Subjectivity): Consider making the title more objective and fact-based to enhance credibility.")

        return advice_list
    

    def generate_body_advice(
            self,
            target_length: int,
            draft_length: int,
            target_polarity: float,
            draft_polarity: float,
            target_subjectivity: float,
            draft_subjectivity: float,
            target_readability: float,
            draft_readability: float
        ) -> list[str]:
        """
        This method generates advice for improving the body based on its features.

        Args:
            target_length (int): Target body length.
            draft_length (int): Draft body length.
            target_polarity (float): Target body polarity.
            draft_polarity (float): Draft body polarity.
            target_subjectivity (float): Target body subjectivity.
            draft_subjectivity (float): Draft body subjectivity.
            target_readability (float): Target body readability.
            draft_readability (float): Draft body readability.

        Returns:
            list[str]: A list of advice strings.
        """

        advice_list: list[str] = []

        # Advice on length
        if draft_length < target_length * 0.8:
            advice_list.append("Body (Length): Consider increasing the body length to provide more comprehensive information.")
        elif draft_length > target_length * 1.2:
            advice_list.append("Body (Length): Consider shortening the body to maintain reader engagement and focus.")

        # Advice on polarity
        if draft_polarity < target_polarity - 0.2:
            advice_list.append("Body (Polarity): Try to make the body more positive to engage readers for example by highlighting benefits or solutions.")
        elif draft_polarity > target_polarity + 0.2:
            advice_list.append("Body (Polarity): Try to make the body more neutral or balanced to avoid alienating readers.")

        # Advice on subjectivity
        if draft_subjectivity < target_subjectivity - 0.2:
            advice_list.append("Body (Subjectivity): Consider adding more personal or emotional elements to the body to connect with readers.")
        elif draft_subjectivity > target_subjectivity + 0.2:
            advice_list.append("Body (Subjectivity): Consider making the body more objective and fact-based to enhance credibility.")
        # Advice on readability
        if draft_readability < target_readability - 5:
            advice_list.append("Body (Readability): Work on improving the readability of the body by using simpler language and shorter sentences.")
        elif draft_readability > target_readability + 5:
            advice_list.append("Body (Readability): Consider using more complex language and varied sentence structures to enhance engagement.")

        return advice_list


    def generate_semantic_advice(
            self, 
            semantic_score: float
        ) -> list[str]:
        """
        This method generates advice for improving the semantic similarity score.

        Args:
            semantic_score (float): The current semantic similarity score.
        Returns:
            list[str]: A list of advice strings.
        """
        
        advice_list: list[str] = []

        if semantic_score < 0.7:
            advice_list.append("Semantic Similarity: Consider aligning the content more closely with successful posts by incorporating similar themes and language.")
        
        return advice_list


    def calculate_global_score (
            self,
            title_weight:float = 0.4,
            body_weight:float = 0.4,
            substance_weight:float = 0.2
        ) -> dict[str, float] :
        """
        This method calculates the Global Engagement Score based on the new criteria.
        It combines all the individual feature scores with their respective weights.
        It also applies the semantic score as a multiplier to the final score.

        args:
            title_weight (float): Weight for the title score.
            body_weight (float): Weight for the body score.
            substance_weight (float): Weight for the substance score.
        Returns:
            dict[str, float]: A dictionary containing the final global score and individual feature scores.
        """

        # STEP 0 : INITIALIZE SCORES
        global_score:float = 0.0
        features_dict:dict[str, float] = dict()

        # Check if weights sum to 1
        total_weight = title_weight + body_weight + substance_weight
        
        if total_weight != 1.0:
            title_weight /= total_weight
            body_weight /= total_weight
            substance_weight /= total_weight

        # STEP 1 : CALCULATE TITLE FEATURES SCORE
        title_score , advice_list = self.__calculate_title_features_scores()

        # STEP 2 : CALCULATE BODY FEATURES SCORE
        body_score, body_advice_list = self.__calculate_body_features_scores()

        # STEP 3 : CALCULATE SUBSTANCE FEATURES SCORE
        substance_score, substance_advice_list = self.__calculate_substance_features_scores()

        # STEP 4 : CALCULATE SEMANTIC FEATURES SCORE
        semantic_score, semantic_advice_list = self.__calculate_semantic_features_scores()

        features_dict["title_score"] = round(title_score, 2)            # Score between 0 and 10
        features_dict["body_score"] = round(body_score, 2)              # Score between 0 and 10
        features_dict["substance_score"] = round(substance_score, 2)    # Score between 0 and 10
        features_dict["semantic_score"] = round(semantic_score, 2)      # Score between 0 and 1

        # STEP 5 : COMBINE ALL FEATURE SCORES WITH THEIR RESPECTIVE WEIGHTS
        combined_score:float = (
            (title_score * title_weight) +
            (body_score * body_weight) +
            (substance_score * substance_weight)
        )

        # STEP 5.1 : COLLECT ALL ADVICE LISTS
        all_advices = advice_list + body_advice_list + substance_advice_list + semantic_advice_list

        # STEP 6 : APPLY SEMANTIC SCORE AS A MULTIPLIER
        global_score = (semantic_score**1.25) * (combined_score) * 10
        global_score = np.clip(global_score, 0, 100)
        global_score = round(global_score, 2)
        
        label:str = ""

        # --- Attribution du Label ---
        if global_score <= 45:
            label = "Bad"
        elif global_score <= 65:
            label = "Medium"
        elif global_score <= 80:
            label = "Good"
        else:
            label = "Really Good"

        return {
            "score_ges": float(global_score),
            "label": label,
            "factors": features_dict,
            "semantic_similarity_avg": semantic_score,
            "advices": all_advices
        }