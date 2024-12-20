# Usage Examples

## 1. Basic Content Pipeline

This example shows how to create a complete content pipeline from analysis to content creation.

```python
from content_agent import ContentAgent
import os

# Initialize the agent
api_key = os.getenv('GOOGLE_API_KEY')
agent = ContentAgent(api_key)

# 1. Analyze topic
result = agent.analyze_topic(
    topic="Machine Learning for Beginners",
    industry="Technology Education"
)

if result['status'] == 'success':
    analysis = result['analysis']
    print("Analysis completed successfully!")
    
    # 2. Generate content plan
    plan_result = agent.generate_content_plan(analysis)
    
    if plan_result['status'] == 'success':
        plan = plan_result['plan']
        print("Content plan generated!")
        
        # 3. Create first piece of content
        first_brief = plan['content_calendar'][0]
        content_result = agent.create_content(first_brief)
        
        if content_result['status'] == 'success':
            print(f"Content created and saved to {content_result['filename']}")
```

## 2. Market Analysis Only

Use the agent to analyze a topic without generating content.

```python
result = agent.analyze_topic(
    topic="Sustainable Living",
    industry="Environmental"
)

if result['status'] == 'success':
    analysis = result['analysis']
    
    # Print target audience
    print("\nTarget Audience:")
    for audience in analysis['market_research']['target_audience']:
        print(f"- {audience}")
        
    # Print content gaps
    print("\nContent Gaps:")
    for gap in analysis['content_gaps']['subtopics']:
        print(f"- {gap}")
```

## 3. Custom Content Brief

Create content from a custom brief without analysis.

```python
custom_brief = {
    "main_content": {
        "type": "Blog Post",
        "title": "Getting Started with AI",
        "description": "Beginner's guide to AI concepts",
        "target_keywords": ["AI basics", "machine learning intro"],
        "estimated_word_count": 1500
    },
    "supporting_content": [
        {
            "platform": "LinkedIn",
            "content_type": "Post",
            "description": "Key takeaways from the blog"
        }
    ]
}

result = agent.create_content(custom_brief)
if result['status'] == 'success':
    print(f"Content saved to {result['filename']}")
```

## 4. Batch Content Creation

Generate multiple content pieces from a plan.

```python
def batch_create_content(agent, plan, start_week=0, num_weeks=4):
    """Create content for multiple weeks."""
    results = []
    
    for i in range(start_week, min(start_week + num_weeks, len(plan['content_calendar']))):
        brief = plan['content_calendar'][i]
        result = agent.create_content(brief)
        results.append({
            'week': i + 1,
            'status': result['status'],
            'filename': result.get('filename', None)
        })
    
    return results

# Use the function
with open('content_plan.json', 'r') as f:
    plan = json.load(f)

results = batch_create_content(agent, plan, start_week=0, num_weeks=4)
for result in results:
    print(f"Week {result['week']}: {result['status']}")
```

## 5. Interactive Usage

Example of using the command-line interface:

```bash
# Start the agent
python content_agent.py

# Follow the prompts:
1  # Choose "Analyze Topic & Market"
AI Development  # Enter topic
Technology  # Enter industry

2  # Choose "Generate Content Plan"
# Review the generated plan

3  # Choose "Create Content"
1  # Select the first content piece
```

## 6. Error Handling

Example with proper error handling:

```python
def safe_create_content(agent, brief):
    """Safely create content with error handling."""
    try:
        result = agent.create_content(brief)
        
        if result['status'] == 'success':
            print(f"Success! Content saved to {result['filename']}")
            return result['content']
        else:
            print(f"Error: {result['error']}")
            return None
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

# Use the function
content = safe_create_content(agent, custom_brief)
if content:
    print(f"Generated {len(content['main_content']['sections'])} sections")
```

## Output Examples

### 1. Analysis Output
```json
{
    "market_research": {
        "target_audience": [
            "Tech professionals (25-40)",
            "Career changers exploring AI"
        ],
        "seo_opportunities": [
            "Long-tail AI learning keywords",
            "Practical ML tutorials"
        ]
    }
}
```

### 2. Content Plan Output
```json
{
    "monthly_themes": [
        {
            "month": "January",
            "theme": "AI Foundations",
            "focus_areas": [
                "Basic Concepts",
                "Real-world Applications"
            ]
        }
    ]
}
```

### 3. Content Output
```json
{
    "main_content": {
        "title": "AI Basics: Your First Steps",
        "sections": [
            {
                "heading": "What is AI?",
                "content": "Artificial Intelligence..."
            }
        ]
    }
}
``` 