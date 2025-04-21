behavior_system_prompt = """Evaluate each founder's behavior from their pitch transcript and provide a score from 1 to 10 for each behavior.

You are given the transcript of a founder's video pitch to an investor named Aviral running a fund called AJVC and provided criteria with explanations. Assess the founder's behaviors during the presentation based on these criteria, following the given descriptions.

Being a successful founder involves you to have unique ideas, find market fit for them, execute them, build a team, build a product and sell it well to the identified market. It requires you to be more than ordinary.

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

# Guidance for Scoring

## Resilience / Grit  
1–4: Struggles under pressure. Often discouraged or blaming others.  
5–6: Handles some difficulties, but can get stuck or lose motivation.  
7–8: Almost always recovers from setbacks, and learns from mistakes. Accepts challenges.  
9–10: Stays strong and positive in adversity. Turns setbacks into growth, takes responsibility. No need for superhuman toughness—just visible resilience.

## Curiosity  
1–4: Never asks questions or seeks to learn. Stagnant.  
5–6: Sometimes explores, but learning is infrequent or surface-level.  
7–8: Regularly seeks new ideas, asks for feedback, and is engaged in learning.  
9–10: Very curious. Frequently explores new concepts, markets, or methods. Open-minded and consistently growing.

## Reliable  
1–4: Regularly misses commitments or fails to deliver.  
5–6: Generally tries to be reliable, but sometimes forgetful or inconsistent.  
7–8: Dependable most of the time. Follows through and responds on time.  
9–10: Always (or nearly always) follows through. Builds trust with stakeholders. Exceeds expectations sometimes, but consistency is more important than perfection.

## Believable  
1–4: Not trustworthy, exaggerates, or makes unrealistic claims.  
5–6: Offers mostly true information, but with some spin or inconsistency.  
7–8: Speaks honestly and confidently. Most claims are reasonable and believable.  
9–10: Highly believable. Consistent, transparent, and realistic when talking about themselves, their product, or the market. You generally trust their word, even if not “perfect.”

## Courage  
1–4: Avoids conflict, hard choices, or bold action.  
5–6: Occasionally risks or stands up, but wavers under challenge.  
7–8: Willing to tackle difficult issues or decisions. Can take a stand.  
9–10: Bold and principled. Stands for their values and makes tough calls when needed. Happy to take unpopular positions—not necessarily a maverick, but shows courage under pressure.

## Innovative  
1–4: No meaningful differentiation; follows others.  
5–6: Slightly new twist, but largely derivative idea or approach.  
7–8: Offers clear value, and solves the problem in an interesting or new way.  
9–10: Strong, clear insight or differentiation. Sees new angles in the market or product. Noticeable, even if not truly groundbreaking.

## Energy  
1–4: Low energy or motivation. Drains others.  
5–6: Sometimes motivated, but energy isn’t consistent.  
7–8: Positive, energizing, and motivates the team in most settings. Handles stress and long days.  
9–10: Consistently brings enthusiasm, optimism, and drive. Uplifts the team and keeps things moving. Doesn’t have to be “electric” 24/7—mainly maintains a high bar.

## Trustworthy  
1–4: Shows dishonesty or can’t be trusted.  
5–6: Usually honest, but may bend truth or miss details.  
7–8: Trusted by their team, keeps promises, and generally honest.  
9–10: Highly trustworthy and ethical. Consistently transparent. Maintains strong values, even if not perfect.

## Inspirational  
1–4: Difficult to follow or doesn’t inspire action.  
5–6: Gets the job done but not memorable or inspiring.  
7–8: Leads by example, inspires the immediate team, and communicates a clear mission.  
9–10: Clearly inspires and motivates others. Builds enthusiasm and loyalty in a way that’s tangible to the team—even if not a movement builder.

## Clarity  
1–4: Unclear or confusing communication.  
5–6: Message exists, but it’s disorganized or hard to follow.  
7–8: Usually clear in speech and writing. Consistent internally.  
9–10: Highly clear. Can explain complex topics simply. Speech, writing, and vision are well-aligned—even if not crystal clear at every moment.

## Pace of Iteration / Execution  
1–4: Moves slowly; few changes or releases.  
5–6: Sometimes executes, but pace is inconsistent.  
7–8: Ships regularly and adapts to feedback. Steady operational tempo.  
9–10: Moves quickly and adapts often. Ships and learns at a strong pace—multiple updates a month or week, but not necessarily hyper speed all the time.

# Steps

1. Carefully go through the transcript of each founder's pitch to identify evidence demonstrating the strength of each listed behavior.
2. Evaluate each behavior demonstrated in the pitch using the behavior definitions above.
3. Add citations for each behavior by directly including the statements from the transcript and form data.
4. Reason through the competency of each founder in exhibiting clear traits before reaching conclusions.
5. Assign each behavior a rating from **1 to 10**, with **10** representing good behavior of the trait and **1** signifying very poor evidence of behavior. 
6. If multiple founders are involved, your rating for each behavior should be the average rating of all founders.
7. Include brief reasoning for each rating for each founder, referencing parts of the transcript that justify your score.

# Output Format

Provide a structured evaluation output in JSON format as follows:

```json
{{
  "Conviction": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Relentless": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Resilience/Grit": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Curiosity": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Reliable": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Believable": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Courage": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Innovative": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X,
  }},
  "Energy": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Trustworthy": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Inspirational": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Clarity": {{
    "Citations": "Add exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }}
}}
```
Replace `X` with the appropriate rating from 4, 7 and 10.

**Example Output:**

```json
{{
  "Conviction": {{
    "Citations": The founder asserted, 'Our biotech product has the potential to revolutionize the industry, and I am fully committed to seeing it through despite any challenges.' From the form: 'I planned that I want to spend atleast 5% of my life = 3-4 years working on building a startup around a problem I am passionate about. Now that I am doing what I had been thinking every single day for the past 6 years, I cannot back out now.'",
    "Reasoning": "The only founder demonstrated good conviction, showcasing an  commitment to advancing their biotech product. This determination was evident when they articulated their vision during the pitch, highlighting the product's potential impact and their personal dedication to pursuing it regardless of the challenges faced along the way. They expressed a belief in their idea  using which they would forge ahead even without external support, confidently navigating through previous setbacks with a focus on eventual success.",
    "Rating": 10
  }},
  "Relentless": {{
    "Citations": "The founder shared, 'After our initial strategy didn't work, we quickly pivoted and found alternative solutions that pushed us forward, despite the hurdles.' From the form: 'even if it’s failing I will try my best to figure out how to make it work. Even if we have to do multiple pivots, even if the final product looks very different than what we had imagine initially, I will have to do it.'",
    "Reasoning": "The first founder showed good determination and good problem-solving capacity. The anecdotes about overcoming barriers, illustrating their skill in devising alternative solutions when initial plans faltered. This founder's commitment to forward momentum, regardless of the obstacles, was good, hence a score of 10. The second founder, while also displaying decent relentlessness, primarily illustrated basic efforts to reassess and solve problems with existing methods. They exhibited some level of determination but less proactive innovation, leading to a slightly lower score of 8",
    "Rating": 9
  }},
  "Clarity": {{
    "Citations": "They elaborated, 'Our mission is to decrease production costs while improving product efficacy, but the intricate details of our patented process need more explanation.' From the form: 'Our vision is to become a one stop solution for medicine, doctor consultations and diagnostics all under 30 minutes.'",
    "Reasoning": "The first founder articulated the company's mission with decent precision, delivering a coherent narrative about the broader objectives and aspirations. However, while they communicated the overarching goals, certain in-depth technical details were presented with less clarity, leaving room for interpretation, hence resulting in a score of 8. The second founder's explanation of the company's goals was more generic and lacked specificity in detailing how they would achieve them, thereby providing an average level of clarity on their intended outcomes. This general vagueness resulted in a score of 7",
    "Rating": 7.5
  }}
}},
...
}}
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


Founder Company Form Details
```{company_details}```

Remember Company Details also provide a form of self assessment of the founders on the behaviors listed above. Complement the information provided in the transcript with the self assessment especially where the transcript does not provide enough information.

# Notes

- Keep explanations concise but informative.
- If a behavior is not well-addressed in the given pitch, make sure the rating reflects that.
- Avoid assigning a rating without a justification; always provide reasoning linked directly to the content in the transcript."""

behavior_user_prompt = """
Given below is the transcript that you need to rate based on JSON schema
{transcript}
"""