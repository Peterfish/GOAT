# GOAT-Storytelling-Agent: Agent for writing consistent and interesting long stories for any fiction form
![Goat Agent](./images/GOAT-story.png)

**Version 1.1.0** - Now with Story Context System for better continuity!

## Description
GOAT-Storytelling-Agent writes consistent and  interesting stories over long context requiring only a standard LLM for text generation. This version uses **Ollama Cloud** with the `kimi-k2-thinking:cloud` model.
The agent consists of several stages of planning and writing to build a story from top to down. A user can control the story creation at any preferred scale - starting from a basic novel description to the text of a specific scene. More details can be found in the [release blogpost](https://www.blog.goat.ai/goat-st/).

### What's New in v1.1.0
- **Story Context System**: Automatic tracking of story elements across chapters for better continuity
- **Chapter Summaries**: Each chapter is summarized after writing
- **Character State Tracking**: Track character locations, emotional states, and goals
- **Key Events Log**: Important plot events are recorded and passed to subsequent chapters
- **Relationship Tracking**: Character relationships are monitored throughout the story

## Novella dataset
To demonstrate the capabilities of the agent, we release 20 novellas generated without human supervision requiring only single initial topic for input. The dataset is hosted as an HF dataset - [generated-novels](https://huggingface.co/datasets/GOAT-AI/generated-novels/tree/main/generated-books).

## Setup
1. Configure your Ollama Cloud API in `goat_storytelling_agent/config.py`:

```python
OLLAMA_HOST = 'https://ollama.com'
OLLAMA_API_KEY = 'your-api-key-here'
MODEL = 'kimi-k2-thinking:cloud'
```

2. Install the dependencies:

    ```pip install -r requirements.txt```

    or install as a package

    ```pip install -e .```

---

## วิธีใช้งาน Story Pipeline (ภาษาไทย)

Story Pipeline ช่วยให้คุณสร้างเรื่องทีละขั้นตอน โดยสามารถแก้ไขผลลัพธ์ในแต่ละขั้นตอนก่อนไปขั้นตอนถัดไป

### ภาพรวม 6 ขั้นตอน

| ขั้นตอน | ชื่อ | คำอธิบาย | ไฟล์ผลลัพธ์ |
|---------|------|----------|-------------|
| 1 | Init Book Spec | สร้างโครงร่างหนังสือจาก topic | `output/step1_book_spec.json` |
| 2 | Enhance Book Spec | ปรับปรุงโครงร่างให้ละเอียดขึ้น | `output/step2_enhanced_spec.json` |
| 3 | Create Plot Chapters | สร้างโครงเรื่องและบท | `output/step3_plot_chapters.json` |
| 4 | Enhance Plot Chapters | ปรับปรุงโครงเรื่อง | `output/step4_enhanced_chapters.json` |
| 5 | Split into Scenes | แบ่งบทเป็นฉาก | `output/step5_scenes.json` |
| 6 | Write Scenes | เขียนเนื้อหาแต่ละฉาก | `output/step6_story.json`, `output/story.txt` |

### ขั้นตอนที่ 1: สร้างโครงร่างหนังสือ

ใช้คำสั่งนี้เพื่อสร้างโครงร่างหนังสือจาก topic ที่คุณต้องการ:

```bash
python story_pipeline.py 1 --topic "หัวข้อเรื่องของคุณ"
```

**ตัวอย่าง:**
```bash
python story_pipeline.py 1 --topic "mystery in Bangkok"
python story_pipeline.py 1 --topic "ความรักในกรุงเทพ"
python story_pipeline.py 1 --topic "treasure hunt in a jungle"
```

**ผลลัพธ์:** ระบบจะสร้างไฟล์ `output/step1_book_spec.json` ที่มีข้อมูล:
- **Genre:** ประเภทเรื่อง
- **Place:** สถานที่
- **Time:** ช่วงเวลา
- **Theme:** ธีมหลัก
- **Tone:** อารมณ์ของเรื่อง
- **Point of View:** มุมมองการเล่า
- **Characters:** ตัวละคร
- **Premise:** เนื้อเรื่องย่อ

**ตัวเลือกเพิ่มเติม:**
```bash
# กำหนดรูปแบบการเขียน (novel, novella, short story)
python story_pipeline.py 1 --topic "your topic" --form novella
```

### ขั้นตอนที่ 2: ปรับปรุงโครงร่าง

หลังจากตรวจสอบและแก้ไข `step1_book_spec.json` แล้ว ให้รันคำสั่งนี้:

```bash
python story_pipeline.py 2
```

**สิ่งที่เกิดขึ้น:**
1. ระบบอ่านไฟล์ `output/step1_book_spec.json`
2. AI ปรับปรุงโครงร่างให้ละเอียดและน่าสนใจมากขึ้น
3. บันทึกผลลัพธ์ลง `output/step2_enhanced_spec.json`

**ผลลัพธ์:** ไฟล์ JSON ที่มีรายละเอียดเพิ่มเติม เช่น:
- สถานที่เฉพาะเจาะจงมากขึ้น
- ตัวละครมีความลึกมากขึ้น
- เนื้อเรื่องมีรายละเอียดมากขึ้น

### การแก้ไขไฟล์ JSON

คุณสามารถเปิดไฟล์ JSON และแก้ไขได้ก่อนรันขั้นตอนถัดไป:

```json
{
  "step": 1,
  "topic": "mystery in Bangkok",
  "book_spec": {
    "Genre": "Neo-noir mystery thriller",
    "Place": "Bangkok, Thailand",
    "Characters": "..."
  }
}
```

**แก้ไขได้ตามต้องการ** เช่น:
- เปลี่ยนชื่อตัวละคร
- เพิ่มรายละเอียดสถานที่
- ปรับแต่งเนื้อเรื่อง

### ขั้นตอนที่ 3: สร้างโครงเรื่องและบท

```bash
python story_pipeline.py 3
```

**สิ่งที่เกิดขึ้น:**
1. อ่าน book spec จากขั้นตอนที่ 2
2. สร้างโครงเรื่องแบ่งเป็น 3 Acts พร้อม Chapters
3. บันทึกลง `output/step3_plot_chapters.json`

### ขั้นตอนที่ 4: ปรับปรุงโครงเรื่อง

```bash
python story_pipeline.py 4
```

**สิ่งที่เกิดขึ้น:**
1. อ่าน plot chapters จากขั้นตอนที่ 3
2. ปรับปรุงแต่ละ Act ให้มีรายละเอียดและน่าสนใจมากขึ้น
3. บันทึกลง `output/step4_enhanced_chapters.json`

### ขั้นตอนที่ 5: แบ่งบทเป็นฉาก

```bash
python story_pipeline.py 5
```

**สิ่งที่เกิดขึ้น:**
1. อ่าน enhanced chapters จากขั้นตอนที่ 4
2. แบ่งแต่ละ Chapter เป็น Scenes พร้อมรายละเอียด (ตัวละคร, สถานที่, เวลา, เหตุการณ์)
3. บันทึกลง `output/step5_scenes.json`

### ขั้นตอนที่ 6: เขียนเนื้อหา

**เขียนทุกบท:**
```bash
python story_pipeline.py 6
```

**เขียนเฉพาะบทที่ต้องการ:**
```bash
python story_pipeline.py 6 --chapter 1    # เขียนเฉพาะบทที่ 1
python story_pipeline.py 6 --chapter 5    # เขียนเฉพาะบทที่ 5
```

**สิ่งที่เกิดขึ้น:**
1. อ่าน scenes จากขั้นตอนที่ 5
2. เขียนเนื้อหาแต่ละ scene
3. บันทึกแต่ละบทเป็นไฟล์แยก: `output/chapters/chapter_01.txt`, `chapter_02.txt`, ...

**ข้อดี:**
- ถ้า API error จะไม่ต้องเริ่มใหม่ทั้งหมด
- บทที่เขียนไปแล้วจะถูก skip โดยอัตโนมัติ
- สามารถเขียนทีละบทเพื่อตรวจสอบได้

### Story Context System (ระบบติดตามบริบทเรื่อง)

ในเวอร์ชัน 1.1.0 ระบบจะติดตามบริบทเรื่องโดยอัตโนมัติเพื่อให้เรื่องต่อเนื่องกัน:

**ไฟล์ที่สร้าง:** `output/story_context.json`

**ข้อมูลที่ติดตาม:**
| ประเภท | คำอธิบาย |
|--------|----------|
| Chapter Summaries | สรุปแต่ละบท (2-3 ประโยค) |
| Character States | สถานะตัวละคร (ตำแหน่ง, อารมณ์, เป้าหมาย) |
| Key Events | เหตุการณ์สำคัญและผลกระทบ |
| Relationships | ความสัมพันธ์ระหว่างตัวละคร |

**การทำงาน:**
1. ก่อนเขียนแต่ละบท - ระบบดึงบริบทจากบทก่อนหน้า
2. ส่ง context ให้ AI เพื่อรักษาความต่อเนื่อง
3. หลังเขียนเสร็จ - สรุปบทและดึงข้อมูลตัวละคร/เหตุการณ์
4. บันทึกลง `story_context.json` สำหรับบทถัดไป

**ตัวอย่าง story_context.json:**
```json
{
  "chapter_summaries": {
    "1": "Dr. Helen discovers an ancient map...",
    "2": "The team assembles and plans their journey..."
  },
  "character_states": {
    "Dr. Helen Carr": {
      "location": "Research facility",
      "emotional_state": "Excited but cautious",
      "goal": "Find the artifact"
    }
  },
  "key_events": [
    {"chapter": 1, "event": "Map discovered", "impact": "Sets the journey in motion"}
  ],
  "relationships": {
    "Helen|Ignacio": {"status": "Professional trust", "change_reason": "Survived danger together"}
  }
}
```

### ตัวอย่างการใช้งานเต็มรูปแบบ

```bash
# ขั้นตอนที่ 1: สร้างโครงร่าง
python story_pipeline.py 1 --topic "นักสืบในเชียงใหม่"

# (เปิด output/step1_book_spec.json แก้ไขตามต้องการ)

# ขั้นตอนที่ 2: ปรับปรุงโครงร่าง
python story_pipeline.py 2

# (เปิด output/step2_enhanced_spec.json แก้ไขตามต้องการ)

# ขั้นตอนที่ 3: สร้างโครงเรื่องและบท
python story_pipeline.py 3

# (เปิด output/step3_plot_chapters.json แก้ไขตามต้องการ)

# ขั้นตอนที่ 4: ปรับปรุงโครงเรื่อง
python story_pipeline.py 4

# (เปิด output/step4_enhanced_chapters.json แก้ไขตามต้องการ)

# ขั้นตอนที่ 5: แบ่งบทเป็นฉาก
python story_pipeline.py 5

# (เปิด output/step5_scenes.json แก้ไขตามต้องการ)

# ขั้นตอนที่ 6: เขียนเนื้อหา (ใช้เวลานาน)
python story_pipeline.py 6

# ผลลัพธ์สุดท้าย: output/story.txt
```

### หมายเหตุ

- ไฟล์ JSON ทั้งหมดอยู่ในโฟลเดอร์ `output/`
- ใช้ encoding UTF-8 สำหรับภาษาไทย
- แต่ละขั้นตอนต้องรันตามลำดับ (1 → 2 → 3 → ...)

---

## Usage (English)
### Generate a complete story from a topic (complete pipeline)
The whole pipeline consists of an interplay between different story elements. A whole story can be generated from scratch using the general pipeline.

```python
from goat_storytelling_agent.storytelling_agent import StoryAgent

writer = StoryAgent(form='novel')
novel_scenes = writer.generate_story('treasure hunt in a jungle')
```

You can also specify a custom model:

```python
writer = StoryAgent(model='kimi-k2-thinking:cloud', form='novel')
```

Under the hood, `generate_story` performs following operations:
```python
msgs, book_spec = self.init_book_spec(topic)
msgs, book_spec = self.enhance_book_spec(book_spec)
msgs, plan = self.create_plot_chapters(book_spec)
msgs, plan = self.enhance_plot_chapters(book_spec, plan)
msgs, plan = self.split_chapters_into_scenes(plan)

form_text = []
for act in plan:
    for ch_num, chapter in act['chapter_scenes'].items():
        sc_num = 1
        for scene in chapter:
            previous_scene = form_text[-1] if form_text else None
            _, generated_scene = self.write_a_scene(
                scene, sc_num, ch_num, plan,
                previous_scene=previous_scene)
            form_text.append(generated_scene)
            sc_num += 1
```

Some of the steps will be reviewed in the examples below.
### Create novel ideas from a seed topic
It is possible to break down the generation process and have a more granular control over the story. `init_book_spec` command takes a topic and comes up with a book description consisting of predefined fields - Genre, Place, Time, Theme, Tone, Point of View, Characters, Premise. It is possible to add your own fields and then pass the spec in subsequent stages.

```python
message, book_spec = writer.init_book_spec(topic='treasure hunt in a jungle')
print(book_spec)
```
```output
Genre: Adventure Thriller
Place: Amazon Jungle, South America
Time: Present Day
Theme: Persistence, Survival, Discovery of ancient culture
Tone: Suspenseful, Tense
Point of View: Third person limited
Characters: Dr. Helen Carr, an archaeology professor; Ignacio, an experienced local guide; Bruno Hafner, a greedy treasure collector; Ana Maria, an idealistic student and local tribe leader, Kaya.
Premise: Dr. Helen Carr uncovers a map to an ancient artifact believed to be deep inside the Amazon Jungle. Teaming up with local guide, Ignacio, she embarks on a tense journey to locate the artifact before the ruthless treasure collector, Bruno Hafner, gets there first. Along the way, their path crosses with the idealistic student Ana Maria who is fascinated by the legend of the artifact. The plot thickens as Helen and her team rediscover a lost civilization and have to navigate through both physical dangers of the jungle and complex local politics represented by the tribe leader Kaya. In this race against time, they will also have to fight against the elements of jungle and not to fall into the trap set by Hafner while handling Kaya's tribe with respect and care.
```
### Create a by-chapter outline of the story
```python
from goat_storytelling_agent.plan import Plan

messages, plan = writer.create_plot_chapters(book_spec)
print(Plan.plan_2_str(plan))
```
```output
Act 1: Setting Up The Expedition
- Chapter 1: Dr. Helen Carr's discovery of an ancient map suggesting the location of a valuable artifact deep inside the Amazon Jungle.
- Chapter 2: rugged guide Ignacio and passionate anthropology student, Ana Maria.
- Chapter 3: The expedition's unexpected adversary - Bruno Hafner, a ruthless treasure collector with his technologically advanced team and similar intentions.

Act 2: Journey Through the Jungle and Revelations
- Chapter 4: The expedition commences - navigating treacherous terrain, confronting dangerous wildlife, and surviving on limited resources.
- Chapter 5: Tensions rise within the group due to the intense conditions. A riveting rescue from a piranha-infested river crossing builds trust.
- Chapter 6: The team discovers Kaya and her tribe, decedents of the tribe that created the artifact.
- Chapter 7: Ana Maria's revelation about her connection to Kaya's tribe creates new alliances and emotions.
- Chapter 8: Bruno Hafner's team attacks the village, attempting to steal the artifact's location. A brief skirmish reveals Ignacio's skilled combat past.
- Chapter 9: The staggering scale and sophistication of the underground cave are discovered. The booby-trapped chamber designed to protect the artifact provides a challenging hurdle.

Act 3: Showdown and Epilogue
- Chapter 10: An intense showdown between Helen's group and Bruno in the underground cave, culminating in thwarting Bruno's plans.
- Chapter 11: The true significance of the artifact unraveled, not just a historical treasure but a record of sustainable agricultural practices of the lost tribe.
- Chapter 12: The struggle to return the artifact from the clutches of Bruno and ensure its safe return to Kaya and her tribe.
- Chapter 13: Helen's team departs from the Amazon, leaving the artifact with Kaya's tribe. The journey has not only been about preserving history but also learning from it.
- Chapter 14: Back at the research facility, Helen's successful expedition has increased respect for her work and sparks new research on sustainable ancient practices. The lives of Helen, Ignacio, and Ana Maria are forever changed through their shared adventure and experiences.
```

### Create a by-scene outline
`split_chapters_into_scenes` takes the generated Plan object with chapter outlines and break each into scenes in a predefined format - Characters, Place, Time, Event, Conflct, Story value, Story value charge, Mood, Outcome.
```python
messages, plan = writer.split_chapters_into_scenes(plan)
act_n = 0
scene_n = 0
chapter_n = 1
scene_descr = plan[act_n]['chapter_scenes'][chapter_n][scene_n]
print(scene_descr)
```
```output
Chapter 1:
Scene 1:
Characters: Dr. Helen Carr
Place: Helen's office
Time: Morning
Event: Helen uncovers an ancient map
Conflict: Decoding the map's information successfully
Story value: Knowledge
Story value charge: Positive
Mood: Curiosity
Outcome: A potential location of the priceless artifact is discovered.
```

### Generate scene text based on the plan
Finally, it is possible to generate the scene text with `write_a_scene`. Sometimes the whole text would not fit into the context window, so there is a `continue_a_scene` function that continues the text for the same scene given the progress so far.
```python
messages, generated_scene = writer.write_a_scene(
    scene_descr, sc_num+1, ch_num, plan, previous_scene=None)
```

### Story Context System (v1.1.0)

The Story Context System automatically tracks story elements across chapters to ensure continuity. This is especially important for long stories where the AI might otherwise lose track of character states, events, and relationships.

#### Using StoryContext

```python
from goat_storytelling_agent import StoryAgent, StoryContext

# Initialize
writer = StoryAgent(form='novel')
story_ctx = StoryContext('output')

# After writing a chapter, update the context
chapter_text = "..."  # The generated chapter text
chapter_num = 1

# Summarize the chapter
summary = writer.summarize_chapter(chapter_num, chapter_text)
story_ctx.add_chapter_summary(chapter_num, summary)

# Extract character states, events, and relationships
context_data = writer.extract_chapter_context(chapter_num, chapter_text,
                                               character_names=['Helen', 'Ignacio'])

# Update character states
for char in context_data.get('characters', []):
    story_ctx.update_character_state(
        char['name'],
        location=char.get('location'),
        emotional_state=char.get('emotional_state'),
        goal=char.get('goal')
    )

# Add key events
for event in context_data.get('key_events', []):
    story_ctx.add_key_event(chapter_num, event['event'], event.get('impact', ''))

# Update relationships
for rel in context_data.get('relationships', []):
    story_ctx.update_relationship(rel['char1'], rel['char2'],
                                   rel['status'], rel.get('reason', ''))

# Get context for writing the next chapter
context_str = story_ctx.get_context_for_writing(chapter_num + 1)

# Write next scene with context
messages, scene = writer.write_a_scene(
    scene_descr, sc_num, ch_num, plan,
    book_spec=book_spec,
    story_context=context_str  # Pass context for continuity
)
```

#### Context Data Structure

The `story_context.json` file contains:

| Field | Description |
|-------|-------------|
| `chapter_summaries` | Brief summary of each chapter (2-3 sentences) |
| `character_states` | Current state of each character (location, emotion, goal) |
| `key_events` | Important plot events with their impact |
| `relationships` | Character relationships and how they evolved |

#### New Methods in v1.1.0

| Method | Description |
|--------|-------------|
| `StoryAgent.summarize_chapter(chapter_num, text)` | Returns a 2-3 sentence summary |
| `StoryAgent.extract_chapter_context(chapter_num, text, characters)` | Extracts structured context data |
| `StoryContext.get_context_for_writing(chapter_num)` | Returns formatted context string |
| `StoryContext.add_chapter_summary(num, summary)` | Adds chapter summary |
| `StoryContext.update_character_state(name, ...)` | Updates character state |
| `StoryContext.add_key_event(chapter, event, impact)` | Adds key event |
| `StoryContext.update_relationship(char1, char2, status, reason)` | Updates relationship |

---

## Configuration

Edit `goat_storytelling_agent/config.py` to customize:

```python
OLLAMA_HOST = 'https://ollama.com'
OLLAMA_API_KEY = 'your-api-key'
MODEL = 'kimi-k2-thinking:cloud'
MAX_TOKENS = 16384  # Maximum output tokens
SYSTEM_PROMPT = "You are an expert fiction writer..."
```
