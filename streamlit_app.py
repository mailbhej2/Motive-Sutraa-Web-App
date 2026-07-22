import streamlit as st

from config import (
    APP_NAME,
    DEFAULT_DURATION,
    LANGUAGES,
    MAX_DURATION,
    MIN_DURATION,
)

from generator import Generator


# ==========================================================
# Setup
# ==========================================================

st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
)

if "generator" not in st.session_state:
    st.session_state.generator = Generator()

if "prompt_text" not in st.session_state:
    st.session_state.prompt_text = ""

if "data" not in st.session_state:
    st.session_state.data = {}

if "scenes" not in st.session_state:
    st.session_state.scenes = []

if "image_prompts" not in st.session_state:
    st.session_state.image_prompts = []

if "video_prompts" not in st.session_state:
    st.session_state.video_prompts = []

generator = st.session_state.generator

st.title(APP_NAME)


# ==========================================================
# Controls row
# ==========================================================

col_duration, col_language, col_mode = st.columns([1, 1, 2])

with col_duration:
    duration = st.number_input(
        "Duration (minutes)",
        min_value=MIN_DURATION,
        max_value=MAX_DURATION,
        value=DEFAULT_DURATION,
    )

with col_language:
    language = st.selectbox(
        "Language",
        LANGUAGES,
    )

with col_mode:
    st.radio(
        "Mode",
        ["Manual JSON", "AI Generation (coming soon)"],
        index=0,
        disabled=False,
        horizontal=True,
    )


# ==========================================================
# Story Idea + Prompt (side by side)
# ==========================================================

col_story, col_prompt = st.columns(2)

with col_story:
    st.subheader("Story Idea")
    story_idea = st.text_area(
        "Story Idea",
        placeholder="Enter story idea...",
        height=200,
        label_visibility="collapsed",
    )

with col_prompt:
    st.subheader("Prompt (copy and paste into your AI tool)")
    if st.session_state.prompt_text:
        st.code(
            st.session_state.prompt_text,
            language=None,
            wrap_lines=True,
            height=200,
        )
    else:
        st.text_area(
            "Prompt",
            value="",
            height=200,
            disabled=True,
            label_visibility="collapsed",
        )


# ==========================================================
# Action buttons
# ==========================================================

btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    generate_prompt_clicked = st.button(
        "Generate Prompt", use_container_width=True
    )

with btn_col2:
    generate_results_clicked = st.button(
        "Generate Results", use_container_width=True
    )

with btn_col3:
    clear_clicked = st.button("Clear", use_container_width=True)


# ==========================================================
# Paste Gemini JSON
# ==========================================================

st.subheader("Paste Gemini JSON")
json_text = st.text_area(
    "Paste Gemini JSON",
    placeholder="Paste Gemini JSON here...",
    height=200,
    label_visibility="collapsed",
)


# ==========================================================
# Button handlers
# ==========================================================

if clear_clicked:
    st.session_state.prompt_text = ""
    st.session_state.data = {}
    st.session_state.scenes = []
    st.session_state.image_prompts = []
    st.session_state.video_prompts = []
    st.rerun()

if generate_prompt_clicked:
    if not story_idea.strip():
        st.warning("Enter a story idea first.")
    else:
        st.session_state.prompt_text = generator.create_manual_prompt(
            story_idea,
            duration,
            language,
        )
        st.rerun()

if generate_results_clicked:
    if not json_text.strip():
        st.warning("Paste the Gemini JSON first.")
    else:
        try:
            data = generator.parse_json(json_text)
        except ValueError as e:
            st.error(str(e))
            data = None

        if data is not None:
            scenes = generator.get_scenes(data)

            if not scenes:
                st.warning(
                    'The pasted JSON does not contain a "scenes" list.'
                )
            else:
                st.session_state.data = data
                st.session_state.scenes = scenes
                st.session_state.image_prompts = (
                    generator.get_individual_image_prompts(scenes)
                )
                st.session_state.video_prompts = (
                    generator.create_all_video_prompts(scenes)
                )
                st.success(f"Generated results for {len(scenes)} scenes.")


# ==========================================================
# Results tabs
# ==========================================================

scenes = st.session_state.scenes

tab_images, tab_scenes, tab_story, tab_stats = st.tabs(
    ["Image Prompts", "Scene/Video Prompt", "Story", "Statistics"]
)

# ------------------------------------------------------
# Image Prompts
# ------------------------------------------------------

with tab_images:
    if not st.session_state.image_prompts:
        st.caption("No image prompts yet. Generate results first.")
    else:
        if st.button("Copy All Image Prompts (show combined text)"):
            st.code(
                generator.get_all_image_prompts(scenes),
                language=None,
                wrap_lines=True,
                height=300,
            )

        for item in st.session_state.image_prompts:
            st.markdown(f"**Photo {item['number']} — Scene {item['scene']}**")
            st.code(
                item["text"],
                language="json",
                height=220,
            )

# ------------------------------------------------------
# Scene / Video Prompt
# ------------------------------------------------------

with tab_scenes:
    if not scenes:
        st.caption("No scenes yet. Generate results first.")
    else:
        for scene, video_prompt in zip(
            scenes, st.session_state.video_prompts
        ):
            scene_number = scene.get("scene", "?")
            with st.expander(f"Scene {scene_number}"):
                st.code(video_prompt, language="json", height=300)

# ------------------------------------------------------
# Story
# ------------------------------------------------------

with tab_story:
    if not scenes:
        st.caption("No story yet. Generate results first.")
    else:
        story_text = "\n\n".join(
            scene.get("story_text", "") for scene in scenes
        )
        st.code(story_text, language=None, wrap_lines=True, height=400)

# ------------------------------------------------------
# Statistics
# ------------------------------------------------------

with tab_stats:
    if not scenes:
        st.caption("No statistics yet. Generate results first.")
    else:
        data = st.session_state.data

        total_words = sum(
            len(scene.get("story_text", "").split())
            + len(scene.get("narration", "").split())
            for scene in scenes
        )

        total_characters = sum(
            len(scene.get("story_text", ""))
            + len(scene.get("narration", ""))
            for scene in scenes
        )

        image_prompt_count = sum(
            1 for scene in scenes if scene.get("image_prompt", "").strip()
        )

        stat_col1, stat_col2, stat_col3 = st.columns(3)
        stat_col1.metric("Scenes", len(scenes))
        stat_col2.metric("Duration", data.get("duration", duration))
        stat_col3.metric("Language", data.get("language", language))

        stat_col4, stat_col5, stat_col6 = st.columns(3)
        stat_col4.metric("Total Words", total_words)
        stat_col5.metric("Characters", total_characters)
        stat_col6.metric("Image Prompts", image_prompt_count)
