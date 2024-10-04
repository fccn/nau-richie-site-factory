from typing import List, Dict
from django import template

register = template.Library()

@register.simple_tag
def course_detail_faq(category: str) -> List[Dict]:
    return [
        { 
            "question": "Lorem ipsum dolor sit amet?", 
            "answer": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, lorem ipsum dolor sit amet, consectetur adipiscing elit."
        },
        { 
            "question": "Lorem ipsum dolor sit amet?", 
            "answer": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, lorem ipsum dolor sit amet, consectetur adipiscing elit."
        },
        { 
            "question": "Lorem ipsum dolor sit amet?", 
            "answer": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, lorem ipsum dolor sit amet, consectetur adipiscing elit."
        },
        { 
            "question": "Lorem ipsum dolor sit amet?", 
            "answer": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, lorem ipsum dolor sit amet, consectetur adipiscing elit."
        },
    ]