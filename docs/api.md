# API Documentation

## ContentAgent Class

The main class that handles all content operations.

### Initialization

```python
from content_agent import ContentAgent

agent = ContentAgent(api_key='your_api_key_here')
```

### Methods

#### 1. analyze_topic(topic: str, industry: str) -> Dict

Analyzes a topic for content opportunities and market gaps.

```python
result = agent.analyze_topic(
    topic="AI Development",
    industry="Technology"
)
```

Returns:
```json
{
    "status": "success",
    "analysis": {
        "market_research": {
            "target_audience": [...],
            "consumption_patterns": [...],
            "competitor_analysis": [...],
            "seo_opportunities": [...]
        },
        ...
    },
    "timestamp": "2024-01-01T12:00:00"
}
```

#### 2. generate_content_plan(analysis: Dict) -> Dict

Generates a structured content calendar based on analysis.

```python
result = agent.generate_content_plan(analysis_data)
```

Returns:
```json
{
    "status": "success",
    "plan": {
        "monthly_themes": [...],
        "content_calendar": [...]
    },
    "timestamp": "2024-01-01T12:00:00"
}
```

#### 3. create_content(brief: Dict) -> Dict

Creates content based on a content brief.

```python
result = agent.create_content(content_brief)
```

Returns:
```json
{
    "status": "success",
    "content": {
        "main_content": {...},
        "seo_elements": {...},
        "supporting_content": {...}
    },
    "filename": "content_20240101_120000.json",
    "timestamp": "2024-01-01T12:00:00"
}
```

### Error Handling

All methods return a dictionary with:
- `status`: "success" or "error"
- `error`: Error message (if status is "error")
- `timestamp`: ISO format timestamp

Example error response:
```json
{
    "status": "error",
    "error": "Could not parse JSON response",
    "timestamp": "2024-01-01T12:00:00"
}
```

### Best Practices

1. **Error Handling**
   ```python
   result = agent.analyze_topic(topic, industry)
   if result['status'] == 'success':
       analysis = result['analysis']
   else:
       print(f"Error: {result['error']}")
   ```

2. **File Management**
   - Analysis is saved to `content_analysis.json`
   - Plans are saved to `content_plan.json`
   - Content is saved with timestamp: `content_YYYYMMDD_HHMMSS.json`

3. **Performance**
   - Large responses may take time
   - Use the debug output for troubleshooting
   - Check `debug_response.txt` for raw API responses

## Command Line Interface

Run the agent interactively:
```bash
python content_agent.py
```

Options:
1. Analyze Topic & Market
2. Generate Content Plan
3. Create Content
4. Optimize Performance
5. Exit 