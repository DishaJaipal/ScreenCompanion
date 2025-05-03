# test.py

from screen_capture import capture_screen, get_active_window_title
from extracting import OCRProcessor
from groq1 import generate_suggestion  # assuming groq1.py has this function
def main():
    ocr_processor = OCRProcessor()

    print("Capturing screen...")
    frame = capture_screen()

    if frame is None:
        print("Failed to capture screen.")
        return

    window_title = get_active_window_title()
    print(f"Active Window Title: {window_title}")

    print("Processing frame...")
    result, _ = ocr_processor.process_frame(frame, window_title)

    if result:
        print("\n--- Extracted Information ---")
        print(f"Window Title: {result['window_title']}")
        print(f"Content Type: {result['content_type']}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Is Code: {result['is_code']}")
        print(f"Is Media: {result['is_media']}")
        print("\nExtracted Text:")
        print(result['text'])

        # Get a Groq suggestion based on extracted text
        suggestion = generate_suggestion("student","studying for history exam",result['text'],result['window_title'])
        print("\n--- Groq Suggestion ---")
        print(suggestion)

    else:
        print("No significant text extracted or no significant screen change detected.")

if __name__ == "__main__":
    main()
