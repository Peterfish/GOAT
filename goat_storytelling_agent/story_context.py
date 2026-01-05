"""
Story Context Manager - ระบบจัดการบริบทเรื่องราวเพื่อความต่อเนื่อง

Components:
1. Chapter Summaries - สรุปแต่ละบท
2. Character States - สถานะตัวละคร (ที่อยู่, อารมณ์, เป้าหมาย)
3. Key Events - เหตุการณ์สำคัญที่เกิดขึ้น
4. Relationships - ความสัมพันธ์ระหว่างตัวละคร
"""

import json
import os


class StoryContext:
    """จัดการบริบทเรื่องราวสำหรับความต่อเนื่องระหว่างบท"""

    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        self.context_file = os.path.join(output_dir, 'story_context.json')

        # Initialize empty context
        self.context = {
            'chapter_summaries': {},  # {ch_num: summary}
            'character_states': {},   # {name: {location, emotional_state, goal, last_action}}
            'key_events': [],         # [{chapter, event, impact}]
            'relationships': {},      # {"A|B": {status, change_reason}}
            'plot_progress': {        # ติดตามความคืบหน้าของ plot
                'current_act': 1,
                'major_conflicts_resolved': [],
                'pending_threads': []
            }
        }

        # Load existing context if available
        self.load()

    def load(self):
        """โหลด context จากไฟล์"""
        if os.path.exists(self.context_file):
            try:
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    self.context = json.load(f)
                print(f"Loaded story context from {self.context_file}")
            except Exception as e:
                print(f"Error loading context: {e}")

    def save(self):
        """บันทึก context ลงไฟล์"""
        os.makedirs(self.output_dir, exist_ok=True)
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, ensure_ascii=False, indent=2)
        print(f"Saved story context to {self.context_file}")

    def add_chapter_summary(self, chapter_num, summary):
        """เพิ่มสรุปบท"""
        self.context['chapter_summaries'][str(chapter_num)] = summary
        self.save()

    def update_character_state(self, name, location=None, emotional_state=None,
                                goal=None, last_action=None):
        """อัปเดตสถานะตัวละคร"""
        if name not in self.context['character_states']:
            self.context['character_states'][name] = {}

        state = self.context['character_states'][name]
        if location:
            state['location'] = location
        if emotional_state:
            state['emotional_state'] = emotional_state
        if goal:
            state['goal'] = goal
        if last_action:
            state['last_action'] = last_action

        self.save()

    def add_key_event(self, chapter_num, event, impact=None):
        """เพิ่มเหตุการณ์สำคัญ"""
        self.context['key_events'].append({
            'chapter': chapter_num,
            'event': event,
            'impact': impact or ''
        })
        self.save()

    def update_relationship(self, char1, char2, status, change_reason=None):
        """อัปเดตความสัมพันธ์ระหว่างตัวละคร"""
        # ใช้ key เรียงตามตัวอักษรเพื่อความ consistent
        key = '|'.join(sorted([char1, char2]))
        self.context['relationships'][key] = {
            'characters': [char1, char2],
            'status': status,
            'change_reason': change_reason or ''
        }
        self.save()

    def get_context_for_writing(self, current_chapter):
        """สร้าง context string สำหรับส่งให้ AI เขียนบท"""
        parts = []

        # 1. Previous chapter summaries (เฉพาะบทที่ผ่านมา)
        summaries = self.context['chapter_summaries']
        if summaries:
            parts.append("=== STORY SO FAR (Chapter Summaries) ===")
            for ch_num in sorted(summaries.keys(), key=int):
                if int(ch_num) < current_chapter:
                    parts.append(f"Chapter {ch_num}: {summaries[ch_num]}")

        # 2. Character states
        char_states = self.context['character_states']
        if char_states:
            parts.append("\n=== CHARACTER STATES ===")
            for name, state in char_states.items():
                state_str = f"{name}: "
                state_parts = []
                if state.get('location'):
                    state_parts.append(f"at {state['location']}")
                if state.get('emotional_state'):
                    state_parts.append(f"feeling {state['emotional_state']}")
                if state.get('goal'):
                    state_parts.append(f"wants to {state['goal']}")
                if state.get('last_action'):
                    state_parts.append(f"last did: {state['last_action']}")
                state_str += "; ".join(state_parts)
                parts.append(state_str)

        # 3. Key events (ล่าสุด 10 events)
        events = self.context['key_events']
        if events:
            parts.append("\n=== KEY EVENTS THAT HAPPENED ===")
            recent_events = events[-10:]  # เอาแค่ 10 events ล่าสุด
            for evt in recent_events:
                evt_str = f"Ch{evt['chapter']}: {evt['event']}"
                if evt.get('impact'):
                    evt_str += f" (Impact: {evt['impact']})"
                parts.append(evt_str)

        # 4. Relationships
        rels = self.context['relationships']
        if rels:
            parts.append("\n=== CHARACTER RELATIONSHIPS ===")
            for key, rel in rels.items():
                rel_str = f"{rel['characters'][0]} <-> {rel['characters'][1]}: {rel['status']}"
                if rel.get('change_reason'):
                    rel_str += f" (because: {rel['change_reason']})"
                parts.append(rel_str)

        return "\n".join(parts) if parts else ""

    def clear(self):
        """ล้าง context ทั้งหมด"""
        self.context = {
            'chapter_summaries': {},
            'character_states': {},
            'key_events': [],
            'relationships': {},
            'plot_progress': {
                'current_act': 1,
                'major_conflicts_resolved': [],
                'pending_threads': []
            }
        }
        self.save()


# Prompt templates สำหรับให้ AI สรุปบท
CHAPTER_SUMMARY_PROMPT = """Based on the chapter text below, provide a BRIEF summary (2-3 sentences, max 50 words) covering:
1. Main events that happened
2. Key character actions/decisions
3. How the story progressed

Chapter {chapter_num} text:
\"\"\"{chapter_text}\"\"\"

Summary (be concise):"""


CHARACTER_UPDATE_PROMPT = """Based on the chapter text below, extract character information.
For each character that appeared, provide:
- Location: where are they now?
- Emotional state: how do they feel?
- Goal: what do they want?
- Last action: what did they just do?

Chapter text:
\"\"\"{chapter_text}\"\"\"

Return in this exact JSON format:
{{
  "characters": [
    {{"name": "...", "location": "...", "emotional_state": "...", "goal": "...", "last_action": "..."}}
  ],
  "key_events": [
    {{"event": "...", "impact": "..."}}
  ],
  "relationship_changes": [
    {{"char1": "...", "char2": "...", "status": "...", "reason": "..."}}
  ]
}}"""
