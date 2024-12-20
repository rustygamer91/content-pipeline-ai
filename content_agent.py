import os
import google.generativeai as genai
from typing import Dict, List, Optional
import json
from datetime import datetime
import sys
import re

class ContentAgent:
    def __init__(self, api_key: str):
        """Initialize with Gemini API key."""
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def analyze_topic(self, topic: str, industry: str) -> Dict:
        """Analyze topic for content opportunities and market gaps."""
        prompt = f"""
        As a content strategy expert, analyze this topic and industry:
        Topic: {topic}
        Industry: {industry}
        
        Provide detailed analysis in these areas:
        1. Market Research:
           - Target audience segments
           - Content consumption patterns
           - Competitor content analysis
           - SEO opportunities
        
        2. Content Gaps:
           - Underserved subtopics
           - Missing content formats
           - Audience pain points
           - Unique angle opportunities
        
        3. Trending Aspects:
           - Current industry trends
           - Rising search terms
           - Social media conversations
           - Seasonal relevance
        
        4. Content Opportunities:
           - High-value content types
           - Platform-specific opportunities
           - Collaboration possibilities
           - Monetization potential
        
        Return your analysis as a JSON object with this exact structure:
        {{
            "market_research": {{
                "target_audience": ["item1", "item2"],
                "consumption_patterns": ["item1", "item2"],
                "competitor_analysis": ["item1", "item2"],
                "seo_opportunities": ["item1", "item2"]
            }},
            "content_gaps": {{
                "subtopics": ["item1", "item2"],
                "formats": ["item1", "item2"],
                "pain_points": ["item1", "item2"],
                "unique_angles": ["item1", "item2"]
            }},
            "trending_aspects": {{
                "industry_trends": ["item1", "item2"],
                "search_terms": ["item1", "item2"],
                "social_media": ["item1", "item2"],
                "seasonal_relevance": ["item1", "item2"]
            }},
            "content_opportunities": {{
                "content_types": ["item1", "item2"],
                "platforms": ["item1", "item2"],
                "collaborations": ["item1", "item2"],
                "monetization": ["item1", "item2"]
            }}
        }}

        Replace all item1, item2 with your actual analysis points. Each array should contain 2-4 detailed points.
        Ensure the response is valid JSON without any markdown formatting or code blocks.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Remove any markdown code block formatting
            if "```json" in text:
                text = text.split("```json")[1]
            if "```" in text:
                text = text.split("```")[0]
            
            text = text.strip()
            
            try:
                analysis = json.loads(text)
            except json.JSONDecodeError as e:
                print(f"\nJSON Parse Error: {str(e)}")
                print("\nAttempting to clean and parse response...")
                
                # Try to extract just the JSON part
                start_idx = text.find('{')
                end_idx = text.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = text[start_idx:end_idx]
                    try:
                        analysis = json.loads(json_str)
                    except json.JSONDecodeError as e2:
                        print(f"\nSecond parse attempt failed: {str(e2)}")
                        raise ValueError("Could not parse response as JSON")
                else:
                    raise ValueError("Could not find valid JSON in response")
            
            # Save the analysis for the next step
            with open('content_analysis.json', 'w') as f:
                json.dump(analysis, f, indent=2)
            
            return {
                'analysis': analysis,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"\nDebug - Raw response: {response.text if 'response' in locals() else 'No response'}")
            return {
                'error': str(e),
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }
    
    def generate_content_plan(self, analysis: Dict) -> Dict:
        """Generate structured content calendar based on analysis."""
        # First, generate monthly themes
        themes_prompt = """
        Create 3 monthly themes for a content plan. Keep all text under 50 characters.
        Return as a JSON array with this exact structure:
        [
            {
                "month": "Month 1",
                "theme": "Brief theme name",
                "focus_areas": ["2-3 key areas"]
            }
        ]
        
        Rules:
        1. Return exactly 3 themes
        2. Keep all text under 50 characters
        3. Include 2-3 focus areas per theme
        4. Return only the JSON array
        """
        
        try:
            # Generate monthly themes
            themes_response = self.model.generate_content(themes_prompt)
            themes_text = themes_response.text.strip()
            
            print("\nDebug - Raw themes response:")
            print(themes_text)
            
            # Clean and parse themes
            themes_text = self._clean_json_text(themes_text)
            
            print("\nDebug - Cleaned themes text:")
            print(themes_text)
            
            monthly_themes = json.loads(themes_text)
            
            if not isinstance(monthly_themes, list) or len(monthly_themes) != 3:
                raise ValueError("Invalid monthly themes format")
            
            # Generate content calendar in batches
            all_weeks = []
            for batch in range(3):  # 3 batches of 4 weeks = 12 weeks
                print(f"\nGenerating weeks {batch*4 + 1}-{batch*4 + 4}...")
                
                # Generate calendar prompt for this month's theme
                calendar_prompt = f"""
                Create a 4-week content calendar that aligns with this monthly theme:
                {json.dumps(monthly_themes[batch], indent=2)}
                
                Keep all text under 30 characters but ensure high quality and relevance.
                Return as a JSON array with this structure:
                [
                    {{
                        "week": "Week 1",
                        "main_content": {{
                            "type": "Blog/Video/Guide/Case Study",
                            "title": "Engaging title",
                            "description": "Value proposition",
                            "target_keywords": ["2-3 relevant terms"],
                            "estimated_word_count": 1500
                        }},
                        "supporting_content": [
                            {{
                                "platform": "Instagram/LinkedIn/Twitter",
                                "content_type": "Post/Video/Story",
                                "description": "Platform-specific hook"
                            }}
                        ]
                    }}
                ]
                
                Rules:
                1. Return exactly 4 weeks of content
                2. Keep text under 30 chars but make it compelling
                3. Ensure all content supports the monthly theme: {monthly_themes[batch]['theme']}
                4. Vary content types and platforms strategically
                5. Focus on delivering practical value
                6. Include clear value propositions
                7. Return only the JSON array
                """
                
                calendar_response = self.model.generate_content(calendar_prompt)
                calendar_text = calendar_response.text.strip()
                
                print(f"\nDebug - Raw calendar response (batch {batch + 1}):")
                print(calendar_text)
                
                # Clean and parse calendar
                calendar_text = self._clean_json_text(calendar_text)
                
                print(f"\nDebug - Cleaned calendar text (batch {batch + 1}):")
                print(calendar_text)
                
                batch_calendar = json.loads(calendar_text)
                
                if not isinstance(batch_calendar, list) or len(batch_calendar) != 4:
                    raise ValueError(f"Invalid calendar format in batch {batch + 1}")
                
                # Validate and standardize word counts
                for week in batch_calendar:
                    main_content = week['main_content']
                    content_type = main_content['type'].lower()
                    
                    # Set default word counts based on content type
                    if main_content['estimated_word_count'] is None or not isinstance(main_content['estimated_word_count'], int):
                        if 'video' in content_type:
                            main_content['estimated_word_count'] = 800  # Script length
                        elif 'guide' in content_type:
                            main_content['estimated_word_count'] = 2000  # Comprehensive guide
                        elif 'case study' in content_type:
                            main_content['estimated_word_count'] = 1500  # Detailed case study
                        else:  # Blog or default
                            main_content['estimated_word_count'] = 1200  # Standard blog post
                    
                    # Ensure word count is within reasonable limits
                    if main_content['estimated_word_count'] < 500:
                        main_content['estimated_word_count'] = 500
                    elif main_content['estimated_word_count'] > 3000:
                        main_content['estimated_word_count'] = 3000
                
                # Update week numbers
                for i, week in enumerate(batch_calendar):
                    week["week"] = f"Week {batch*4 + i + 1}"
                
                all_weeks.extend(batch_calendar)
            
            # Combine into final plan
            plan = {
                "monthly_themes": monthly_themes,
                "content_calendar": all_weeks
            }
            
            # Save the plan
            with open('content_plan.json', 'w') as f:
                json.dump(plan, f, indent=2)
            
            return {
                'plan': plan,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"\nError generating content plan: {str(e)}")
            if 'themes_response' in locals():
                print(f"\nThemes response length: {len(themes_response.text)}")
            if 'calendar_response' in locals():
                print(f"\nCalendar response length: {len(calendar_response.text)}")
            return {
                'error': str(e),
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }
    
    def _clean_json_text(self, text: str) -> str:
        """Clean and format JSON text for parsing."""
        # Remove markdown formatting and extract JSON
        if "```" in text:
            parts = text.split("```")
            for part in parts:
                if "{" in part or "[" in part:
                    text = part.strip()
                    break
        text = text.replace("```json", "").replace("```JSON", "").replace("```", "").strip()
        
        # Find and extract JSON object
        start_idx = text.find('{')
        end_idx = text.rfind('}') + 1
        if start_idx == -1:
            raise ValueError("Could not find JSON object in response")
        text = text[start_idx:end_idx]
        
        # Basic cleanup
        text = text.replace('\n', ' ')
        text = ' '.join(text.split())
        
        print("\n=== Original JSON ===")
        print(text[:200] + "...")
        
        # Fix the actual issues we're seeing
        # 1. Fix double-quoted colons
        text = text.replace('"":', '":')
        
        # 2. Fix missing commas in arrays
        text = re.sub(r'"\s*"([^"]+)"', '", "\1"', text)
        
        # 3. Fix any remaining structural issues
        text = re.sub(r',\s*([}\]])', r'\1', text)  # Remove trailing commas
        text = re.sub(r':\s*,', ':"",', text)  # Fix empty values
        
        print("\n=== Cleaned JSON ===")
        print(text[:200] + "...")
        
        try:
            # Test if valid JSON
            parsed = json.loads(text)
            return json.dumps(parsed)
        except json.JSONDecodeError as e:
            print(f"\n=== JSON Error ===")
            print(f"Error: {str(e)}")
            print(f"Position: {'^'.rjust(e.colno)}")
            print(f"Near: {text[max(0, e.colno-50):min(len(text), e.colno+50)]}")
            raise ValueError("Could not clean JSON response")
    
    def create_content(self, brief: Dict) -> Dict:
        """Generate actual content based on brief."""
        prompt = f"""
        Create high-quality content based on this content brief:
        {json.dumps(brief, indent=2)}

        Generate a complete content package with these components.
        Return as a JSON object with this exact structure:
        {{
            "main_content": {{
                "title": "Your engaging title",
                "meta_description": "Your 150-160 char summary",
                "introduction": "Your introduction paragraph",
                "sections": [
                    {{
                        "heading": "First subheading",
                        "content": "First section content"
                    }}
                ],
                "conclusion": "Your conclusion paragraph",
                "word_count": 1500
            }},
            "seo_elements": {{
                "primary_keyword": "Main target phrase",
                "secondary_keywords": ["2-3 related terms"],
                "internal_links": ["2-3 relevant topics"],
                "meta_title": "SEO title",
                "url_slug": "url-friendly-slug"
            }},
            "supporting_content": {{
                "social_media": [
                    {{
                        "platform": "Platform name",
                        "type": "Post type",
                        "content": "Post content"
                    }}
                ],
                "newsletter_snippet": "Email preview text",
                "pull_quotes": ["2-3 quotable excerpts"],
                "image_suggestions": ["2-3 image descriptions"]
            }},
            "engagement": {{
                "questions": ["2-3 discussion starters"],
                "cta_primary": "Main call to action",
                "cta_secondary": "Secondary call to action",
                "share_triggers": ["2-3 shareable moments"]
            }}
        }}

        IMPORTANT FORMATTING RULES:
        1. Use ONLY simple quotes (") for ALL strings
        2. Do NOT use any special characters in keys
        3. Do NOT use colons (:) within text content
        4. Separate sentences with periods instead of commas
        5. Keep all text content clean and simple
        6. Format arrays with proper commas
        7. Ensure all JSON keys are properly quoted
        8. Return ONLY the JSON object, no additional text
        """
        
        try:
            print("\nGenerating content... (this may take a moment)", flush=True)
            response = self.model.generate_content(prompt)
            
            # Save the raw response for debugging
            with open('debug_response.txt', 'w') as f:
                f.write(response.text)
            
            print(f"\nResponse length: {len(response.text)}", flush=True)
            
            # Basic cleanup first
            text = response.text.strip()
            if "```" in text:
                text = text.split("```")[1] if "```json" in text else text.split("```")[0]
            text = text.strip()
            
            # Find the JSON object
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            if start_idx == -1 or end_idx <= start_idx:
                raise ValueError("Could not find valid JSON object in response")
            
            text = text[start_idx:end_idx]
            
            # Basic string cleanup
            text = text.replace('\n', ' ').replace('\r', '')
            text = ' '.join(text.split())
            
            print("\n=== Initial JSON ===")
            print(text[:200] + "...")
            
            try:
                # First attempt: direct parse
                content = json.loads(text)
            except json.JSONDecodeError as e:
                print(f"\nInitial parse failed: {str(e)}")
                
                # Clean up common issues
                text = text.replace('"":', '":')  # Fix double-quoted colons
                text = re.sub(r':\s*"([^"]*?)"([^"]*?)"(?=[,}])', r':"\1\2"', text)  # Fix nested quotes
                text = re.sub(r',\s*([}\]])', r'\1', text)  # Remove trailing commas
                
                print("\n=== Cleaned JSON ===")
                print(text[:200] + "...")
                
                try:
                    content = json.loads(text)
                except json.JSONDecodeError as e:
                    print(f"\nJSON Error: {str(e)}")
                    print(f"Near: {text[max(0, e.colno-50):min(len(text), e.colno+50)]}")
                    raise ValueError("Could not parse content as JSON")
            
            # Save the generated content
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'content_{timestamp}.json'
            with open(filename, 'w') as f:
                json.dump(content, f, indent=2)
            
            return {
                'content': content,
                'filename': filename,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"\nError generating content: {str(e)}", flush=True)
            if 'response' in locals():
                print(f"\nResponse length: {len(response.text)}", flush=True)
                print("\nSaved raw response to debug_response.txt for inspection", flush=True)
            return {
                'error': str(e),
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }
    
    def optimize_performance(self, content: Dict, metrics: Dict) -> Dict:
        """Analyze content performance and suggest improvements."""
        prompt = f"""
        Based on this content and its performance metrics:
        Content: {json.dumps(content)}
        Metrics: {json.dumps(metrics)}
        
        Provide optimization recommendations:
        1. Content Improvements:
           - Engagement bottlenecks
           - Missing elements
           - Format optimization
           - Value proposition clarity
        
        2. Distribution Adjustments:
           - Platform performance
           - Timing optimization
           - Audience targeting
           - Promotion strategies
        
        3. SEO Enhancements:
           - Keyword opportunities
           - Technical improvements
           - Content gaps
           - Link building tactics
        
        4. Conversion Optimization:
           - CTA performance
           - User journey friction
           - Trust elements
           - Social proof placement
        
        Return as a JSON with actionable improvements.
        """
        
        try:
            response = self.model.generate_content(prompt)
            optimization = json.loads(response.text)
            return {
                'optimization': optimization,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }

def main():
    try:
        print("=== Starting Content Agent ===", flush=True)
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("Error: GOOGLE_API_KEY environment variable not set", flush=True)
            return
        
        print("API key found, initializing agent...", flush=True)
        agent = ContentAgent(api_key)
        
        while True:
            try:
                print("\n=== Content Strategy & Creation Pipeline ===", flush=True)
                print("1. Analyze Topic & Market", flush=True)
                print("2. Generate Content Plan", flush=True)
                print("3. Create Content", flush=True)
                print("4. Optimize Performance", flush=True)
                print("5. Exit", flush=True)
                print("\nEnter your choice (1-5):", flush=True)
                
                choice = input().strip().replace('.', '').strip()
                print(f"You selected: {choice}", flush=True)
                
                if choice == '5':
                    print("Goodbye!", flush=True)
                    break
                
                if choice == '1':
                    print("\nEnter your topic (e.g., 'AI Development', 'Digital Marketing'):", flush=True)
                    topic = input().strip()
                    print("\nEnter your industry (e.g., 'Technology', 'Healthcare'):", flush=True)
                    industry = input().strip()
                    
                    print("\nAnalyzing... (this may take a moment)", flush=True)
                    result = agent.analyze_topic(topic, industry)
                    
                    if result['status'] == 'success':
                        print("\nAnalysis completed successfully!", flush=True)
                        print("\nSummary of insights:", flush=True)
                        analysis = result['analysis']
                        
                        for category, details in analysis.items():
                            print(f"\n{category.replace('_', ' ').title()}:", flush=True)
                            for aspect, items in details.items():
                                print(f"  {aspect.replace('_', ' ').title()}:", flush=True)
                                for item in items:
                                    print(f"    - {item}", flush=True)
                        
                        print("\nFull analysis saved to content_analysis.json", flush=True)
                    else:
                        print(f"\nError: {result['error']}", flush=True)
                
                elif choice == '2':
                    try:
                        print("\nLoading previous analysis...", flush=True)
                        with open('content_analysis.json', 'r') as f:
                            analysis = json.load(f)
                        
                        print("\nGenerating content plan... (this may take a moment)", flush=True)
                        result = agent.generate_content_plan(analysis)
                        
                        if result['status'] == 'success':
                            print("\nContent plan generated successfully!", flush=True)
                            plan = result['plan']
                            
                            print("\nMonthly Themes:", flush=True)
                            for month in plan['monthly_themes']:
                                print(f"\n{month['month']}: {month['theme']}", flush=True)
                                print("Focus Areas:", flush=True)
                                for area in month['focus_areas']:
                                    print(f"  - {area}", flush=True)
                            
                            print("\nContent Calendar Preview:", flush=True)
                            for week in plan['content_calendar'][:3]:  # Show first 3 weeks
                                print(f"\n{week['week']}:", flush=True)
                                print("Main Content:", flush=True)
                                main = week['main_content']
                                print(f"  Type: {main['type']}", flush=True)
                                print(f"  Title: {main['title']}", flush=True)
                                print(f"  Description: {main['description']}", flush=True)
                                print(f"  Keywords: {', '.join(main['target_keywords'])}", flush=True)
                                
                                print("\nSupporting Content:", flush=True)
                                for support in week['supporting_content']:
                                    print(f"  - {support['platform']} {support['content_type']}: {support['description']}", flush=True)
                            
                            print("\nFull content plan saved to content_plan.json", flush=True)
                        else:
                            print(f"\nError: {result['error']}", flush=True)
                    
                    except FileNotFoundError:
                        print("\nError: Please analyze a topic first (option 1)", flush=True)
                    except Exception as e:
                        print(f"\nUnexpected error: {str(e)}", flush=True)
                
                elif choice == '3':
                    try:
                        print("\nLoading content plan...", flush=True)
                        with open('content_plan.json', 'r') as f:
                            plan = json.load(f)
                        
                        print("\nContent Plan Overview:", flush=True)
                        print("\nMonthly Themes:", flush=True)
                        for theme in plan['monthly_themes']:
                            print(f"- {theme['month']}: {theme['theme']}", flush=True)
                        
                        print("\nSelect content to create:", flush=True)
                        for i, week in enumerate(plan['content_calendar'], 1):
                            main = week['main_content']
                            print(f"{i}. Week {week['week']}: {main['type']} - {main['title']}", flush=True)
                        
                        print("\nEnter the number of the content piece to create (1-12):", flush=True)
                        content_choice = input().strip().rstrip('.')  # Remove trailing period
                        try:
                            content_choice = int(content_choice)
                            
                            if 1 <= content_choice <= len(plan['content_calendar']):
                                brief = plan['content_calendar'][content_choice - 1]
                                print(f"\nCreating content for: {brief['main_content']['title']}", flush=True)
                                
                                result = agent.create_content(brief)
                                
                                if result['status'] == 'success':
                                    print("\nContent created successfully!", flush=True)
                                    content = result['content']
                                    
                                    print("\nContent Summary:", flush=True)
                                    print(f"\nTitle: {content['main_content']['title']}", flush=True)
                                    print(f"Meta Description: {content['main_content']['meta_description']}", flush=True)
                                    
                                    if 'word_count' in content['main_content']:
                                        print(f"\nWord Count: {content['main_content']['word_count']}", flush=True)
                                    
                                    print("\nSEO Elements:", flush=True)
                                    seo = content.get('seo_elements', {})
                                    if 'primary_keyword' in seo:
                                        print(f"Primary Keyword: {seo['primary_keyword']}", flush=True)
                                    if 'secondary_keywords' in seo:
                                        print("Secondary Keywords:", flush=True)
                                        for keyword in seo['secondary_keywords']:
                                            print(f"- {keyword}", flush=True)
                                    
                                    print(f"\nFull content saved to {result['filename']}", flush=True)
                                    print("\nPress Enter to continue...", flush=True)
                                    sys.stdout.flush()  # Force flush before input
                                    input()
                                else:
                                    print(f"\nError: {result['error']}", flush=True)
                            else:
                                print("\nInvalid selection. Please choose a number between 1 and 12.", flush=True)
                        except ValueError:
                            print("\nPlease enter a valid number between 1 and 12.", flush=True)
                    
                    except FileNotFoundError:
                        print("\nError: Please generate a content plan first (option 2)", flush=True)
                    except ValueError as e:
                        print(f"\nError: Invalid input - {str(e)}", flush=True)
                    except Exception as e:
                        print(f"\nUnexpected error: {str(e)}", flush=True)
                
                elif choice in ['4']:
                    print("\nThis feature is coming soon!", flush=True)
                
                else:
                    print("\nInvalid choice! Please try again.", flush=True)
                
                print("\nPress Enter to continue...", flush=True)
                input()
            
            except EOFError:
                print("\nExiting due to EOF", flush=True)
                break
            except KeyboardInterrupt:
                print("\nExiting due to user interrupt", flush=True)
                break
            except Exception as e:
                print(f"\nUnexpected error: {str(e)}", flush=True)
                break
    
    except Exception as e:
        print(f"Critical error: {str(e)}", flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()