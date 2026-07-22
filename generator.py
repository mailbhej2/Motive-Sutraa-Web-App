import json

from config import (
    IMAGE_SHOT_TYPE,
    PROMPTS_DIR,
    VIDEO_MAIN_VISUAL_REFERENCE,
    VIDEO_SHOT_TYPE,
    VIDEO_VOICE_CONSISTENCY,
    VIDEO_VOICE_PROFILE,
)


class Generator:

    def __init__(self):
        self.manual_prompt_file = PROMPTS_DIR / "manual_json.txt"

    # =========================================================
    # Scene Count
    # =========================================================

    def calculate_scene_count(
        self,
        duration: int,
    ) -> int:

        if duration <= 2:
            return duration * 10

        if duration <= 5:
            return duration * 8

        if duration <= 10:
            return duration * 7

        if duration <= 20:
            return duration * 6

        return duration * 5

    # =========================================================
    # Manual Prompt
    # =========================================================

    def create_manual_prompt(
        self,
        story_idea: str,
        duration: int,
        language: str,
    ) -> str:

        scene_count = self.calculate_scene_count(
            duration
        )

        template = self.manual_prompt_file.read_text(
            encoding="utf-8"
        )

        return (
            template
            .replace(
                "<<STORY_IDEA>>",
                story_idea.strip(),
            )
            .replace(
                "<<LANGUAGE>>",
                language,
            )
            .replace(
                "<<DURATION>>",
                str(duration),
            )
            .replace(
                "<<SCENE_COUNT>>",
                str(scene_count),
            )
        )

    # =========================================================
    # Parse JSON
    # =========================================================

    def parse_json(
        self,
        json_text: str,
    ) -> dict:

        try:

            return json.loads(
                json_text.strip()
            )

        except json.JSONDecodeError as e:

            raise ValueError(
                f"Invalid JSON\n\n{e}"
            )

    # =========================================================
    # Scenes
    # =========================================================

    def get_scenes(
        self,
        data: dict,
    ) -> list:

        return data.get(
            "scenes",
            [],
        )

    # =========================================================
    # Image Prompt (JSON)
    # =========================================================

    def create_image_prompt(
        self,
        scene: dict,
    ) -> str:
        """
        Builds a JSON structure for a single scene's image prompt —
        ready to paste directly into Google Gemini, Google Flow/Imagen,
        or ChatGPT/DALL-E, instead of a plain text sentence.
        """

        prompt = {
            "shot_type": IMAGE_SHOT_TYPE,
            "main_visual_reference": VIDEO_MAIN_VISUAL_REFERENCE,
            "scene": scene.get("scene"),
            "image_prompt": scene.get("image_prompt", "").strip(),
        }

        return json.dumps(
            prompt,
            ensure_ascii=False,
            indent=2,
        )

    # =========================================================
    # Standalone Prompt Formatting
    # =========================================================

    def format_standalone_prompts(
        self,
        scenes: list,
        start_index: int = 0,
    ) -> str:
        """
        Formats a set of scenes as clearly separated, independently-
        generatable JSON image prompts (see create_image_prompt).

        Google Flow (and most image generators) create ONE image per
        prompt submission — they do not split a combined prompt into
        multiple images. So instead of joining prompts into a single
        blob, each photo gets its own numbered, clearly delimited
        JSON block with an explicit instruction not to merge them.
        """

        header = (
            f"Generate {len(scenes)} SEPARATE, INDEPENDENT photos — "
            "one image per JSON prompt block below. Do NOT merge these "
            "into a single combined or collage image. Paste and "
            "generate each numbered prompt ONE AT A TIME in Google "
            "Gemini, Google Flow, ChatGPT, or your image tool of choice."
        )

        blocks = [header]

        for offset, scene in enumerate(scenes):

            scene_number = scene.get(
                "scene",
                start_index + offset + 1,
            )

            image_prompt_json = self.create_image_prompt(scene)

            blocks.append(
                f"===== Photo {offset + 1} (Scene {scene_number}) =====\n"
                f"{image_prompt_json}"
            )

        return "\n\n".join(blocks)

    # =========================================================
    # Individual Image Prompts
    # =========================================================

    def get_individual_image_prompts(
        self,
        scenes: list,
    ) -> list:
        """
        Returns each scene's image prompt as its own numbered entry:
            {"number": 1, "scene": <scene number>, "text": "<JSON prompt>"}
        Used by the "Image Prompts" tab, where every prompt is shown
        individually, as JSON, with its own Copy button.
        """

        return [
            {
                "number": index + 1,
                "scene": scene.get("scene", index + 1),
                "text": self.create_image_prompt(scene),
            }
            for index, scene in enumerate(scenes)
        ]

    # =========================================================
    # Copy All Image Prompts
    # =========================================================

    def get_all_image_prompts(
        self,
        scenes: list,
    ) -> str:

        return self.format_standalone_prompts(scenes)

    # =========================================================
    # Scene / Video Prompt (JSON)
    # =========================================================

    def create_video_prompt(
        self,
        scene: dict,
    ) -> str:
        """
        Builds the fixed JSON structure used for the "Scene/Video Prompt"
        tab. Only voiceover_text_hindi (narration) and visual_requirements
        (visual_info) vary per scene; everything else stays constant so
        every scene stays consistent.
        """

        prompt = {
            "shot_type": VIDEO_SHOT_TYPE,
            "main_visual_reference": VIDEO_MAIN_VISUAL_REFERENCE,
            "native_audio": {
                "voice_profile": VIDEO_VOICE_PROFILE,
                "consistency": VIDEO_VOICE_CONSISTENCY,
            },
            "voiceover_text_hindi": scene.get("narration", ""),
            "visual_requirements": scene.get("visual_info", ""),
        }

        return json.dumps(
            prompt,
            ensure_ascii=False,
            indent=2,
        )

    # =========================================================
    # All Scene / Video Prompts
    # =========================================================

    def create_all_video_prompts(
        self,
        scenes: list,
    ) -> list:

        return [

            self.create_video_prompt(
                scene
            )

            for scene in scenes

        ]
