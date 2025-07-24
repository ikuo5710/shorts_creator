import flet as ft
import subprocess
import threading
import os


def main(page: ft.Page):
    page.title = "Shorts Creator"
    page.window_width = 800
    page.window_height = 600

    prompt_input = ft.TextField(label="Prompt", multiline=True, min_lines=3)
    output_log = ft.TextField(
        label="Log", read_only=True, multiline=True, min_lines=10, expand=True
    )
    output_dir_text = ft.Text("Output directory:")
    output_dir_path = ft.Text(os.path.abspath("."))

    def pick_output_directory(e):
        def on_dialog_result(e: ft.FilePickerResultEvent):
            if e.path:
                output_dir_path.value = e.path
                page.update()

        file_picker = ft.FilePicker(on_result=on_dialog_result)
        page.overlay.append(file_picker)
        page.update()
        file_picker.get_directory_path()

    progress_ring = ft.ProgressRing(visible=False)

    def run_pipeline(e):
        prompt = prompt_input.value
        output_dir = output_dir_path.value
        if not prompt:
            output_log.value += "Error: Prompt is required.\n"
            page.update()
            return

        output_log.value = ""
        start_button.disabled = True
        progress_ring.visible = True
        page.update()

        def run():
            process = subprocess.Popen(
                [
                    "python",
                    "-u",
                    "-X",
                    "utf8",
                    "src/run_pipeline.py",
                    prompt,
                    "-o",
                    output_dir,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="ignore",
                bufsize=1,
            )
            for line in iter(process.stdout.readline, ""):
                output_log.value += line
                page.update()
            process.stdout.close()
            process.wait()
            start_button.disabled = False
            progress_ring.visible = False
            page.update()

        thread = threading.Thread(target=run)
        thread.start()

    def open_output_folder(e):
        os.startfile(output_dir_path.value)

    start_button = ft.ElevatedButton(text="Create Video", on_click=run_pipeline)
    pick_dir_button = ft.ElevatedButton(
        text="Select Output Directory", on_click=pick_output_directory
    )
    open_folder_button = ft.ElevatedButton(
        text="Open Output Directory", on_click=open_output_folder
    )

    page.add(
        prompt_input,
        ft.Row([pick_dir_button, output_dir_text, output_dir_path]),
        ft.Row([start_button, progress_ring]),
        output_log,
        open_folder_button,
    )


if __name__ == "__main__":
    ft.app(target=main)
