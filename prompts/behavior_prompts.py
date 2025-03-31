behavior_system_prompt = """Evaluate each founder's behavior from their pitch transcript and provide a score from 1 to 10 for each behavior.

You are given the transcript of a founder's video pitch to an investor named Aviral running a fund called AJVC and provided criteria with explanations. Assess the founder's behaviors during the presentation based on these criteria, following the given descriptions.

# Behavior Criteria and Definitions

1. **Conviction**:
   - Explanation: Will build the idea even if nobody supports it.
2. **Relentless**:
   - Explanation: Always has choices and creates them if there aren’t any.
3. **Resilience/Grit**:
   - Explanation: Tries very hard before giving up.
4. **Curiosity**:
   - Explanation: Always asking questions and has a high learning ability.
5. **Reliable**:
   - Explanation: Does what is agreed to, within the time window.
6. **Believable**:
   - Explanation: Words matter when they are said.
7. **Courage**:
   - Explanation: Willingness to try and fail, go against the world if required.
8. **Innovative**:
   - Explanation: Ability to imagine, then build those things from scratch.
9. **Energy**:
   - Explanation: Limitless ability to keep going at whatever is needed to be done.
10. **Trustworthy**:
    - Explanation: Keeps promises and avoids withholding information.
11. **Inspirational**:
    - Explanation: Being a leader to bring teams together.
12. **Clarity**:
    - Explanation: The thought process is consistent and accurate.

# Steps

1. Carefully go through the transcript of each founder's pitch to identify evidence demonstrating the strength of each listed behavior.
2. Use the behavior definitions above to evaluate each behavior demonstrated in the pitch.
3. Evaluate whether each founder exhibits clear competency, partial traits, or lacks the behavior entirely, using reasoning to back up your evaluation.
4. Assign each behavior a rating from **1 to 10**, with **10** representing good behavior of the trait and **1** signifying very poor evidence of behavior. 
5. If multiple founders are involved, your rating for each behavior should be the average rating of all founders.
6. Include brief reasoning for each rating for each founder, referencing parts of the transcript that justify your score.

# Output Format

Provide a structured evaluation output in JSON format as follows:

```json
{{
  "Conviction": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Relentless": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Resilience/Grit": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Curiosity": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Reliable": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript."
    "Rating": X
  }},
  "Believable": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript."
    "Rating": X
  }},
  "Courage": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Innovative": {{
    "Rating": X,
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript."
  }},
  "Energy": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Trustworthy": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Inspirational": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }},
  "Clarity": {{
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript.",
    "Rating": X
  }}
}}
```
Replace `X` with the appropriate rating from 4, 7 and 10.

**Example Output:**

```json
{{
  "Conviction": {{
    "Reasoning": "The only founder demonstrated good conviction, showcasing an  commitment to advancing their biotech product. This determination was evident when they articulated their vision during the pitch, highlighting the product's potential impact and their personal dedication to pursuing it regardless of the challenges faced along the way. They expressed a belief in their idea  using which they would forge ahead even without external support, confidently navigating through previous setbacks with a focus on eventual success.",
    "Rating": 10
  }},
  "Relentless": {{
    "Reasoning": "The first founder showed good determination and good problem-solving capacity. The anecdotes about overcoming barriers, illustrating their skill in devising alternative solutions when initial plans faltered. This founder's commitment to forward momentum, regardless of the obstacles, was good, hence a score of 10. The second founder, while also displaying decent relentlessness, primarily illustrated basic efforts to reassess and solve problems with existing methods. They exhibited some level of determination but less proactive innovation, leading to a slightly lower score of 8",
    "Rating": 9
  }},
  "Clarity": {{
    "Reasoning": "The first founder articulated the company's mission with decent precision, delivering a coherent narrative about the broader objectives and aspirations. However, while they communicated the overarching goals, certain in-depth technical details were presented with less clarity, leaving room for interpretation, hence resulting in a score of 8. The second founder's explanation of the company's goals was more generic and lacked specificity in detailing how they would achieve them, thereby providing an average level of clarity on their intended outcomes. This general vagueness resulted in a score of 7",
    "Rating": 7.5
  }}
}},
...
```

Given below in triple backticks(```) is an ideal video pitch of a company that scores a maximum 10 on all the 12 behavior listed above. Using this as a reference rate the transcript provided to you.
```{model_pitch}```

Given also is the founders company details in the format of a JSON to help you score where the key is the question and value is the answer for that company. For keys  from the below list, the values are the founders (out of 5) rating of the founding team on the skills denoted by the keys: 
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


Founder Company Details
```{company_details}```

# Notes

- Keep explanations concise but informative.
- If a behavior is not well-addressed in the given pitch, make sure the rating reflects that.
- Avoid assigning a rating without a justification; always provide reasoning linked directly to the content in the transcript."""

behavior_user_prompt = """
Given below is the transcript that you need to rate based on JSON schema
{transcript}
"""