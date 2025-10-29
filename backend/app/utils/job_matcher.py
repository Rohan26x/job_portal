from typing import List, Dict
from openai import OpenAI
from app.core.config import settings
import json


class JobMatcher:
    """AI-powered job matching system"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def calculate_match_score(
            self,
            candidate_profile: Dict,
            job_description: Dict
    ) -> Dict:
        """Calculate match score between candidate and job using AI"""

        prompt = f"""
        You are a job matching expert. Analyze the candidate profile and job requirements below.
        Calculate a match score from 0-100 and provide reasoning.

        Candidate Profile:
        - Skills: {candidate_profile.get('skills', [])}
        - Education: {candidate_profile.get('education', [])}
        - Experience: {candidate_profile.get('work_experience', [])}
        - Summary: {candidate_profile.get('summary', '')}

        Job Requirements:
        - Title: {job_description.get('job_title', '')}
        - Description: {job_description.get('description', '')}
        - Location: {job_description.get('location', '')}

        Return JSON with:
        - match_score (0-100)
        - reasoning (string explaining the match)
        - matched_skills (list of skills that match)
        - missing_skills (list of skills candidate lacks)
        - recommendations (string with suggestions for candidate)
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert job matching analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )

            result = response.choices[0].message.content
            match_data = json.loads(result)
            return match_data

        except Exception as e:
            print(f"Error calculating match score: {e}")
            return {
                "match_score": 0,
                "reasoning": "Error calculating match",
                "matched_skills": [],
                "missing_skills": [],
                "recommendations": ""
            }

    def find_best_matching_jobs(
            self,
            candidate_profile: Dict,
            jobs: List[Dict],
            top_n: int = 10
    ) -> List[Dict]:
        """Find best matching jobs for a candidate"""

        job_matches = []

        for job in jobs:
            match_result = self.calculate_match_score(candidate_profile, job)
            job_matches.append({
                "job": job,
                "match_score": match_result.get("match_score", 0),
                "reasoning": match_result.get("reasoning", ""),
                "matched_skills": match_result.get("matched_skills", []),
                "missing_skills": match_result.get("missing_skills", [])
            })

        # Sort by match score descending
        job_matches.sort(key=lambda x: x["match_score"], reverse=True)

        return job_matches[:top_n]

    def search_jobs_by_description(
            self,
            search_query: str,
            jobs: List[Dict]
    ) -> List[Dict]:
        """AI-powered job search based on natural language description"""

        prompt = f"""
        A job seeker described what they're looking for:
        "{search_query}"

        Analyze this description and extract:
        - desired_roles (list of job titles/roles they want)
        - key_skills (list of skills they mentioned or implied)
        - preferred_location (if mentioned)
        - experience_level (entry/mid/senior if mentioned)
        - other_preferences (any other requirements)

        Return as JSON.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a job search assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            result = response.choices[0].message.content
            search_criteria = json.loads(result)

            # Filter jobs based on extracted criteria
            filtered_jobs = self._filter_jobs_by_criteria(jobs, search_criteria)

            return filtered_jobs

        except Exception as e:
            print(f"Error in AI job search: {e}")
            return jobs

    def _filter_jobs_by_criteria(self, jobs: List[Dict], criteria: Dict) -> List[Dict]:
        """Filter jobs based on extracted criteria"""
        filtered = []

        for job in jobs:
            score = 0

            # Check title match
            desired_roles = criteria.get("desired_roles", [])
            for role in desired_roles:
                if role.lower() in job.get("job_title", "").lower():
                    score += 30

            # Check location
            preferred_location = criteria.get("preferred_location", "")
            if preferred_location and preferred_location.lower() in job.get("location", "").lower():
                score += 20

            # Check skills in description
            key_skills = criteria.get("key_skills", [])
            job_desc = job.get("description", "").lower()
            for skill in key_skills:
                if skill.lower() in job_desc:
                    score += 10

            if score > 0:
                job["relevance_score"] = score
                filtered.append(job)

        # Sort by relevance
        filtered.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

        return filtered
