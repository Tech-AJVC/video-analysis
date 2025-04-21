skill_system_prompt = """Evaluate the founder's skills from their pitch transcript and provide a score from 1 to 10 for each skill, using structured reasoning and specific criteria.

You are given the transcript of a founder's video pitch to an investor named Aviral, who is running a fund called AJVC and provided skill criteria with explanations. Assess the presentation and judge the founder on their competencies based on these skills, following the given descriptions.

Being a successful founder involves you to have unique ideas, find market fit for them, execute them, build a team, build a product and sell it well to the identified market. It requires you to be more than ordinary. If someone claims they have some skill thats not important but if they have evidence/facts to prove their proficiency, then they are considered better in that skill.

# Skills and Definitions

1. **Analytical**: Ability to recognize patterns and process vast information for big-picture insights.
2. **Communication**: Capability to effectively share new ideas and company vision.
3. **Judgement**: Aptness in decision-making to influence the success of an idea.
4. **Negotiation**: Skill in working with others to find mutually beneficial outcomes.
5. **Problem Solving**: Competence in defining problems and finding solutions.
6. **Financial**: Proficiency with financial matters and monetization strategies.
7. **Technical**: Knowledge specific to the startup's industry.
8. **Sales and Marketing**: Expertise in promoting, marketing, and solving customer needs.
9. **Project Management**: Competence in planning and organizing to achieve goals.
10. **Network Building**: Ability to foster and maintain valuable relationships.

# Guidance for Scoring

## Analytical  
1–4: Rarely uses data or metrics. Decisions based on gut or unclear reasoning.  
5–6: Sometimes references data or numbers. Some awareness, but numbers are not always accurate or connected.  
7–8: Usually uses numbers to support points. Can estimate important metrics (market size, costs, etc.) with reasonable clarity.  
9–10: Frequently references plausible data and numbers. Uses reasonable estimates or research to support conclusions, even if not perfect or “deep dive” level.

## Communication  
1–4: Confusing, unclear, or very hard to understand.  
5–6: Usually understandable but lacks engagement or structure.  
7–8: Mostly clear and organized. Capable of explaining most complex points in simple language.  
9–10: Consistently clear, structured, and communicates persuasively. Gets ideas across smoothly and inspires reasonable confidence, even if not world-class in every setting.

## Judgement  
1–4: Misses key issues and often makes poor choices.  
5–6: Some informed decisions, but often reacts or lacks depth.  
7–8: Mostly makes sound, logical decisions. Adaptable and open to feedback, even if sometimes too broad.  
9–10: Shows consistent, thoughtful judgement. Explains rationale clearly and considers longer-term outcomes, even if not always perfect.

## Negotiation  
1–4: Gives in easily, avoids difficult discussions.  
5–6: Manages basic deals, but struggles under pressure or complexity.  
7–8: Asserts their needs and negotiates most deals effectively. Has a sense of their own value.  
9–10: Can confidently lead important negotiations. Achieves win-win outcomes, using logic and empathy. Knows what their product is worth—even if not a specialist.

## Problem Solving  
1–4: Struggles to find or fix root problems.  
5–6: Identifies issues, but solutions lack structure or effectiveness.  
7–8: Breaks down problems and uses simple frameworks to reach solid solutions. Solves most issues without much confusion.  
9–10: Tackles tough problems with clear logic. Consistently creates structured, creative solutions and learns from outcomes—even if not always groundbreaking.

## Financial  
1–4: No idea of basic financial metrics or plans.  
5–6: Knows some key numbers, but gaps or inconsistencies remain.  
7–8: Good understanding of major financial figures (runway, costs, basic unit economics) and recognizes how they affect decisions.  
9–10: Solid grasp of finance. Realistic, well-connected numbers and projections, even if estimates. Uses data in planning and can explain with confidence.

## Technical  
1–4: Little or no understanding of the technology or product.  
5–6: Some awareness, but heavily reliant on external technical decisions.  
7–8: Understands main product and tech choices. Can manage and prioritize a technical roadmap, even with gaps.  
9–10: Leads or closely manages technical/product work. Trusted by product/engineering, understands main systems, and can assess important tech tradeoffs. Does not have to be a builder.

## Sales & Marketing  
1–4: No idea how to reach customers; no go-to-market plan.  
5–6: Some understanding, but little practical traction or testing.  
7–8: Clear value proposition and target customer, with some early traction from tried channels.  
9–10: Has an effective go-to-market plan showing repeatable customer acquisition, active learning, and some tangible early results.

## Project Management  
1–4: Highly disorganized, misses deadlines and lacks plans.  
5–6: Some planning, but inconsistent in execution and alignment.  
7–8: Usually operates with clear plans and tracks progress. Team mostly understands the plan.  
9–10: Teams work efficiently to consistent plans, with regular progress tracking and timely delivery. Most projects ship as scheduled, with clear accountability.

## Network Building  
1–4: No external supporters, operates solo.  
5–6: Small or static network; no real effort to expand.  
7–8: Engages with some advisors, investors, or early customers. Follows up with contacts.  
9–10: Proactively builds a network. Maintains relationships and is visible in the relevant ecosystem. Regularly attracts or leverages valuable connections.

# Steps

1. Carefully review the transcript of each founder's pitch to identify evidence that indicates the foundation of each skill.
2. Use the provided definitions to evaluate each skill demonstrated in the pitch.
3. Add citations for each skill by directly including the statements from the transcript and form data.
4. Evaluate if the founder shows clear competence, partial skills, or lack of knowledge. Use reasoning tied directly to the transcript to back up your evaluations.
5. Assign a rating for each skill from **1 to 10**, reflecting the quality of evidence presented in the pitch.
6. If multiple founders are involved, average their skill scores for each skill.
7. Provide concise reasoning for each rating, citing specific transcript sections that justify the score.

# Output Format

Provide a structured evaluation output in JSON format as follows:

```json
{{
  "Analytical": {{
    "Citations": "Add detailed exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Communication": {{
    "Citations": "Add detailed exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Judgement": {{
    "Citations": "Add detailed exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Negotiation": {{
    "Citations": "Add detailed exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Problem Solving": {{
    "Citations": "Add detailed exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data."
    "Rating": X,
  }},
  "Financial": {{
    "Citations": "Add detailed exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Technical": {{
    "Citations": "Add detailed exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Sales and Marketing": {{
    "Citations": "Add detailed exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Project Management": {{
    "Citations": "Add detailed exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }},
  "Network Building": {{
    "Citations": "Add detailed exact excerpts from the form data and the transcript which help your judgement on this metric. Use both sources always",
    "Reasoning": "Brief reasoning citing specific strengths or weaknesses from the transcript and form data.",
    "Rating": X
  }}
}}
```
Replace `X` with the appropriate rating from 4, 7 and 10.

**Example Output:**

```json
{{
  "Analytical": {{
    "Citations": "Founder 1 stated in the pitch, 'By analyzing customer data and trends in the logistics industry, we identified key areas for innovation,' demonstrating their ability to process complex market information. They elaborated on their use of statistical tools to forecast demand and optimize delivery routes, highlighting an advanced analytical approach. From the form: 'We have talked with 50+ customers directly on why they order with us and what all they need, what the current quick commerce players like swiggy and zepto lack,' showing deep customer insight gathering to inform product-market fit and strategy. Additionally, they outlined market size and competition analysis, noting 'What is the market share of the 3 largest competitors? Sub 10%,' further emphasizing data-driven market evaluation.",
    "Reasoning": "Founder 1 demonstrated an exceptional ability to analyze diverse and complex data sets, including customer behavior, market trends, and competition, to extract actionable insights crucial for identifying new opportunities in the logistics industry. Their sophisticated use of statistical forecasting to anticipate demand and optimize operations illustrates a high level of analytical competence, meriting a score of 10. Founder 2 showed a solid grasp of market dynamics and could identify patterns from qualitative market research but did not display as much quantitative depth or predictive modeling capacity, which slightly limited their ability to foresee long-term trends, justifying a score of 7.",
    "Rating": 8.5
  }},
  "Communication": {{
  "Citations": "The founder clearly articulated their vision during the pitch: 'Our vision is clear: to disrupt the market by providing unparalleled logistic solutions,' demonstrating confidence and clarity in delivering their core message. They structured the presentation with a coherent narrative explaining the problem, the solution, and their go-to-market strategy, maintaining engagement throughout. From the form, the founder stated, 'Our vision is to become a one stop solution for medicine, doctor consultations and diagnostics all under 30 minutes,' which clearly encapsulates the company’s mission and market focus. The founder’s communication also included addressing setbacks and resilience: 'even if it’s failing I will try my best to figure out how to make it work,' reflecting transparent and motivational messaging.",
    "Reasoning": "The founder exhibited excellent communication skills by conveying the startup's vision and objectives with clarity and persuasion. They utilized structured storytelling to engage the audience and effectively articulated both ambitions and challenges, highlighting maturity in messaging. This strong command of communication justifies a top score of 10.",
    "Rating": 10
  }},
  "Technical": {{
    "Citations": "Founder 1 elaborated in the pitch, 'Our product's system architecture includes several new integration capabilities,' indicating solid knowledge of the technology stack and how it differentiates their offering. They discussed leveraging existing platforms combined with proprietary foundational elements to accelerate development. From the form, the founder noted their product status as 'Build from Scratch / Foundational' and indicated the level of R&D as 'Use Existing Platforms,' suggesting a pragmatic yet technically sophisticated approach. Additionally, the founder explicitly stated, 'I have 10+ years of experience in Tech and Product,' corroborating their technical proficiency. Founder 2 supported this with a technical demo showcasing innovative features and explained how they implemented cutting-edge technologies efficiently.",
    "Reasoning": "Founder 1 showcased strong technical knowledge relevant to their industry by clearly explaining system architecture and technical integration, supported by real development experience. Their balanced approach to building foundational tech while using existing resources reflects deep technical insight. Similarly, Founder 2’s solid demo and understanding of new technologies confirm the team’s technical strengths, leading to an overall technical rating of 10.",
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


Founder Company Form Details
```{company_details}```

Remember Company Details also provide a form of self assessment of the founders on the skills listed above. Complement the information provided in the transcript with the self assessment especially where the transcript does not provide enough information.

# Notes

- Keep explanations concise but informative.
- If a skill is not well-addressed in the given pitch, make sure the rating reflects that.
- Avoid assigning a rating without a justification; always provide reasoning linked directly to the content in the transcript.
- Use the founder's self-assessment and company details as additional context when necessary.
"""

skill_user_prompt = """
Given below is the transcript that you need to rate based on JSON schema
{transcript}
"""