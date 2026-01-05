system = (
    "You are a helpful assistant for fiction writing. "
    "Always cut the bullshit and provide concise outlines with useful details. "
    "Do not turn your stories into fairy tales, be realistic.")

book_spec_fields = ['Genre', 'Place', 'Time', 'Theme',
                    'Tone', 'Point of View', 'Characters', 'Premise']

book_spec_format = (
    "Genre: genre\n"
    "Place: place\n"
    "Time: period\n"
    "Theme: main topics\n"
    "Tone: tone\n"
    "Point of View: POV\n"
    "Characters: use specific names already\n"
    "Premise: describe some concrete events already")

scene_spec_format = (
    "Chapter [number]:\nScene [number]:\nCharacters: character list\nPlace: place\nTime: absolute or relative time\nEvent: what happens\nConflict: scene micro-conflict\n"
    "Story value: story value affected by the scene\nStory value charge: the charge of story value by the end of the scene (positive or negative)\nMood: mood\nOutcome: the result.")

prev_scene_intro = "\n\nHere is the ending of the previous scene:\n"
cur_scene_intro = "\n\nHere is the last written snippet of the current scene:\n"


def init_book_spec_messages(topic, form):
    messages = [
        {"role": "system", "content": system},
        {"role": "user",
         "content": f"Given the topic, come up with a specification to write a {form}. Write spec using the format below. "
                    f"Do not use Markdown format. "
                    f"Topic: {topic}\nFormat:\n\"\"\"\n{book_spec_format}\"\"\""},
    ]
    return messages


def missing_book_spec_messages(field, text_spec):
    messages = [
        {"role": "system", "content": system},
        {"role": "user",
         "content": (
            f"Given a hypothetical book spec, fill the missing field: {field}."
            f"Do not use Markdown format. "
            f'Return only field, separator and value in one line like "Field: value".\n'
            f'Book spec:\n"""{text_spec}"""')
        }
    ]
    return messages


def enhance_book_spec_messages(book_spec, form):
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content":
            f"Make the specification for an upcoming {form} more detailed "
            f"Do not use Markdown format. "
            f"(specific settings, major events that differentiate the {form} "
            f"from others). Do not change the format or add more fields."
            f"\nEarly {form} specification:\n\"\"\"{book_spec}\"\"\""}
    ]
    return messages


def create_plot_chapters_messages(book_spec, form):
    messages = [
        {"role": "user", "content": (
            f"Come up with a plot for a bestseller-grade {form} in 3 acts taking inspiration from its description. "
            "Break down the plot into chapters using the following structure:\nActs\n- Chapters\n\n"
            f"Do not use Markdown format. "
            f"Early {form} description:\n\"\"\"{book_spec}\"\"\".")}
    ]
    return messages


def enhance_plot_chapters_messages(act_num, text_plan, book_spec, form):
    act_num += 1
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"Come up with a plot for a bestseller-grade {form} in 3 acts. Break down the plot into chapters using the following structure:\nActs\n- Chapters\n\nEarly {form} description:\n\"\"\"{book_spec}\"\"\""},
        {"role": "assistant", "content": text_plan},
        {"role": "user", "content": f"Take Act {act_num}. Rewrite the plan so that chapter's story value alternates (i.e. if Chapter 1 is positive, Chapter 2 is negative, and so on). Describe only concrete events and actions (who did what). Make it very short (one brief sentence and value charge indication per chapter) "
         f"Do not use Markdown format. "}
    ]
    return messages


def split_chapters_into_scenes_messages(act_num, text_act, form, book_spec=None):
    # สร้าง prompt พร้อม book_spec ถ้ามี
    content = f"Break each chapter in Act {act_num} into scenes (number depends on how packed a chapter is), give scene specifications for each.\n"
    content += f"Do not use Markdown format.\n\n"

    # เพิ่ม book_spec เพื่อให้ AI รู้ข้อมูลตัวละคร, สถานที่, ธีม
    if book_spec:
        content += f"Book specification (characters, setting, tone):\n\"\"\"{book_spec}\"\"\"\n\n"

    content += f"Here is the by-chapter plot summary for the act in a {form}:\n\"\"\"{text_act}\"\"\"\n\n"
    content += f"Scene spec format:\n\"\"\"{scene_spec_format}\"\"\""

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": content}
    ]
    return messages


def scene_messages(scene, sc_num, ch_num, text_plan, form, book_spec=None, story_context=None):
    # สร้าง content พร้อม book_spec และ story_context
    content = f"Write a long detailed scene for a {form} for scene {sc_num} in chapter {ch_num} based on the information. "
    content += "Be creative, explore interesting characters and unusual settings. Do NOT use foreshadowing.\n"
    content += "IMPORTANT: Maintain consistency with previous chapters - use the story context below.\n\n"

    # เพิ่ม book_spec เพื่อให้ AI รู้ข้อมูลตัวละคร, ธีม, โทน
    if book_spec:
        content += f"Book specification (characters, setting, tone, theme):\n\"\"\"{book_spec}\"\"\"\n\n"

    # เพิ่ม story_context เพื่อความต่อเนื่อง
    if story_context:
        content += f"Story context (what happened before - MUST maintain consistency):\n\"\"\"{story_context}\"\"\"\n\n"

    content += f"Here is the scene specification:\n\"\"\"{scene}\"\"\"\n\n"
    content += f"Here is the overall plot:\n\"\"\"{text_plan}\"\"\""

    messages = [
        {"role": "system", "content": 'You are an expert fiction writer. Write detailed scenes with lively dialogue. Maintain story continuity and character consistency.'},
        {"role": "user", "content": content},
        {"role": "assistant", "content": f"\nChapter {ch_num}, Scene {sc_num}\n"},
    ]
    return messages


# =====================================================
# Story Context Prompts - สำหรับสรุปและ track ข้อมูลเรื่อง
# =====================================================

def chapter_summary_messages(chapter_num, chapter_text):
    """Prompt สำหรับสรุปบท"""
    messages = [
        {"role": "system", "content": "You are a story analyst. Provide brief, factual summaries."},
        {"role": "user", "content": f"""Summarize Chapter {chapter_num} in 2-3 sentences (max 50 words).
Focus on: main events, character actions, plot progression.
Do not use Markdown format.

Chapter text:
\"\"\"{chapter_text[:3000]}\"\"\"

Brief summary:"""}
    ]
    return messages


def extract_story_context_messages(chapter_num, chapter_text, character_names=None):
    """Prompt สำหรับดึงข้อมูล context จากบท"""
    char_hint = ""
    if character_names:
        char_hint = f"\nKnown characters: {', '.join(character_names)}"

    messages = [
        {"role": "system", "content": "You are a story analyst. Extract structured information from story text. Return valid JSON only."},
        {"role": "user", "content": f"""Analyze Chapter {chapter_num} and extract:
1. Character states (location, emotional state, current goal)
2. Key events that happened
3. Relationship changes between characters
{char_hint}

Chapter text:
\"\"\"{chapter_text[:3000]}\"\"\"

Return ONLY valid JSON in this exact format (no markdown, no explanation):
{{"characters": [{{"name": "...", "location": "...", "emotional_state": "...", "goal": "..."}}], "key_events": [{{"event": "...", "impact": "..."}}], "relationships": [{{"char1": "...", "char2": "...", "status": "...", "reason": "..."}}]}}"""}
    ]
    return messages
