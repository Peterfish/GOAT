"""
Story Pipeline - รวมทุกขั้นตอนการสร้างเรื่อง
Usage:
    python story_pipeline.py 1 --topic "your topic"   # Step 1: Init book spec
    python story_pipeline.py 2                         # Step 2: Enhance book spec
    python story_pipeline.py 3                         # Step 3: Create plot chapters
    python story_pipeline.py 4                         # Step 4: Enhance plot chapters
    python story_pipeline.py 5                         # Step 5: Split into scenes
    python story_pipeline.py 6                         # Step 6: Write scenes
"""
import sys
import os
import json
import argparse
from goat_storytelling_agent.storytelling_agent import StoryAgent
from goat_storytelling_agent.plan import Plan
from goat_storytelling_agent.story_context import StoryContext

# Output directory
OUTPUT_DIR = 'output'

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_json(filename, data):
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {filepath}")
    return filepath

def load_json(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        print("Please run the previous step first.")
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# =============================================================================
# Step 1: Initialize Book Specification
# =============================================================================
def step1_init_book_spec(topic, form='novel'):
    """สร้าง book specification จาก topic"""
    print(f"{'='*60}")
    print(f"Step 1: Initialize Book Specification")
    print(f"{'='*60}")
    print(f"Topic: {topic}")
    print(f"Form: {form}")
    print()

    writer = StoryAgent(form=form)
    print("Generating initial book specification...")
    messages, book_spec = writer.init_book_spec(topic)
    spec_dict = writer.parse_book_spec(book_spec)

    output_data = {
        "step": 1,
        "step_name": "init_book_spec",
        "topic": topic,
        "form": form,
        "book_spec_text": book_spec,
        "book_spec": spec_dict
    }

    save_json('step1_book_spec.json', output_data)

    print(f"\n{'='*60}")
    print("Book Specification:")
    print(f"{'='*60}")
    print(book_spec)
    print(f"\n>> You can edit 'output/step1_book_spec.json' before running step 2")

# =============================================================================
# Step 2: Enhance Book Specification
# =============================================================================
def step2_enhance_book_spec():
    """ปรับปรุง book specification ให้ละเอียดยิ่งขึ้น"""
    print(f"{'='*60}")
    print(f"Step 2: Enhance Book Specification")
    print(f"{'='*60}")

    step1_data = load_json('step1_book_spec.json')
    book_spec = step1_data['book_spec_text']
    form = step1_data.get('form', 'novel')

    print(f"Form: {form}")
    print(f"Topic: {step1_data.get('topic', '')}")
    print()

    writer = StoryAgent(form=form)
    print("Enhancing book specification...")
    messages, enhanced_spec = writer.enhance_book_spec(book_spec)
    spec_dict = writer.parse_book_spec(enhanced_spec)

    output_data = {
        "step": 2,
        "step_name": "enhance_book_spec",
        "topic": step1_data.get('topic', ''),
        "form": form,
        "original_book_spec": step1_data['book_spec'],
        "enhanced_book_spec_text": enhanced_spec,
        "enhanced_book_spec": spec_dict
    }

    save_json('step2_enhanced_spec.json', output_data)

    print(f"\n{'='*60}")
    print("Enhanced Book Specification:")
    print(f"{'='*60}")
    print(enhanced_spec)
    print(f"\n>> You can edit 'output/step2_enhanced_spec.json' before running step 3")

# =============================================================================
# Step 3: Create Plot Chapters
# =============================================================================
def step3_create_plot_chapters():
    """สร้าง plot และ chapters จาก book specification"""
    print(f"{'='*60}")
    print(f"Step 3: Create Plot Chapters")
    print(f"{'='*60}")

    # โหลดข้อมูลจาก Step 2
    step2_data = load_json('step2_enhanced_spec.json')
    book_spec = step2_data['enhanced_book_spec_text']
    form = step2_data.get('form', 'novel')
    topic = step2_data.get('topic', '')

    print(f"Form: {form}")
    print(f"Topic: {topic}")
    print()

    writer = StoryAgent(form=form)
    print("Creating plot chapters...")
    messages, plan = writer.create_plot_chapters(book_spec)

    # แปลง plan เป็น text สำหรับแสดงผล
    plan_text = Plan.plan_2_str(plan)

    output_data = {
        "step": 3,
        "step_name": "create_plot_chapters",
        "topic": topic,
        "form": form,
        "book_spec_text": book_spec,
        "plan": plan,
        "plan_text": plan_text
    }

    save_json('step3_plot_chapters.json', output_data)

    print(f"\n{'='*60}")
    print("Plot Chapters:")
    print(f"{'='*60}")
    print(plan_text)
    print(f"\n>> You can edit 'output/step3_plot_chapters.json' before running step 4")

# =============================================================================
# Step 4: Enhance Plot Chapters
# =============================================================================
def step4_enhance_plot_chapters():
    """ปรับปรุง plot และ chapters ให้น่าสนใจยิ่งขึ้น"""
    print(f"{'='*60}")
    print(f"Step 4: Enhance Plot Chapters")
    print(f"{'='*60}")

    # โหลดข้อมูลจาก Step 3
    step3_data = load_json('step3_plot_chapters.json')
    book_spec = step3_data['book_spec_text']
    plan = step3_data['plan']
    form = step3_data.get('form', 'novel')
    topic = step3_data.get('topic', '')

    print(f"Form: {form}")
    print(f"Topic: {topic}")
    print(f"Number of Acts: {len(plan)}")
    print()

    writer = StoryAgent(form=form)
    print("Enhancing plot chapters (this may take a while)...")
    print()

    # enhance_plot_chapters ปรับปรุงแต่ละ act
    messages, enhanced_plan = writer.enhance_plot_chapters(book_spec, plan)

    # แปลง plan เป็น text สำหรับแสดงผล
    plan_text = Plan.plan_2_str(enhanced_plan)

    output_data = {
        "step": 4,
        "step_name": "enhance_plot_chapters",
        "topic": topic,
        "form": form,
        "book_spec_text": book_spec,
        "original_plan": step3_data['plan'],
        "enhanced_plan": enhanced_plan,
        "plan_text": plan_text
    }

    save_json('step4_enhanced_chapters.json', output_data)

    print(f"\n{'='*60}")
    print("Enhanced Plot Chapters:")
    print(f"{'='*60}")
    print(plan_text)
    print(f"\n>> You can edit 'output/step4_enhanced_chapters.json' before running step 5")

# =============================================================================
# Step 5: Split Chapters into Scenes
# =============================================================================
def step5_split_into_scenes():
    """แบ่ง chapters เป็น scenes"""
    print(f"{'='*60}")
    print(f"Step 5: Split Chapters into Scenes")
    print(f"{'='*60}")

    # โหลดข้อมูลจาก Step 4
    step4_data = load_json('step4_enhanced_chapters.json')
    plan = step4_data['enhanced_plan']
    form = step4_data.get('form', 'novel')
    topic = step4_data.get('topic', '')
    book_spec = step4_data.get('book_spec_text', '')

    print(f"Form: {form}")
    print(f"Topic: {topic}")
    print(f"Number of Acts: {len(plan)}")
    print()

    writer = StoryAgent(form=form)
    print("Splitting chapters into scenes (this may take a while)...")
    print()

    # split_chapters_into_scenes แบ่งแต่ละ chapter เป็น scenes
    # ส่ง book_spec ไปด้วยเพื่อให้ AI รู้ข้อมูลตัวละคร, สถานที่, ธีม
    messages, plan_with_scenes = writer.split_chapters_into_scenes(plan, book_spec=book_spec)

    # นับจำนวน scenes ทั้งหมด
    total_scenes = 0
    scenes_summary = []
    for act_idx, act in enumerate(plan_with_scenes, start=1):
        if 'chapter_scenes' in act:
            for ch_num, scenes in act['chapter_scenes'].items():
                total_scenes += len(scenes)
                scenes_summary.append(f"  Chapter {ch_num}: {len(scenes)} scenes")

    output_data = {
        "step": 5,
        "step_name": "split_chapters_into_scenes",
        "topic": topic,
        "form": form,
        "book_spec_text": book_spec,
        "plan_with_scenes": plan_with_scenes,
        "total_scenes": total_scenes
    }

    save_json('step5_scenes.json', output_data)

    print(f"\n{'='*60}")
    print("Scenes Summary:")
    print(f"{'='*60}")
    print(f"Total scenes: {total_scenes}")
    print()
    for line in scenes_summary:
        print(line)
    print(f"\n>> You can edit 'output/step5_scenes.json' before running step 6")

# =============================================================================
# Step 6: Write Scenes
# =============================================================================
def get_all_chapters(plan):
    """รวบรวม chapters ทั้งหมดจาก plan"""
    chapters = []
    for act_idx, act in enumerate(plan):
        if 'chapter_scenes' not in act:
            continue
        for ch_num, scenes in act['chapter_scenes'].items():
            chapters.append({
                'act_idx': act_idx,
                'ch_num': ch_num,
                'scenes': scenes
            })
    return chapters

def write_single_chapter(writer, plan, chapter_info, previous_chapter_text=None,
                         book_spec=None, story_context_str=None):
    """เขียน chapter เดียว พร้อม story context สำหรับความต่อเนื่อง"""
    ch_num = chapter_info['ch_num']
    scenes = chapter_info['scenes']

    chapter_text = []
    previous_scene = previous_chapter_text  # ใช้ scene สุดท้ายของบทก่อนหน้า

    for sc_idx, scene in enumerate(scenes, start=1):
        print(f"  Writing Scene {sc_idx}/{len(scenes)}...")

        try:
            # ส่ง book_spec และ story_context ไปด้วยเพื่อความต่อเนื่อง
            messages, generated_scene = writer.write_a_scene(
                scene, sc_idx, ch_num, plan,
                previous_scene=previous_scene,
                book_spec=book_spec,
                story_context=story_context_str
            )
            chapter_text.append(generated_scene)
            previous_scene = generated_scene
        except Exception as e:
            print(f"    Error: {e}")
            chapter_text.append(f"[Error generating scene: {e}]")

    return "\n\n".join(chapter_text)


def update_story_context(writer, story_ctx, chapter_num, chapter_text, character_names=None):
    """อัปเดต story context หลังเขียนบทเสร็จ"""
    print(f"  Updating story context...")

    # 1. สรุปบท
    try:
        summary = writer.summarize_chapter(chapter_num, chapter_text)
        story_ctx.add_chapter_summary(chapter_num, summary)
        print(f"    - Chapter summary added")
    except Exception as e:
        print(f"    - Warning: Could not summarize chapter: {e}")

    # 2. ดึงข้อมูล context (ตัวละคร, เหตุการณ์, ความสัมพันธ์)
    try:
        context_data = writer.extract_chapter_context(chapter_num, chapter_text, character_names)

        # อัปเดตสถานะตัวละคร
        for char in context_data.get('characters', []):
            if char.get('name'):
                story_ctx.update_character_state(
                    name=char['name'],
                    location=char.get('location'),
                    emotional_state=char.get('emotional_state'),
                    goal=char.get('goal'),
                    last_action=char.get('last_action')
                )
        print(f"    - Character states updated: {len(context_data.get('characters', []))}")

        # เพิ่มเหตุการณ์สำคัญ
        for evt in context_data.get('key_events', []):
            if evt.get('event'):
                story_ctx.add_key_event(chapter_num, evt['event'], evt.get('impact'))
        print(f"    - Key events added: {len(context_data.get('key_events', []))}")

        # อัปเดตความสัมพันธ์
        for rel in context_data.get('relationships', []):
            if rel.get('char1') and rel.get('char2'):
                story_ctx.update_relationship(
                    rel['char1'], rel['char2'],
                    rel.get('status', 'unknown'),
                    rel.get('reason')
                )
        print(f"    - Relationships updated: {len(context_data.get('relationships', []))}")

    except Exception as e:
        print(f"    - Warning: Could not extract context: {e}")

def get_character_names_from_book_spec(book_spec):
    """ดึงชื่อตัวละครจาก book_spec"""
    names = []
    if 'Characters:' in book_spec:
        char_line = book_spec.split('Characters:')[1].split('\n')[0]
        # แยกชื่อตัวละคร (มักอยู่ในรูปแบบ "Name (age, description)")
        import re
        # หาชื่อที่อยู่ก่อนวงเล็บหรือ comma
        matches = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', char_line)
        names = matches[:10]  # จำกัด 10 ชื่อ
    return names


def step6_write_scenes(chapter_num=None):
    """เขียนเนื้อหาแต่ละ scene - สามารถเขียนทีละบทหรือทั้งหมด

    ใหม่: ใช้ Story Context System สำหรับความต่อเนื่องของเรื่อง
    """
    print(f"{'='*60}")
    print(f"Step 6: Write Scenes (with Story Context)")
    print(f"{'='*60}")

    # โหลดข้อมูลจาก Step 5
    step5_data = load_json('step5_scenes.json')
    plan = step5_data['plan_with_scenes']
    form = step5_data.get('form', 'novel')
    topic = step5_data.get('topic', '')
    book_spec = step5_data.get('book_spec_text', '')

    # รวบรวม chapters ทั้งหมด
    all_chapters = get_all_chapters(plan)
    total_chapters = len(all_chapters)

    # ดึงชื่อตัวละครจาก book_spec
    character_names = get_character_names_from_book_spec(book_spec)

    print(f"Form: {form}")
    print(f"Topic: {topic}")
    print(f"Total chapters: {total_chapters}")
    if book_spec:
        print(f"Book spec: Loaded ({len(book_spec)} chars)")
    if character_names:
        print(f"Characters: {', '.join(character_names[:5])}...")

    # สร้าง directory สำหรับ chapters
    chapters_dir = os.path.join(OUTPUT_DIR, 'chapters')
    os.makedirs(chapters_dir, exist_ok=True)

    # Initialize Story Context
    story_ctx = StoryContext(OUTPUT_DIR)
    print(f"Story context: Loaded from {story_ctx.context_file}")

    writer = StoryAgent(form=form)

    if chapter_num is not None:
        # เขียนเฉพาะบทที่ระบุ
        print(f"\nWriting Chapter {chapter_num} only...")

        # หา chapter ที่ต้องการ
        target_chapter = None
        for ch in all_chapters:
            if int(ch['ch_num']) == chapter_num:
                target_chapter = ch
                break

        if target_chapter is None:
            print(f"Error: Chapter {chapter_num} not found!")
            print(f"Available chapters: {[int(ch['ch_num']) for ch in all_chapters]}")
            return

        # อ่าน previous chapter ถ้ามี
        previous_text = None
        if chapter_num > 1:
            prev_file = os.path.join(chapters_dir, f'chapter_{chapter_num-1:02d}.txt')
            if os.path.exists(prev_file):
                with open(prev_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    words = content.split()
                    previous_text = ' '.join(words[-400:]) if len(words) > 400 else content

        # ดึง story context สำหรับบทนี้
        story_context_str = story_ctx.get_context_for_writing(chapter_num)
        if story_context_str:
            print(f"  Story context loaded ({len(story_context_str)} chars)")

        print(f"\nChapter {chapter_num}: {len(target_chapter['scenes'])} scenes")
        chapter_text = write_single_chapter(
            writer, plan, target_chapter, previous_text,
            book_spec=book_spec, story_context_str=story_context_str
        )

        # บันทึกไฟล์
        chapter_file = os.path.join(chapters_dir, f'chapter_{chapter_num:02d}.txt')
        with open(chapter_file, 'w', encoding='utf-8') as f:
            f.write(f"# Chapter {chapter_num}\n\n")
            f.write(chapter_text)
        print(f"\nSaved to {chapter_file}")

        # อัปเดต story context หลังเขียนเสร็จ
        update_story_context(writer, story_ctx, chapter_num, chapter_text, character_names)

    else:
        # เขียนทุกบท
        print(f"\nWriting all {total_chapters} chapters...")
        print("(Already written chapters will be skipped)")
        print("(Story context will be updated after each chapter)")
        print()

        previous_text = None
        written_count = 0
        skipped_count = 0

        for ch_info in all_chapters:
            ch_num = int(ch_info['ch_num'])
            chapter_file = os.path.join(chapters_dir, f'chapter_{ch_num:02d}.txt')

            # ตรวจสอบว่ามีไฟล์อยู่แล้วหรือไม่
            if os.path.exists(chapter_file):
                print(f"Chapter {ch_num}: Already exists, skipping...")
                # อ่าน previous text สำหรับบทถัดไป
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    words = content.split()
                    previous_text = ' '.join(words[-400:]) if len(words) > 400 else content

                # ถ้ายังไม่มี summary ให้สร้าง
                if str(ch_num) not in story_ctx.context['chapter_summaries']:
                    print(f"  Creating summary for existing chapter...")
                    update_story_context(writer, story_ctx, ch_num, content, character_names)

                skipped_count += 1
                continue

            # ดึง story context สำหรับบทนี้
            story_context_str = story_ctx.get_context_for_writing(ch_num)
            if story_context_str:
                print(f"  Story context: {len(story_context_str)} chars")

            print(f"\nChapter {ch_num}: {len(ch_info['scenes'])} scenes")
            chapter_text = write_single_chapter(
                writer, plan, ch_info, previous_text,
                book_spec=book_spec, story_context_str=story_context_str
            )

            # บันทึกไฟล์
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(f"# Chapter {ch_num}\n\n")
                f.write(chapter_text)
            print(f"  Saved to {chapter_file}")

            # อัปเดต story context หลังเขียนเสร็จ
            update_story_context(writer, story_ctx, ch_num, chapter_text, character_names)

            # เก็บ previous text สำหรับบทถัดไป
            words = chapter_text.split()
            previous_text = ' '.join(words[-400:]) if len(words) > 400 else chapter_text
            written_count += 1

        print(f"\n{'='*60}")
        print("Story Generation Complete!")
        print(f"{'='*60}")
        print(f"Chapters written: {written_count}")
        print(f"Chapters skipped: {skipped_count}")
        print(f"Files saved to: output/chapters/")
        print(f"Story context saved to: {story_ctx.context_file}")

# =============================================================================
# Main
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description='Story Pipeline - สร้างเรื่องทีละขั้นตอน',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python story_pipeline.py 1 --topic "treasure hunt in a jungle"
  python story_pipeline.py 2
  python story_pipeline.py 3
  python story_pipeline.py 4
  python story_pipeline.py 5
  python story_pipeline.py 6                    # เขียนทุกบท
  python story_pipeline.py 6 --chapter 1        # เขียนเฉพาะบทที่ 1
  python story_pipeline.py 6 --chapter 5        # เขียนเฉพาะบทที่ 5
        """
    )
    parser.add_argument('step', type=int, choices=[1, 2, 3, 4, 5, 6],
                        help='Step number (1-6)')
    parser.add_argument('--topic', type=str,
                        help='Topic for the story (required for step 1)')
    parser.add_argument('--form', type=str, default='novel',
                        help='Form of writing: novel, novella, etc. (default: novel)')
    parser.add_argument('--chapter', type=int,
                        help='Chapter number to write (step 6 only). If not specified, write all chapters.')

    args = parser.parse_args()

    # Step 1 requires topic
    if args.step == 1:
        if not args.topic:
            parser.error("Step 1 requires --topic argument")
        step1_init_book_spec(args.topic, args.form)
    elif args.step == 2:
        step2_enhance_book_spec()
    elif args.step == 3:
        step3_create_plot_chapters()
    elif args.step == 4:
        step4_enhance_plot_chapters()
    elif args.step == 5:
        step5_split_into_scenes()
    elif args.step == 6:
        step6_write_scenes(chapter_num=args.chapter)

if __name__ == '__main__':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
