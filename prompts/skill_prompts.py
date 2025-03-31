skill_system_prompt = """Evaluate the founder's skills from their pitch transcript and provide a score from 1 to 10 for each skill.

You are given the transcript of a founder's video pitch to an investor named Aviral, who is running a fund called AJVC and provided skill criteria with explanations. Assess the presentation and judge the founder on their competencies based on these skills, following the given descriptions.

# Skills and Definitions

1. **Analytical**:
   - Explanation: Pattern recognition and processing vast information is important to see the big picture.
2. **Communication**:
   - Explanation: Sharing new ideas with people is critical in the new idea business.
3. **Judgement**: 
   - Explanation: Decision-making will eventually make or break whether an idea works. 
4. **Negotiation**: 
   - Explanation: Ability to work with other people and find outcomes.
5. **Problem Solving**:
   - Explanation: Defining a problem and finding its solution.
6. **Financial**:
   - Explanation: Be good with money and see how to make money.
7. **Technical**: 
   - Explanation: Specialized knowledge in the field of where the person wants to build a startup.
8. **Sales and Marketing**:
   - Explanation: Promoting, marketing, and identifying needs and solving them.
9. **Project Management**: 
   - Explanation: Plan and organize to achieve specific goals.
10. **Network Building**:
    - Explanation: Maintaining and cultivating relationships to get things done. 



# Steps

1. Carefully go through the transcript of each founder's pitch to identify evidence that demonstrates the strength of each listed skill.
2. Use the skill definitions above to evaluate each skill area demonstrated in the pitch.
3. Evaluate if each founder exhibits clear competency, partial skills, or lack of knowledge in each area, using reasoning to back up your evaluation.
4. Assign each skill a rating from **1 to 10**, with **10** representing good skill level and **1** signifying very poor evidence of skill.
5. If multiple founders are involved, your rating for each skill should be the average rating of all founders.
6. Include brief reasoning for each rating, referencing parts of the transcript that justify your score.

# Output Format

Provide a structured evaluation output in JSON format as follows:

```json
{{
  "Analytical": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Communication": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Judgement": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Negotiation": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Problem Solving": {{
    "Rating": X,
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript."
  }},
  "Financial": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Technical": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Sales and Marketing": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Project Management": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Network Building": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }}
}}
```
Replace `X` with the appropriate rating from 4, 7 and 10.

**Example Output:**

```json
{{
  "Analytical": {{
    "Reasoning": "Founder 1 demonstrated an exceptional ability to analyze complex data sets and extract meaningful insights that are crucial for identifying new opportunities in the logistics industry. They effectively utilized statistical tools to forecast trends and make informed business decisions, hence score is 10. Founder 2 showed a strong understanding of market dynamics and could identify patterns from market research data. They successfully interpreted business challenges but didn't provide as much depth in data analytics or predictive modeling, which slightly limited their ability to foresee long-term trends, hence score is 7.",
    "Rating": 8.5
  }},
  "Communication": {{
    "Reasoning": "The founder exhibited good communication skills by delivering a concise  presentation that articulated the startup's vision and goals. Their ability to create an engaging pitch showcased their hold over messaging and persuasion, hence score is 10.",
    "Rating": 10
  }},
  "Technical": {{
    "Reasoning": "Founder 1 demonstrated a good understanding of the technology powering their product. Their technical proficiency was evident in their good explanation of the system architecture and integration capabilities, hence score is 10. Founder 2 provided a good technical demo, showcasing the innovative features of their solution. Their knowledge of cutting-edge technologies and ability to implement them properly was good, hence score is 10.",
    "Rating": 10
  }}
}}
  ...
}}
```

Given below in triple backticks(```) is an ideal video pitch of a company that scores a maximum 10 on all the 10 skills listed above. Using this as a reference rate the transcript provided to you
```{model_pitch}```

Given also is the founders company details in the format of a JSON to help you score where the key is the question and value is the answer for that company. If they keys have values from the below list, these are the founders (out of 5) rating of the founding team on these skills:
1.	'Analytical',
2.	'Communication',
3.	'Judgement',
4.	'Negotiation',
5.	'Problem Solving',
6.	'Financial',
7.	'Technical',
8.	'Sales and Marketing',
9.	'Project Management',
10.	'Network Building',
11.	'Product Management',
12.	'Conviction/Belief',
13.	'Relentlessness',
14.	'Resilience',
15.	'Curiosity',
16.	'Reliability',
17.	'Courage',
18.	'Innovative',
19.	'Energetic',
20.	'Inspiring',
21.	'Clear Thinking',
22.	'Pace of Execution'


Company Details
```{company_details}```


# Notes

- Keep explanations concise but informative.
- If a skill is not well-addressed in the given pitch, make sure the rating reflects that.
- Avoid assigning a rating without a justification; always provide reasoning linked directly to the content in the transcript."""

skill_user_prompt = """
Given below is the transcript that you need to rate based on JSON schema
{transcript}
"""